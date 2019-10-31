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
#     babelpoint.py
#

class BasePoint:

    def __init__(self, x, y, segmentType=None, smooth=False, name=None,
            identifier=None, start=False, onCurve=True):
        """Point on a Bézier curve."""
        self.x = x
        self.y = y
        self.segmentType = segmentType
        self.smooth = smooth
        self.name = name
        self.identifier = identifier
        self.start = start
        self.onCurve = onCurve

    def __repr__(self):
        return '(x=%s, y=%s, onCurve=%s)' % (self.x, self.y, self.onCurve)

