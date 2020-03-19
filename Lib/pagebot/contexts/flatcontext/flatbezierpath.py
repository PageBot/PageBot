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
from pagebot.contexts.basecontext.basepoint import BasePoint

class FlatBezierPath(BaseBezierPath):
    """Bézier path that implements commands like Flat, but with the same API
    as DrawBot.BezierPath.

    >>> import flat
    >>> path = FlatBezierPath(flat)
    >>> path.moveTo((0, 0))
    >>> path.lineTo((0, 100))
    >>> path.lineTo((100, 100))
    >>> path.lineTo((100, 0))
    >>> path.lineTo((0, 0))
    >>> path.closePath()
    >>> len(path.points)
    6
    """
    def __init__(self, b):
        self.b = b
        self.commands = []
        super().__init__()

    def __repr__(self):
        return '<FlatBezierPath>'

    def addToPath(self, p, onCurve=True):
        """Keeps track of Bézier points, needs to be in sync with Flat
        commands."""
        x, y = p
        point = BasePoint(x, y, onCurve=onCurve)
        self._path.append(point)

    #def append(self, command):
    #    self.commands.append(command)

    # Drawing.

    def moveTo(self, p):
        self.commands.append(self.b.moveto(p[0], p[1]))
        self.addToPath(p)

    def lineTo(self, p):
        self.commands.append(self.b.lineto(p[0], p[1]))
        self.addToPath(p)

    def quadTo(self, cp, p):
        """
        * cp: control point, off curve.
        * p: on curve point.
        """
        self.commands.append(self.b.quadto(cp[0], cp[1], p[0], p[1]))
        self.addToPath(cp, onCurve=False)
        self.addToPath(p)

    def curveTo(self, cp1, cp2, p):
        """
        * cp1: control point 1, off curve.
        * cp2: control point 2, off curve.
        * p: on curve point.
        """
        self.commands.append(self.b.curveto(cp1[0], cp1[1], cp2[0], cp2[1],
            p[0], p[1]))
        self.addToPath(cp1, onCurve=False)
        self.addToPath(cp2, onCurve=False)
        self.addToPath(p)

    def qCurveTo(self, *points):
        """Draws an entire string of quadratic curve segments. The last point
        specified is on-curve, all others are off-curve (control) points.
        """
        raise NotImplementedError

    def closePath(self):
        """Closes the path, add the first point to the end of the points
        list."""
        p0 = self._path[0]
        self._path.append(p0)
        self.commands.append(self.b.closepath)

    def appendPath(self, path):
        """Joins another path with this one.

        TODO: also parse each command and add its points.
        """
        # for command in path.commands:
        # ...
        self.commands += path.commands

    # Shapes.

    def rect(self, x, y, w, h):
        """Adds a rectangle at position `x`, `y` with a size of `w`, `h`."""
        x1 = x + w
        y1 = y + h
        p0 = (x, y)
        p1 = (x1, y)
        p2 = (x1, y1)
        p3 = (x, y1)
        self.moveTo(p0)
        self.lineTo(p1)
        self.lineTo(p2)
        self.lineTo(p3)
        self.closePath()

    def oval(self, x, y, w, h):
        """Adds an oval at position `x`, `y` with a size of `w`, `h`"""
        # Control point offsets.
        kappa = .5522848
        offsetX = (w / 2) * kappa
        offsetY = (h / 2) * kappa

        # Middle and other extreme points.
        x0 = x + (w / 2)
        y0 = y + (h / 2)
        x1 = x + w
        y1 = y + h

        self.moveTo((x0, y0))

        cp1 = (x, y0 - offsetY)
        cp2 = (x0 - offsetX, y)
        p = (x1, y0)
        self.curveTo(cp1, cp2, p)

        cp1 = (x0 + offsetX, y)
        cp2 = (x1, y0 - offsetY)
        p = (x1, y0)
        self.curveTo(cp1, cp2, p)

        cp1 = (x1, y0 + offsetY)
        cp2 = (x0 + offsetX, y1)
        p = (x0, y1)
        self.curveTo(cp1, cp2, p)

        cp1 = (x0 - offsetX, y1)
        cp2 = (x, y0 + offsetY)
        p = (x, y0)
        self.curveTo(cp1, cp2, p)

    def line(self, point1, point2):
        """Adds a line between two given points."""
        self.moveTo(point1)
        self.lineTo(point2)

    def polygon(self, *points, **kwargs):
        """Draws a polygon with `n` points. Optionally a `close` argument can
        be provided to open or close the path. By default a `polygon` is a
        closed path."""
        self.moveTo(points[0])

        for point in points[1:]:
            self.lineTo(point)

        # TODO: optional close

    def text(self, txt, offset=None, font=None, fontSize=10, align=None):
        raise NotImplementedError

    def textBox(self, txt, box, font=None, fontSize=10, align=None,
            hyphenation=None):
        raise NotImplementedError

    # Path operations.

    def getBezierPath(self):
        """Returns the BezierPath."""

    def setBezierPath(self, path):
        """Sets a BezierPath."""

    def pointInside(self, xy):
        """Checks if a point `x`, `y` is inside a path."""

    def bounds(self):
        """Returns the bounding box of the path."""

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

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
