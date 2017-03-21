#!/bin/env python
#-*- coding: utf8 -*-
'''
查找符合实际的文件
判断 是否存在 .dmp 的文件

判断 rar文件的大小
判断 log文件中 是否存在关键字

计算文件的个数

t = 'users:(("zabbix_agentd",21703,5),("zabbix_agentd",21705,5),("zabbix_agentd",21706,5),("zabbix_agentd",21707,5))'
'''
import  sys
import json
try:
    import  commands as subprocess
except:
    import  subprocess

    
def port_discovery():
    process_name = ['cupsd', 'rpc.statd', 'rpcbind', 'master', 'sshd']
    res = {}
    t_info = []
    status,outputs = subprocess.getstatusoutput('''ss -ltunp | awk -F' ' '{print $1,$2,$5,$7}' ''')
    outputs = outputs.split('\n')[1:]
    for info in outputs:
        try:
            info = info.split(' ')
            protocal = info[0]
            if protocal == "udp": continue
            status   = info[1]
            ip       = info[2]
            ips      = ip.split(':')
            port     = ips[-1]
            if port == "10050": continue  # zabbix client listen
            local_ip = ips[0]
            if local_ip == '' or local_ip == '127.0.0.1':
                continue
            app      = info[3].split(":")[-1]
            app_name = app.strip("(())").split("),(")
            app_name = set([ i.split(',')[0] for i in app_name ])
            if app_name in process_name: continue
            t_info += [{
                '{#PROTOCOL}':protocal, 
                '{#STATUS}': status,
                '{#PORT}': port,
                '{#APPNAME}': app_name.pop().strip('"')
                }]
        except IndexError,e:
            info = []
    res['data'] = t_info    
    return json.dumps(res, sort_keys=True, indent=4)
    
    
    
if __name__ == "__main__":
    if sys.argv[1] == 'discovery':
        print port_discovery()