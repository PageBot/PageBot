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
from pagebot.toolbox.transformer import pointOrigin2D
from pagebot import setStrokeColor, setFillColor
from pagebot.elements.element import Element

class Line(Element):

    def draw(self, origin):
        p = pointOrigin2D(self.point, origin)
        p = self._applyOrigin(p)    
        p = self._applyScale(p)    
        px, py = self._applyAlignment(p)
 
        setStrokeColor(self.style.get('stroke', NO_COLOR), self.style.get('strokeWidth'))
        newPath()
        moveTo((px, py))
        lineTo((px + self.w, py + self.h))
        drawPath()

        self._restoreScale()
