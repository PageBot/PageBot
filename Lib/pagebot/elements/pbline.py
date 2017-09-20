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

    #   D R A W B O T  S U P P O R T

    def build_drawBot(self, view, origin=ORIGIN, drawElements=True):
        b = view.b
        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(view, p)    
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.
 
        view.setStrokeColor(self.css('stroke', NO_COLOR), self.css('strokeWidth'))
        b.newPath()
        b.moveTo((px, py))
        b.lineTo((px + self.w, py + self.h))
        b.drawPath()

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        if drawElements:
            # If there are child elements, recursively draw them over the pixel image.
            for e in self.elements:
                if e.show:
                    e.build_drawBot(view, origin)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)
  
        self._restoreScale(view)
        view.drawElementMetaInfo(self, origin)

    #   F L A T  S U P P O R T

    def build_flat(self, view, origin=ORIGIN, drawElements=True):
        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(p)    
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        if drawElements:
            for e in self.elements:
                e.build_flat(view, p)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreScale(view)
        view.drawElementMetaInfo(self, origin)
       
    #   H T M L  /  C S S  S U P P O R T

    def build_html(self, origin, view, drawElements=True):

        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(p)    
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        if drawElements:
            for e in self.elements:
                e.build_html(view, p)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreScale(view)
        view.drawElementMetaInfo(self, origin)
