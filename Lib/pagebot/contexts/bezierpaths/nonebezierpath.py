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
#     nonebezierpath.py
#

class NoneBezierPath:
    """Bézier path that does nothing."""

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
