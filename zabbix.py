import sys
import logging

from pyzabbix import ZabbixAPI

stream = logging.StreamHandler(sys.stdout)
stream.setLevel(logging.DEBUG)
log = logging.getLogger('pyzabbix')
log.addHandler(stream)
log.setLevel(logging.DEBUG)


ZABBIXURL = 'http://192.168.15.39/zabbix'
TIMEOUT   = 3
zapi = ZabbixAPI(ZABBIXURL, timeout=TIMEOUT)
zapi.login('admin', 'zabbix')

zapi.template.get({'output':'extend'})
'''
zapi.host.create({
    'host': 'test',
    'groups' : [{
        'groupid': '2'
    }],
    'interfaces':[
        {
            "type": 2,
            "main": 1,
            "useip": 1,
            "ip": "10.0.10.10",
            "dns": "",
            "port": "10050"
        }
    ],
     "templates": [
            {
                "templateid": "20045"
            }
        ],

}
    
)
'''