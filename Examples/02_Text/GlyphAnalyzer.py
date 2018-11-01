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
#     UseGlyphAnalyzer.py
#
#     Implements a PageBot font classes to get info from a TTFont.
#     Show the values that the GlyphAnalyzer get derive from font and glyph outline.
#   
from pagebot.fonttoolbox.objects.font import findFont
from pagebot import getContext

GLYPH_NAME = 'B'

context = getContext()
font = findFont('Georgia')
print(font.analyzer) 
print(font.analyzer.name) 
glyph = font[GLYPH_NAME]
ga = glyph.analyzer
print(ga)
print('Glyph horizontals width:', ga.width, ga.glyph.width, glyph.width)
print('Glyph bounding box:', ga.boundingBox)
# X position of vertical lines also includes sides of serifs.
print('x-position of verticals:', sorted(ga.verticals.keys()))
# Y position of horizontal lines
print('y-position of horizontals:', sorted(ga.horizontals.keys()))

