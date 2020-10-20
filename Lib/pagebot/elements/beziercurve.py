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
from pagebot.toolbox.units import upt, point2D# , degrees
from pagebot.toolbox.color import noColor

class BezierCurve(Element):
    """Implements a BaseBezierPath as an element.

    TODO: isOpenLine?
    TODO: what about contours (supported by BaseBezierPath)?
    TODO: what about components (currently not implemented by BaseBezierPath)?
    """

    def __init__(self, **kwargs):
        Element.__init__(self, **kwargs)

    def build(self, view, origin=ORIGIN, **kwargs):
        p = self.getPosition(view, origin)
        self.buildFrame(view, p) # Draw optional frame or borders.
        view.drawElementFrame(self, p)
        self.context.fill(self.css('fill', noColor))
        self.context.stroke(self.css('stroke', noColor), self.css('strokeWidth'))
        self.context.drawPath()
        self.buildChildElements(view, p, **kwargs)
        self.restore(view, p)
        self.drawMeta(view, origin)

    def newPath(self, identifier=None):
        # Creates a new BaseBezierPath.
        self.context.newPath()

    def closePath(self):
        self.context.closePath()

    def moveTo(self, p):
        self.context.moveTo(p)

    def lineTo(self, p):
        self.context.lineTo(p)
