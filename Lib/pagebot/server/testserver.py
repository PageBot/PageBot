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
#     testserver.py
#
#     https://www.tornadoweb.org
#
#     Testing available parameters on the url page call.

import tornado.ioloop
import tornado.web

counter = 0

PORT = 8888

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        global counter
        self.write('<html><head><title>PageBot Server</title></head><body>')
        self.write("<h1>Hello, %d world</h1>" % counter)
        self.write(str(self.__dict__.keys()))
        self.write('<br/>')
        self.write(str(self.request))
        self.write('<br/>')
        self.write(str(self.path_args))
        self.write('<br/>')
        self.write(str(self.path_kwargs))
        self.write('<br/>')
        self.write(str(self.ui))
        self.write('<br/>')
        self.write(str(self._headers))
        self.write('</body></html>')
        counter += 1

    def data_received(self):
        pass

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(PORT)
    print('Starting Tornado web application on port %s' % PORT)
    tornado.ioloop.IOLoop.current().start()
