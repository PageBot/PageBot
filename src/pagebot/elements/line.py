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
#     line.py
#
"""
import os
import copy

from drawBot import FormattedString, textSize, stroke, strokeWidth, fill, font, fontSize, text, \
    newPath, drawPath, moveTo, lineTo, line, rect, oval, save, scale, image, textOverflow, \
    textBox, hyphenation, restore, imageSize, shadow, BezierPath, clipPath, drawPath
from pagebot import getFormattedString, setFillColor, setStrokeColor, getMarker
from pagebot.style import LEFT_ALIGN, TOP_ALIGN, RIGHT_ALIGN, CENTER, NO_COLOR, makeStyle
"""
from pagebot.elements.element import Element

class Line(Element):
    def __init__(self, style=None, eId=None, **kwargs):
        Element.__init__(self, point, parent, eId, style, **kwargs)
        assert self.w is not None and self.h is not None

    def draw(self, origin):
        ox, oy = pointOrigin2D(self.point, origin)
        setStrokeColor(self.style.get('stroke', NO_COLOR), self.style.get('strokeWidth'))
        newPath()
        moveTo((ox, oy))
        lineTo((ox + self.w, oy + self.h))
        drawPath()
