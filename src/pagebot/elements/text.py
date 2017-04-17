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
#     Using the DrawBot textBox() instead of text() for better control
#     of alugnment, position and leading (in case there are "\n" returns
#     in the string)
#
from drawBot import textSize, textBox, fill, stroke, rect, FormattedString
from pagebot import getFormattedString, setFillColor, setStrokeColor
from pagebot.elements.element import Element
from pagebot.toolbox.transformer import pointOffset, point3D
from pagebot.style import RIGHT_ALIGN, CENTER, TOP_ALIGN, NO_COLOR

class Text(Element):

    # Initialize the default behavior tags as different from Element.
    isText = True  # This element is capable of handling text.

    def __init__(self, fs, point=None, parent=None, style=None, eId=None, w=0, h=0, **kwargs):
        Element.__init__(self, point=point, parent=parent, style=style, eId=eId, **kwargs)
        self.fs = getFormattedString(fs, self)
        self.w = w # If undefined or 0, then answer the current width of the string.
        self.h = h # If Undefined or 0, then ansser the curernt height of the sctring.

    def _get_w(self):
        return self.getTextSize()[0]
    def _set_w(self, w):
        pass # Ignore
    w = property(_get_w, _set_w)
   
    def _get_h(self):
        return self.getTextSize()[1]
    def _set_h(self, h):
        pass # Ignore
    h = property(_get_h, _set_h)
        
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
        px, py, pz = point3D(p) # We cannot assume here it is a point3D list.
        if self.css('align') == CENTER:
            px -= self.w/2/self.scaleX
        elif self.css('align') == RIGHT_ALIGN:
            px -= self.w/self.scaleX
        if self.originTop:
            if self.css('vAlign') == CENTER:
                py += self.h/2/self.scaleY + self.h
            elif self.css('vAlign') == TOP_ALIGN:
                py += self.h/self.scaleY + self.h
        else:
            if self.css('vAlign') == CENTER:
                py -= self.h/2/self.scaleY - self.h
            elif self.css('vAlign') == TOP_ALIGN:
                py -= self.h/self.scaleY - self.h
        return px, py, pz


    def _get_top(self):
        ascenderDescender = self.fs.fontAscender() - self.fs.fontDescender()
        #if self.css('vAlign') == CENTER:
        #    return self.y - ascenderDescender/2
        #if self.css('vAlign') == BOTTOM_ALIGN:
        #    return self.y - self.h
        return self.y + (self.h - ascenderDescender)/2 + self.fs.fontAscender()
    def _set_top(self, topY):
        ascenderDescender = self.fs.fontAscender() - self.fs.fontDescender()
        #if self.css('vAlign') == CENTER:
        #    self.y = y + self.h/2
        #elif self.css('vAlign') == BOTTOM_ALIGN:
        #    self.y = y + self.h
        #else:
        self.y = topY - (self.h - ascenderDescender)/2 + self.fs.fontAscender()
    top = property(_get_top, _set_top)


    def _get_bottom(self):
        ascenderDescender = self.fs.fontAscender() - self.fs.fontDescender()
        #if self.css('vAlign') == TOP_ALIGN:
        #    return self.y + self.h
        #if self.css('vAlign') == CENTER:
        #    return self.y + self.h/2
        return self.y + (self.h - ascenderDescender)/2 + self.fs.fontDescender()
    def _set_bottom(self, bottomY):
        ascenderDescender = self.fs.fontAscender() - self.fs.fontDescender()
        #if self.css('vAlign') == TOP_ALIGN:
        #    self.y = y - self.h
        #elif self.css('vAlign') == CENTER:
        #    self.y = y - self.h/2
        #else:
        self.y = bottomY - (self.h - ascenderDescender)/2 + self.fs.fontDescender()
    bottom = property(_get_bottom, _set_bottom)

    def draw(self, origin):
        u"""Draw the formatted text. Since this is not a text column, but just a
        typeset text line, background and stroke of a text column needs to be drawn elsewere."""
        p = pointOffset(self.point, origin)
        p = self._applyOrigin(p)    
        p = self._applyScale(p)    
        px, py, _ = self._applyAlignment(p) # Ignore z-axis for now.
        self._setShadow()
        """
        if self.css('fill') or self.css('stroke'):
            setFillColor(self.css('fill'))
            setStrokeColor(self.css('stroke'))
            ascenderDescender = self.fs.fontAscender() - self.fs.fontDescender()
            #print '====', self.h, self.css('fontSize'), self.fs.fontAscender(), self.fs.fontDescender(), ascenderDescender, self.h - ascenderDescender
            realDescender = (self.h - ascenderDescender)/2 + self.fs.fontDescender()
            #print realDescender
            rect(px, py + realDescender, self.w, self.h)
        """
        # In order to better control the alignment and flow of single text string
        # (they may include "\n" returns, forming multiple lines), we always use
        # the DrawBot textBox( ), instead of the single text( ) 
        textBox(self.fs, (px, py, self.w, self.h))

        self._resetShadow()
        self._restoreScale()
        self._drawElementInfo(origin) # Depends on css flag 'showElementInfo'



