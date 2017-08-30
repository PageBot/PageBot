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
#     webnuilder.py
#
import codecs

class WebData(object):
    u"""Generic output builder container, used of collecting html, css, js, include paths and other data
    needed to export the website, e.g. by the MampView."""
    def __init__(self):
        self.html = []
        self.css = []
        self.js = []
        self.includePaths = []

    def appendHtml(self, html):
        u"""Add the html chunk to self.html, the ordered list of html for output."""
        self.html.append(html)

    def readHtml(self, path):
        u"""Read a chunk of HTML code from the path."""
        f = codecs.open(path, 'r', 'utf-8')
        self.html(f.read())
        f.close()

    def writeHtml(self, path):
        u"""Write the collected set of html chunks to path."""
        f = codecs.open(path, 'w', 'utf-8')
        f.write(''.join(self.html))
        f.close()

    def appendCss(self, css):
        u"""Add the css chunk to self.css, the ordered list of css for output."""
        self.css.append(css)

    def readCss(self, path):
        f = codecs.open(path, 'r', 'utf-8')
        self.appendCss(f.read())
        f.close()

    def writeCss(self, path):
        u"""Write the collected set of css chunks to path."""
        f = codecs.open(path, 'w', 'utf-8')
        f.write(''.join(self.css))
        f.close()

    def appendJs(self, js):
        self.js.append(js)

    def appendIncludePath(self, path):
        self.includePaths.append(path)

