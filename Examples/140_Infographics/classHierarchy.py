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
from pagebot.toolbox.color import Color, blackColor, blueColor

context = getContext()

X0 = 100
Y0 = 100
WIDTH = 1190
HEIGHT = 842
HBOX = 50
WBOX = 180
GAP = 20
HGAP = 100
P = 15
TEXTSIZE = pt(14)

def drawClassHierarchy(obj):
    previous = None
    y = Y0
    x = X0
    
    for c in list(obj.__mro__)[::-1]:
        current = c.__name__
        drawClass(current, x, y)
        
        if previous is not None:
            drawConnection(current, previous)
        previous = current
        y += HGAP

def drawConnection(current, previous):
    # TODO: as Bézier curves.
    pos0 = drawnclasses[current]
    p0x, p0y = pos0
    pos1 = drawnclasses[previous]
    p1x, p1y = pos1
    context.stroke(blueColor)
    
    if p0y > p1y:
        print('%s > %s' % (current, previous))

        p0x += WBOX / 2
        p1x += WBOX / 2
        p1y += HBOX
    elif p0y < p1y:

        p0x + WBOX / 2
        p1x + WBOX / 2
        p0y += HBOX
    elif p0y == p1y:
        p0y += HBOX / 2
        p1y += HBOX / 2
        if p1x > p0x:
            p0x += WBOX
        elif p1x < p0x:
            p1x += WBOX
        
    context.line((p0x, p0y), (p1x, p1y))

def drawClass(name, x, y):
    if name in drawnclasses:
        return
        
    pos = (x, y)
    
    while pos in positions:
        px, py = pos
        newx = px + GAP + WBOX
        if newx >= WIDTH - WBOX - GAP:
            newx = X0
            py += HGAP# / 2
        pos = (newx, py)
        
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

def drawClasses(classes):
    for name, obj in classes:
        if inspect.isclass(obj):
            drawClassHierarchy(obj)

#size('A1')
context.newPage(pt(WIDTH), pt(HEIGHT))
drawnclasses = {}
positions = []
classes = []    
classes.extend(inspect.getmembers(sys.modules['pagebot.fonttoolbox.objects.font']))
drawClasses(classes)

context.newPage(pt(WIDTH), pt(HEIGHT))
drawnclasses = {}
positions = []
classes = []    
classes.extend(inspect.getmembers(sys.modules['pagebot.contexts.drawbotcontext']))
drawClasses(classes)

context.newPage(pt(WIDTH), pt(HEIGHT))
drawnclasses = {}
positions = []
classes = []    
classes.extend(inspect.getmembers(sys.modules['pagebot.toolbox.units']))
drawClasses(classes)

context.newPage(pt(WIDTH), pt(HEIGHT))
drawnclasses = {}
positions = []
classes = []    
classes.extend(inspect.getmembers(sys.modules['pagebot.fonttoolbox.objects.glyph']))
drawClasses(classes)