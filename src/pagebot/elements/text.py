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
#     text.py
#
"""
import os
import copy

from drawBot import FormattedString, textSize, stroke, strokeWidth, fill, font, fontSize, text, \
    newPath, drawPath, moveTo, lineTo, line, rect, oval, save, scale, image, textOverflow, \
    textBox, hyphenation, restore, imageSize, shadow, BezierPath, clipPath, drawPath
from pagebot import getFormattedString, setFillColor, setStrokeColor, getMarker
"""
from drawBot import textSize, text
from pagebot import getFormattedString
from pagebot.elements.element import Element
from pagebot.toolbox.transformer import pointOrigin2D
from pagebot.style import RIGHT_ALIGN, CENTER, TOP_ALIGN

class Text(Element):

    # Initialize the default behavior tags as different from Element.
    isText = True  # This element is capable of handling text.

    def __init__(self, fs, point=None, parent=None, style=None, eId=None, **kwargs):
        Element.__init__(self, point=point, parent=parent, style=style, eId=eId, **kwargs)
        self.fs = getFormattedString(fs, self)

    def append(self, fs):
        u"""Append s to the running formatted string of the self. Note that the string
        is already assumed to be styled or can be added as plain string."""
        self.fs += fs

    def getTextSize(self, fs=None, w=None):
        """Figure out what the width/height of the text self.fs is, with or given width or
        the styled width of this text box. If fs is defined as external attribute, then the
        size of the string is answers, as if it was already inside the text box."""
        if fs is None:
            fs = self.fs
        return textSize(self.fs)

    def _applyOrigin(self, p):
        u"""If self.css('originTop') is False, then the y-value is interpreted as mathemtcs, 
        starting at the bottom of the parent element, moving up.
        If the flag is True, then move from top down, where the text still draws upward."""
        px, py = p
        if self.css('originTop') and self.parent:
            py = self.parent.h - py
        return px, py

    def _applyAlignment(self, p):
        w, h = textSize(self.fs)   
        px, py = p
        if self.css('align') == CENTER:
            px -= w/2/self.scaleX
        elif self.css('align') == RIGHT_ALIGN:
            px -= w/self.scaleX
        if self.css('originTop'):
            if self.css('vAlign') == CENTER:
                py += h/2/self.scaleY
            elif self.css('vAlign') == TOP_ALIGN:
                py += h/self.scaleY
        else:
            if self.css('vAlign') == CENTER:
                py -= h/2/self.scaleY
            elif self.css('vAlign') == TOP_ALIGN:
                py -= h/self.scaleY
        return px, py

    def draw(self, origin):
        u"""Draw the formatted text. Since this is not a text column, but just a
        typeset text line, background and stroke of a text column needs to be drawn elsewere."""
        p = pointOrigin2D(self.point, origin)
        p = self._applyOrigin(p)    
        p = self._applyScale(p)    
        p = self._applyAlignment(p)
        self._setShadow()

        text(self.fs, p)

        self._resetShadow()
        self._restoreScale()




