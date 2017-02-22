#!/usr/bin/env python
#-*- coding: utf8 -*-
#date: 2016-09-13

_autor = "xxx"
import time
import datetime
import os
import weixin

FILE_SIZE="scan.log"

#定位时间
def time_among(f_create_time):
    start_time = "11:00:00"
    end_time = "10:59:59"
    yesterday = str(datetime.date.today() - datetime.timedelta(1)) +" " + start_time
    today     = str(datetime.date.today()) + " " + end_time
    y_time = time.mktime(time.strptime(yesterday,"%Y-%m-%d %H:%M:%S"))
    t_time = time.mktime(time.strptime(today,"%Y-%m-%d %H:%M:%S"))
    return y_time <= f_create_time <= t_time
     
#判断文件的创建时间是否正确
def check_time(fd):
    #yesterday = time.time() - 86400
    return time_among(os.stat(fd).st_mtime)
        
#判断日志文件是否正常
def check_log(logfile):
    with open(logfile) as fd:
        lines = fd.readlines()
        last_line = lines[-1]
        if ("successfully" in last_line) or ("成功" in last_line):
            return True
    return False
    
#判断文件大小
def check_file_size(rarfile):
    return os.path.getsize(rarfile)
    
def check_file(fdlist):
    fd_size = {}
    errfile = []
    for fd in fdlist:
        if fd.endswith(".rar"):
            logfile = fd.strip(".rar") + ".log"
            if check_log(logfile):
                fd_size[fd] = check_file_size(fd)
            else:
                errfile = []     
    return (fd_size,errfile)        
    
#文件大小比较
def get_last_file(resfile):
    res_dict = {}
    if not os.path.exists(resfile):
        return res_dict
    with open(resfile) as fd:
        for l in fd:
            name,size = l.split(" ")
            if name == "" or size == "":
                continue
            try:
                res_dict[name]=int(size)
            except:
                res_dict[name]=-1 
    return res_dict
    
#把当前结果写入扫描文件
def write_curr_file(res_dict,resfile):
    with open(resfile,"w") as fd:
        for k,v in res_dict.items():
            line = " ".join((k,str(v))) + "\n"
            fd.write(line)
"""
def change_dict(checked_dict):
    new_update_dict = {}
    for k in checked_dict:
        if "-" in k:
            n_k = k[:-14]
        else:
            n_k = k[:-12]
        new_update_dict[n_k] = checked_dict[k]
    return new_update_dict            
""" 
#比较上次扫描和当前的扫描结果
def check_scan_res(curr_dict, last_dict=None):
    if last_dict is None:
        last_dict = get_last_file(FILE_SIZE)
        #last_dict = change_dict(last_dict)
    #curr_dict = change_dict(curr_dict)
    res_dict = {"warn":{}, "add":{} , 'reduce':{}}
    
    if len(set(curr_dict).difference(set(last_dict))) == 0:
        for k in last_dict:
            if int(curr_dict[k]) - int(last_dict[k]) >= 0:
                return res_dict
            else:
                #文件变小了
                res_dict["warn"].update({k:curr_dict})
    elif len(set(curr_dict).difference(set(last_dict))) > 0:
        k_sets = set(curr_dict).difference(set(last_dict))
        for k in k_sets:
            res_dict["add"].update({k:curr_dict[k]})
    elif len(set(last_dict).difference(set(curr_dict))) > 0:
        k_sets = set(last_dict).difference(set(curr_dict))
        for k in k_sets:
            res_dict["reduce"].update({k:last_dict[k]})
    write_curr_file(curr_dict,FILE_SIZE)    
    return res_dict  
   
#获取昨天到今天的文件名        
def get_files(url, postfix):
    f_list = []
    if type(url) is tuple:
        scan_url = "\\\\" + "\\".join(url)
    for fd in os.scandir(scan_url):
        fd = fd.name
        if "." in fd and fd[fd.rfind("."):] in postfix:
            if type(url) is tuple:
                full_fd = os.sep.join((os.sep,) + url + (fd,))
                #full_fd = scan_url + "\\" + fd
                if check_time(full_fd):
                    f_list.append(full_fd)
    return f_list    

def check_list(url):
    #返回符合标准的文件
    postfix = [r".rar", r".log"]
    res_l = get_files(url, postfix)
    if res_l == []:
        return False
    return res_l


if __name__ == "__main__":
    started = time.time()
    check_url = [ ("192.168.15.71","jlfncbak"),("192.168.15.236","ncbak")]
    d_dict = {}
    for url in check_url:
        res_l = check_list(url)
        if not res_l:
            #没有检查到文件
            exit(2)
        curr_dict, err = check_file(res_l)
        test_dict = {"\\".join(url):len(curr_dict)}
        d_dict.update(curr_dict)
        d_dict.update(test_dict)
    res = check_scan_res(d_dict)
    ended = time.time()
    weixin.send_msg("check finished")
    print(res)
    print("本次检查花费时间: %f"% (ended - started)) 
 
