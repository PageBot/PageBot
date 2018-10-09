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
# -----------------------------------------------------------------------------
#
#     testFontMetrics.py
#
import sys
from pagebot import getContext
context = getContext()
if not context.isDrawBot:
    print('Example only runs on DrawBot.')
    sys.exit()

from pagebot.fonttoolbox.fontpaths import getTestFontsPath
from pagebot.fonttoolbox.objects.font import findFont

f = findFont('Amstelvar-Roman-VF')
print('Family %s, style %s, em %d, ascender %d, descender: %d, capHeight %d, xHeight %d' % (
    f.info.familyName, f.info.styleName, f.info.unitsPerEm, f.info.ascender, f.info.descender,
    f.info.capHeight, f.info.xHeight))

spacer = context.newString('-----\n ', style=dict(lineHeight=1,
                                            font=f.path,
                                            fontSize=12))

# Create DrawBotString, inheriting from BabelString, based on view type.
bs = context.newString('Hlxg', style=dict(font=f.path,
                                    textFill=(1, 0, 0),
                                    fontSize=300,
                                    leading=320,
                                    baselineShift=200))

M = 20
context.fill(0.9)
context.rect(M, M, 1000-2*M, 800-2*M)

Y = 1000 - M
BASE = (f.info.ascender + f.info.descender + f.info.lineGap)/2
print('%s %s %s %s' % (f.info.familyName, f.info.styleName, 'Ascender + Descender + lineGap =', BASE))
YS = (BASE,)
print(YS)
for y in YS:
    context.stroke(0)
    context.strokeWidth(0.5)
    context.line((0, y), (1000, y))

context.fill(0)
context.stroke(None)
context.textBox(bs, (M, M, 1000-2*M, 400-2*M))
