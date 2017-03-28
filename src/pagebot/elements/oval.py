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
#     oval.py
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

class Oval(Element):
    def __init__(self, point=None, parent=None, eId=None, style=None, **kwargs):
        Element.__init__(self, point, parent, eId, style, **kwargs)
        assert self.w is not None and self.h is not None
        # Initialize the default Element behavior tags.
        self.isContainer = False
        self.isText = False
        self.isFlow = False

    def draw(self, origin):
        ox, oy = pointOrigin2D(self.point, origin)
        setFillColor(self.style.get('fill', NO_COLOR))
        setStrokeColor(self.style.get('stroke', NO_COLOR), self.style.get('strokeWidth'))
        if self.style.get('align') == 'right':
            w, _ = self.fs.getSize()
            ox -= w
        elif self.style.get('align') == 'center':
            w, _ = self.fs.getSize()
            ox -= w/2
        oval(ox, oy, self.w, self.h)

