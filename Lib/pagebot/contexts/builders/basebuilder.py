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
#     basebuilder.py
#

import os
from pagebot.toolbox.transformer import path2Name

class BaseBuilder:
    """The BaseBuilder is the abstract builder class, for all builders that
    need to import and write files in a directory, or draw on their builders,
    besides the binary export formats that are already supported by e.g.
    DrawBot."""

    def __init__(self):
        self._installedFonts = []

    def installedFonts(self, pattern=None):
        return []

    def newDrawing(self, path=None):
        raise NotImplementedError

    def frameDuration(self, secondsPerFrame):
        raise NotImplementedError

    def restore(self):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError

    def drawPath(self):
        raise NotImplementedError

    def newPath(self):
        raise NotImplementedError

    def scale(self, sx, sy):
        raise NotImplementedError

    def translate(self, x, y):
        raise NotImplementedError

    def newPage(self, w, h):
        raise NotImplementedError

    def moveTo(self, p):
        raise NotImplementedError

    lineTo = moveTo

    def curveTo(self, bcp1, bcp2, p):
        raise NotImplementedError

    def openTypeFeatures(self, **openTypeFeatures):
        raise NotImplementedError

    def closePath(self):
        raise NotImplementedError

    def line(self, p1, p2):
        raise NotImplementedError

    def oval(self, x, y, w, h):
        raise NotImplementedError

    def rect(self, x, y, w, h):
        raise NotImplementedError

    def line(self, p1, p2):
        raise NotImplementedError

    def fill(self, r, g=None, b=None, a=None, alpha=None):
        # Covering API inconsistencies in DrawBot
        raise NotImplementedError

    setFillColor = setStrokeColor = stroke = fill

    def cmykFill(self, c, m=None, y=None, k=None, a=None, alpha=None):
        # Covering API inconsistencies in DrawBot
        raise NotImplementedError

    cmykStroke = cmykFill

    def strokeWidth(self, w):
        raise NotImplementedError

    def sizes(self):
        return dict(screen=(800, 600))

    #   T E X T

    def font(self, font, fontSize=None):
        raise NotImplementedError

    def fontSize(self, fontSize):
        raise NotImplementedError

    def textSize(self, bs, width=None, height=None, align=None):
        #return 10, 10
        raise NotImplementedError

    def hyphenation(self, language):
        raise NotImplementedError

    def image(self, path, p, pageNumber=0, alpha=None):
        raise NotImplementedError

    def imageSize(self, path):
        """Answers the image size of our test image

        path = getResourcesPath() + '/images/peppertom_lowres_398x530.png'
        """
        return 398, 530

    def clipPath(self, clipPath):
        raise NotImplementedError

    def numberOfImages(self, path):
        return 1

    def transform(self, t):
        raise NotImplementedError

    def rotate(self, angle, center=None):
        raise NotImplementedError

    def text(self, s, p):
        raise NotImplementedError

    def textBox(self, s, r):
        raise NotImplementedError

    def saveImage(self, path, multipage=True):
        raise NotImplementedError

    def installFont(self, fontPath):
        self._installedFonts.append(fontPath)
        if os.path.exists(fontPath):
            return path2Name(fontPath)
        return None

    def save(self):
        raise NotImplementedError

    def restore(self):
        raise NotImplementedError

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
        raise NotImplementedError
