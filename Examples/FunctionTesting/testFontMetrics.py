#!/usr/bin/env python

import sys
from pagebot.builders.drawbotbuilder import drawBotBuilder as b
if b is None:
	sys.exit('Example only runs in DrawBot')

from pagebot import getFontPath
from pagebot.fonttoolbox.objects.font import Font
from pagebot.elements.views.strings import newDrawBotString

fontPath = getFontPath() + "fontbureau/AmstelvarAlpha-VF.ttf"
f = Font(fontPath)
spacer = newDrawBotString('-----\n ', style=dict(lineHeight=1, font=f.installedName, fontSize=12))
b.fontSize(400)
# Create DrawBotString, inheriting from BabelString, based on view type.
fs = newDrawBotString('Hlxg', style=dict(font=f.installedName, textFill=(1, 0, 0),
    fontSize=300, leading=320, baselineShift=200))

M = 20
b.fill(0.9)
b.rect(M, M, 1000-2*M, 800-2*M)

Y = 1000 - M
BASE = f.info.ascender + f.info.descender + f.info.lineGap
print f.info.familyName, f.info.styleName, 'Ascender + Descender + lineGap =', BASE
YS = (BASE,)
for y in YS:
    b.stroke(0)
    b.strokeWidth(0.5)
    b.line((0, y), (1000, y))

b.fill(0)
b.stroke(None)
b.textBox(fs.s, (M, M, 1000-2*M, 400-2*M))

