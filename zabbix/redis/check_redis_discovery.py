#!/bin/env python

import  sys
import json


try:
    import  commands as subprocess
except:
    import  subprocess

def redis_discovery():
    res = {}
    info = []
    #status,outputs = subprocess.getstatusoutput('''sudo ss -tlnp|grep 'redis-server'|awk '{print $4}'|awk -F':' '{print $(NF)}'|sort -u''')
    status,outputs = subprocess.getstatusoutput('''sudo ss -tlnp|grep 'redis-server'|awk '{print $4}' ''')
    outputs = outputs.split('\n')
    for ips in outputs:
        ip = ips.split(':')[0]
        if ip == '0.0.0.0' or ip == '*':
            ip = '127.0.0.1'
        port = ips.split(':')[1]
        info += [{'{#REDISIP}':ip,'{#REDISPORT}': int(port)}]
    res['data'] = info
    print json.dumps(res, sort_keys=True, indent=4)

def redis_status(ip, port, status):
    REDISCMD="redis-cli -h %s -p %s" % (ip, port)
    res = {}
    if status == 'ping':
        st,outputs = subprocess.getstatusoutput('''redis-cli -h %s -p %s ping | grep PONG | wc -l ''' % (ip,port))
        print outputs
        return
    st,outputs = subprocess.getstatusoutput('''redis-cli -h %s -p %s info | grep %s''' % (ip,port,status))
    outputs = outputs.split('\n')
    
    for line in outputs:
        if line.startswith('#'):
            continue
        da = line.split(':')
        if len(da) < 2:
            continue
        k,v = da
        v = v.rstrip('\r')
        res.update({k:v})
    print res.get(status,0)
   
if __name__ == "__main__":
    if sys.argv[1] == 'discovery':
        redis_discovery()
    elif sys.argv[1] == 'status':
        redis_status(sys.argv[2], sys.argv[3], sys.argv[4])
        
