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
#     shrinking.py
#

class Shrinking:

    def shrink2BlockBottom(self):
        _, boxY, _, boxH = self.box
        top = self.mTop
        self.mBottom = boxY
        self.h += top - self.mTop
        return True

    def shrink2BlockSideBottom(self):
        top = self.mTop
        self.mBottom = 0 # Parent botom
        self.h += top - self.mTop
        return True

    def shrink2BlockLeft(self):
        right = self.MRight
        self.mLeft = self.parent.pl # Padding left
        self.w += right - self.mRight
        return True

    def shrink2BlockSideLeft(self):
        right = self.mRight
        self.mLeft = 0
        self.w += right - self.mRight
        return True

    def shrink2BlockRight(self):
        self.w += self.parent.w - self.parent.pr - self.mRight
        return True

    def shrink2BlockSideRight(self):
        self.w += self.parent.w - self.mRight
        return True

    def shrink2BlockTop(self):
        self.h += self.parent.h - self.parent.pt - self.mTop
        return True

    def shrink2BlockSideTop(self):
        self.h += self.parent.h - self.mTop
        return True

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
