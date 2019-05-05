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
#     TextBoxAllBaselineConditions.py
#
#     Position fixed size textbox elements by their page side with conditions
#
# Document is the main instance holding all information about
# the document togethers (pages, styles, etc.)
from pagebot.document import Document
from pagebot.elements import newTextBox
from pagebot.toolbox.units import p, pt
from pagebot.toolbox.color import color, whiteColor, blackColor
from pagebot.conditions import *
from pagebot.constants import *
from pagebot.fonttoolbox.objects.font import findFont

BASELINE_GRID = 20
PAD = pt(30)
PADDING = PAD, PAD, PAD, PAD
NUM_LINES = 20
W = H = NUM_LINES * BASELINE_GRID + 2*PAD

doc = Document(w=W, h=H, originTop=False, baselineGrid=BASELINE_GRID, 
    padding=PADDING, baselineGridStart=PAD/2)
view = doc.view
view.showBaselineGrid = True
view.showPadding = True
view.showOrigin = True

page = doc[1] # Get the single page from the document.

font = findFont('PageBot-Regular')
fontSize = pt(40)

def getText(s):
    style = dict(font=font, fontSize=fontSize, leading=fontSize,
        textFill=whiteColor, xTextAlign=CENTER)
    tmp = doc.context.newString(s, style=style) # Hack, first one does not find the font.
    return doc.context.newString(s, style=style)

def makePage(page, data, xAlign, yAlign):
    for ix, col in enumerate(data):
        for iy, row in enumerate(col):
            name = 'Hkpx%d%d' % (ix, iy)
            c = [Shrink2TextBounds()] + list(row)
            bgColor = color(ix/3, 0, iy/3, 0.8)
            newTextBox(getText(name), conditions=c, 
                xAlign=xAlign, yAlign=yAlign,
                parent=page, fill=bgColor,
                showOrigin=True)
    page.solve()
    
# Make data tables more readable by prefabricated conditons.
bl2t = Baseline2Top()
bl2b = Baseline2Bottom()
m2m = Middle2Middle()
bl2g = Baseline2Grid()

l2l = Left2Left()
r2r = Right2Right()
c2c = Center2Center()

data = (
    ((l2l, bl2t),(c2c, bl2t),(r2r, bl2t)),
    ((l2l, m2m, bl2g),    (c2c, m2m, bl2g),  (r2r, m2m, bl2g)),
    #((l2l, bl2b),(c2c, bl2b),(r2r, bl2b)),
) 

for ax in (LEFT, CENTER, RIGHT):
    for ay in (TOP, MIDDLE, BOTTOM):
        makePage(page, data, ax, ay) # Position for element origin at bottom
        page = page.next

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/TextBoxALlBaselineConditions.pdf'
doc.export(EXPORT_PATH)


