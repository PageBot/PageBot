#!/usr/bin/env python
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
#     nonebezierpath.py
#

class NoneBezierPath:
    """Make NoneBezierPath with the same API for NoneDrawBotBuilder drawing
    texting."""

    def moveTo(self, p):
        pass

    lineTo = moveTo

    def quadTo(self, pcp, p):
        pass

    def curveTo(self, bcp1, bcp2, p):
        pass

    def closePath(self):
        pass

    def appendPath(self, path):
        pass

class CommandBezierPath:
    """Make BezierPath with the same API for DrawBotBuilder drawing.
    """

    def __init__(self, b):
        self.b = b
        self.commands = []

    def append(self, command):
        self.commands.append(command)

    def moveTo(self, p):
        pass

    def lineTo(self, p):
        pass

    def quadTo(self, bcp, p):
        pass

    def curveTo(self, bcp1, bcp2, p):
        pass

    def closePath(self):
        pass

    def appendPath(self, path):
        self.commands += path.commands

