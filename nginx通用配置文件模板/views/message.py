#!/usr/bin/python
#coding: utf8

import os.path

import tornado.web
import tornado.ioloop
import tornado.options
from tornado.options import define, options, parse_command_line

import wx

define('port', default=8888, help='run on the given port', type=int)

class SendMsg(tornado.web.RequestHandler):
    def get(self):
        user=None
        obj="this is a test message"
        msg='hollo,  welcome to beijing'
        wx.send_msg(user, obj, msg)
        
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', SendMsg)
        ]
        settings = dict(
            cookie_secret = "this is nginx api",
            template_path = os.path.join(os.path.dirname(__file__),'templates'),
            static_path   = os.path.join(os.path.dirname(__file__), 'static'),
            xsrf_cookies  = True,
        )
        super(Application, self).__init__(handlers, **settings)

        
def main():
    parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
    
if __name__ == "__main__":
    main()
        
