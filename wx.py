#!/usr/bin/python

version = '1.0.1'
version_info = (1,0,1)
import requests
import json
import sys
import time

user_secret = {'appid' : 'wxe94db0c2eaa455a1' ,
          'secure':'jb9Yoejq4aLgrgO9ChQxgOEAtNWZ0zAgUSys6ni6EpsfDfBSCGsfOQw7Ne6363rr',
         }

def _get_token(appid,secure):
    _start_time = 0
    _end_time = time.time()
    time_among = 7200
    if _start_time = 0 or _end_time - _start_time >= 7200:
        url='https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={0}&corpsecret={1}'.format(appid,secure)
        req = requests.get(url)  
        data = json.loads(req.text)
        _start_time = _end_time
    return data["access_token"]
 
 
def send_msg(user,obj,msg,token=None):
    if not token:
        token = _get_token(**user_secret)
    url="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(token)
    if user:
        user="@all"
    values={
        "touser":user,
        "toparty": "2",
        "totag": "",
        "msgtype": "text",
        "agentid": 2,
        "text": {
            "content": '\n'.join((obj,msg))
               },
        "safe": "0"
        }
    data = json.dumps(values,ensure_ascii=False)
    req = requests.post(url,data)  
    
if __name__ == '__main__':
    user = 'lizhen'
    obj = 'xx'
    msg = 'oo'
    send_msg(obj=obj,msg=msg,user=None)
