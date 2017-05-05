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
#     polygon.py
#
from pagebot.elements.element import Element
from pagebot.style import
class Polygon(Element):

    def __init__(self, fs, points=None, **kwargs):
        Element.__init__(self, **kwargs)
        if points is None:
            points = []
        self.points = points
        self._size = None # Cached propertions, will reset by self.points

    def _get_size(self):
        if self._size is None:
            w = h = None
            for point in self.points:
                if w 
    def _get_w(self):
        return self.size()[0]
    w = property(_get_w)

    def _get_h(self):
        return self.
    def draw(self, origin, view):

        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(p)    
        px, py, _ = self._applyAlignment(p) # Ignore z-axis for now.
        setStrokeColor(self.css('stroke', NO_COLOR), self.css('strokeWidth'))
        newPath()
        for index, (ppx, ppy) in enumerate(self.points):
            if index == 0:
                moveTo((px + ppx, py + ppy))
            else:
                lineTo((px + ppx, py + ppy))
        drawPath()

        # If there are child elements, draw them over the text.
        self._drawElements(origin, view)

        # Draw markers on TextLine and TextRun positions.
        self.drawFrame(origin, view)
        self._drawBaselines(view)
 
        self._restoreScale()
        view.drawElementMetaInfo(self, origin) # Depends on css flag 'showElementInfo'

