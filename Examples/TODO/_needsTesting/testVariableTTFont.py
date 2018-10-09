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
#     testVariableTTFont.py
#
from pagebot import getContext
from pagebot.document import Document
from pagebot.constants import A4
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.elements import newText
from pagebot.fonttoolbox.variablefontbuilder import getVarFontInstance

context = getContext()

f = findFont('Skia')

wghtMin, wghtDef, wghtMax = f.axes['wght']
wdthMin, wdthDef, wdthMax = f.axes['wdth']

#wghtMin, wghtDef, wghtMax = (-1, 0, 1)
#wdthMin, wdthDef, wdthMax = (-1, 0, 1)

print('wght %s %s %s' % (wghtMin, wghtDef, wghtMax))
print('wdth %s %s %s' % (wdthMin, wdthDef, wdthMax))


NORMAL = getVarFontInstance(f, dict(wght=wghtDef, wdth=wdthDef), styleName='Normal', normalize=False)
LIGHT = getVarFontInstance(f, dict(wght=wghtMin, wdth=wdthDef), styleName='Light', normalize=False)
BOLD = getVarFontInstance(f, dict(wght=wghtMax, wdth=wdthDef), styleName='Bold', normalize=False)
COND = getVarFontInstance(f, dict(wght=wghtDef, wdth=wdthMin), styleName='Cond', normalize=False)
WIDE = getVarFontInstance(f, dict(wght=wghtDef, wdth=wdthMax), styleName='Wide', normalize=False)

W, H = A4
doc = Document(w=W, h=H, autoPages=1)
page = doc[1]

bs = context.newString('Q', style=dict(fontSize=250, font=NORMAL.path, textFill=blackColor))
newText(bs, x=350, y=400, parent=page)
bs = context.newString('Q', style=dict(fontSize=250, font=LIGHT.path, textFill=blackColor))
newText(bs, x=50, y=400, parent=page)
bs = context.newString('Q', style=dict(fontSize=250, font=BOLD.path, textFill=blackColor))
newText(bs, x=650, y=400, parent=page)
bs = context.newString('Q', style=dict(fontSize=250, font=COND.path, textFill=blackColor))
newText(bs, x=350, y=700, parent=page)
bs = context.newString('Q', style=dict(fontSize=250, font=WIDE.path, textFill=blackColor))
newText(bs, x=350, y=100, parent=page)

doc.export('_export/TestVariableTTFont.pdf')

print('Done')
