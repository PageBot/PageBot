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

from pagebot.elements.element import Element
from pagebot.toolbox.units import upt, point2D# , degrees

class BezierCurve(Element):
    """Implements a BaseBezierPath as an element.

    TODO: isOpenLine?
    TODO: what about contours (supported by BaseBezierPath)?
    TODO: what about components (currently not implemented by BaseBezierPath)?
    """

    def __init__(self, **kwargs):
        Element.__init__(self, **kwargs)
        self.bezierPath = None
        self.isOpenPath = False

    def beginPath(self, identifier=None):
        msg = '%s.beginPath: Path is already open.' % self.__class__.__name__
        assert not self.isOpenPath, msg
        self.isOpenPath = True

        # Creates a new BaseBezierPath.
        self.bezierPath = self.context.newPath()
        self.bezierPath.beginPath(identifier)

    def closePath(self):
        msg = 'endPath: Pen path is not open. Call self.beginPath() first.'
        msg = '%s.%s' % self.__class__.__name__, msg
        assert self.isOpenPath, msg
        self.isOpenPath = False
        self.bezierPath.closePath()

    def moveTo(self, p):
        ptp = upt(point2D(p))
        self.bezierPath.moveTo(ptp)

    def lineTo(self, p):
        ptp = upt(point2D(p))
        self.bezierPath.lineTo(ptp)
