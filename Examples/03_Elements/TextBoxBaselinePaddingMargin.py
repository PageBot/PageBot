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
#     TextBoxBaselinePaddingMargin.py
#
#     Show element padding and margin
#
from pagebot.document import Document
from pagebot.elements import newTextBox
from pagebot.toolbox.units import p, pt
from pagebot.toolbox.color import color
from pagebot.conditions import *
from pagebot.fonttoolbox.objects.font import findFont

W = H = 500
PADDING = p(2)
MARGIN = p(1)
BASELINE_GRID = pt(48)

font = findFont('PageBot-Regular')

doc = Document(w=W, h=H, originTop=False,
    baselineGrid=BASELINE_GRID)
view = doc.view
view.showPadding = True # Show padding and margin on page

page = doc[1] # Get the single page from te document.
page.margin = page.bleed = MARGIN
page.padding = PADDING
page.showBaselineGrid = True

# Condition alignment takes the element margin into account.
style = dict(font=font, fontSize=100, textFill=(1, 0, 0))
bs = doc.context.newString('Hkpx', style=style)
newTextBox(bs, parent=page, fill=color(0.7, 0.7, 0.7, 0.3), 
    w=300, h=300, showMargin=True, showPadding=True, 
    margin=MARGIN, padding=PADDING, showBaselineGrid=True,
    conditions=[Right2Right(), Top2Top(), BaselineDown2Grid()])

page.solve()

# Export in _export folder that does not commit in Git. 
# Force to export PDF.
EXPORT_PATH = '_export/TextBoxBaselinePaddingMargin.pdf'
doc.export(EXPORT_PATH)


