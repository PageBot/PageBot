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
#     beziercontour.py
#


from pagebot.contexts.basecontext.basecontext import BaseContext

class BezierContour:
    """Wraps a Bézier contour.

    FIXME: is this really needed?
    """

    def __init__(self, context=None, bezierContour=None):
        assert isinstance(context, BaseContext)
        self.context = context
        self.bc = bezierContour

    def __repr__(self):
        return '<%s %d>' % (self.__class__.__name__, len(self.bc or []))

    def __len__(self):
        return len(self.points)

    def _get_points(self):
        if self.bc:
            return self.bc.points
        return []

    points = property(_get_points)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
