#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     pagebotserver.py
#

import sys
import tornado.httpserver
import tornado.ioloop
import tornado.web
from pagebot.server.pagebothandler import PageBotHandler



PORT = 7777
SSLPORT = 443

regex = r"/([^/]+)"

class PageBotServer:

    def __init__(self, args=None, cert=None, key=None):
        #self.handlers = [('/', PageBotHandler),]
        self.handlers = [(regex, PageBotHandler),]

        if args and '--port' in args:
            #try:
            port = int(args[-1])
            self.port = port
            #except Exception as e:
            #    self.port = PORT
            #    print(e)

        else:
            self.port = PORT

        self.app = tornado.web.Application(self.handlers)


        if cert and key:
            ssl_options = {
                "certfile": cert,
                "keyfile": key,
            }

            http_server = tornado.httpserver.HTTPServer(self.app, ssl_options=ssl_options)
            http_server.listen(SSLPORT)
        else:
            http_server = tornado.httpserver.HTTPServer(self.app)
            http_server.listen(self.port)
            #self.app.listen(self.port)

    def run(self):
        print('Starting PageBot/Tornado web application on port %s' % self.port)
        tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    args = sys.argv[1:]
    server = PageBotServer(args=args)
    server.run()
