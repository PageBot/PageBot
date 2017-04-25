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
#     plygon.py
#
"""
import os
import copy

from drawBot import FormattedString, textSize, stroke, strokeWidth, fill, font, fontSize, text, \
    newPath, drawPath, moveTo, lineTo, line, rect, oval, save, scale, image, textOverflow, \
    textBox, hyphenation, restore, imageSize, shadow, BezierPath, clipPath, drawPath
from pagebot import getFormattedString, setFillColor, setStrokeColor, getMarker
from pagebot.style import LEFT, TOP, RIGHT, CENTER, NO_COLOR, makeStyle
"""
from pagebot.elements.element import Element

class Polygon(Element):
    def __init__(self, points, style=None, name=None, eId=None, **kwargs):
        self.name = name
        self.points = points
        self.eId = eId
        self.style = makeStyle(style, **kwargs)

    def draw(self, origin):
        ox, oy = pointOrigin2D(self.point, origin)
        setFillColor(self.style.get('fill'), NO_COLOR)
        setStrokeColor(self.style.get('stroke', NO_COLOR), self.style.get('strokeWidth'))
        newPath()
        for index, (px, py) in enumerate(self.points):
            if index == 0:
                moveTo((ox + px, y + py))
            else:
                lineTo((ox + px, y + py))
        drawPath()

