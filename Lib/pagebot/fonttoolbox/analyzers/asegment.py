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
#
class ASegment:
    """
    >>> p0 = Point(101, 303, True)
    >>> p1 = Point(202, 404, False)
    >>> p2 = Point(303, 808, False)
    >>> p3 = Point(909, 808, True)
    >>> points = [p0, p1, p2, p3]
    >>> s = Segment(points)
    >>> len(s)
    4
    >>> p4 = Point(111, 313, False)
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

