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
#     adserver.py
#
#     Server that creates/hosts online ads, using PageBot as engine.
#     http://localhost:5555/index.html
#

import sys
import json
import tornado.httpserver
import tornado.ioloop
import tornado.web

#from pagebot.server.pagebothandler import PageBotHandler
from pagebot.contexts import HtmlContext
from pagebot.web.nanosite.nanosite import NanoSite

PORT = 5555
SSLPORT = 443

regex = r"/([^/]+)"
context = HtmlContext()

class AdHandler(tornado.web.RequestHandler):

    def get(self, slug):
        print('get %s' % slug)
        html = self.get_html()
        self.write(html)

    def post(self, slug):
        print('post %s' % slug)
        data = json.loads(self.request.body.decode('utf-8'))
        print('Got JSON data:', data)
        self.write({ 'got' : 'your data' })

    def get_html(self):
        self.site = NanoSite(context=context)
        html = ''
        html += '<html><head><title>PageBot Server</title></head><body>'
        html += "<h1>Hello world</h1>"
        html += '</body></html>'
        return html

    def data_received(self):
        pass

class AdServer:

    def __init__(self, args=None, cert=None, key=None):
        #self.handlers = [('/', PageBotHandler),]
        self.handlers = [(regex, AdHandler),]

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
    server = AdServer(args=args)
    server.run()
