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
from pagebot.constants import A3
from pagebot.document import Document
from pagebot.elements import *
from pagebot.toolbox.units import *
from pagebot.conditions import *
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.fonttoolbox.fontpaths import *
from pagebot.fonttoolbox.objects.family import getFamilyPaths

W, H = A3

def showAll():
    context = getContext()
    doc = Document(w=W, h=H, originTop=False, autoPages=1, context=context)
    page = doc[1]
    c1 = (Fit2Right(), Left2Left(), Float2Top())
    c2 = (Left2Left(), Top2Top())
    c3 = (Float2Right(), Top2Top())

    families = getFamilyPaths()
    #print(families['Roboto'])
    fontPaths = getFontPaths()
    print('Number of fonts found: %d' % len(fontPaths))
    import glob
    tfp = getTestFontsPath()
    pbFonts = getPageBotFontPaths()
    print('Number of fonts shipped with PageBot: %d' % len(pbFonts))
    #print(sorted(pbFonts.keys()))
    font = findFont('Roboto-Black')
    print('The Font object from the pagebot.fonttoolbox.objects module: %s' % font)
    print('Number of glyphs: %d' % len(font))
    
    for pbFont in sorted(pbFonts.keys()):
        if 'Bungee' in pbFont or 'Roboto' in pbFont:
            g = newGroup(parent=page, conditions=c1, stroke=0, fill=(1, 0, 0.5), padding=7)
            newText('%s\n' % pbFont, parent=g, conditions=c2, fontSize=30, stroke=None, fill=(1, 1, 0), padding=7)
            f = findFont(pbFont)
            path = PageBotPath(context=context)
            path.text('ABCDEFGHIJK0123456789', style=dict(font=f, fontSize=pt(30), fill=(0, 1, 0)))
            #path = path.removeOverlap()
            newPaths(path, parent=g, fill=(0, 1, 1), conditions=c3, stroke=None, margin=20)

    page.solve()
    doc.build()

showAll()
