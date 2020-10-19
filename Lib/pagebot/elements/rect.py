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
#     pbrect.py
#

from pagebot.constants import ORIGIN
from pagebot.elements.element import Element
from pagebot.toolbox.units import pointOffset, point2D
from pagebot.toolbox.color import noColor

class Rect(Element):
    """Draw rectangle, default identical to Element itself.

    >>> from pagebot.toolbox.color import color
    >>> from pagebot.toolbox.units import pt
    >>> from pagebot import getContext
    >>> from pagebot.document import Document
    >>> c = getContext()
    >>> w, h = pt(300, 400)
    >>> doc = Document(w=w, h=h, autoPages=1, padding=30, context=c)
    >>> c.newDrawing(doc=doc)
    >>> page = doc[1]
    >>> e = Rect(parent=page, xy=(0, 20), size=(page.w, '3p2'), fill=color(1, 0, 0))
    >>> e.build(doc.getView(), (0, 0))
    >>> e.xy
    (0pt, 20pt)
    >>> e.size
    (300pt, 3p2)
    >>> view = doc.getView()
    >>> e.build(view, (0, 0))
    >>> doc.export('_export/TestRect-%s.pdf' % c.name)
    """

    def build(self, view, origin=ORIGIN, **kwargs):
        """Draws the oval in the current context canvas.

        >>> e = Rect(x=0, y=20, w=500, h=3)
        >>> e.xy
        (0pt, 20pt)
        >>> e.size
        (500pt, 3pt)
        """
        p = self.getPosition(view, origin)
        self.buildFrame(view, p) # Draw optional frame or borders.
        view.drawElementFrame(self, p)
        self.context.fill(self.css('fill', noColor))
        self.context.stroke(self.css('stroke', noColor), self.css('strokeWidth'))
        px, py, _ = p
        self.context.rect(px, py, self.w, self.h)
        self.buildChildElements(view, p, **kwargs)
        self.restore(view, p)
        self.drawMeta(view, origin)

    def build_inds(self, view, origin):
        """It is better to have a separate InDesignContext build tree, since we
        need more information down there than just drawing instructions. This
        way the InDesignContext just gets the PageBot Element passed over,
        using it's own API."""
        context = view.context
        p = pointOffset(self.origin, origin)
        # Ignore z-axis for now.
        px, py = p2D = point2D(self._applyAlignment(p))
        context.rect(px, py, e=self)

        for e in self.elements:
            e.build_inds(view, p2D)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
