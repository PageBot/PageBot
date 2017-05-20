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
#     path.py
#
from drawBot import drawPath, save, restore, transform, scale
from pbpath import Path
from pagebot.toolbox.transformer import pointOffset
from pagebot import setStrokeColor, setFillColor
from pagebot.style import NO_COLOR

class GlyphPath(Path):

    def __init__(self, glyph, w=None, h=None, pathFilter=None, **kwargs):
        Path.__init__(self, **kwargs)
        self.glyph = glyph 
        self.w = w or 100
        self.h = h or 100
        self.pathFilter = pathFilter # Optional pathFilter method, called with self as param.

    def draw(self, origin, view):

        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(p)    
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        save()
        scale(0.25)
        transform((1, 0, 0, 1, px, py))
        if self.pathFilter is not None:
            self.pathFilter(self, self.glyph.path)
        else:
            setFillColor(self.css('fill'))
            setStrokeColor(self.css('stroke', NO_COLOR), self.css('strokeWidth'))
            drawPath(self.glyph.path)
        restore()

        # If there are child elements, draw them over the polygon.
        self._drawElements(p, view)

        # Draw optional bouning box.
        self.drawFrame(origin, view)
 
        self._restoreScale()
        view.drawElementMetaInfo(self, origin) # Depends on css flag 'showElementInfo'
