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
#     flatbuilder.py
#
from pagebot.contexts.builders.nonebuilder import NoneFlatBuilder

try:
    # ID to make builder hook name. Views will try to call e.build_flat().
    import flat
    flatBuilder = flat
    flatBuilder.PB_ID = 'flat'
except ImportError:
    flatBuilder = NoneFlatBuilder()

class BezierPath:
    """Make BezierPath with the same API as DrawBot.BezierPath.

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
        self.commands.append(self.b.moveto(p[0], p[1]))

    def lineTo(self, p):
        self.commands.append(self.b.lineto(p[0], p[1]))

    def quadTo(self, bcp, p):
        self.commands.append(self.b.quadto(bcp[0], bcp[1], p[0], p[1]))

    def curveTo(self, bcp1, bcp2, p):
        self.commands.append(self.b.curveto(bcp1[0], bcp1[1], bcp2[0], bcp2[1], p[0], p[1]))

    def closePath(self):
    	pass
    	# TODO Seems to be a problem in direct closing, not storing as command?
    	#self.commands.append(self.b.closepath

    def appendPath(self, path):
        self.commands += path.commands
