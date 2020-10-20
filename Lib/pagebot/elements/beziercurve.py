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
#     beziercurve.py
#

from pagebot.constants import ORIGIN
from pagebot.elements.element import Element
from pagebot.toolbox.color import noColor

class BezierCurve(Element):
    """Implements a BaseBezierPath as an element.

    TODO: isOpenLine?
    TODO: what about contours (supported by BaseBezierPath)?
    TODO: what about components (currently not implemented by BaseBezierPath)?
    """

    def __init__(self, points=None, closed=True, **kwargs):
        if points is None:
            points = []
        # Force copy, so caller can't change size cache.
        self.points = points[:]
        self.closed = closed
        Element.__init__(self, **kwargs)

    def build(self, view, origin=ORIGIN, **kwargs):
        p = self.getPosition(view, origin)
        self.buildFrame(view, p) # Draw optional frame or borders.
        view.drawElementFrame(self, p)
        self.context.newPath()
        self.context.fill(self.css('fill', noColor))
        self.context.stroke(self.css('stroke', noColor), self.css('strokeWidth'))

        '''
        points = []

        for point in self.points:
            if len(point) == 1:
                px = point[0] + p[0]
                py = point[1] + p[1]
            else:
        '''
        p0 = self.points[0]
        self.context.moveTo(p0)

        for point in self.points[1:]:
            if len(point) == 2:
                self.context.lineTo(point)
            elif len(point) == 3:
                self.context.curveTo(point[0], point[1], point[2])

        self.context.closePath()
        self.context.drawPath()
        self.buildChildElements(view, p, **kwargs)
        self.restore(view, p)
        self.drawMeta(view, origin)
