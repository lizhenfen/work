#!/usr/bin/env python

import time
import datetime
import os


'''
    1. 查找符合条件的文件
        1. err_xxxxx.txt  
        2. 昨天到今天
    2. 查看文件大小 ， 确认存在关键字: failed
    3. 如果出现了failed， 打印出 |Data flow
    (14.2) 12-03-16 02:00:30 (X) (2856:11952) DBS-070402: |Data flow JW_DW抽取掌上金网基础数据|Reader SQL
'''


#定位时间
def time_among(f_create_time):
    start_time = "11:00:00"
    #end_time = "15:59:59"
    end_time = str(time.strftime("%H:%M:%S", time.localtime(time.time())))
    yesterday = str(datetime.date.today() - datetime.timedelta(1)) +" " + start_time
    today     = str(datetime.date.today()) + " " + end_time
    y_time = time.mktime(time.strptime(yesterday,"%Y-%m-%d %H:%M:%S"))
    t_time = time.mktime(time.strptime(today,"%Y-%m-%d %H:%M:%S"))
    return y_time <= f_create_time <= t_time
    
def check_file_name(fname):
    # error_04_27_2016_15_19_xxxx
    return time_among(os.stat(fname).st_mtime)

#文件读取,生成错误日志列表
def file_read(err_char, fname):
    err_list = []
    with open(fname,encoding="utf-8") as fd:
        data = fd.read()
        for c in err_char:
            if c in data:
                err_list.append(fname)
    return err_list 
  
def check_all_files(url, postfix):
    f_list = []
    if type(url) is tuple:
        scan_url = "\\\\" + "\\".join(url)
    for fd in os.scandir(scan_url):
        fd = fd.name
        if "." in fd and fd[fd.rfind("."):] in postfix:
            if type(url) is tuple and fd.startswith('err'):
                full_fd = os.sep.join((os.sep,) + url + (fd,))
                if check_file_name(full_fd):
                    f_list.append(full_fd)
    return f_list    

def check_right_files(url):
    postfix = [".txt"]
    return check_all_files(url, postfix)


if __name__ == "__main__":
    CHECK_FILES = [("192.168.15.233\JobServer","192.168.15.91,1433_c6_sa")]
    res = []
    ERROR_CHAR = ['failed',]
    for url in CHECK_FILES:
        data = check_right_files(url)
        for d in data:
            if file_read(ERROR_CHAR, d):
                res.extend(file_read(ERROR_CHAR, d))
    if res:
        print('\n'.join(res))
