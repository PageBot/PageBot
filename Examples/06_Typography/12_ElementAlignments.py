#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     12_ElementALignments.py
#
#     Build a square page with a number of circle elements on top of each other.
#     ALl with the same proportion on the same position, where measures are derived
#     in a different way. If all alignments work, a single circle should be
#     visibile.

from pagebot.document import Document # Get the main Document class
from pagebot.toolbox.units import pt, inch
from pagebot.toolbox.color import color, noColor
from pagebot import getContext
from pagebot.constants import BASE_LINE_BG, BASE_Y_LEFT, BASE_INDEX_LEFT, CENTER, MIDDLE
from pagebot.elements import *
from pagebot.conditions import *

context = getContext() # Get the current context (e.g. DrawBotContext instance)

W = H = pt(500)

doc = Document(W=W, H=H, autoPages=2)

page = doc[1]
page.originTop = True
page.padding = pt(40)
page.originTop = True # Origin on top of bottom should make not difference
# Fitting by condition on the page padding
newCircle(parent=page, fill=noColor, stroke=color(rgb='green'), strokeWidth=pt(0.5), conditions=[Fit()]) 
# Fit (x, y) on middle of page.
newCircle(parent=page, x=page.w/2, y=page.h/2, r=page.pw/2, fill=noColor, stroke=color(rgb='red'), strokeWidth=pt(0.5)) 
# Fit with origin in (CENTER, MiDDLE)
newCircle(parent=page, xAlign=CENTER, yAlign=MIDDLE, x=page.w/2, y=page.h/2, r=page.pw/2, fill=noColor, stroke=color(rgb='orange'), strokeWidth=pt(0.5)) 
# Fit with origin in (CENTER, MiDDLE)
c = newCircle(parent=page, r=page.pw/2, fill=noColor, stroke=color(rgb='blue'), strokeWidth=pt(10.5)) 
c.left = page.pl
c.bottom = page.pb
page.solve()

doc.export('_export/ElemenAlignments.pdf')
