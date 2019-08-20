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


from pagebot.elements.element import Element
from pagebot.toolbox.units import pointOffset, point2D

class Rect(Element):
    """Draw rectangle, default identical to Element itself.

    >>> from pagebot.toolbox.color import color
    >>> from pagebot.toolbox.units import pt
    >>> from pagebotcocoa.contexts.drawbot.drawbotcontext import DrawBotContext
    >>> from pagebot.document import Document
    >>> c = DrawBotContext()
    >>> w, h = pt(300, 400)
    >>> doc = Document(w=w, h=h, autoPages=1, padding=30, originTop=False, context=c)
    >>> page = doc[1]
    >>> e = Rect(parent=page, xy=(0, 20), size=(page.w, '3p2'), fill=color(1, 0, 0))
    >>> e.build(doc.getView(), (0, 0))
    >>> e.xy
    (0pt, 20pt)
    >>> e.size
    (300pt, 3p2)
    >>> view = doc.getView()
    >>> e.build(view, (0, 0))
    >>> doc.export('_export/TestRect.pdf')

    """
    """ TODO: Get to work in Flat
    >>> from pagebot.contexts.flat.flatcontext import FlatContext
    >>> from pagebot.document import Document
    >>> c = FlatContext()
    >>> doc = Document(w=w, h=h, autoPages=1, padding=30, originTop=False, context=c)
    >>> page = doc[1]
    >>> e = Rect(parent=page, x=0, y=20, w=page.w, h=3)
    >>> # Allow the context to create a new document and page canvas. Normally view does it.
    >>> c.newPage(w, h)
    >>> e.build(doc.getView(), (0, 0))
    >>> e.xy
    (0pt, 20pt)
    >>> e.size
    (300pt, 3pt)
    """

    # No separate build, default behavior is in Element.build()

    def build_inds(self, view, origin, drawElements=True):
        """It is better to have a separate InDesignContext build tree, since we need more
        information down there than just drawing instructions.
        This way the InDesignContext just gets the PageBot Element passed over, using
        it's own API."""
        context = view.context
        p = pointOffset(self.origin, origin)
        px, py = p2D = point2D(self._applyAlignment(p)) # Ignore z-axis for now.
        context.rect(px, py, e=self)
        if drawElements:
            for e in self.elements:
                e.build_inds(view, p2D)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
