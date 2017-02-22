#!/usr/bin/env python
#-*- coding: utf8 -*-
import json
import sys

PY2 = sys.version_info[0] == 2 

def getDEVInfo():
    res = {}
    data = []
    
    with open('/proc/mounts') as fp:
        for line in fp:
            dev_dict = {}
            if line.startswith('/dev'):
                line = line.split()
                dev_name, mount_point = line[0], line[1]
                dev_dict['{#DEVNAME}'] = dev_name.split('/')[-1]
                dev_dict['{#MOUNTNAME}'] = mount_point
                data.append(dev_dict)
                
    res['data'] = data
    return json.dumps(res, sort_keys=True, indent=4)
    
def getDEVStatis(devName, item):
    data = {}
    with open('/proc/diskstats') as fp:
        for line in fp:
            if devName in line:
                line = line.strip().split()
                dev_read_counts = line[3]
                dev_read_ms = line[6]
                dev_write_counts = line[7]
                dev_write_ms = line[8]
                dev_io_ms = line[12]
                dev_read_sector = line[5]
                dev_write_sector = line[9]
                data = {
                    'read.ops' : dev_read_counts,
                    'read.ms'  : dev_read_ms,
                    'write.ops': dev_write_counts,
                    'write.ms' : dev_write_ms,
                    'io.ms' : dev_io_ms,
                    'read.sector' : dev_read_sector,
                    'write_sector': dev_write_sector
                }
                if PY2:
                    print data.get(item)
                else:
                    print(data.get(item))
                         
if __name__ == "__main__":
    if sys.argv[1] == 'discovery':
        print getDEVInfo()
    elif sys.argv[1] == 'status':
        getDEVStatis(sys.argv[2], sys.argv[3])
    else:
        print "ERROR: argument error"