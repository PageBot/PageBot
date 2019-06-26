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
#     pbquire.py
#

from pagebot.elements.element import Element
from pagebot.constants import QUIRE_SINGLE

class Quire(Element):
    """A Quire element typically holds a set of pages, such as left+right -->
    spread, quires --> folded sheets, that can print as a single page.

    http://www.ndl.go.jp/incunabula/e/chapter3/index.html

    After the middle ages books took the form of codices rather than scrolls
    and printed books were made of quires, sheets of paper that were folded
    over. Quires are sewn in the middle with a thread to make a booklet, the
    minimum component of a book. By putting a number of quires together and
    stitching their edges, we can make a book. The number of times the whole
    sheet of paper is folded determines the size of the book, which is called
    "format." The format of books produced by folding the whole sheet of paper
    once is called "folio," twice "quarto," and three times "octavo," which are
    abbreviated as "2o," "4o" and "8o." These format names are derived from the
    number of leaves in a quire produced by folding the sheet of paper."""

    def __init__(self, folds=None, **kwargs):
        Element.__init__(self,  **kwargs)
        if folds is None:
            # Default is single page. E.g. (2, 1) would be a spread, etc.
            # Types of Quire formats, how to compose pages
            # The gap between the pages is defined by page.margin values
            # QUIRE_SINGLE = (1, 1)
            # QUIRE_SPREAD = (2, 1) # Spread of 2 connected pages, without gutter for crop-marks or bleed
            # QUIRE_2x2 = (2, 2) # is a Quire of 4 pages, e.g. to be cut as separate sheets
            # QUIRE_8x4 = (8, 4) # is a Quire of 32 separate pages, e.g. to be cut as 32 business cards.
            # QUIRE_LEPARELLO3 = (3, 1) # is a leparello of 3 connected pages.
            # QUIRE_LEPARELLO4 = (4, 1) # is a leparello of 4 connected pages.
            # QUIRE_FOLIO = (QUIRE_SPREAD, 2) # 2°, a Quire of 2 spreads
            # QUIRE_QUARTO = (2, QUIRE_FOLIO) # 4°
            # QUIRE_OCTAVO = (QUIRE_QUARTO, 2) # 8°, folding into 16 pages
            folds = QUIRE_SINGLE # 1, 1
        self.piw, self.pih = self.folds = folds # Split value of page-index-width and page-index-height
        self.pages = {}

    def place(self, page, pix, piy):
        u"""Add the page to the page list at location (pix, piy). If there is no
        list yet at that location, then first create an empty list.
        Note that the pages are kept in the self.pages by reference, not changing their
        parent and no
        """
        assert pix in range(self.piw) and piy in range(self.pih) # Check if page is set in range.
        if (pix, piy) not in self.pages:
            self.pages[(pix, piy)] = []
        self.pages[(pix, piy)].append(page)

    def __len__(self):
        """Answers the amount of required pages, based on the `self.wi * self.hi`
        compositions.

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
