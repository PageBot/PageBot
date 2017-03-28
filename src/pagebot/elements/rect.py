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
#     rect.py
#
"""
import os
import copy

from drawBot import FormattedString, textSize, stroke, strokeWidth, fill, font, fontSize, text, \
    newPath, drawPath, moveTo, lineTo, line, rect, oval, save, scale, image, textOverflow, \
    textBox, hyphenation, restore, imageSize, shadow, BezierPath, clipPath, drawPath
from pagebot.style import LEFT_ALIGN, TOP_ALIGN, RIGHT_ALIGN, CENTER, NO_COLOR, makeStyle
"""
from drawBot import rect
from pagebot.style import NO_COLOR
from pagebot.elements.element import Element
from pagebot.toolbox.transformer import pointOrigin2D

from pagebot import setFillColor, setStrokeColor

class Rect(Element):
    def __init__(self, point=None, parent=None, style=None, eId=None, **kwargs):
        Element.__init__(self, point=point, parent=parent, style=style, eId=eId, **kwargs)
        assert self.w is not None and self.h is not None

    def draw(self, origin):
        px, py, pw, ph = self.getPaddedBox()
        ox, oy = pointOrigin2D((px, py), origin)
        setFillColor(self.style.get('fill', NO_COLOR))
        setStrokeColor(self.style.get('stroke', NO_COLOR), self.style.get('strokeWidth'))
        rect(px, py, pw, ph)

