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
#     commandbezierpath.py
#

class CommandBezierPath:
    """Bézier path that stores commands to be executed later."""

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

