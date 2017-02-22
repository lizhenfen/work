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
    res = {}
    t_info = []
    status,outputs = subprocess.getstatusoutput('''ss -ltnp | awk -F' ' 'NR>2 {print $4}' | awk -F':' '{print $NF}' | sort | uniq''')
    outputs = outputs.split('\n')
    for info in outputs:
        t_info.append({
            '{#PORT}': info,
            })
    res['data'] = t_info    
    return json.dumps(res, sort_keys=True, indent=4)
    
    
    
if __name__ == "__main__":
    if sys.argv[1] == 'discovery':
        print port_discovery()