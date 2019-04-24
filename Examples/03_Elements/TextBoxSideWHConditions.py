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
#     TextBoxSideWHConditions.py
#
#     Position fixed size textbox elements by their page side with conditions
#
# Document is the main instance holding all information about
# the document togethers (pages, styles, etc.)
from pagebot.document import Document
from pagebot.elements import newTextBox
from pagebot.toolbox.units import p, pt
from pagebot.toolbox.color import color, whiteColor
from pagebot.conditions import *
from pagebot.constants import *
from pagebot.fonttoolbox.objects.font import findFont

W = H = pt(500)
PADDING = p(4)
w = p(8)

doc = Document(w=W, h=H, originTop=False)
page = doc[1] # Get the single page from te document.
page.padding = PADDING

page.showPadding = True
font = findFont('PageBot Regular')

t = doc.context.newString('TEXT', style=dict(font=font, fontSize=36, textFill=whiteColor, xTextAlign=CENTER))
newTextBox(t, parent=page, w=w, h=w, fill=color('red'), conditions=[Left2Left(), Bottom2Bottom()])
newTextBox(t, parent=page, w=w, h=w, fill=color('green'), conditions=[Center2Center(), Top2Top()])
newTextBox(t, parent=page, w=w, h=w, fill=color('blue'), conditions=[Right2Right(), Top2Top()])
newTextBox(t, parent=page, w=w, h=w, fill=color('orange'), conditions=[Left2Left(), Middle2Middle()])
newTextBox(t, parent=page, w=w, h=w, fill=color('yellow').darker(0.8), conditions=[Left2Left(), Top2Top()])
newTextBox(t, parent=page, w=w, h=w, fill=color('purple'), conditions=[Bottom2Bottom(), Right2Right()])
newTextBox(t, parent=page, w=w, h=w, fill=color('violet'), conditions=[Middle2Middle(), Right2Right()])
newTextBox(t, parent=page, w=w, h=w, fill=color('cyan').darker(0.8), conditions=[Center2Center(), Bottom2Bottom()])
newTextBox(t, parent=page, w=w, h=w, fill=color('black'), conditions=[Center2Center(), Middle2Middle()])

page.solve()

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/TextBoxSideWHConditions.pdf'
doc.export(EXPORT_PATH)


