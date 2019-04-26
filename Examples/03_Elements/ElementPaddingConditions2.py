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
#     ElementConditions.py
#
#     Position elements by their page padding position with conditions
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
w = p(8)

doc = Document(w=W, h=H, originTop=False)
page = doc[1] # Get the single page from te document.
page.padding = PADDING

page.showPadding = True

# Position on the outside of the page padding
newRect(parent=page, w=w, h=w, fill=color('red'), conditions=[Right2Left(), Top2Bottom()])
newRect(parent=page, w=w, h=w, fill=color('green'), conditions=[Center2Center(), Bottom2Top()])
newRect(parent=page, w=w, h=w, fill=color('blue'), conditions=[Left2Right(), Bottom2Top()])
newRect(parent=page, w=w, h=w, fill=color('orange'), conditions=[Right2Left(), Middle2Middle()])
newRect(parent=page, w=w, h=w, fill=color('yellow'), conditions=[Right2Left(), Bottom2Top()])
newRect(parent=page, w=w, h=w, fill=color('purple'), conditions=[Top2Bottom(), Left2Right()])
newRect(parent=page, w=w, h=w, fill=color('violet'), conditions=[Middle2Middle(), Left2Right()])
newRect(parent=page, w=w, h=w, fill=color('cyan'), conditions=[Center2Center(), Top2Bottom()])
newRect(parent=page, w=w, h=w, fill=color('black'), conditions=[Center2Center(), Middle2Middle()])

page.solve()

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/ElementConditions.pdf'
doc.export(EXPORT_PATH)


