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
#     flattextline.py
#

class FlatTextLine:

    def __init__(self, i, x, y, placedText):
        self.i = i
        self.x = x
        self.y = y
        self.placedTexts = []
        self.placedTexts.append(placedText)

    def __repr__(self):
        return '<FlatTextLine #%s y:%s Runs:%d>' % (self.i, self.y, len(self.placedTexts))

    def append(self, placedText):
        self.placedTexts.append(placedText)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
