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
#     ElementPaddingMargin.py
#
#     Shoe element padding and margin
#
from pagebot.document import Document
from pagebot.elements import newRect
from pagebot.toolbox.units import p, pt
from pagebot.toolbox.color import color
from pagebot.conditions import *

W = H = 500
PADDING = p(2)
MARGIN = p(1)

doc = Document(w=W, h=H, originTop=False)
view = doc.view
view.padding = p(4)
view.showCropMarks = True
view.showFrame = True
view.showPadding = True # Show padding and margin on page
view.showMargin = True

page = doc[1] # Get the single page from te document.
page.margin = page.bleed = MARGIN
page.padding = PADDING

# Add element without conditions. Hard positioning from bottom-left
newRect(parent=page, x=60, y=60, fill=color(0.7, 0.7, 0.7, 0.3), 
    w=150, h=200, showMargin=True, showPadding=True, 
    margin=MARGIN, padding=PADDING)

# Condition alignment takes the element margin into account.
newRect(parent=page, fill=color(0.7, 0.7, 0.7, 0.3), 
    w=150, h=200, showMargin=True, showPadding=True, 
    margin=MARGIN, padding=PADDING,
    conditions=[Right2Right(), Top2Top()])

page.solve()

# Export in _export folder that does not commit in Git. 
# Force to export PDF.
EXPORT_PATH = '_export/ElementPaddingMargin.pdf'
doc.export(EXPORT_PATH)


