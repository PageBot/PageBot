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
from pagebot.style import NO_COLOR, CENTER, RIGHT_ALIGN, TOP_ALIGN
from pagebot.elements.element import Element
from pagebot.toolbox.transformer import pointOrigin2D

class Rect(Element):
    def __init__(self, point=None, parent=None, style=None, eId=None, **kwargs):
        Element.__init__(self, point=point, parent=parent, style=style, eId=eId, **kwargs)
        # Initialize the default Element behavior tags.
        self.isContainer = False
        self.isText = False
        self.isFlow = False

    def draw(self, origin):
        p = pointOrigin2D(self.point, origin)
        p = self._applyOrigin(p)    
        p = self._applyScale(p)    
        px, py = self._applyAlignment(p)
        
        setFillColor(self.css('fill', NO_COLOR))
        setStrokeColor(self.css('stroke', NO_COLOR), self.css('strokeWidth'))
        rect(px, py, self.w, self.h)

        self._restoreScale()
        self._drawElementInfo(origin) # Depends on css flag 'showElementInfo'

