#!/usr/bin/env python
#-*- coding:utf8 -*-
import sys
import smtplib
import socket
from email.mime.text import MIMEText

#配置SMTP服务器
smtp_server =  "mail.vats.com.cn"
smtp_port   = 465
username = "lz999@vats.com.cn"
password = "Vats888"
from_addr = 'lz999@vats.com.cn'
to_addr = '743564797@qq.com'

#获取发送内容
err_content = sys.argv[1:]
err_content = ' '.join(err_content)
if not err_content:
    pass

#本机信息
ip = socket.gethostbyname(socket.gethostname())
  
#组装信息
msg = MIMEText(err_content,_charset='utf8')
msg['Subject']= 'nginx api(%s)' % (ip,)
msg['From'] = from_addr
msg['To'] = to_addr

#发送信息
smtpobj = smtplib.SMTP_SSL()
smtpobj.connect(smtp_server,smtp_port)
smtpobj.login(username,password)
smtpobj.sendmail(from_addr,to_addr,msg.as_string())
smtpobj.close()
