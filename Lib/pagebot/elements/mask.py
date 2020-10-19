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

from pagebot.constants import DEFAULT_WIDTH, DEFAULT_HEIGHT, ORIGIN
from pagebot.toolbox.units import pointOffset
from pagebot.toolbox.color import noColor
from pagebot.elements.polygon import Polygon

class Mask(Polygon):
    """Masks don't draw by themselves, unless a fill color or stroke color
    is defined for debugging. Masks get interpreted by sibling elements,
    such as Image.
    """

    def __init__(self, points=None, w=None, h=None, **kwargs):
        if points is None:
            if w is None:
                w = DEFAULT_WIDTH
            if h is None:
                h = DEFAULT_HEIGHT
            # If no points, then initialize as default rectangle.
            points = [(0, 0), (0, h), (w, h), (w, 0)]
        Polygon.__init__(self, points=points, w=w, h=h, **kwargs)

    def build(self, view, origin=ORIGIN, **kwargs):
        context = self.context # Get current context and builder.
        b = context.b # This is a bit more efficient than self.b once we got context
        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.
        self._applyRotation(view, p)

        doDraw = False
        if self.fill not in (None, noColor):
            context.fill(self.fill)
            doDraw = True

        if self.stroke not in (None, noColor) and self.strokeWidth:
            context.stroke(self.stroke)
            context.strokeWidth(self.strokeWidth)
            doDraw = True

        if doDraw:
            context.rect(px, py, self.w, self.h)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        # Let the view draw frame info for debugging, in case view.showFrame ==
        # True and self.isPage or if self.showFrame. Mark that we are drawing
        # foreground here.
        view.drawPageMetaInfo(self, p)

        # Supposedly drawing outside rotation/scaling mode, so the origin of
        # the element is visible.
        view.drawElementOrigin(self, origin)

        self._restoreRotation(view, p)
        self._restoreScale(view)
        view.drawElementInfo(self, origin) # Depends on flag 'view.showElementInfo'

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
