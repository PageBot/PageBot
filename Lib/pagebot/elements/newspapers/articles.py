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
#     articles.py
#
from pagebot.elements import *
from pagebot.conditions import *

class Article(Rect):
    pass

class ArticleHCC(Rect):
    """Implements a specialized newspaper article, as group of a
    headline and 2 columns underneath

    >>> from pagebot.document import Document
    >>> from pagebot.constants import Tabloid
    >>> from pagebot.toolbox.units import mm
    >>> doc = Document(size=Tabloid, padding=mm(20))
    >>> page = doc[1]
    >>> a = ArticleHCC(parent=page)
    >>> score = page.solve()
    >>> page['ArticleHead'].box
    (0pt, 0pt, 100pt, 100pt)
    """
    def __init__(self, **kwargs):
        Rect.__init__(self, **kwargs)
        newText(parent=self, name='ArticleHead', conditions=(Left2Left(), Top2Top(), Fit2Width()))
        newText(parent=self, name='ArticleCol1', conditions=(Left2Left(), Fit2ColSpan(1), Float2Top()))
        # FIXME: Left2ColSpan doesn't exist.
        #newText(parent=self, name='ArticleCol2', conditions=(Left2ColSpan(1), Fit2ColSpan(1), Float2Top()))

class ArticleHCCC(Rect):
    pass

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
