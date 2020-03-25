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
#     abstractbezierpath.py
#

from fontTools.pens.basePen import BasePen

_FALLBACKFONT = "LucidaGrande"

class AbstractBezierPath(BasePen):
    """Abstract class with same interface as DrawBot Bézier path:

    a Bézier path object, if you want to draw the same over and over again.
    """

    # Pen support.

    def moveTo(self, point):
        raise NotImplementedError

    def lineTo(self, point):
        raise NotImplementedError

    def curveTo(self, *points):
        raise NotImplementedError

    def qCurveTo(self, *points):
        raise NotImplementedError

    def closePath(self):
        raise NotImplementedError

    def beginPath(self, identifier=None):
        raise NotImplementedError

    def addPoint(self, point, segmentType=None, smooth=False, name=None,
            identifier=None, **kwargs):
        raise NotImplementedError

    def endPath(self):
        raise NotImplementedError

    def addComponent(self, glyphName, transformation):
        raise NotImplementedError

    def drawToPen(self, pen):
        raise NotImplementedError

    def drawToPointPen(self, pointPen):
        raise NotImplementedError

    def arc(self, center, radius, startAngle, endAngle, clockwise):
        raise NotImplementedError

    def arcTo(self, point1, point2, radius):
        raise NotImplementedError

    def rect(self, x, y, w, h):
        raise NotImplementedError

    def oval(self, x, y, w, h):
        raise NotImplementedError

    def line(self, point1, point2):
        raise NotImplementedError

    def polygon(self, *points, **kwargs):
        raise NotImplementedError

    def text(self, txt, offset=None, font=_FALLBACKFONT, fontSize=10,
            align=None):
        raise NotImplementedError

    def textBox(self, txt, box, font=_FALLBACKFONT, fontSize=10, align=None,
            hyphenation=None):
        raise NotImplementedError

    def traceImage(self, path, threshold=.2, blur=None, invert=False, turd=2,
            tolerance=0.2, offset=None):
        raise NotImplementedError

    # These are specific for a DrawBot path, dropping from interface.

    #def getNSBezierPath(self):

    #def setNSBezierPath(self, path):

    def pointInside(self, xy):
        raise NotImplementedError

    def bounds(self):
        raise NotImplementedError

    def controlPointBounds(self):
        raise NotImplementedError

    def optimizePath(self):
        raise NotImplementedError

    def copy(self):
        raise NotImplementedError

    def reverse(self):
        raise NotImplementedError

    def appendPath(self, otherPath):
        raise NotImplementedError

    # Transformations.

    def translate(self, x=0, y=0):
        raise NotImplementedError

    def rotate(self, angle, center=(0, 0)):
        raise NotImplementedError

    def scale(self, x=1, y=None, center=(0, 0)):
        raise NotImplementedError

    def skew(self, angle1, angle2=0, center=(0, 0)):
        raise NotImplementedError

    def transform(self, transformMatrix, center=(0, 0)):
        raise NotImplementedError

    # Boolean operations.

    def union(self, other):
        raise NotImplementedError

    def removeOverlap(self):
        raise NotImplementedError

    def difference(self, other):
        raise NotImplementedError

    def intersection(self, other):
        raise NotImplementedError

    def xor(self, other):
        raise NotImplementedError

    def intersectionPoints(self, other=None):
        raise NotImplementedError

    def expandStroke(self, width, lineCap="round", lineJoin="round",
            miterLimit=10):
        raise NotImplementedError
