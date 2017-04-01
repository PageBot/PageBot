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
#     ruler.py
#
from pagebot import setFillColor
from pagebot.elements.element import Element
from pagebot.toolbox.transformer import pointOrigin2D

class Ruler(Element):

    def _get_h(self):
        return self.css('strokeWidth', 0)
    def _set_h(self, h):
        self.style['h'] = self.style['strokeWidth'] = h # Overwrite style from here.
    h = property(_get_h, _set_h)

    def draw(self, origin):
        p = pointOrigin2D(self.point, origin)
        p = self._applyOrigin(p)    
        p = self._applyScale(p)    
        px, py = self._applyAlignment(p)
        sIndent = self.css('indent')
        sTailIndent = self.css('tailIndent')
        w = self.w - sIndent - sTailIndent
        
        setFillColor(None)
        setStrokeColor(self.css('stroke', NO_COLOR), self.css('strokeWidth'))
        line((px + sIndent, py), (px + w, py))

        self._restoreScale()

