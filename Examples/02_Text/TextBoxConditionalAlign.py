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
#     TextBoxConditionalAlign.py
#
#     If a TextBox as self.nextElement defined as name for another text box on the
#     same page, then overflow of self will go into the other text box.

from pagebot.contexts import getContext
from pagebot.constants import *
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.conditions import *
from pagebot.elements import *
from pagebot.document import Document
from pagebot.toolbox.color import color, noColor, blackColor
from pagebot.toolbox.units import pt

context = getContext()
P = 100 # Page padding and box size
G = 6 # Gutter
W = H = 6*P + 5*G

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/useTextBoxConditionalAlign.pdf'

font = findFont('Roboto-Regular')

# Create a new document, default to the defined page size.
doc = Document(w=W, h=H, padding=P+G, originTop=False)
c = doc.context

# Get list of pages with equal y, then equal x.
page = doc[1] # Get page on pageNumber, first in row (this is only one now).

style = dict(font=font, fontSize=pt(8), xTextAlign=CENTER)

bs = c.newString('Left2LeftSide\nTop2TopSide', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, padding=G, conditions=(Left2LeftSide(), Top2TopSide()))
bs = c.newString('Left2Left\nTop2Top', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, padding=G, conditions=(Left2Left(), Top2Top()))
bs = c.newString('Left2Left\nTop2TopSide', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, padding=G, conditions=(Left2Left(), Top2TopSide()))
bs = c.newString('Left2LeftSide\nTop2Top', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, padding=G, conditions=(Left2LeftSide(), Top2Top()))

bs = c.newString('Right2Right\nTop2Top', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, padding=G, conditions=(Right2Right(), Top2Top()))
bs = c.newString('Right2RightSide\nTop2Top', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, padding=G, conditions=(Right2RightSide(), Top2Top()))
bs = c.newString('Right2RightSide\nTop2TopSide', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, padding=G, conditions=(Right2RightSide(), Top2TopSide()))
bs = c.newString('Right2Right\nTop2TopSide', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, padding=G, conditions=(Right2Right(), Top2TopSide()))

bs = c.newString('Right2Right\nBottom2Bottom', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, mr=G/2, padding=G, conditions=(Right2Right(), Bottom2Bottom()))
bs = c.newString('Right2RightSide\nBottom2Bottom', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, padding=G, conditions=(Right2RightSide(), Bottom2Bottom()))
bs = c.newString('Right2RightSide\nBottom2BottomSide', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, padding=G, conditions=(Right2RightSide(), Bottom2BottomSide()))
bs = c.newString('Right2Right\nBottom2BottomSide', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, mr=G/2, padding=G, conditions=(Right2Right(), Bottom2BottomSide()))

bs = c.newString('Left2LeftSide\nBottom2BottomSide', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, padding=G, conditions=(Left2LeftSide(), Bottom2BottomSide()))
bs = c.newString('Left2Left\nBottom2Bottom', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, padding=G, conditions=(Left2Left(), Bottom2Bottom()))
bs = c.newString('Left2Left\nBottom2BottomSide', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, padding=G, conditions=(Left2Left(), Bottom2BottomSide()))
bs = c.newString('Left2LeftSide\nBottom2Bottom', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, padding=G, conditions=(Left2LeftSide(), Bottom2Bottom()))

# Centers

bs = c.newString('Right2Center\nTop2TopSide', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, mr=G/2, padding=G, conditions=(Right2Center(), Top2TopSide()))
bs = c.newString('Left2Center\nTop2TopSide', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, ml=G/2, padding=G, conditions=(Left2Center(), Top2TopSide()))
bs = c.newString('Right2Center\nTop2Top', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, mr=G/2, padding=G, conditions=(Right2Center(), Top2Top()))
bs = c.newString('Left2Center\nTop2Top', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, ml=G/2, padding=G, conditions=(Left2Center(), Top2Top()))


bs = c.newString('Right2Center\nBottom2BottomSide', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, mr=G/2, padding=G, conditions=(Right2Center(), Bottom2BottomSide()))
bs = c.newString('Left2Center\nBottom2BottomSide', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, ml=G/2, padding=G, conditions=(Left2Center(), Bottom2BottomSide()))
bs = c.newString('Right2Center\nBottom2Bottom', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, mr=G/2, padding=G, conditions=(Right2Center(), Bottom2Bottom()))
bs = c.newString('Left2Center\nBottom2Bottom', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, ml=G/2, padding=G, conditions=(Left2Center(), Bottom2Bottom()))

"""
bs = c.newString('Left2LeftSide\nBottom2Middle', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, mb=G, padding=G, conditions=(Left2LeftSide(), Bottom2Middle()))
bs = c.newString('Left2LeftSide\nTop2Middle', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, padding=G, conditions=(Left2LeftSide(), Top2Middle()))
bs = c.newString('Left2Left\nBottom2Middle', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, mb=G, padding=G, conditions=(Left2Left(), Bottom2Middle()))
bs = c.newString('Left2Left\nTop2Middle', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, padding=G, conditions=(Left2Left(), Top2Middle()))

bs = c.newString('Right2RightSide\nBottom2Middle', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, mb=G, padding=G, conditions=(Right2RightSide(), Bottom2Middle()))
bs = c.newString('Right2RightSide\nTop2Middle', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, padding=G, conditions=(Right2RightSide(), Top2Middle()))
bs = c.newString('Right2Right\nBottom2Middle', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, mb=G, padding=G, conditions=(Right2Right(), Bottom2Middle()))
bs = c.newString('Right2Right\nTop2Middle', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, padding=G, conditions=(Right2Right(), Top2Middle()))

# Middle 4
bs = c.newString('Right2Center\nBottom2Middle', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, mr=G/2, mb=G, padding=G, conditions=(Right2Center(), Bottom2Middle()))
bs = c.newString('Left2Center\nBottom2Middle', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, ml=G/2,mb=G, padding=G, conditions=(Left2Center(), Bottom2Middle()))
bs = c.newString('Right2Center\nTop2Middle', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, mr=G/2, padding=G, conditions=(Right2Center(), Top2Middle()))
bs = c.newString('Left2Center\nTop2Middle', style=style)
newTextBox(bs, parent=page, fill=0.8, stroke=0, w=P, h=P, ml=G/2, padding=G, conditions=(Left2Center(), Top2Middle()))
"""

page = page.next
page.showPadding = True

page.baselineGrid = pt(12)
page.baselineGridStart = page.pt
page.showBaselines = [BASE_LINE]
page.baselineColor = color(0, 1, 0)

style = dict(font=font, fontSize=pt(18), leading=18, textFill=0, fill=(1, 0, 0), xTextAlign=LEFT)

bs = c.newString('Aaaa\nBbbb\nCccc\nDddd', style=style)
tb = newTextBox(bs, parent=page, padding=G, fill=(1, 1, 0), w=page.pw, h=page.ph, 
    baselineWidth=pt(3), 
    baselineColor=color(1, 0, 0), 
    conditions=[Left2Left(), Baseline2Grid(index=2)])
tb.showBaselines = True
tb.baselineGrid=pt(28)

doc.solve()

doc.export(EXPORT_PATH)

