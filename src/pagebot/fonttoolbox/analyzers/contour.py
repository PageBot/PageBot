# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     contour.py
#
class Contour(object):
    def __init__(self):
        self.points = []
        self._clockWise = True

    def __len__(self):
        return len(self.points)

    def __repr__(self):
        return 'Cnt(%d)' % len(self.points)

    def __getitem__(self, index):
        return self.points[index]

    def __setitem__(self, index, p):
        self.points[index] = p

    def _get_clockWise(self):
        return self._clockWise
    clockWise = property(_get_clockWise)
    
    def append(self, p):
        self.points.append(p)

