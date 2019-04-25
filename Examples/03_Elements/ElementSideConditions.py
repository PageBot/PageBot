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
#     ElementSideConditions.py
#
#     Position elements by their page sides with conditions
#
# Document is the main instance holding all information about
# the document togethers (pages, styles, etc.)
from pagebot.document import Document
from pagebot.elements import newRect
from pagebot.toolbox.units import p, pt
from pagebot.toolbox.color import color
from pagebot.conditions import *

W = H = pt(500)
PADDING = w = p(10) # Make square will the page padding

doc = Document(w=W, h=H, originTop=False)
page = doc[1] # Get the single page from te document.
page.padding = PADDING

page.showPadding = True

newRect(parent=page, w=w, h=w, fill=color('red'), conditions=[Left2LeftSide(), Bottom2BottomSide()])
newRect(parent=page, w=w, h=w, fill=color('green'), conditions=[Center2Center(), Top2TopSide()])
newRect(parent=page, w=w, h=w, fill=color('blue'), conditions=[Right2RightSide(), Top2TopSide()])
newRect(parent=page, w=w, h=w, fill=color('orange'), conditions=[Left2LeftSide(), Middle2Middle()])
newRect(parent=page, w=w, h=w, fill=color('yellow'), conditions=[Left2LeftSide(), Top2TopSide()])
newRect(parent=page, w=w, h=w, fill=color('purple'), conditions=[Bottom2BottomSide(), Right2RightSide()])
newRect(parent=page, w=w, h=w, fill=color('violet'), conditions=[Right2RightSide(), Middle2Middle()])
newRect(parent=page, w=w, h=w, fill=color('cyan'), conditions=[Center2Center(), Bottom2BottomSide()])
newRect(parent=page, w=w, h=w, fill=color('black'), conditions=[Center2Center(), Middle2Middle()])

page.solve() # Solve conditions of the page child elements

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/ElementSideConditions.pdf'
doc.export(EXPORT_PATH)


