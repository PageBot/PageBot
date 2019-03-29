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
from pagebot.toolbox.units import point2D, units

class Polygon(Element):
    """The Polygon element is a simple implementation of the polygon DrawBot
    function. More complex path-like elements inherit from the Path element."""

    def __init__(self, points=None, closed=True, **kwargs):
        self.closed = closed
        if points is None:
            points = []
        self.points = points[:] # Force copy, so caller cannot change and not change size cache.
        Element.__init__(self, **kwargs)

    def append(self, p):
        p = units(point2D(p))
        assert p is not None
        self.points.append(p)

    def _get_block(self):
        """Answer the bounding box of the containted points.

        >>> e = Polygon()
        >>> e.append((0, 0))
        >>> e.append((100, 0))
        >>> e.append((50, 80))
        >>> e.closePath = True
        >>> e.points
        [(0pt, 0pt), (100pt, 0pt), (50pt, 80pt)]
        >>> e.block
        (100pt, 80pt)
        """
        if not self.points:
            block = units(0, 0)
        else:
            maxX = maxY = -XXXL
            minX = minY = XXXL
            for point in self.points:
                maxX = max(maxX, point[0])
                minX = min(minX, point[0])
                maxY = max(maxY, point[1])
                minY = min(minY, point[1])
            block = maxX - minX, maxY - minY
        return block
    block = property(_get_block)

    #   D R A W B O T / F L A T  S U P P O R T

    def build(self, view, origin, drawElements=True, **kwargs):
        context = self.context # Get current context and builder.
        b = context.b # This is a bit more efficient than self.b once we got context

        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        self._applyRotation(view, p)

        self.buildFrame(view, p) # Draw optional frame or borders.

        # Let the view draw frame info for debugging, in case view.showFrame == True
        # and self.isPage or if self.showFrame. Mark that we are drawing background here.
        view.drawPageMetaInfo(self, p, background=True)

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
        if self.closed:
            b.closePath()
        b.drawPath()

        if drawElements:
            # If there are child elements, recursively draw them over the pixel image.
            self.buildChildElements(view, p, **kwargs)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        # Let the view draw frame info for debugging, in case view.showFrame == True
        # and self.isPage or if self.showFrame. Mark that we are drawing foreground here.
        view.drawPageMetaInfo(self, p, background=False)

        self._restoreRotation(view, p)
        self._restoreScale(view)
        view.drawElementInfo(self, origin) # Depends on flag 'view.showElementInfo'

    #   H T M L  /  C S S  S U P P O R T

    def build_html(self, view, origin=None, drawElements=True):
        """Drawing HTML Polygon through SVG?"""
        context = self.context # Get current context and builder.
        b = context.b # This is a bit more efficient than self.b once we got context
        # TODO: Needs a solution, SVG or pixels?

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
