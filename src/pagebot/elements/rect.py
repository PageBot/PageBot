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
#     rect.py
#
from __future__ import division # Make integer division result in float.
from drawBot import rect

from pagebot import setStrokeColor, setFillColor
from pagebot.style import NO_COLOR
from pagebot.elements.element import Element
from pagebot.toolbox.transformer import pointOffset

class Rect(Element):

    def draw(self, origin, view):

        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(p)    
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        setFillColor(self.css('fill', NO_COLOR))
        setStrokeColor(self.css('stroke', NO_COLOR), self.css('strokeWidth'))
        rect(px, py, self.w, self.h)

       	# Draw embedded elements.
        self._drawElements(p, view)

        self._restoreScale()
        view.drawElementMetaInfo(self, origin)

