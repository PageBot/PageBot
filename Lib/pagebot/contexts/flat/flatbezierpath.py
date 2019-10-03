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

class BezierPath:
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

    """
    def __init__(self, b):
        self.b = b
        self.commands = []

    def append(self, command):
        self.commands.append(command)

    def moveTo(self, p):
        self.commands.append(self.b.moveto(p[0], p[1]))

    def lineTo(self, p):
        self.commands.append(self.b.lineto(p[0], p[1]))

    def quadTo(self, cp, p):
        """
        * cp: control point, off curve.
        * p: on curve point.
        """
        self.commands.append(self.b.quadto(cp[0], cp[1], p[0], p[1]))

    def curveTo(self, cp1, cp2, p):
        """
        * cp1: control point 1, off curve.
        * cp2: control point 2, off curve.
        * p: on curve point.
        """
        self.commands.append(self.b.curveto(cp1[0], cp1[1], cp2[0], cp2[1],
            p[0], p[1]))

    def closePath(self):
        self.commands.append(self.b.closepath)

    def appendPath(self, path):
        self.commands += path.commands

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
