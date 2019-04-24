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
#     ElementPaddingPositions.py
#
#     Position elements by their sides
#
# Document is the main instance holding all information about
# the document togethers (pages, styles, etc.)
from pagebot.document import Document
from pagebot.elements import newRect
from pagebot.toolbox.units import p
from pagebot.toolbox.color import color
from pagebot.conditions import *

W = H = 500
PADDING = p(5)

doc = Document(w=W, h=H, originTop=False)
page = doc[1] # Get the single page from te document.
page.padding = PADDING

page.showPadding = True

e = newRect(parent=page, fill=color('red'))
e.left = page.pl
e.bottom = page.pb

e = newRect(parent=page, fill=color('green'))
e.top = page.h - page.pt
e.center = page.w/2

e = newRect(parent=page, fill=color('blue'))
e.top = page.h - page.pt
e.right = page.w - page.pr

e = newRect(parent=page, fill=color('orange'))
e.left = page.pl
e.middle = page.h/2

e = newRect(parent=page, fill=color('yellow'))
e.left = page.pl
e.top = page.h - page.pt

e = newRect(parent=page, fill=color('purple'))
e.bottom = page.pb
e.right = page.w - page.pr

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/ElementPaddingPositions.pdf'
doc.export(EXPORT_PATH)


