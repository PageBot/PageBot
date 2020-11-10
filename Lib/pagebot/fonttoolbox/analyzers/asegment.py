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
#     asegment.py

class ASegment:
    """
    >>> from pagebot.fonttoolbox.analyzers.apoint import APoint
    >>> p0 = APoint((101, 303), onCurve=True)
    >>> p1 = APoint((202, 404), onCurve=False)
    >>> p2 = APoint((303, 808), onCurve=False)
    >>> p3 = APoint((909, 808), onCurve=True)
    >>> points = [p0, p1, p2, p3]
    >>> s = ASegment(points)
    >>> len(s)
    4
    >>> p4 = APoint((111, 313), onCurve=False)
    >>> s.append(p4)
    >>> len(s)
    5
    >>> s.points[-1].onCurve
    False
    """
    def __init__(self, points=None):
        if points is None:
            points = []
        self.points = points

    def __len__(self):
        return len(self.points)

    def __repr__(self):
        return 'Sg(%s)' % self.points

    def append(self, p):
        self.points.append(p)
