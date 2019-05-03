#!/usr/bin/env python3
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
#     12_ElementAlignments.py
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

doc = Document(w=W, h=H, context=context)

view = doc.view
view.showPadding = True

page = doc[1]
page.padding = pt(30) # Make page area to fit the circles
page.originTop = False # Origin on top of bottom should make not difference
page.showOrigin = True
# Fitting by condition on page sides
newCircle(parent=page, fill=noColor, stroke=color(rgb='violet'), 
    strokeWidth=pt(4), conditions=[Fit2Sides()]) 
# Fitting by condition on the page padding
newCircle(parent=page, fill=noColor, stroke=color(rgb='blue'), 
    strokeWidth=pt(4), conditions=[Fit()]) 
# Fit (x, y) on middle of page.
newCircle(parent=page, r=page.pw/2-30, fill=noColor, 
    stroke=color(rgb='red'), strokeWidth=pt(4), 
    conditions=[Center2Center(), Middle2Middle()]) 
# Direct position with origin on bottom left
c = newCircle(parent=page, r=page.pw/2-60, fill=noColor, 
    stroke=color(rgb='orange'), strokeWidth=pt(4)) 
c.left = page.pl+60
c.bottom = page.pb+60
# Direct position with origin on (center, middle)
newCircle(parent=page, xAlign=CENTER, yAlign=MIDDLE,
    r=page.pw/2-90, stroke=noColor, x=page.w/2, y=page.h/2,
    fill=color(rgb='yellow'), strokeWidth=pt(4)) 

page.solve()

doc.export('_export/ElemenAlignments.pdf')
