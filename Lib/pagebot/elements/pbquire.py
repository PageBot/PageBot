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

from pagebot.elements.element import Element
from pagebot.constants import QUIRE_SINGLE

class Quire(Element):
    u"""A Quire element typically holds a set of pages, such as left+right -->
    spread, quires --> folded sheets, that can print as a single page.

    http://www.ndl.go.jp/incunabula/e/chapter3/index.html

    After the medieval times, books took the form of codices rather than
    scrolls, and printed books came to be made of quires, sheets of paper
    folded over.  Quires are sewn in the middle by thread to make a booklet,
    the minimum component of a book. By putting a number of quires together and
    stitching their edges, we can make a book. The number of times the whole
    sheet of paper is folded determines the size of the book, which is called
    "format." The format of books produced by folding the whole sheet of paper
    once is called "folio," twice "quarto," and three times "octavo," which are
    abbreviated as "2o," "4o" and "8o." These format names are derived from the
    number of leaves in a quire produced by folding the sheet of paper."""

    def __init__(self, folds=None, startPage=None, **kwargs):
        Element.__init__(self,  **kwargs)
        if folds is None:
            # Default is single page. E.g. (2, 1) would be a spread, etc.
            # Types of Quire formats, how to compose pages
            # QUIRE_SINGLE = (1, 1)
            # QUIRE_SPREAD = (-2, 1) # Spread of 2 connected pages, without gutter for crop-marks or bleed
            # QUIRE_2x2 = (2, 2) # is a Quire of 4 pages, e.g. to be cut as separate sheets
            # QUIRE_8x4 = (8, 4) # is a Quire of 32 separate pages, e.g. to be cut as 32 business cards.
            # QUIRE_LEPARELLO3 = (-3, 1) # is a leparello of 3 connected pages.
            # QUIRE_LEPARELLO4 = (-4, 1) # is a leparello of 4 connected pages.
            # QUIRE_FOLIO = (QUIRE_SPREAD, 2) # 2o, a Quire of 2 spreads
            # QUIRE_QUARTO = (2, QUIRE_FOLIO) # 4o
            # QUIRE_OCTAVO = (QUIRE_QUARTO, 2) # 8o, folding into 16 pages
            folds = QUIRE_SINGLE # 1, 1
        self.folds = folds
        self.startPage = startPage or 1

    def __len__(self):
        u"""Answer the amount of required pages, based on the self.folds compositions.

        >>> from pagebot.constants import *
        >>> q = Quire(QUIRE_LEPARELLO4)
        >>> len(q)
        4
        >>> q = Quire(QUIRE_QUARTO)
        >>> len(q)
        8
        >>> q = Quire(QUIRE_OCTAVO)
        >>> len(q)
        16
        """
        def size(folds):
            if isinstance(folds, (list, tuple)):
                assert len(folds) == 2
                return abs(size(folds[0]) * size(folds[1])) # Calculate
            return folds

        return size(self.folds)




if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
