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
#     basebezierpoint.py
#

class BaseBezierPoint:

    def __init__(self, x, y, segmentType=None, smooth=False, name=None,
            identifier=None, start=False, onCurve=True):
        """Point on a Bézier curve.

        See also

        http://www.drawbot.com/content/shapes/bezierPath.html#drawBot.context.baseContext.BezierPath.addPoint
        """
        self.x = float(x)
        self.y = float(y)
        self.segmentType = segmentType
        self.smooth = smooth
        self.name = name
        self.identifier = identifier
        self.start = start
        self.onCurve = onCurve

    def __repr__(self):
        # TODO: put back later.
        #return '(x=%s, y=%s, onCurve=%s)' % (self.x, self.y, self.onCurve)
        return '(%s, %s)' % (self.x, self.y)

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            # TODO: more expicit message, add to logger.
            raise TypeError
