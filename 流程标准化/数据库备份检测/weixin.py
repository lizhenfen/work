#!/usr/bin/env python
version = '1.0.1'
version_info = (1,0,1)
import requests
import json

_user_secret = {'appid' : 'wxe94db0c2eaa455a1' ,
          'secure':'jb9Yoejq4aLgrgO9ChQxgOEAtNWZ0zAgUSys6ni6EpsfDfBSCGsfOQw7Ne6363rr',
         }

def _get_token(appid,secure):
  url='https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={0}&corpsecret={1}'.format(appid,secure)
  req = requests.get(url)  
  data = json.loads(req.text)
  print(data["access_token"])
  return data["access_token"]
  
def send_msg(msg,user='lizhen',token=None):
    #headers = {"Content-Type": "application/json;charset=utf-8"} 
    headers = {"Content-Type": "application/json"} 
    token = _get_token(**_user_secret)
    url="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(token)
    values = """{
        "touser": "%s",
        "toparty": "2",
        "totag": "",
        "msgtype": "text",
        "agentid": 2,
        "text": {
            "content": '%s'
        },
        "safe":0
            }"""  % (user, msg)
    data = json.dumps(values)
    req = requests.post(url,data=data,headers=headers)  
    print(req)
  
if __name__ == '__main__':
    msg = "中"
    send_msg(msg, '@all')
