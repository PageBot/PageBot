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
#     ShowFontContent.py
#
#
from __future__ import print_function
import pagebot
from pagebot.contexts.platform import getContext
from pagebot.fonttoolbox.objects.font import findFont

c = getContext()

f = findFont('Amstelvar-Roman-VF') # Get PageBot Font instance of Variable font.
EXPORT_PATH = '_export/ShowFontContent.pdf'

L = 50
# Names and text fields
print('-- Names', '-'*L)
print('Full name:', f.info.fullName)
print('Family name:', f.info.familyName)
print('Style name:', f.info.styleName)
print('PS name:', f.info.psName)
print('Designer:', f.info.designer)
print('Description:', f.info.description)
print('Trademark:', f.info.trademark)
#(Metrics)
print('-- Metrics', '-'*L)
print('Ascender:', f.info.ascender)
print('Typo Ascender:', f.info.typoAscender)
print('capHeight:', f.info.capHeight)
print('xHeight:', f.info.xHeight)
print('Descender:', f.info.descender)
print('Typo Descender:', f.info.typoDescender)
print('Line gap:', f.info.lineGap)
print('superscriptXSize:', f.info.superscriptXSize)
print('OS/2 Width class:', f.info.widthClass)
print('OS/2 Weight class:', f.info.weightClass)
print('subscriptXOffset:', f.info.subscriptXOffset)
print('strikeoutPosition:', f.info.strikeoutPosition)
print('SubscriptXSize:', f.info.subscriptXSize)
print('superscriptYOffset:', f.info.superscriptYOffset)
print('strikeoutSize:', f.info.strikeoutSize)
print('subscriptYSize:', f.info.subscriptYSize)
print('superscriptYSize:', f.info.superscriptYSize)
print('italicAngle:', f.info.italicAngle)
print('unitsPerEm:', f.info.unitsPerEm)
#(GPOS)
print('-- GPOS', '-'*L)
print('gposFeatures:', f.info.gposFeatures)
#(GSUB)
print('-- GSUB', '-'*L)
print('gsubFeatures:', f.info.gsubFeatures)
# Glyph content of the font
print('-- Glyhps', '-'*L)
print('Char set:', f.info.charSet)
print('Glyph set:', f.info.glyphSet)

W = H = 1000
GX = GY = 11
M = 50
# Scale em of 2048 back to page size.
glyphIndex = 1
s = 0.04

for y in range(GY):
    for x in range(GX):
        # Offset of drawing origin
        if glyphIndex > len(f.info.glyphSet):
            break
        c.save()
        c.translate(M+(W-2*M)/GX*x, H-M-(H-2*M)/GY*(y+1))
        g = f[f.info.glyphSet[glyphIndex-1]]
        c.drawPath(g.path, (0, 0), s)
        glyphIndex += 1
        c.restore()

c.saveImage(EXPORT_PATH)

