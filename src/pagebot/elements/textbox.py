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

from pagebot.style import LEFT, RIGHT, CENTER, NO_COLOR, makeStyle
from pagebot.elements.element import Element
from pagebot.toolbox.transformer import pointOffset
from pagebot import getFormattedString, setStrokeColor, setFillColor

class TextBox(Element):

    # Initialize the default behavior tags as different from Element.
    isText = True  # This element is capable of handling text.
    isTextBox = True

    def __init__(self, fs, **kwargs):
        Element.__init__(self, **kwargs)
        # Make sure that this is a formatted string. Otherwise create it with the current style.
        # Note that in case there is potential clash in the double usage of fill and stroke.
        if isinstance(fs, str):
            fs = getFormattedString(fs, self)
        self.fs = fs

    def _get_h(self):
        u"""Answer the height of the textBox. If self.style['vacuumH'] is set, then answer the 
        vertical space that the text needs. This overwrites the setting of self._h."""
        if self.style.get('vacuumH'):
            return self.getTextSize()[1]
        return self.css('h')
    def _set_h(self, h):
        self.style['h'] = h # Overwrite style from here, unless self.style['vacuum'] is True
    h = property(_get_h, _set_h)

    def __len__(self):
        return len(self.fs)

    def setText(self, s):
        u"""Set the formatted string to s, using self.style."""
        self.fs = getFormattedString(s, self)

    def appendString(self, fs):
        u"""Append s to the running formatted string of the self. Note that the string
        is already assumed to be styled or can be added as plain string."""
        assert fs is not None
        if self.fs is None:
            self.fs = fs
        else:
            self.fs += fs
        return self.getOverflow(self.w, self.h)

    def appendMarker(self, markerId, arg=None):
        self.appendString(getMarker(markerId, arg=arg))

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
        return textOverflow(self.fs, (0, 0, w or self.w, h or self.h), LEFT)

    def getBaselinePositions(self, y=0, w=None, h=None):
        u"""Answer the list vertical baseline positions, relative to y (default is 0)
        for the given width and height. If omitted use (self.w, self.h)"""
        baselines = []
        for _, baselineY in textBoxBaseLines(self.fs, (0, y, w or self.w, h or self.h)):
            baselines.append(baselineY)
        return baselines

    def draw(self, origin, view):
        u"""Draw the text on position (x, y). Draw background rectangle and/or frame if
        fill and/or stroke are defined."""
        p = pointOffset(self.point, origin)
        #p = self._applyOrigin(p)    
        p = self._applyScale(p)    
        px, py, _ = self._applyAlignment(p) # Ignore z-axis for now.
   
        sFill = self.css('fill', NO_COLOR)
        if sFill != NO_COLOR:
            setStrokeColor(None)
            setFillColor(sFill)
            rect(px, py, self.w, self.h)
        hyphenation(True)
        textBox(self.fs, (px, py, self.w, self.h))
        sStroke = self.css('stroke', NO_COLOR)
        sStrokeWidth = self.css('strokeWidth')
        if sStroke != NO_COLOR and sStrokeWidth is not None:
            setStrokeColor(sStroke, sStrokeWidth)
            setFillColor(None)
            rect(px, py, self.w, self.h)
        else: # If debugging,then draw the rectangle. Only self.css('showElementBox') is True
            self.drawFrame(origin)

        # If there are child elements, draw them over the text.
        self._drawElements(origin, view)

        self._restoreScale()
        view.drawElementInfo(self, origin) # Depends on css flag 'showElementInfo'

        

