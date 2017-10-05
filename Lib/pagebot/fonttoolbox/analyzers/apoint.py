# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#     
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     point.py
#
from pagebot.toolbox.transformer import point3D

class APoint(object):
    u"""Analyzer Point, used if addition information (like its type) needs to be stored.
    Otherwise just use the point2D() and point3D() which are simple tuples.

    >>> p = APoint(101, 303, True)
    >>> p.onCurve is False
    False
    >>> print p
    Pt(101,303,On)
    """

    def __init__(self, xy, onCurve=True):
        self.p = point3D(xy)
        self.onCurve = bool(onCurve)

    def __getitem__(self, index):
        return self.p[index]
    def __setitem__(self, index, value):
        self.p = list(p)
        self.p[index] = value

    def __getitem__(self, i):
        u"""Allow APoint to be indexed like a point2D tuple."""
        return self.p[i]
    def __setitem__(self, i, v):
        self.p[i] = v
    
    def __sub__(self, p):
        return self.p[0] - p[0], self.p[1] - p[1]

    def __add__(self, p):
        return self.p[0] + p[0], self.p[1] + p[1]

    def __mul__(self, v):
        return self.p[0] * v, self.p[1] * v

    def __div__(self, v):
        return self.p[0] / v, self.p[1] / v
            
    def _get_x(self):
        return self.p[0]
    def _set_x(self, x):
        self.p[0] = x
    x = property(_get_x, _set_x)

    def _get_y(self):
        return self.p[1]
    def _set_y(self, y):
        self.p[1] = y
    y = property(_get_y, _set_y)

    def _get_z(self):
        return self.p[2]
    def _set_z(self, z):
        self.p[2] = z
    z = property(_get_z, _set_z)

    def __repr__(self):
        return 'Pt(%s,%s,%s)' % (self.x, self.y,{True:'On', False:'Off'}[self.onCurve])

