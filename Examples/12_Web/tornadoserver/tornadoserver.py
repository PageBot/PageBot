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
#     baseserver.py
#
#     https://www.tornadoweb.org
#
import tornado.ioloop
import tornado.web

ioloop = None
counter = 0

PORT = 7777

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        global counter, ioloop
        self.write("Hello, %d worlds" % counter)
        counter += 1
        if counter > 10:
            ioloop.stop()

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    global loop
    app = make_app()
    app.listen(PORT)
    ioloop = tornado.ioloop.IOLoop.current()
    ioloop.start()
    print('Done')

