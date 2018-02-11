#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     drawbotbuilder.py
#

try:
    import drawBot
    drawBotBuilder = drawBot
    # Id to make builder hook name. Views will be calling e.build_html()
    drawBotBuilder.PB_ID = 'drawBot' 
    # Text by import if MacOS specific imports are available.
    import CoreText, AppKit, Quartz # #pylint: disable=unused-import

except ImportError:
    drawBotBuilder = None

class NoneDrawBotBuilder(object):
    """Make NoneDrawBotBuilder with the same API for docTesting, in case the platform does not support DrawBot.
    More methods to be added here, if DrawBotContext docTests fail in non-DrawBot platforms.
    Eventually should be a matching set of methods, compare to DrawBot itself."""

    PB_ID = 'drawBot'

    def newDrawing(self):
        pass

    restore = save = newPath = drawPath = newDrawing # Nethods without attributes

    def scale(self, sx, sy):
        pass

    def translate(self, x, y):
        pass

    def newPage(self, w, h):
        pass

    def moveTo(self, p):
        pass

    lineTo = moveTo

    def openTypeFeatures(self, **openTypeFeatures):
        pass

    def line(self, p1, p2):
        pass

    def oval(self, x, y, w, h):
        pass

    rect = oval

    def line(self, p1, p2):
        pass
        
    def fill(self, *c):
        pass

    setFillColor = cmykFill = fill

    def stroke(self, *c):
        pass

    setStrokeColor = cmykStroke = stroke

    def strokeWidth(self, w):
        pass

    def sizes(self):
        return dict(screen=(800, 600))

    def fontSize(self, fontSize):
        pass

    def textSize(self, s):
        return 10, 10

    def hyphenation(self, language):
        pass

    def image(self, path, p, pageNumber=0, alpha=None):
        pass

    def imageSize(self, path):
        u"""Answer the image size of our test image
        rootPath + '/Examples/Magazines/Fashion/images/IMG_8914.jpg'
        """
        return 3024, 4032

    def FormattedString(self, s):
        class FS(object):
            def __init__(self, s):
                self.s = s
        return FS(s)
        
    def text(self, s, p):
        pass

    def saveImage(self, path, multipage=True):
        pass


noneDrawBotBuilder = NoneDrawBotBuilder()
