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
#     TextBoxSideConditions2.py
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
font = findFont('PageBot Regular')

doc = Document(w=W, h=H, originTop=False)
t = doc.context.newString('TEXT', style=dict(font=font, fontSize=36, textFill=whiteColor, xTextAlign=CENTER))
PADDING = t.size[0]

page = doc[1] # Get the single page from te document.
page.padding = PADDING

page.showPadding = True

newTextBox(t, parent=page, fill=color('red'), conditions=[Right2Left(), Top2Bottom()])
newTextBox(t, parent=page, fill=color('green'), conditions=[Center2Center(), Bottom2Top()])
newTextBox(t, parent=page, fill=color('blue'), conditions=[Left2Right(), Bottom2Top()])
newTextBox(t, parent=page, fill=color('orange'), conditions=[Right2Left(), Middle2Middle()])
newTextBox(t, parent=page, fill=color('yellow').darker(0.8), conditions=[Right2Left(), Bottom2Top()])
newTextBox(t, parent=page, fill=color('purple'), conditions=[Left2Right(), Top2Bottom()])
newTextBox(t, parent=page, fill=color('violet'), conditions=[Left2Right(), Middle2Middle()])
newTextBox(t, parent=page, fill=color('cyan').darker(0.8), conditions=[Center2Center(), Top2Bottom()])
newTextBox(t, parent=page, fill=color('black'), conditions=[Center2Center(), Middle2Middle()])

page.solve()

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/TextBoxSideConditions2.pdf'
doc.export(EXPORT_PATH)


