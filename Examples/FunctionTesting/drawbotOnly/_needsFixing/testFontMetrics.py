#!/usr/bin/env python
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     testFontMetrics.py
#
import sys
from pagebot.contexts import defaultContext as context
if not context.isDrawBot:
    sys.exit('Example only runs on DrawBot.')

from pagebot.contexts.platform import getRootFontPath
from pagebot.fonttoolbox.objects.font import Font

fontPath = getRootFontPath() + "fontbureau/AmstelvarAlpha-VF.ttf"
f = Font(fontPath)
print('Family %s, style %s, em %d, ascender %d, descender: %d, capHeight %d, xHeight %d' % (
    f.info.familyName, f.info.styleName, f.info.unitsPerEm, f.info.ascender, f.info.descender, 
    f.info.capHeight, f.info.xHeight))
    
spacer = context.newString('-----\n ', style=dict(lineHeight=1,
                                            font=f.installedName,
                                            fontSize=12))

# Create DrawBotString, inheriting from BabelString, based on view type.
bs = context.newString('Hlxg', style=dict(font=f.installedName,
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
print YS
for y in YS:
    context.stroke(0)
    context.strokeWidth(0.5)
    context.line((0, y), (1000, y))

context.fill(0)
context.stroke(None)
context.textBox(bs, (M, M, 1000-2*M, 400-2*M))
