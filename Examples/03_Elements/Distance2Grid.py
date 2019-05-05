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
#     TextBoxSideWHConditions.py
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

W = H = pt(500)
PADDING = pt(4*12)
w = pt(8*12)

doc = Document(w=W, h=H, originTop=False)

page = doc[1] # Get the single page from te document.
page.padding = PADDING
page.baselineGrid = pt(24)
page.baselineGridStart = PADDING * 1.5
page.showBaselineGrid = True
page.showPadding = True
page.showOrigin = True

font = findFont('PageBot Regular')

def getText(s):
    style1 = dict(font=font, fontSize=36, leading=pt(40),
        textFill=whiteColor, xTextAlign=CENTER)
    style2 = dict(font=font, fontSize=10, leading=pt(12),
        textFill=blackColor, xTextAlign=CENTER)
    t = doc.context.newString('TEXT', style=style1)
    t += doc.context.newString('\n'+s, style=style2)
    return t
    
e1 = newTextBox(getText('e1 Bottom2Bottom'), 
    parent=page, fill=color('red'), 
    showOrigin=True, conditions=[Left2Left(), Bottom2Bottom()])
e2 = newTextBox(getText('e2 Middle2Middle'), 
    parent=page, fill=color('orange'), 
    showOrigin=True, conditions=[Left2Left(), Middle2Middle()])
e3 = newTextBox(getText('e3 Top2Top'), parent=page, 
    fill=color('yellow').darker(0.8), 
    showOrigin=True, conditions=[Left2Left(), Top2Top()])

e4 = newTextBox(getText('e4 Bottom y on grid'), 
    parent=page, fill=color('red'), 
    showOrigin=True, conditions=[Center2Center(), Bottom2Bottom()])
e5 = newTextBox(getText('e5 Bottom y on grid'), 
    parent=page, fill=color('orange'), 
    showOrigin=True, conditions=[Center2Center(), Middle2Middle()])
e6 = newTextBox(getText('e6 Bottom y on grid'), 
    parent=page, fill=color('yellow').darker(0.8), 
    showOrigin=True, conditions=[Center2Center(), Top2Top()])

e7 = newTextBox(getText('e7 Top y on grid'), 
    parent=page, fill=color('red'), yAlign=TOP,
    showOrigin=True, conditions=[Right2Right(), Bottom2Bottom()])
e8 = newTextBox(getText('e8 Top y on grid'), 
    parent=page, fill=color('orange'), yAlign=TOP,
    showOrigin=True, conditions=[Right2Right(), Middle2Middle()])
e9 = newTextBox(getText('e9 Top y on grid'), 
    parent=page, fill=color('yellow').darker(0.8), yAlign=TOP,
    showOrigin=True, conditions=[Right2Right(), Top2Top()])

page.solve()

e4.y += e4.distance2Grid
e5.y += e5.distance2Grid
e6.y += e6.distance2Grid

e7.y += e7.distance2Grid
e8.y += e8.distance2Grid
e9.y += e9.distance2Grid

page = page.next

page.padding = PADDING
page.baselineGrid = pt(24)
page.baselineGridStart = PADDING * 1.5
page.showBaselineGrid = True
page.showPadding = True
page.showOrigin = True

e1 = newTextBox(getText('Middle y on grid'), parent=page, 
    fill=color('red'), yAlign=MIDDLE, showOrigin=True, 
    conditions=[Left2Left(), Bottom2Bottom(), Baseline2Grid()])
e2 = newTextBox(getText('Middle y on grid'), parent=page, 
    fill=color('orange'), yAlign=MIDDLE, showOrigin=True, 
    conditions=[Left2Left(), Middle2Middle(), Baseline2Grid()])
e3 = newTextBox(getText('Middle y on grid'), parent=page, 
    fill=color('yellow').darker(0.8), yAlign=MIDDLE, showOrigin=True, 
    conditions=[Left2Left(), Top2Top(), Baseline2Grid()])

page.solve()

e1.y += e1.distance2Grid
e2.y += e2.distance2Grid
e3.y += e3.distance2Grid

page = page.next

page.padding = PADDING
page.baselineGrid = pt(24)
page.baselineGridStart = PADDING * 1.5
page.showBaselineGrid = True
page.showPadding = True
page.showOrigin = True

e1 = newTextBox(getText('Baseline2Grid'), parent=page, showBaselineGrid=True,
    fill=color('red'), yAlign=MIDDLE, showOrigin=True, 
    conditions=[Left2Left(), Bottom2Bottom(), Baseline2Grid()])
e2 = newTextBox(getText('Baseline2Grid'), parent=page, showBaselineGrid=True,
    fill=color('orange'), yAlign=MIDDLE, showOrigin=True, 
    conditions=[Left2Left(), Middle2Middle(), Baseline2Grid()])
e3 = newTextBox(getText('Baseline2Grid'), parent=page, showBaselineGrid=True, 
    fill=color('yellow').darker(0.8), yAlign=MIDDLE, showOrigin=True, 
    conditions=[Left2Left(), Top2Top(), Baseline2Grid()])

e4 = newTextBox(getText('BaselineUp2Grid'), parent=page, 
    fill=color('red'), showOrigin=True, 
    conditions=[Center2Center(), Bottom2Bottom(), BaselineUp2Grid()])
e5 = newTextBox(getText('BaselineUp2Grid'), parent=page, 
    fill=color('orange'), showOrigin=True, 
    conditions=[Center2Center(), Middle2Middle(), BaselineUp2Grid()])
e6 = newTextBox(getText('BaselineUp2Grid'), parent=page, 
    fill=color('yellow').darker(0.8), showOrigin=True, 
    conditions=[Center2Center(), Top2Top(), BaselineUp2Grid()])

e7 = newTextBox(getText('BaselineDown2Grid'), parent=page, 
    fill=color('red'), yAlign=TOP, showOrigin=True, 
    conditions=[Right2Right(), Bottom2Bottom(), BaselineDown2Grid()])
e8 = newTextBox(getText('BaselineDown2Grid'), parent=page, 
    fill=color('orange'), yAlign=TOP, showOrigin=True, 
    conditions=[Right2Right(), Middle2Middle(), BaselineDown2Grid()])
e9 = newTextBox(getText('BaselineDown2Grid'), parent=page, 
    fill=color('yellow').darker(0.8), yAlign=TOP, showOrigin=True, 
    conditions=[Right2Right(), Top2Top(), BaselineDown2Grid()])


page.solve()

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/Distance2Grid.pdf'
doc.export(EXPORT_PATH)


