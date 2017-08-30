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
#     basebuilder.py
#
import codecs

class BaseBuilder(object):
    u"""The BaseBuilder is the abstract builder class, for all builders that need
    to import and write files in a directory, besides the binary export formats that are already
    supported by DrawBot."""

    def __init__(self):
        self._htmlOut = [] 
        self._cssOut = []  
        self._jsOut = []  
        self._copyPaths = []
        self._initialize()
        
    def addHtml(self, html):
        u"""Add the html chunk to self.html, the ordered list of html for output."""
        self._htmlOut.append(html)

    write = addHtml

    def importHtml(self, path):
        u"""Import a chunk of UTF-8 HTML code from the path."""
        f = codecs.open(path, 'r', 'utf-8')
        self.addHtml(f.read())
        f.close()

    def writeHtml(self, path):
        u"""Write the collected set of html chunks to path."""
        f = codecs.open(path, 'w', 'utf-8')
        f.write(''.join(self._htmlOut))
        f.close()

    def addCss(self, css):
        u"""Add the css chunk to self.css, the ordered list of css for output."""
        self._cssOut.append(css)

    def importCss(self, path):
        u"""Import a chunk of UTF-8 CSS code from the path."""
        f = codecs.open(path, 'r', 'utf-8')
        self.addCss(f.read())
        f.close()

    def writeCss(self, path):
        u"""Write the collected set of css chunks to path."""
        f = codecs.open(path, 'w', 'utf-8')
        f.write(''.join(self._cssOut))
        f.close()

    def addJs(self, js):
        self._jsOut.append(js)

    def importJs(self, path):
        u"""Import a chunk of UTF-8 CSS code from the path."""
        f = codecs.open(path, 'r', 'utf-8')
        self.addJs(f.read())
        f.close()

    def copyPath(self, path):
        u"""Collect path of files to copy to the output website."""
        self._copyPaths.append(path)


