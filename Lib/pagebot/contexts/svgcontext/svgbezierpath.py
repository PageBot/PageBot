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
#     svgbezierpath.py
#

'''
from fontTools.pens.pointPen import PointToSegmentPen
from fontTools.pens.boundsPen import BoundsPen
from pagebot.errors import PageBotError
'''
from pagebot.contexts.basecontext.basebezierpath import BaseBezierPath
from pagebot.constants import MOVETO, LINETO, CURVETO


class SvgBezierPath(BaseBezierPath):
    """Bézier path that implements commands like SVG, but with the same API
    as DrawBot.BezierPath, based on the FontTools pen implementation.
    """

    def __init__(self, b, path=None, glyphSet=None):
        self.b = b
        self.commands = []
        super().__init__(path=path, glyphSet=glyphSet)

    def __repr__(self):
        return '<SvgBezierPath>'

    # Curve.

    def _moveTo(self, p):
        self.commands.append(self.b.moveto(p[0], p[1]))
        point = self.getPoint(p)
        self.addSegment(MOVETO, [point])

    def _lineTo(self, p):
        self.commands.append(self.b.lineto(p[0], p[1]))
        point = self.getPoint(p)
        self.addSegment(LINETO, [point])

    def _curveToOne(self, cp1, cp2, p):
        """
        * cp1: control point 1, off curve.
        * cp2: control point 2, off curve.
        * p: on curve point.
        """
        self.commands.append(self.b.curveto(cp1[0], cp1[1], cp2[0], cp2[1],
            p[0], p[1]))
        cpoint1 = self.getPoint(cp1, onCurve=False)
        cpoint2 = self.getPoint(cp2, onCurve=False)
        point = self.getPoint(p)
        points = [cpoint1, cpoint2, point]
        self.addSegment(CURVETO, points)

    # To be implemented.

    def addComponent(self, glyphName, transformation):
        pass

    def arc(self, center, radius, startAngle, endAngle, clockwise):
        pass

    def arcTo(self, point1, point2, radius):
        pass

    def copy(self):
        """Copy the Bézier path."""
        return None

    def reverse(self):
        """Reverse the path direction."""

    def appendPath(self, path):
        pass

    def pointInside(self, xy):
        """Checks if a point `x`, `y` is inside a path."""

    def controlPointBounds(self):
        """Returns the bounding box of the path including the offcurve
        points."""

    def optimizePath(self):
        pass

    def text(self, txt, offset=None, font=None, fontSize=10, align=None):
        """Draws a `txt` with a `font` and `fontSize` at an `offset` in the
        Bézier path. If a font path is given the font will be installed and
        used directly.

        - Optionally an alignment can be set.
        - Possible `align` values are: `"left"`, `"center"` and `"right"`.
        - The default alignment is `left`.
        - Optionally `txt` can be a `FormattedString`.
        """

    def textBox(self, txt, box, font=None, fontSize=10, align=None,
            hyphenation=None):
        """Draws a `txt` with a `font` and `fontSize` in a `box` in the Bézier
        path. If a font path is given the font will be installed and used
        directly.

        - Optionally an alignment can be set.
        - Possible `align` values are: `"left"`, `"center"` and `"right"`.
        - The default alignment is `left`.
        - Optionally `hyphenation` can be provided.
        - Optionally `txt` can be a `FormattedString`.
        - Optionally `box` can be a `BezierPath`.
        """
