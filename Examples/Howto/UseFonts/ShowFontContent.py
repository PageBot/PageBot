# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     ShowFontContent.py
#
#
import pagebot
from pagebot.contexts.platform import getContext
from pagebot.fonttoolbox.objects.font import Font
from __future__ import print_function

EXPORT_PATH = '_export/UpgradeFontOverviewr.pdf'
FONT_PATH = pagebot.getFontPath() + "/fontbureau/AmstelvarAlpha-VF.ttf"
FONT_PATH = u"/Users/petr/Desktop/TYPETR-git/TYPETR-Upgrade/scripts/export/ttf/Upgrade-Medium.ttf"

L = 50
f = Font(FONT_PATH)
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
print('(ubscriptXSize:', f.info.subscriptXSize))
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
GX = GY = 20
M = 50
# Scale em of 2048 back to page size.
glyphIndex = 1
s = 0.04
for y in range(GY):
    for x in range(GX):
        # Offset of drawing origin
        c.save()
        c.translate(M+(W-2*M)/GX*x, H-M-(H-2*M)/GY*(y+1))
        g = f[f.info.glyphSet[glyphIndex]]
        c.drawPath(g.path, (0, 0), s)
        glyphIndex += 1
        c.restore()

c.saveImage(EXPORT_PATH)

