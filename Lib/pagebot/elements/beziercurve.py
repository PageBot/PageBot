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
    """Implements a (Base)BezierPath as an element.

    TODO: isOpenLine?
    TODO: what about contours (supported by BaseBezierPath)?
    TODO: what about components (currently not implemented by BaseBezierPath)?
    """

    def __init__(self, points=None, closed=True, **kwargs):
        if points is None:
            points = []
        # Force copy, so calling function can't change size cache.
        self.points = points[:]
        self.closed = closed
        Element.__init__(self, **kwargs)

    def translatePoint(self, p0, p):
        x0, y0, _ = p0
        x, y = p
        return x0 + x, y0 + y


    def build(self, view, origin=ORIGIN, **kwargs):
        pOrigin = self.getPosition(view, origin)
        self.buildFrame(view, pOrigin) # Draw optional frame or borders.
        view.drawElementFrame(self, pOrigin)
        self.context.newPath()
        self.context.fill(self.css('fill', noColor))
        self.context.stroke(self.css('stroke', noColor), self.css('strokeWidth'))
        p0 = self.translatePoint(pOrigin, self.points[0])
        self.context.moveTo(p0)

        for point in self.points[1:]:
            if len(point) == 2:
                p = self.translatePoint(pOrigin, point)
                self.context.lineTo(p)
            elif len(point) == 3:
                cp0 = self.translatePoint(pOrigin, point[0])
                cp1 = self.translatePoint(pOrigin, point[1])
                p = self.translatePoint(pOrigin, point[2])
                self.context.curveTo(cp0, cp1, p)

        if self.closed:
            self.context.closePath()
        self.context.drawPath()
        self.buildChildElements(view, pOrigin, **kwargs)
        self.restore(view, pOrigin)
        self.drawMeta(view, origin)
