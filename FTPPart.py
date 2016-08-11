#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
from ftplib import FTP
import os
import time
def ftp_up(filename):  
    ftp.set_debuglevel(2)
    #打开调试级别2，显示详细信息;0为关闭调试信息 
    #print ftp.getwelcome()
    #显示ftp服务器欢迎信息 
    #ftp.cwd('xxx/xxx/')
    #选择操作目录 
    bufsize = 1024
    #设置缓冲块大小 
    file_handler = open(filename,'rb')
    #以读模式在本地打开文件 
    ftp.storbinary('STOR %s' % os.path.basename(filename),file_handler,bufsize)
    #上传文件 
    ftp.set_debuglevel(0) 
    file_handler.close() 
    ftp.quit() 
    print("ftp up OK")
def ftp_down(filename):  
    ftp.set_debuglevel(2)  
    #print ftp.getwelcome()
    #显示ftp服务器欢迎信息 
    #ftp.cwd('xxx/xxx/')
    #选择操作目录 
    bufsize = 1024
    path = 'F:/workspace/PythonVersion4/JsonPart/'+ filename    # 文件保存路径
    #filename1 = r"F:\workspace\PythonVersion4\JsonPart\Suc.txt"
    file_handler = open(filename,'wb')
    #以写模式在本地打开文件 
    ftp.retrbinary('RETR %s' % os.path.basename(filename),file_handler.write,bufsize)
    #接收服务器上文件并写入本地文件 
    ftp.set_debuglevel(0) 
    file_handler.close() 
    ftp.quit() 
    print("ftp down OK")
    
if __name__ == '__main__':
    ftp=FTP()
    ftp.connect('169.254.145.129',21)
    #连接
    ftp.login('','')
    #登录，如果匿名登录则用空串代替即可 

    #ftp_up(r"F:\workspace\PythonVersion4\config.py")
    #ftp_down('config.py')

    ftp.mkd('/ToPlatForm')
    ftp.mkd('/ToPlatForm/1_BK')
    ftp.mkd('/ToPlatForm/1_BK/Data')
    ftp.mkd('/ToPlatForm/1_BK/Ctrl')
    ftp.cwd('/ToPlatForm/1_BK/Data')
    ftp_up(r"F:\workspace\PythonVersion4\video2.0.py")
