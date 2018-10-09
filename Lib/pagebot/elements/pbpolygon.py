#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     polygon.py
#
from pagebot.elements.element import Element
from pagebot.constants import XXXL
from pagebot.toolbox.units import pointOffset
from pagebot.toolbox.color import noColor

class Polygon(Element):
    """The Polygon element is a simple implementation of the polygon DrawBot
    function. More complex path-like elements inherit from the Path element."""

    def __init__(self, points=None, **kwargs):
        Element.__init__(self, **kwargs)

        if points is None:
            points = []
        self.points = points[:] # Force copy, so caller cannot change and not change size cache.

    def _get_points(self):
        return self._points
    def _set_points(self, points):
        self._points = points
        self._size = None # Cached propertions, will reset by self.w, self.h and self.size

    def _get_size(self):
        if self._size is None:
            if not self.points:
                self._size = 0, 0
            else:
                maxX = maxY = -XXXL
                minX = minY = XXXL
                w = h = None
                for point in self.points:
                    maxX = max(maxX, point[0])
                    minX = min(minX, point[0])
                    maxY = max(maxY, point[1])
                    minY = min(minY, point[1])
                self._size = maxX - minX, maxY - minY
        return self._size
    size = property(_get_size)

    def _get_w(self):
        return self.size[0] # Calculate cache self._size if undefined.
    w = property(_get_w)

    def _get_h(self):
        return self.size[1] # Calculate cache self._size if undefined.

    #   D R A W B O T / F L A T  S U P P O R T

    def build(self, view, origin, drawElements=True):
        context = self.context # Get current context and builder.
        b = context.b # This is a bit more efficient than self.b once we got context
        print('building poly')

        p = pointOffset(self.origin, origin)
        p = self._applyScale(p)
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        context.fill(self.css('fill'))
        context.stroke(self.css('stroke', noColor), self.css('strokeWidth'))
        b.newPath()
        for index, (ppx, ppy) in enumerate(self.points):
            if index == 0:
                b.moveTo((px + ppx, py + ppy))
            else:
                b.lineTo((px + ppx, py + ppy))
        b.drawPath()

        if drawElements:
            # If there are child elements, recursively draw them over the pixel image.
            self.buildElements(view, p)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        # Draw optional bounding box.
        self.drawFrame(origin, view)

        self._restoreScale()
        view.drawElementInfo(self, origin) # Depends on css flag 'showElementInfo'

    #   H T M L  /  C S S  S U P P O R T

    def build_html(self, view, origin=None, drawElements=True):
        """Drawing HTML Polygon through SVG?"""
        context = self.context # Get current context and builder.
        b = context.b # This is a bit more efficient than self.b once we got context
        # TODO: Needs a solution, SVG or pixels?
