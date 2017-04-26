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
#     polygon.py
#
from pagebot.elements.element import Element

class Polygon(Element):
    
    def __init__(self, fs, points=None, **kwargs):
        Element.__init__(self, **kwargs)
        if points is None:
            points = []
        self.points = points

    def draw(self, origin):
        ox, oy = pointOrigin2D(self.point, origin)
        setFillColor(self.css('fill', NO_COLOR))
        setStrokeColor(self.css('stroke', NO_COLOR), self.css('strokeWidth'))
        newPath()
        for index, (px, py) in enumerate(self.points):
            if index == 0:
                moveTo((ox + px, y + py))
            else:
                lineTo((ox + px, y + py))
        drawPath()

