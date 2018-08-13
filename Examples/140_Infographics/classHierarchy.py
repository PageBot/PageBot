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
#     classHierarchy.py
#

import sys, inspect
import pagebot.contexts.drawbotcontext
from pagebot.contexts.platform import getContext
from pagebot.toolbox.units import *
from pagebot.toolbox.color import Color, blackColor

context = getContext()

HBOX = 30
WBOX = 180
GAP = 20
P = 5
TEXTSIZE = pt(20)

drawnclasses = {}
positions = []

def drawClassHierarchy(obj):
    x = 100
    y = 100
    for c in list(obj.__mro__)[::-1]:
        drawClass(c, x, y)
        y += 100
    print('...')

def drawClass(c, x, y):
    key = c.__name__

    if key in drawnclasses:
        return
        
    pos = (x, y)
    
    while pos in positions:
        px, py = pos
        pos = (px + GAP + WBOX, py)
        
    context.fill(blackColor)
    context.fontSize(TEXTSIZE)

    boxx, boxy = pos
    textx = boxx + P
    texty = boxy + P
    color = Color(0.6, 1, 0.6)
    context.fill(color)
    context.rect(pt(boxx), pt(boxy), pt (WBOX), pt(HBOX))
    context.fill(blackColor)
    context.text(key, (pt(textx), pt(texty)))
    drawnclasses[key] = pos
    positions.append(pos)
    
context.newPage(pt(1000), pt(1000))
#size('A1')
    
classes = inspect.getmembers(sys.modules['pagebot.contexts.drawbotcontext'])

for name, obj in classes:
    if inspect.isclass(obj):
        drawClassHierarchy(obj)