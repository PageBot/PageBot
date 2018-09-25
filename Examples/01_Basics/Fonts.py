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
from pagebot import *
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.fonttoolbox.fontpaths import *
from pagebot.fonttoolbox.objects.family import getFamilyPaths

def showAll():
    families = getFamilyPaths()
    print(families['Roboto'])
    fontPaths = getFontPaths()
    print('Number of fonts found: %d' % len(fontPaths))
    import glob
    tfp = getTestFontsPath()
    '''
    print(glob.glob('%s/*' % tfp))
    roboto = tfp + '/google/roboto'
    print(glob.glob('%s/*' % roboto))
    '''
    pbFonts = getPageBotFontPaths()
    print('Number of fonts shipped with PageBot: %d' % len(pbFonts))
    print(sorted(pbFonts.keys()))
    font = findFont('Roboto-Black')
    print('The Font object from the pagebot.fonttoolbox.objects module: %s' % font)
    print('Number of glyphs: %d' % len(font))

showAll()
