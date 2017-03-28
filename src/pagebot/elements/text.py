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
from pagebot.style import LEFT_ALIGN, TOP_ALIGN, RIGHT_ALIGN, CENTER, NO_COLOR, makeStyle
"""
from pagebot.elements.element import Element

class Text(Element):

    # Initialize the default behavior tags as different from Element.
    isText = True  # This element is capable of handling text.

    def __init__(self, fs, point=None, parent=None, eId=None, style=None, **kwargs):
        Element.__init__(self, point, parent, eId, style, **kwargs)
        #self.fs = fs # Caller must make sure that this is a rightly formatted string.
        # @@@ TODO: Style working?
        self.fs = getFormattedString(fs, self.style)

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

    def draw(self, origin):
        u"""Draw the formatted text. Since this is not a text column, but just a
        typeset text line, background and stroke of a text column needs to be drawn elsewere."""
        self._setShadow()
        w, h = textSize(self.fs)   
        if self.style.get('align') == RIGHT_ALIGN:
            x -= w
        elif self.style.get('align') == CENTER:
            x -= w/2
        text(self.fs, (x, y))
        self._resetShadow()

