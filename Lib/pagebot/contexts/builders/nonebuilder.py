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
#     nonebuilder.py
#

import os
from pagebot.toolbox.transformer import path2Name
from pagebot.contexts.builders.basebuilder import BaseBuilder
from pagebot.contexts.bezierpaths.nonebezierpath import NoneBezierPath
from pagebot.contexts.imageobjects.noneimageobject import NoneImageObject

class NoneBuilder(BaseBuilder):
    """Make NoneBuilder with a general builder API for docTesting. Used for
    example when the platform does not support DrawBot. Methods need to be
    added here when DrawBotContext docTests fail with non-DrawBot platforms.

    NOTE: when completed this set of methods should match with DrawBot
    itself."""

    BezierPath = NoneBezierPath

    def newDrawing(self, path=None):
        pass

    def newPage(self, w, h):
        pass

    def frameDuration(self, v):
        pass

    def restore(self):
        pass

    def save(self):
        pass

    def drawPath(self):
        pass

    def newPath(self):
        pass

    def scale(self, sx, sy):
        pass

    def translate(self, x, y):
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

    def rect(self, x, y, w, h):
        pass

    def line(self, p1, p2):
        pass

    def fill(self, r, g=None, b=None, a=None, alpha=None):
        # Covering API inconsistencies in DrawBot
        pass

    setFillColor = setStrokeColor = stroke = fill

    def cmykFill(self, c, m=None, y=None, k=None, a=None, alpha=None):
        # Covering API inconsistencies in DrawBot
        pass

    cmykStroke = cmykFill

    def strokeWidth(self, w):
        pass

    def sizes(self):
        return dict(screen=(800, 600))

    def installedFonts(self, pattern=None):
        return []

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
        """Answers the image size of our test image

        path = getResourcesPath() + '/images/peppertom_lowres_398x530.png'
        """
        return 398, 530

    def clipPath(self, clipPath):
        pass

    def numberOfImages(self, path):
        return 1

    def transform(self, t):
        pass

    def rotate(self, angle, center=None):
        pass

    def text(self, s, p):
        pass

    def textBox(self, s, r):
        pass

    def saveImage(self, path, multipage=True):
        pass

    def installFont(self, fontPath):
        self._installedFonts.append(fontPath)
        if os.path.exists(fontPath):
            return path2Name(fontPath)
        return None

    def save(self):
        pass

    def restore(self):
        pass

    def fontName2FontPath(self, fontName):
        """We cannot tell the relation of the font name and the font path for
        DrawBot without OS X unless it is a path."""
        if os.path.exists(fontName):
            return fontName
        return None

    def FormattedString(self, s):
        class FS:
            def __init__(self, s):
                self.s = s
        return FS(s)

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
