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
#     flatbezierpath.py
#

from pagebot.contexts.basecontext.basebezierpath import BaseBezierPath
from pagebot.constants import MOVETO, LINETO, CURVETO, CLOSEPATH

class FlatBezierPath(BaseBezierPath):
    """Bézier path that implements commands like Flat, but with the same API
    as DrawBot.BezierPath, based on the FontTools pen implementation.

    >>> import flat
    >>> path = FlatBezierPath(flat)
    >>> path
    <FlatBezierPath>
    >>> path.moveTo((0, 0))
    >>> path
    <FlatBezierPath>
    >>> path.lineTo((0, 100))
    >>> path.lineTo((100, 100))
    >>> path.lineTo((100, 0))
    >>> path.lineTo((0, 0))
    >>> path.curveTo((50, 50), (100, 100), (120, 80))
    >>> path.closePath()
    >>> contour = path.contours[-1]
    >>> len(contour)
    6
    >>> contour
    [[(0.0, 0.0)], [(0.0, 100.0)], [(100.0, 100.0)], [(100.0, 0.0)], [(0.0, 0.0)], [(50.0, 50.0), (100.0, 100.0), (120.0, 80.0)]]
    >>> contour.points
    [(0.0, 0.0), (0.0, 100.0), (100.0, 100.0), (100.0, 0.0), (0.0, 0.0), (50.0, 50.0), (100.0, 100.0), (120.0, 80.0)]
    """

    def __init__(self, b, path=None, glyphSet=None):
        self.b = b
        self.commands = []
        super().__init__(path=path, glyphSet=glyphSet)

    def __repr__(self):
        return '<FlatBezierPath>'

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

    def closePath(self):
        """Closes the path, add the first point to the end of the points
        list."""
        contour = self.contours[-1]
        p0 = contour[0][0]
        point = self.getPoint(p0)
        self.addSegment(CLOSEPATH, [])
        self.addSegment(MOVETO, [point])
        self.commands.append(self.b.closepath)

    def appendPath(self, path):
        """Joins another path with this one.

        TODO: also parse each command and add its points.
        """
        # for command in path.commands:
        # ...
        self.commands += path.commands


    # To be implemented.

    def getBezierPath(self):
        """Returns the BezierPath."""

    def setBezierPath(self, path):
        """Sets a BezierPath."""

    def pointInside(self, xy):
        """Checks if a point `x`, `y` is inside a path."""

    def controlPointBounds(self):
        """Returns the bounding box of the path including the offcurve
        points."""

    def optimizePath(self):
        pass

    def copy(self):
        """Copy the Bézier path."""
        return None

    def reverse(self):
        """Reverse the path direction."""

    def appendPath(self, otherPath):
        """Append a path."""
        return None

    def addComponent(self, glyphName, transformation):
        pass

    def arc(self, center, radius, startAngle, endAngle, clockwise):
        pass

    def arcTo(self, point1, point2, radius):
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


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
