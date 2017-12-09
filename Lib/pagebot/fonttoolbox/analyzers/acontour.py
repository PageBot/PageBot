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
#     acontour.py
#
class AContour(object):
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

