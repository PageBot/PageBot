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
#     bezier.py
#

from pagebot.elements.element import Element

class BezierCurve(Element):

    def __init__(self, **kwargs):
        Element.__init__(self, **kwargs)
        self.bezierPath = None

    def beginPath(self, identifier=None):
        self.bezierPath = self.context.newPath()
        self.bezierPath.beginPath(identifier)

    def closePath(self):
        self.bezierPath.closePath()
