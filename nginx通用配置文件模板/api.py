#!/usr/bin/python
#coding: utf8

import os
import tornado.web
import tornado.ioloop
import tornado.options
from tornado.options import define, options, parse_command_line
import tornado.template as template
#import torndb 


define('port', default=8888, help='run on the given port', type=int)
define('mysql_host', default="127.0.0.1:3306", help='mysql host')
define('mysql_database', default="jobs", help='job db')
define('mysql_user', default="job", help='run on the given port')
define('mysql_passwd', default="job", help='run on the given port')



#执行命令
try:
    import commands as subprocess
except:
    import subprocess


'''
    1. 用户填写记录，发送到后台
    2. 后台接收信息，并保存到数据库
    3. 页面上显示记录
    4. 可修改页面

'''

#加载模板文件
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates")


def filehandle(template_name, save__file_name, project_name=None, template_param=None):
    TEMPLATE_PATH1 = os.path.join(TEMPLATE_PATH, project_name)
    loader = template.Loader(TEMPLATE_PATH1)
    t = loader.load(template_name)
    with open(save__file_name, 'wb') as fd:
        fd.write(t.generate(**template_param))


class NginxMainHandler(tornado.web.RequestHandler):
    '''
        文件名称: nginx.conf
        1. 获取请求，保存文件
        2. 文件分发
        3. 文件测试
        5. 服务重启
    '''
    #db = self.application.db
    def get(self):
        self.render('index.html')
    def post(self):
        NGINX_NAME = 'nginx.conf'
        nginx_user = self.get_argument('nginx_user') or 'nginx'
        worker_connections = self.get_argument('worker_connections') or 10240
        worker_rlimit_nofile = self.get_argument('worker_rlimit_nofile') or 65535
        server_tokens = self.get_arguments('server_tokens') or 'off'
        network_control = self.get_argument('network_control') or 'on'
        net_push = self.get_argument('net_push') or 'on'
        keepalive_timeout = self.get_argument('keepalive_timeout') or 65
        gzip_switch = self.get_argument('gzip_switch') or 'on'
        gzip_min_length = self.get_argument('gzip_min_length') or 1000
        nginx = {
            'nginx_user': nginx_user,
            'worker_connections': worker_connections,
            'worker_rlimit_nofile': worker_rlimit_nofile,
            'server_tokens': server_tokens,
            'network_control': network_control,
            'net_push': net_push,
            'keepalive_timeout': keepalive_timeout,
            'gzip_switch': gzip_switch,
            'gzip_min_length': gzip_min_length,
        }
        #数据库

        #db.execute("insert into nginx values(%(nginx_user)s,%(worker_connections)s,%(worker_rlimit_nofile)d,%(server_tokens)s,%(network_control)s,%(net_push)s,%(keepalive_timeout)d,%(gzip_switch)s,%(gzip_min_length)d )",**nginx)
        ##写文件后期使用celery
        filehandle('nginx.yaml', NGINX_NAME, loader, nginx)
        res = subprocess.getstatusoutput('\cp %s /tmp/' % NGINX_NAME)
        if res[0] != 0:
            pass
        self.render('nginx.yaml', **nginx)

        
class NginxLocationHandler(tornado.web.RequestHandler):
    def post(self):
        self.render('index.html')
    def get(self):
        NGINX_NAME = 'location.conf'
        location = {
           'expression' : ' ',
           'uri': '/',
           'uri_rewrite': True,
           'uri_src': '/token/(.*)$',
           'uri_dest': "/vats-api-test/$1",
           'upstream_name' : 'test', 
        }
        #模板写成文件
        filehandle('location.yaml', NGINX_NAME, loader, location)
        self.render('location.yaml', **location )    

        
class NginxUpstreamHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html')
        
    def post(self): 
        upstream = {
            'name': 'test',
            'port': 443,
            'ips': [{
                'ip': '10.0.0.1',
                'weight': 10,
                'count': 2,
                'timeout': 2,
                },],
            'server_name': 'test.vats.com.cn',
            'ssl': True,
            'log_swith': True
        }
        PROJECT_NAME = 'nginx'
        UPSTREAM_NAME = upstream['server_name'] + '.upstream'
        #模板写成文件
        filehandle('upstream.yaml', UPSTREAM_NAME, PROJECT_NAME, upstream)
        
        self.redirect('/')

        
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/xxo', NginxLocationHandler),
            (r'/', NginxUpstreamHandler),
            (r'/xx', NginxMainHandler)
        ]
        settings = dict(
            cookie_secret = "this is nginx api",
            template_path = os.path.join(os.path.dirname(__file__),'templates'),
            static_path   = os.path.join(os.path.dirname(__file__), 'static'),
            xsrf_cookies  = True,
        )
        super(Application, self).__init__(handlers, **settings)
        '''
        self.db = torndb.Connection(
            host = options.mysql_host,
            database = options.mysql_database,
            user = options.mysql_user,
            password = options.mysql_passwd,
            
        )'''
        
def main():
    parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
    
if __name__ == "__main__":
    main()
        
