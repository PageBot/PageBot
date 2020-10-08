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
#     textalignments.py
#

class TextAlignments:
    # Implemented for elements that support text boxes. Default is True
    # for non-text elements, so the calling condition is satisfied.

    def isBaselineOnGrid(self, tolerance=0, index=0):
        return True

    def isBaselineOnTop(self, tolerance=0, index=0):
        return True

    def isBaselineOnBottom(self, tolerance=0, index=0):
        return True

    def isAscenderOnGrid(self, tolerance=0, index=0):
        return True

    def isAscenderOnTop(self, tolerance=0, index=0):
        return True

    def isAscenderOnBottom(self, tolerance=0, index=0):
        return True

    def isCapHeightOnGrid(self, tolerance=0, index=0):
        return True

    def isCapHeightOnTop(self, tolerance=0, index=0):
        return True

    def isCapHeightOnBottom(self, tolerance=0, index=0):
        return True

    def isXHeightOnGrid(self, tolerance=0, index=0):
        return True

    def isXHeightOnTop(self, tolerance=0, index=0):
        return True

    def isXHeightOnBottom(self, tolerance=0, index=0):
        return True

    def isDescenderOnGrid(self, tolerance=0, index=0):
        return True

    def isDescenderOnTop(self, tolerance=0, index=0):
        return True

    def isDescenderOnBottom(self, tolerance=0, index=0):
        return True

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
