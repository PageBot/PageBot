# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#     
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     ruler.py
#
from pagebot.elements.element import Element
from pagebot.toolbox.transformer import pointOffset
from pagebot.style import ORIGIN

class Ruler(Element):

    def _get_h(self):
        return self.css('strokeWidth', 0)
    def _set_h(self, h):
        self.style['h'] = self.style['strokeWidth'] = h # Overwrite style from here.
    h = property(_get_h, _set_h)

    #   D R A W B O T  S U P P O R T

    def build_drawBot(self, view, origin, drawElement=True):

        context = self.context # Get current context and builder.
        b = context.b # This is a bit more efficient than self.b once we got context

        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(p)    
        px, py, _ = self._applyAlignment(p) # Ignore z-axis for now.
        sIndent = self.css('indent')
        sTailIndent = self.css('tailIndent')
        w = self.w - sIndent - sTailIndent
 
        if self.drawBefore is not None: # Call if defined
            self.drawBefore(p, view)

        context.setFillColor(None)
        context.setStrokeColor(self.css('stroke', NO_COLOR), self.css('strokeWidth'))
        b.line((px + sIndent, py), (px + w, py))

        if drawElements:
            # If there are child elements, recursively draw them over the pixel image.
            for e in self.elements:
                if e.show:
                    e.build_drawBot(origin, view)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, p, view)

        self._restoreScale(view)
        view.drawElementMetaInfo(self, origin)

    #   F L A T  S U P P O R T

    def build_flat(self, view, origin=ORIGIN, drawElements=True):

        context = self.context # Get current context and builder.
        b = context.b # This is a bit more efficient than self.b once we got context

        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(view, p)    
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        context.setFillColor(None)
        context.setStrokeColor(self.css('stroke', NO_COLOR), self.css('strokeWidth'))
        #b.line((px + sIndent, py), (px + w, py))

        if drawElements:
            for e in self.elements:
                e.build_flat(view, p)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreScale(view)
        view.drawElementMetaInfo(self, origin)
        
    #   H T M L  /  C S S  S U P P O R T

    def build_html(self, view, origin=None, drawElements=True):

        context = self.context # Get current context and builder.
        b = context.b # This is a bit more efficient than self.b once we got context
 
        self.build_css(view)
        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(view, p)    
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        context.setFillColor(None)
        context.setStrokeColor(self.css('stroke', NO_COLOR), self.css('strokeWidth'))
        #b.line((px + sIndent, py), (px + w, py))

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        if drawElements:
            for e in self.elements:
                e.build_html(view, p)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreScale(view)
        view.drawElementMetaInfo(self, origin)

