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
#     oval.py
#

from pagebot.constants import ORIGIN
from pagebot.elements.element import Element
from pagebot.toolbox.units import pointOffset, point2D
from pagebot.toolbox.color import noColor

class Oval(Element):

    def build(self, view, origin=ORIGIN, **kwargs):
        """Draws the oval in the current context canvas.

        >>> e = Oval(x=0, y=20, w=500, h=3)
        >>> e.xy
        (0pt, 20pt)
        >>> e.size
        (500pt, 3pt)
        """
        p = self.getPosition(view, origin)
        px, py, _ = p
        self.buildFrame(view, p)
        view.drawElementFrame(self, p)
        self.context.fill(self.css('fill', noColor))
        self.context.stroke(self.css('stroke', noColor), self.css('strokeWidth'))
        self.context.oval(px - self.w / 2, py - self.h / 2, self.w, self.h)
        self.buildChildElements(view, p, **kwargs)
        self.restore(view, p)
        self.drawMeta(view, origin)

    def build_inds(self, view, origin):
        """It is better to have a separate InDesignContext build tree, because
        we need more information than just drawing instructions. We just pass
        the PageBot Element to the InDesignContext, using it's own API."""
        context = view.context
        p = pointOffset(self.origin, origin)
        px, py = p2D = point2D(self._applyAlignment(p)) # Ignore z-axis for now.
        context.oval(px, py, e=self)
        for e in self.elements:
            e.build_inds(view, p2D)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
