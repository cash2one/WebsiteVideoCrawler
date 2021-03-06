# coding: utf-8
from __future__ import unicode_literals

import base64
import re

from .common import InfoExtractor
from ..compat import compat_urllib_parse_unquote


class BigflixIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?bigflix\.com/.+/(?P<id>[0-9]+)'
    _TESTS = [{
        'url': 'http://www.bigflix.com/Hindi-movies/Action-movies/Singham-Returns/16537',
        'md5': 'ec76aa9b1129e2e5b301a474e54fab74',
        'info_dict': {
            'id': '16537',
            'ext': 'mp4',
            'title': 'Singham Returns',
            'description': 'md5:3d2ba5815f14911d5cc6a501ae0cf65d',
        }
    }, {
        # 2 formats
        'url': 'http://www.bigflix.com/Tamil-movies/Drama-movies/Madarasapatinam/16070',
        'info_dict': {
            'id': '16070',
            'ext': 'mp4',
            'title': 'Madarasapatinam',
            'description': 'md5:63b9b8ed79189c6f0418c26d9a3452ca',
            'formats': 'mincount:2',
        },
        'params': {
            'skip_download': True,
        }
    }, {
        # multiple formats
        'url': 'http://www.bigflix.com/Malayalam-movies/Drama-movies/Indian-Rupee/15967',
        'only_matching': True,
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)

        webpage = self._download_webpage(url, video_id)

        title = self._html_search_regex(
            r'<div[^>]+class=["\']pagetitle["\'][^>]*>(.+?)</div>',
            webpage, 'title')

        def decode_url(quoted_b64_url):
            return base64.b64decode(compat_urllib_parse_unquote(
                quoted_b64_url).encode('ascii')).decode('utf-8')

        formats = []
        for height, encoded_url in re.findall(
                r'ContentURL_(\d{3,4})[pP][^=]+=([^&]+)', webpage):
            video_url = decode_url(encoded_url)
            f = {
                'url': video_url,
                'format_id': '%sp' % height,
                'height': int(height),
            }
            if video_url.startswith('rtmp'):
                f['ext'] = 'flv'
            formats.append(f)

        file_url = self._search_regex(
            r'file=([^&]+)', webpage, 'video url', default=None)
        if file_url:
            video_url = decode_url(file_url)
            if all(f['url'] != video_url for f in formats):
                formats.append({
                    'url': decode_url(file_url),
                })

        self._sort_formats(formats)

        description = self._html_search_meta('description', webpage)

        return {
            'id': video_id,
            'title': title,
            'description': description,
            'formats': formats
        }
