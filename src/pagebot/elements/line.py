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
#     line.py
#
from drawBot import newPath, moveTo, lineTo, drawPath 
from pagebot.style import NO_COLOR
from pagebot.toolbox.transformer import pointOffset
from pagebot.elements.element import Element

class Line(Element):

    def draw(self, origin, view):
        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(p)    
        px, py, _ = self._applyAlignment(p) # Ignore z-axis for now.
 
        setStrokeColor(self.css('stroke', NO_COLOR), self.css('strokeWidth'))
        newPath()
        moveTo((px, py))
        lineTo((px + self.w, py + self.h))
        drawPath()

        # If there are child elements, draw them over the text.
        self._drawElements(origin)

        self._restoreScale()
        view.drawElementMetaInfo(self, origin)
