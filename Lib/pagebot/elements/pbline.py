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
#     line.py
#
from pagebot.style import NO_COLOR
from pagebot.toolbox.transformer import pointOffset
from pagebot.elements.element import Element
from pagebot.style import ORIGIN

class Line(Element):

    #   D R A W B O T / F L A T  S U P P O R T

    def build(self, view, origin=ORIGIN, drawElements=True):

        context = self.context # Get current context and builder.
               
        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(view, p)    
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.
 
        view.setStrokeColor(self.css('stroke', NO_COLOR), self.css('strokeWidth'))
        context.newPath()
        context.moveTo((px, py))
        context.lineTo((px + self.w, py + self.h))
        context.drawPath()

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        if drawElements:
            # If there are child elements, recursively draw them over the pixel image.
            self.buildChildElements(view, p)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)
  
        self._restoreScale(view)
        view.drawElementMetaInfo(self, origin)
     
    #   H T M L  /  C S S  S U P P O R T

    def build_html(self, view, origin=None, drawElements=True):

        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(p)    
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        if drawElements:
            self.drawChildElements(view, p)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreScale(view)
        view.drawElementMetaInfo(self, origin)
