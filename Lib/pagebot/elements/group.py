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
#     group.py
#
#from pagebot.elements.rect import Rect
from pagebot.elements.element import Element

class Group(Element):
    """Groups elements, default identical to Element itself.

    FIXME: nested alignments need more testing.

    >>> from pagebot.toolbox.units import pt
    >>> from pagebot import getContext
    >>> from pagebot.elements.element import Element
    >>> from pagebot.document import Document
    >>> c = getContext()
    >>> w, h = pt(300), pt(400)
    >>> doc = Document(w=w, h=h, autoPages=1, padding=30, context=c)
    >>> page = doc[1]
    >>> page
    <Page #1 default (300pt, 400pt)>
    >>> e1, e2, e3 = Element(w=123),Element(w=234),Element(w=345)
    >>> e = Group(parent=page, x=0, y=20, w=page.w, elements=(e1, e2, e3))
    """

    # TODO: restore tests.
    """
    >>> e.build(doc.getView(), (0, 0))
    >>> e.xy,  e.size
    ((0pt, 20pt), (300pt, 100pt))
    >>> view = doc.getView()
    >>> e.build(view, (0, 0))
    >>> from pagebot.document import Document
    >>> doc = Document(w=w, h=h, autoPages=1, padding=30, context=c)
    >>> page = doc[1]
    >>> e1, e2, e3 = Element(w=123), Element(w=234), Element(w=345)
    >>> e = Group(parent=page, x=0, y=20, w=page.w, elements=(e1, e2, e3))
    >>> # Allow the context to create a new document and page canvas. Normally view does it.
    >>> c.newPage(w, h)
    >>> e.build(doc.getView(), (0, 0))
    >>> e.xy, e.xyz
    ((0pt, 20pt), (0pt, 20pt, 0pt))
    >>> e.size, e.size3D
    ((300pt, 100pt), (300pt, 100pt, 100pt))
    """
    # No separate build, default behavior is in Element.build().


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
