#!/usr/bin/env python
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     Fonts.py
#
#     Shows how to get fonts.
#    

from pagebot.fonttoolbox.objects.font import findFont
from pagebot.fonttoolbox.fontpaths import getFontPaths

fontPaths = getFontPaths()
print(len(fontPaths))
fontName = list(fontPaths.keys())[0]
print(fontName)
getFontPaths()
font = findFont(fontName)
print(font)
print(len(font))