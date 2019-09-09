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
    """BezierPath with the same API as DrawBot.BezierPath.

    >>> path = BezierPath(flatBuilder)
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
        self.commands.append(self.b.moveto(p[0].pt, p[1].pt))

    def lineTo(self, p):
        self.commands.append(self.b.lineto(p[0].pt, p[1].pt))

    def quadTo(self, bcp, p):
        self.commands.append(self.b.quadto(bcp[0].pt, bcp[1].pt, p[0].pt,
            p[1].pt))

    def curveTo(self, bcp1, bcp2, p):
        self.commands.append(self.b.curveto(bcp1[0].pt, bcp1[1].pt, bcp2[0].pt,
            bcp2[1].pt, p[0].pt, p[1].pt))

    def closePath(self):
    	self.commands.append(self.b.closepath)

    def appendPath(self, path):
        self.commands += path.commands
