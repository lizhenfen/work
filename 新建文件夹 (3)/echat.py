#!/usr/bin/python
#coding: utf8

import os.path

import tornado.web
import tornado.ioloop
import tornado.options
from tornado.options import define, options, parse_command_line
import tornado.escape
#引入websocket
import tornado.websocket

#引入日志功能
import logging

#其他
import uuid

define('port', default=8080, help='run on the given port', type=int)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')
        
class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()   #保存所有的聊天连接
    
    def open(self):
        #新建一个连接时调用
        ChatSocketHandler.waiters.add(self)
        
    def on_close(self):
        #关闭当前连接时调用
        ChatSocketHandler.waiters.remove(self)
        
    def on_message(self, message):
        logging.info("got meesages %r", message)
        parsed = tornado.escape.json_decode(message)
        self.username = parsed["username"]
        chat = {
            "id": str(uuid.uuid4()),
            "body": parsed["body"],
            "type": "message",
        }
        chat["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=chat))
        ChatSocketHandler.send_updates(chat)
        
    @classmethod
    def send_updates(cls, chat):
        logging.info("sending message to %d waiters", len(cls.waiters))
        for waiter in waiters:
            try:
                waiter.write_message(chat)
            exceptL
                logging.error("Error sendding message", exec_info=True)
                
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/chatsocket', ChatSocketHandler),
        ]
        settings = dict([
            cookie_secret = "this is tornado chat",
            template_path = os.path.join(os.path.dirname(__file__),'templates'),
            static_path   = os.path.join(os.path.dirname(__file__), 'static'),
            xsrf_cookies  = True,
        ])
        super(Application, self).__init__(handlers, **settings)

def main():
    parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
    
if __name__ == "__main__":
    main()
        
