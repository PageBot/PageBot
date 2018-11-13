#!/usr/bin/env python3
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
#     03_Fonts.py
#
#     Shows how to get fonts.
#
from pagebot import *
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.fonttoolbox.fontpaths import *
from pagebot.fonttoolbox.objects.family import getFamilyPaths
from pagebot.constants import A3
from pagebot.document import Document
from pagebot.elements import *
from pagebot.toolbox.units import *

from pagebot.conditions import *

H, W = A3
W = W * 1.5
def showAll():
    context = getContext()
    doc = Document(w=W, h=H, originTop=False, autoPages=1, context=context)
    page = doc[1]
    c = (Right2Right(), Top2Top(), Float2Left())

    families = getFamilyPaths()
    print(families['Roboto'])
    fontPaths = getFontPaths()
    print('Number of fonts found: %d' % len(fontPaths))
    import glob
    tfp = getTestFontsPath()
    pbFonts = getPageBotFontPaths()
    print('Number of fonts shipped with PageBot: %d' % len(pbFonts))
    print(sorted(pbFonts.keys()))
    font = findFont('Roboto-Black')
    print('The Font object from the pagebot.fonttoolbox.objects module: %s' % font)
    print('Number of glyphs: %d' % len(font))
    for pbFont in list(pbFonts.keys()):
        if 'Bungee' in pbFont:
            newText('%s\n' % pbFont, parent=page, conditions=c, fontSize=30)
            f = findFont(pbFont)
            path = PageBotPath(context=context)
            path.text('CDE', style=dict(font=f, fontSize=pt(30)))
            path = path.removeOverlap()
            newPaths(path, parent=page, fill=0, conditions=c)
    
    page.solve()
    doc.build()

showAll()
