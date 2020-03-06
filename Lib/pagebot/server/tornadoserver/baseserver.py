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
#     BaseServer.py
#
#     usinghttps://www.tornadoweb.org
#
#     Testing available parameters on the url page call.
#     This example server shows how different paths (detected by regular expressions)
#     are connected to different handlers, ranging from a simple request, reading a static 
#     html page file, getting specific URL arguments (http://localhost:8886/query/aaa?n=100)
#     or disassembling the URL path by regular expressions.
#     This means that "parts" of the site can use different handlers than other parts.
#
#     http://localhost:8889
#     http://localhost:8889/blog
#     http://localhost:8889/query?n=100
#     http://localhost:8889/query/aaa?n=100
#     http://localhost:8889/resource/1234
#     http://localhost:8889/resource/abcd-200/xyz-100

from tornado.ioloop import IOLoop
from pagebot.server.tornadoserver.basehandlers import BaseHandler

PORT = 8889

if __name__ == '__main__':
    requestHandler = [
        ('/', BasicRequestHandler), # http://localhost:8889
        ('/blog', StaticRequestHandler), # http://localhost:8889/blog
        ('/query', QueryRequestHandler), # http://localhost:8889/query?n=100
        ('/query/aaa', QueryRequestHandler), # http://localhost:8889/query/aaa?n=100
        ('/resource/([0-9]+)', ResourceRequestHandler), # http://localhost:8889/resource/1234
        ('/path/([A-Za-z0-9-]+)/([A-Z,a-z,0-9-]+)', PathRequestHandler), # http://localhost:8889/path/aaa/bbb
    ]
    app = Application(requestHandler)
    app.listen(PORT)
    print('Server on port', PORT)
    IOLoop.current().start()
