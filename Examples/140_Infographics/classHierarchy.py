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
    previous = None
    
    for c in list(obj.__mro__)[::-1]:
        current = c.__name__
        drawClass(current, x, y)
        
        if previous is not None:
            drawConnection(current, previous)
        previous = current
        y += 100

def drawConnection(current, previous):
    
    pos0 = drawnclasses[current]
    p0x, p0y = pos0
    pos1 = drawnclasses[previous]
    p1x, p1y = pos1
    context.stroke(blackColor)
    context.line((p0x + WBOX / 2, p0y), (p1x + WBOX / 2, p1y + HBOX))

def drawClass(name, x, y):
    if name in drawnclasses:
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
    context.stroke(None)
    color = Color(0.6, 1, 0.6)
    context.fill(color)
    context.rect(pt(boxx), pt(boxy), pt (WBOX), pt(HBOX))
    context.fill(blackColor)
    context.text(name, (pt(textx), pt(texty)))
    drawnclasses[name] = pos
    positions.append(pos)
    
context.newPage(pt(1000), pt(1000))
#size('A1')
    
classes = inspect.getmembers(sys.modules['pagebot.contexts.drawbotcontext'])

for name, obj in classes:
    if inspect.isclass(obj):
        drawClassHierarchy(obj)