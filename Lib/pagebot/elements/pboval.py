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
#     oval.py
#
from __future__ import division # Make integer division result in float.

from pagebot.style import NO_COLOR, ORIGIN
from pagebot.elements.element import Element
from pagebot.toolbox.transformer import pointOffset

class Oval(Element):

    #   G E N E R I C  C O N T E X T  S U P P O R T

    def build(self, view, origin=ORIGIN, drawElements=True):

        context = self.context # Get current context and builder.

        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(view, p)    
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.
    
        self.drawFrame(view, p) # Draw optional frame or borders.
  
        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        context.setFillColor(self.css('fill', NO_COLOR))
        context.setStrokeColor(self.css('stroke', NO_COLOR), self.css('strokeWidth'))
        context.oval(px, py, self.w, self.h)

        if drawElements:
            self.buildElements(view, p)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreScale(view)
        view.drawElementMetaInfo(self, origin)
        

