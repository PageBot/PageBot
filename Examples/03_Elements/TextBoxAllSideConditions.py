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
#     ElementConditionSides.py
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
fontSize = pt(30)

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
t2t = Top2TopSide()
b2b = Bottom2BottomSide()
l2l = Left2LeftSide()
r2r = Right2RightSide()
m2m = Middle2Middle()
c2c = Center2Center()

data = (
    ((l2l, t2t), (c2c, t2t), (r2r, t2t)),
    ((l2l, m2m), (c2c, m2m), (r2r, m2m)),
    ((l2l, b2b), (c2c, b2b), (r2r, b2b)),
) 

for ax in (LEFT, CENTER, RIGHT):
    for ay in (TOP, MIDDLE, BOTTOM):
        makePage(page, data, ax, ay) # Position for element origin at bottom
        page = page.next

c2l = Center2LeftSide()
m2t = Middle2TopSide()
m2b = Middle2BottomSide()
c2r = Center2RightSide()

data = (
    ((c2l, m2t), (c2c, m2t), (c2r, m2t)),
    ((c2l, m2m), (c2c, m2m), (c2r, m2m)),
    ((c2l, m2b), (c2c, m2b), (c2r, m2b)),
) 

for ax in (LEFT, CENTER, RIGHT):
    for ay in (TOP, MIDDLE, BOTTOM):
        makePage(page, data, ax, ay) # Position for element origin at bottom
        page = page.next

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/TextBoxALlSidesConditions.pdf'
doc.export(EXPORT_PATH)


