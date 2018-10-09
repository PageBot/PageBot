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
#     gitview.py
#
from pagebot.elements.views.siteview import SiteView
from pagebot.constants import ORIGIN

class GitView(SiteView):
    viewId = 'Git'

    GIT_PATH = 'docs/'
    DEFAULT_HTML_FILE = 'index.html'
    DEFAULT_HTML_PATH = GIT_PATH + DEFAULT_HTML_FILE
    DEFAULT_CSS_PATH = GIT_PATH + 'css/style.css'

    #   B U I L D  H T M L  /  C S S

    def build(self, path=None, pageSelection=None, multiPage=True):

        doc = self.doc

        sitePath = self.GIT_PATH
        if not sitePath.endswith('/'):
            sitePath += '/'

        b = self.b # Get builder from self.doc.context of this view.
        for pn, pages in doc.pages.items():
            for page in pages:
                b.resetHtml()

                hook = 'build_' + b.PB_ID
                getattr(page, hook)(self, ORIGIN) # Typically calling page.build_drawBot or page.build_flat

                fileName = page.name
                if not fileName:
                    fileName = self.DEFAULT_HTML_FILE
                if not fileName.lower().endswith('.html'):
                    fileName += '.html'

                b.writeHtml(sitePath + fileName)
        # Write all collected CSS into one file
        #b.writeCss(self.DEFAULT_CSS_PATH)

    def getUrl(self, name):
        return 'http://%s/%s' % (name, self.DEFAULT_HTML_FILE)


