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
#     nonebuilder.py
#
import os
from pagebot.toolbox.transformer import path2Name

class NoneBezierPath(object):
    u"""Make NoneBezierPath with the same API for NoneDrawBotBuilder drawing texting."""

    def moveTo(self, p):
        pass

    lineTo = moveTo

    def quadTo(self, pcp, p):
        pass

    def curveTo(self, bcp1, bcp2, p):
        pass

    def closePath(self):
        pass

    def appendPath(self, path):
        pass

        
class NoneImageObject(object):
    u"""Nabe NoneImageObject with the same API got NonDrawBotBuilder."""
    def __init__(self, path):
        self.path = path

class NoneBuilder(object):
    """Make NoneBuilder with the same API for docTesting, in case the platform does not support DrawBot.
    More methods to be added here, if DrawBotContext docTests fail in non-DrawBot platforms.
    Eventually should be a matching set of methods, compare to DrawBot itself."""

    def __init__(self):
        self._installedFonts = []

    def newDrawing(self, path=None):
        pass

    def frameDuration(self, v):
        pass

    restore = save = drawPath = newDrawing # Methods without attributes

    BezierPath = NoneBezierPath

    def newPath(self):
        return NoneBezierPath()

    def scale(self, sx, sy):
        pass

    def translate(self, x, y):
        pass

    def newPage(self, w, h):
        pass

    def moveTo(self, p):
        pass

    lineTo = moveTo

    def curveTo(self, bcp1, bcp2, p):
        pass

    def openTypeFeatures(self, **openTypeFeatures):
        pass

    def closePath(self):
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

    def font(self, font):
        pass

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

    def transform(self, t):
        pass

    def FormattedString(self, s):
        class FS(object):
            def __init__(self, s):
                self.s = s
        return FS(s)

    def text(self, s, p):
        pass

    def saveImage(self, path, multipage=True):
        pass

    def installFont(self, fontPath):
        self._installedFonts.append(fontPath)
        if os.path.exists(fontPath):
            return path2Name(fontPath)
        return None

    def fontName2FontPath(self, fontName):
        u"""We cannot tell the relation of the font name and the font path for DrawBot without OSX
        Unless it is a path."""
        if os.path.exists(fontName):
            return fontName
        return None

    def ImageObject(self, path):
        return NoneImageObject(path)


class NoneDrawBotBuilder(NoneBuilder):

    PB_ID = 'drawBot'

class NoneSvgBuilder(NoneBuilder):

    PB_ID = 'svg'

class NoneFlatBuilder(NoneBuilder):

    PB_ID = 'flat'

    def document(self, w, h, units):
        pass


if __name__ == '__main__':
    import doctest
    doctest.testmod()
