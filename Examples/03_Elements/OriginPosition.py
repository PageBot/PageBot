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
#     OriginPosition.py
#
# Document is the main instance holding all information about
# the document togethers (pages, styles, etc.)
from pagebot.document import Document
from pagebot.elements import newTextBox, newRect
from pagebot.toolbox.units import p
from pagebot.toolbox.color import color
from pagebot.conditions import *
from pagebot.constants import *

W = H = 500
PADDING = p(5)

doc = Document(w=W, h=H, padding=PADDING, originTop=False)
view = doc.view
view.padding = PADDING
view.showOrigin = True
view.showPadding = True
view.showFrame = True

page = doc[1] # Get the single page from te document.
print(page, 'Origin on top:', page.originTop) # Inherited from document
e = newRect(x=0, y=0, w=100, h=100, parent=page, fill=0.5)
print(e, 'yAlign', e.yAlign)

page = page.next
page.originTop = True # Force this page to have origin on top
print(page, 'Origin on top:', page.originTop)
# Auto aligns on top, yAlign initializing from page.originTop
e = newRect(x=0, y=0, w=100, h=100, parent=page, fill=0.5)
print(e, 'yAlign', e.yAlign)

#doc.originTop = True
page = page.next
print(page, 'Origin on top:', page.originTop) # Inherited from document
# Auto aligns on top, yAlign initializing from page.originTop
e = newRect(x=0, y=0, w=100, h=100, parent=page, fill=0.5)
print(e, 'yAlign', e.yAlign)

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/OriginPosition.pdf'
doc.export(EXPORT_PATH)


