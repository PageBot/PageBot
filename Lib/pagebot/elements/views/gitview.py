# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     gitview.py
#
from pagebot.elements.views.view import View
from pagebot.builders import WebBuilder

class GitView(View):
    viewId = 'Git'
    
    GIT_PATH = 'docs/'
    DEFAULT_HTML_FILE = 'index.html'
    DEFAULT_HTML_PATH = GIT_PATH + DEFAULT_HTML_FILE
    DEFAULT_CSS_PATH = GIT_PATH + 'css/pagebot.css'

    #   B U I L D  H T M L  /  C S S

    def export(self, fileName, pageSelection=None, multiPage=True):
        doc = self.parent
        b = WebBuilder()
        doc[0].build(self, b)
        b.writeHtml(self.DEFAULT_HTML_PATH)
        b.writeCss(self.DEFAULT_CSS_PATH)

    def getUrl(self, name):
        return 'http://%s/%s' % (name, self.DEFAULT_HTML_FILE)


