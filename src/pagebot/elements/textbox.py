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
#     textbox.py
#
from drawBot import textOverflow, hyphenation, textBox, rect, textSize, FormattedString

from pagebot.style import LEFT_ALIGN, RIGHT_ALIGN, CENTER, NO_COLOR, makeStyle
from pagebot.elements.element import Element
from pagebot.toolbox.transformer import pointOrigin2D
from pagebot import getFormattedString, setStrokeColor, setFillColor

class TextBox(Element):

    # Initialize the default behavior tags as different from Element.
    isText = True  # This element is capable of handling text.

    def __init__(self, fs, point=None, parent=None, style=None, eId=None, **kwargs):
        Element.__init__(self, point=point, parent=parent, style=style, eId=eId, **kwargs)
        # Make sure that this is a formatted string. Otherwise create it with the current style.
        # Note that in case there is potential clash in the double usage of fill and stroke.
        if isinstance(fs, str):
            fs = getFormattedString(fs, parent, self.style)
        self.fs = fs
        # Initialize the default Element behavior tags, in case this is a flow.
        self.isTextBox = True
        self.isFlow = self.eId is not None and self.nextBox is not None and self.nextPage is not None

    def _get_h(self):
        u"""Answer the height of the textBox. If self.style['vacuumH'] is set, then answer the 
        vertical space that the text needs. This overwrites the setting of self._h."""
        if self.style.get('vacuumH'):
            return self.getTextSize()[1]
        if self._h is None:
            return self.style.get('h') # Can be None in case the height is undefined. 
        return self._h
    def _set_h(self, h):
        self._h = h # Overwrite style from here, unless self.style['vacuum'] is True
    h = property(_get_h, _set_h)

    def _get_nextBox(self):
        return self.style.get('nextBox')
    nextBox = property(_get_nextBox)

    def _get_nextPage(self):
        return self.style.get('nextPage')
    nextPage = property(_get_nextPage)

    def __len__(self):
        return len(self.fs)

    def _get_next(self):
        if self.isFlow:
            return self.nextBox, self.nextPage
        return None
    next = property(_get_next)

    def setText(self, s):
        u"""Set the formatted string to s, using self.style."""
        self.fs = getFormattedString(s, self.style)

    def append(self, fs):
        u"""Append s to the running formatted string of the self. Note that the string
        is already assumed to be styled or can be added as plain string."""
        assert fs is not None
        if self.fs is None:
            self.fs = fs
        else:
            self.fs += fs
        return self.getOverflow(self.w, self.h)

    def appendMarker(self, markerId, arg=None):
        self.append(getMarker(markerId, arg=arg))

    def getTextSize(self, fs=None, w=None):
        """Figure out what the width/height of the text self.fs is, with or given width or
        the styled width of this text box. If fs is defined as external attribute, then the
        size of the string is answers, as if it was already inside the text box."""
        if fs is None:
            fs = self.fs
        return textSize(self.fs, width=w or self.w)

    def getOverflow(self, w=None, h=None):
        """Figure out what the overflow of the text is, with the given (w,h) or styled
        (self.w, self.h) of this text box. If self.style['vacuumH'] is True, then by
        definintion overflow will allways be empty."""
        if self.css('vacuumH'): # In case vacuumH, box will aways fit the content.
            return ''
        return textOverflow(self.fs, (0, 0, w or self.w, h or self.h), LEFT_ALIGN)

    def getBaselinePositions(self, y=0, w=None, h=None):
        u"""Answer the list vertical baseline positions, relative to y (default is 0)
        for the given width and height. If omitted use (self.w, self.h)"""
        baselines = []
        for _, baselineY in textBoxBaseLines(self.fs, (0, y, w or self.w, h or self.h)):
            baselines.append(baselineY)
        return baselines

    def draw(self, origin):
        u"""Draw the text on position (x, y). Draw background rectangle and/or frame if
        fill and/or stroke are defined."""
        ox, oy = pointOrigin2D(self.point, origin)
        if self.style.get('align') == RIGHT_ALIGN:
            ox -= self.w
        elif self.style.get('align') == CENTER:
            ox -= self.w/2
        sFill = self.style.get('fill', NO_COLOR)
        if sFill != NO_COLOR:
            setStrokeColor(None)
            setFillColor(sFill)
            rect(ox, oy, self.w, self.h)
        hyphenation(True)
        textBox(self.fs, (ox, oy, self.w, self.h))
        sStroke = self.style.get('stroke', NO_COLOR)
        sStrokeWidth = self.style.get('strokeWidth')
        if sStroke != NO_COLOR and sStrokeWidth is not None:
            setStrokeColor(sStroke, sStrokeWidth)
            setFillColor(None)
            rect(ox, oy, self.w, self.h)
        else: # If debugging,then draw the rectangle. Only self.css('showElementBox') is True
            self._drawElementBox(origin)


