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
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     pbquire.py
#
from pagebot.style import ORIGIN
from pagebot.elements.element import Element
from pagebot.toolbox.units import pointOffset
from pagebot.toolbox.color import color

class Quire(Element):
    u"""A Quire element typically holds a set of pages, such as left+right --> spread, 
    quires --> folded sheets, that can print as a single page.

    http://www.ndl.go.jp/incunabula/e/chapter3/index.html

    After the medieval times, books took the form of codices rather than scrolls, 
    and printed books came to be made of quires, sheets of paper folded over. 
    Quires are sewn in the middle by thread to make a booklet, the minimum component 
    of a book. By putting a number of quires together and stitching their edges, 
    we can make a book. The number of times the whole sheet of paper is folded 
    determines the size of the book, which is called "format." The format of books 
    produced by folding the whole sheet of paper once is called "folio," twice 
    "quarto," and three times "octavo," which are abbreviated as "2o," "4o" and 
    "8o." These format names are derived from the number of leaves in a quire 
    produced by folding the sheet of paper.
    """
    

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
