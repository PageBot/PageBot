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

import tornado.ioloop
import tornado.web
from pagebot.server.pagebothandler import PageBotHandler


handlers = [(r"/entry/([^/]+)", BaseHandler),]

PORT = 7777

if __name__ == "__main__":
    app = tornado.web.Application(handlers)
    app.listen(PORT)
    print('Started PageBot/Tornado web application on port %s' % PORT)
    tornado.ioloop.IOLoop.current().start()
