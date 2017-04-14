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
from drawBot import textSize, text
from pagebot import getFormattedString
from pagebot.elements.element import Element
from pagebot.toolbox.transformer import pointOffset, point3D
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
        u"""If self.originTop is False, then the y-value is interpreted as mathematics, 
        starting at the bottom of the parent element, moving up.
        If the flag is True, then move from top down, where the text still draws upward."""
        if self.originTop and self.parent:
            p = point3D(p) # We cannot assume here it is a point3D list.
            p[1] = self.parent.h - p[1] # We assume here it is a point3D list.
        return p

    def _applyAlignment(self, p):
        w, h = textSize(self.fs)   
        px, py, pz = point3D(p) # We cannot assume here it is a point3D list.
        if self.css('align') == CENTER:
            px -= w/2/self.scaleX
        elif self.css('align') == RIGHT_ALIGN:
            px -= w/self.scaleX
        if self.originTop:
            if self.css('vAlign') == CENTER:
                py += h/2/self.scaleY
            elif self.css('vAlign') == TOP_ALIGN:
                py += h/self.scaleY
        else:
            if self.css('vAlign') == CENTER:
                py -= h/2/self.scaleY
            elif self.css('vAlign') == TOP_ALIGN:
                py -= h/self.scaleY
        return px, py, pz

    def draw(self, origin):
        u"""Draw the formatted text. Since this is not a text column, but just a
        typeset text line, background and stroke of a text column needs to be drawn elsewere."""
        p = pointOffset(self.point, origin)
        p = self._applyOrigin(p)    
        p = self._applyScale(p)    
        px, py, _ = self._applyAlignment(p) # Ignore z-axis for now.
        self._setShadow()

        text(self.fs, (px, py))

        self._resetShadow()
        self._restoreScale()




