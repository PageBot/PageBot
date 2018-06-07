#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     rect.py
#
from __future__ import division # Make integer division result in float.

from pagebot.elements.element import Element

class Rect(Element):
    u"""Draw rectangle, default identical to Element itself.

    >>> from pagebot.contexts.drawbotcontext import DrawBotContext
    >>> from pagebot.document import Document
    >>> c = DrawBotContext()
    >>> w, h = 300, 400
    >>> doc = Document(w=w, h=h, autoPages=1, padding=30, originTop=False, context=c)
    >>> page = doc[1]
    >>> e = Rect(parent=page, x=0, y=20, w=page.w, h=3)
    >>> e.build(doc.getView(), (0, 0))
    >>> e.xy
    (0, 20)
    >>> e.size
    (300, 3, 1)
    >>> view = doc.getView()
    >>> e.build(view, (0, 0))

    >>> from pagebot.contexts.flatcontext import FlatContext 
    >>> from pagebot.document import Document
    >>> c = FlatContext()
    >>> doc = Document(w=w, h=h, autoPages=1, padding=30, originTop=False, context=c)
    >>> page = doc[1]
    >>> e = Rect(parent=page, x=0, y=20, w=page.w, h=3)
    >>> # Allow the context to create a new document and page canvas. Normally view does it.
    >>> c.newPage(w, h) 
    >>> e.build(doc.getView(), (0, 0))
    >>> e.xy
    (0, 20)
    >>> e.size
    (300, 3, 1)
    """

    # No separate build, default behavior is in Element.build()


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
