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

from pagebot.contexts.base.basebezierpath import BaseBezierPath
from pagebot.contexts.base.basepoint import BasePoint

class FlatBezierPath(BaseBezierPath):
    """Bézier path that implements commands like Flat, but with the same API
    as DrawBot.BezierPath.

    >>> import flat
    >>> path = BezierPath(flat)
    >>> path.moveTo((0, 0))
    >>> path.lineTo((0, 100))
    >>> path.lineTo((100, 100))
    >>> path.lineTo((100, 0))
    >>> path.lineTo((0, 0))
    >>> path.closePath()
    >>> len(path.points)
    5
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

    def append(self, command):
        self.commands.append(command)

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

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
