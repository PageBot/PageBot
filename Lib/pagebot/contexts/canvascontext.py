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
#     canvascontext.py
#

from pagebot.contexts.basecontext import BaseContext
from pagebot.contexts.builders.canvasbuilder import CanvasBuilder
from pagebot.toolbox.units import upt, point2D

class CanvasContext(BaseContext):

    def __init__(self):
        super().__init__()
        self.b = CanvasBuilder()
        self.name = self.__class__.__name__

    def newPage(self, width, height):
        return self.b.newPage(width, height)

    def update(self):
        self.b.update()

    def newPath(self):
        self.b.newPath()

    def moveTo(self, pt):
        ppt = upt(point2D(pt))
        self.b.moveTo(ppt)

    def lineTo(self, pt):
        ppt = upt(point2D(pt))
        self.b.lineTo(ppt)

    def curveTo(self, bcp1, bcp2, pt):
        b1pt = upt(point2D(bcp1))
        b2pt = upt(point2D(bcp2))
        ppt = upt(point2D(pt))
        self.b.curveTo(b1pt, b2pt, ppt)

    def stroke(self, c):
        if c is None:
            self.b.stroke(None)
        else:
            r, g, b = c.rgb
            self.b.stroke(r, g, b, a=c.a)

        self.strokeWidth(0.5)

    def strokeWidth(self, w):
        wpt = upt(w)
        self.b.strokeWidth(wpt)

    def getFlattenedPath(self, path=None):
        pass

    def getFlattenedContours(self, path=None):
        pass

    def getGlyphPath(self, glyph, p=None, path=None):
        pass
