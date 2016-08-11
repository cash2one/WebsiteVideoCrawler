#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from HTMLParser import HTMLParser
from urllib.request import urlopen
import re
import sys
import pymysql
import os
import configparser
import time
import youtube_dl
from you_get.common import *

#读取配置文件
config=configparser.ConfigParser()
with open('config_info.cfg','r') as cfgfile:  
    config.readfp(cfgfile) 
download_file=config.get('info','download_file')
workspace_path=config.get('info','workspace_path')
bb = workspace_path+r'\Failed.txt'
cc = workspace_path+r'\Succeed.txt'


#创建数据库
conn = pymysql.connect(host=str(config.get('info','host')), port=int(config.get('info','port')), user=str(config.get('info','user')),
                       passwd=str(config.get('info','passwd')),db=str(config.get('info','db')),charset="utf8")
cur = conn.cursor()
cur.execute("create table if not exists VideoInfo(uid int(100) NOT NULL AUTO_INCREMENT,links varchar(1024),title varchar(1024),uploader varchar(1024),upload_date varchar(1024),download_time varchar(1024),save_path varchar(1024),PRIMARY KEY(uid))")
conn.commit()
conn.close()

newurl = []

class myHtmlParser(HTMLParser):  

    def __init__(self):  
        HTMLParser.__init__(self)  
        self.flag=None  
  
    # 这里重新定义了处理开始标签的函数  
    def handle_starttag(self,tag,attrs):

        #处理youtube网站
        if re.search('https://www.youtube.com',f) is not None:
            # 判断标签<a>的属性  
            if tag=='a':  
                self.flag='a'  
                for href,link in attrs:  
                    if href=='href':
                        url = 'https://www.youtube.com'
                        whole_link = url+link
                        valid_link = re.findall('https://www.youtube.com/watch\?v=...........',whole_link)
                        for i in range(len(valid_link)):
                            final_link.append(valid_link[i])
                            for name,value in attrs:
                                if name == 'title':
                                    final_title.append(value)
                #筛选channel用
                for name,value in attrs:
                    if name == 'title':
                        channel.append(value)
        
        #处理No.2倍可亲网站
        if re.search('http://www.backchina.',f) is not None:
            if re.search('www.youtube',f) is not None:
                if tag=='iframe':  
                    self.flag='iframe'
                    for src,link in attrs:  
                        if src=='src':
                            final_link.append(link)
            else:
                self.flag='a'
                for href,link in attrs:  
                    if href=='href':
                        url = 'http://www.backchina.com/'
                        whole_link = url+link
                        if re.search('^http://www.backchina.com/video/showlist',whole_link) is not None:
                            contemporary_link.append(whole_link)
                              
        #处理No.4新唐人网站
        if re.search('http://www.ntdtv.com/',f) is not None:
            if tag=='a':  
                self.flag='a'  
                for href,link in attrs:  
                    if href=='href':
                        url = 'http://www.ntdtv.com'
                        whole_link = url+link
                        if re.match('http://www.ntdtv.com/xtr/gb/...........a[0-9]{7}.html$',whole_link) is not None:
                            final_link.append(whole_link)


        #处理No.7八阕网站时政&历史频道
        if re.search('http://video.popyard.com/',f) is not None:
            if tag=='a':  
                self.flag='a'  
                for href,link in attrs:  
                    if href=='href':
                        url = 'http://video.popyard.com/cgi-mod'
                        whole_link = url+link
                        if re.search('^http://video.popyard.com/cgi-mod./show',whole_link) is not None:
                            final_link.append(re.sub('./show','/show',whole_link))


        #处理No.8苹果日报网站
        if re.search('http://hk.apple.nextmedia.com/',f) is not None:
            if tag=='a':  
                self.flag='a'  
                for href,link in attrs:  
                    if href=='href':
                        if re.search('http://hk.apple.nextmedia.com/.................................',link) is not None:
                            final_link.append(link)
                        else:
                            url = 'http://hk.apple.nextmedia.com'
                            whole_link = url+link
                            if re.search('http://hk.apple.nextmedia.com/open/footer/news/...',whole_link) is not None:
                                final_link.append(whole_link)
                            if re.search('http://hk.apple.nextmedia.com/open/footer/international/...',whole_link) is not None:
                                final_link.append(whole_link)

                           
        #处理No.9华尔街日报中文网站
        if re.search('http://www.wsj.com/video/china',f) is not None:
            if tag=='a':  
                self.flag='a'  
                for href,link in attrs:  
                    if href=='href':
                        if re.search('.html$',link) is not None:
                            final_link.append(link)
                            

         #处理No.10文学城网站
        if re.search('http://bbs.wenxuecity.com',f) is not None:
            if tag=='a':  
                self.flag='a'  
                for href,link in attrs:  
                    if href=='href':
                        url = 'http://bbs.wenxuecity.com/80912969724'
                        whole_link = url+link
                        if re.search('^http://bbs.wenxuecity.com/80912969724./[0-9]{6}.html',whole_link) is not None:
                            final_link.append(re.sub('\./','/',whole_link))
                            

         #处理No.11德国之声网站
        if re.search('http://www.dw.com/',f) is not None:
            if tag=='a':  
                self.flag='a'  
                for href,link in attrs:  
                    if href=='href':
                        url = 'http://www.dw.com'
                        whole_link = url+link
                        if re.search('av-[0-9]{8}$',whole_link) is not None:
                            final_link.append(whole_link)


          #处理台湾苹果日报网站local频道
        if re.search('http://www.appledaily',f) is not None: 
            if tag=='a':  
                self.flag='a'  
                for href,link in attrs:  
                    if href=='href':
                        url = 'http://www.appledaily.com.tw'
                        whole_link = url+link
                        if re.match('http://www.appledaily.com.tw/realtimenews/article/local/[0-9]{8}/[0-9]{6}',whole_link) is not None:
                            final_link.append(whole_link[0:72])
#                            print('test1')
                        if re.match('http://www.appledaily.com.tw/realtimenews/article/politics/[0-9]{8}/[0-9]{6}',whole_link) is not None:
                            final_link.append(whole_link[0:75])
#                            print('test2')
                        if re.match('http://www.appledaily.com.tw/realtimenews/article/international/[0-9]{8}/[0-9]{6}',whole_link) is not None:
                            final_link.append(whole_link[0:80])

         #处理No.30石涛网站
        if re.search('http://www.shitaotv.org/',f) is not None:
            if tag=='a':  
                self.flag='a'  
                for href,link in attrs:  
                    if href=='href':
                        if re.match('http://www.shitaotv.org/gb/..../../../Art....html',link) is not None:
                            final_link.append(link)

         #处理No.32Antennas网站
        if re.search('https://plus.google.com/102841474457094676116',f) is not None:
            # 判断标签<a>的属性  
            if tag=='a':  
                self.flag='a'  
                for href,link in attrs:  
                    if href=='href':
                        if re.search('https://www.youtube.com/w',link) is not None:
                            final_link.append(link)
                           
if __name__ == '__main__':
    count=1
    while True:
        conn = pymysql.connect(host=str(config.get('info','host')), port=int(config.get('info','port')), user=str(config.get('info','user')),
                       passwd=str(config.get('info','passwd')),db=str(config.get('info','db')),charset="utf8")
        cur = conn.cursor()
        #从数据库读取youbute网站列表
        cur.execute("SELECT url FROM foreignwebsite")
        url = cur.fetchall()
        ydl_opts = {'outtmpl': '%(id)s.%(ext)s',}
        os.chdir('%s'%download_file)
        failed = open(bb,'w')
        succeed = open(cc,'w')
    
        #爬取链接并写入数据库
        for eachline in url: 
            final_link=[]
            final_title = []
            channel = []
            contemporary_link=[] #爬两级网站用
            f = urlopen('%s'%eachline).read().decode('utf-8','ignore')
            m=myHtmlParser()  
            m.feed(f)
            m.close()
            if re.search('youtube','%s'%eachline) is None:
                for i in range(len(final_link)):
                #查询是否为新link
                    m = cur.execute("SELECT links FROM VideoInfo WHERE links like '%s'"%final_link[i])
                    if m is 0:
                        print(final_link[i])
                        newurl.append(final_link[i])
                        #把新的links写入数据库
                        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                            try:
                                dict=ydl.extract_info('%s'%final_link[i],download=False,)
                                videoid=dict.get('display_id')
                                title=dict.get('title')#re.sub("\'|\"",' ',dict.get('title'))
                                print(title)
                                ext=dict.get('ext')
                                upload_date=dict.get('upload_date')
                                uploader=dict.get('uploader')
                                filename=re.sub(r'\\',r'\\\\',r'%s'%download_file)+r'\\'+videoid+'.'+ext
                                succeed.write('%s\n'%final_link[i])
                                print(111222333)
                                cur.execute("INSERT INTO VideoInfo(links,title,uploader,upload_date,download_time,save_path) VALUES('%s','%s','%s','%s','%s','%s')"%(final_link[i],title,uploader,upload_date,time.ctime(),filename))
                                conn.commit()
                                print(1111)
                            except:
                                failed.write('%s\n'%final_link[i])
                                pass

            if re.search('http://www.backchina',f) is not None:
                for i in range(len(contemporary_link)):
                    #print(contemporary_link[i])
                    f = urlopen(contemporary_link[i]).read().decode('utf-8','ignore')
                    m=myHtmlParser()  
                    m.feed(f)
                    m.close() 
                for i in range(len(final_link)):
                    #查询是否为新link
                    m = cur.execute("SELECT links FROM VideoInfo WHERE links like '%s'"%final_link[i])
                    if m is 0:
                        final_link[i]='http:'+final_link[i]
                        print(final_link[i])
                        newurl.append(final_link[i])
                    #把新的links写入数据库
                        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                            try:
                                dict=ydl.extract_info('%s'%final_link[i],download=False,)
                                videoid=dict.get('display_id')
                                title=dict.get('title')#re.sub("\'|\"",' ',dict.get('title'))
                                print(title)
                                ext=dict.get('ext')
                                upload_date=dict.get('upload_date')
                                uploader=dict.get('uploader')
                                filename=re.sub(r'\\',r'\\\\',r'%s'%download_file)+r'\\'+videoid+'.'+ext
                                succeed.write('%s\n'%final_link[i]) 
                                cur.execute("INSERT INTO VideoInfo(links,title,uploader,upload_date,download_time,save_path) VALUES('%s','%s','%s','%s','%s','%s')"%(final_link[i],title,uploader,upload_date,time.ctime(),filename))
                                conn.commit()
                            except:
                                failed.write('%s\n'%final_link[i])
                                pass          
            else:
                for i in range(int(len(final_link)/2)):
                    #查询是否为新link
                    m = cur.execute("SELECT links FROM VideoInfo WHERE links like '%s'"%final_link[2*i+1])
                    if m is 0:
                        print(final_link[2*i+1])
                        newurl.append(final_link[2*i+1])
                        #把新的links写入数据库
                        #try:
                            #print(final_title[i])
                        #except:
                            #final_title[i]='有不可识别的字符'
                        #try:
                            #num = channel.index("%s"%final_title[0])-1
                        #except:
                            #pass
                        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                            try:
                                dict=ydl.extract_info('%s'%final_link[2*i+1],download=False,)
                                videoid=dict.get('display_id')
                                title=dict.get('title')#re.sub(' ',',',dict.get('title'))
                                print(title)
                                ext=dict.get('ext')
                                upload_date=dict.get('upload_date')
                                uploader=dict.get('uploader')
                                filename=re.sub(r'\\',r'\\\\',r'%s'%download_file)+r'\\'+videoid+'.'+ext
                                succeed.write('%s\n'%final_link[2*i+1])
                                cur.execute("INSERT INTO VideoInfo(links,title,uploader,upload_date,download_time,save_path) VALUES('%s','%s','%s','%s','%s','%s')"%(final_link[2*i+1],title,uploader,upload_date,time.ctime(),filename))
                                conn.commit()
                            except:
                                failed.write('%s\n'%final_link[2*i+1])
                                pass
        succeed.close()
        failed.close()
        cur.execute("INSERT INTO VideoInfo(links,title,uploader,upload_date,download_time,save_path) VALUES('sleeping','%s','sleeping','sleeping','%s','sleeping')"%(count,time.ctime()))
        conn.commit()
        count+=1
        time.sleep(600)
        cur.close()
        conn.close()
        
