
import time
import datetime
import os
import logging
import sys

stream = logging.StreamHandler(sys.stdout)
stream.setLevel(logging.DEBUG)
log = logging.getLogger('通用服务包')
log.addHandler(stream)
log.setLevel(logging.DEBUG)
'''
    1. 解析共享文件
    2. 判断文件是否符合要求: 指定文件开头, 指定文件结尾符, 创建时间，
    3. 判断文件中国是否存在 错误关键字
    5. 报警格式， 报警

'''

def _check_time(f_create_time,starttime=None, endtime=None, days=1):
    '''
        判断输入的时间是否发生在 开始时间和 结束时间。
    '''
    if starttime is None:
        start_time = "11:00:00"
    if endtime is None:
        end_time = str(time.strftime("%H:%M:%S", time.localtime(time.time())))   
    yesterday = str(datetime.date.today() - datetime.timedelta(days)) +" " + start_time
    today     = str(datetime.date.today()) + " " + end_time
    y_time = time.mktime(time.strptime(yesterday,"%Y-%m-%d %H:%M:%S"))
    t_time = time.mktime(time.strptime(today,"%Y-%m-%d %H:%M:%S"))
    return y_time <= f_create_time <= t_time
    

def check_file_time(fd):
    '''
        判断输入的文件的时间戳是否符合要求
        @parameter: fd  输入文件的名称
    '''
    fd_time = os.stat(fd).st_mtime
    return _check_time(fd_time)

    
def read_err_log(err_char, fname):
    '''
        读取日志文件, 返回错误信息。
        @parameter: err_char  匹配的错误文件的关键字
                                ['err1', 'err2']
        @parameter: fname     错误文件名
        @parameter: 返回错误文件的完整路径
    '''
    err_log_files = []
    no_err_read
    with open(fname,encoding="utf-8") as fd:
        data = fd.read()
        for c in err_char:
            if c in data:
                err_log_files.append(fname)
    return err_log_files 
 

def check_file_size(fd):
    '''
        当前函数主要用来判断文件的大小
        只获取 rar文件
    '''
    return os.path.getsize(fd)
 
 
def check_file_size(fd, size=4089):
    fd_size = os.path.getsize(fd)
    return True if fd_size > size else False
 
def check_correct_files(url, postfix=None):
    '''
        获取正确的文件列表
        @parameter: url  windows共享文件路径
                        ('ip','path')
        @parameter: postfix  文件名后缀列表
                        ['.log', '.txt','.rar']
        @parameter: 返回正确的文件列表
    '''
    result = {"bi":[], 'oracle':[], 'log': []}
    if type(url) is tuple:
        scan_url = "\\\\" + "\\".join(url)
       
    if postfix is None:
        postfix = ['.log', '.rar','.txt']
    
    for fd in os.scandir(scan_url):
        fd = fd.name
        full_fd = scan_url + '\\' + fd
        if check_file_time(full_fd) and fd.startswith('err') and fd.endswith('.txt'): 
            #此文件判断BI系统
            if check_file_size(full_fd, 0): continue
            result['bi'].append(full_fd)
            
        if check_file_time(full_fd) and fd.endswith('.rar'):
            # 数据库备份
            # 判断 rar 文件是否小于 8KB
            if full_fd.endswith('.rar'):
                if not check_file_size(full_fd):
                    result['oracle'].append(full_fd)
                    continue
            if full_fd.endswith('.log'):
                result['log'].append(full_fd)

    return result    
    
    
if __name__ == "__main__":
    CHECK_FILES = [("192.168.15.233","JobServer","192.168.15.91,1433_c6_sa"),
                    ("192.168.15.71", "jlfncbak"),
                    ("192.168.15.236",   "ncbak"),
                  ]
    err_msg = []
    ERROR_CHAR = ['failed','成功', 'successfully ']
    for url in CHECK_FILES:
        data = check_correct_files(url)
        print(data)
        '''
        for d in data:
            err_msg += read_err_log(ERROR_CHAR, d)
            print(err_msg)
        '''



    