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
#     ElementBleedConditions.py
#
#     Position elements by their bleed sides with conditions
#
# Document is the main instance holding all information about
# the document togethers (pages, styles, etc.)
from pagebot.document import Document
from pagebot.elements import newRect
from pagebot.toolbox.units import p, pt
from pagebot.toolbox.color import color
from pagebot.conditions import *

W = H = pt(500)
PADDING = p(8)
BLEED = p(1)
w = PADDING + BLEED # Square fills bleed and padding

doc = Document(w=W, h=H, originTop=False)
doc.view.padding = p(6) # View padding around the page.

page = doc[1] # Get the single page from te document.
page.padding = PADDING

page.showPadding = True
page.showFrame = True
page.showCropMarks = True
page.bleed = BLEED

newRect(parent=page, w=w, h=w, fill=color('red'), conditions=[Left2LeftBleed(), Bottom2BottomBleed()])
newRect(parent=page, w=w, h=w, fill=color('green'), conditions=[Center2Center(), Top2TopBleed()])
newRect(parent=page, w=w, h=w, fill=color('blue'), conditions=[Right2RightBleed(), Top2TopBleed()])
newRect(parent=page, w=w, h=w, fill=color('orange'), conditions=[Left2LeftBleed(), Middle2Middle()])
newRect(parent=page, w=w, h=w, fill=color('yellow'), conditions=[Left2LeftBleed(), Top2TopBleed()])
newRect(parent=page, w=w, h=w, fill=color('purple'), conditions=[Bottom2BottomBleed(), Right2RightBleed()])
newRect(parent=page, w=w, h=w, fill=color('violet'), conditions=[Right2RightBleed(), Middle2Middle()])
newRect(parent=page, w=w, h=w, fill=color('cyan'), conditions=[Center2Center(), Bottom2BottomBleed()])
newRect(parent=page, w=w, h=w, fill=color('black'), conditions=[Center2Center(), Middle2Middle()])

page.solve()

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/ElementSideConditions.pdf'
doc.export(EXPORT_PATH)


