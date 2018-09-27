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
#     TODO: make OO
#     TODO: graphics elements
#     TODO: element alignments

import sys, inspect
from pagebot import getContext
from pagebot.constants import A3
from pagebot.toolbox.units import *
from pagebot.toolbox.color import Color, blackColor, blueColor, greenColor

context = getContext()


X0 = 100
Y0 = 100

# Landscape A3.
HEIGHT, WIDTH = A3

HBOX = 50
WBOX = 180
GAP = 20
HGAP = 100
P = 15
TEXTSIZE = pt(14)
OFFSET = 9

def drawClassHierarchy(obj, colorRange, i):

    previous = None
    y = Y0
    x = X0

    for c in list(obj.__mro__)[::-1]:
        current = c.__name__
        if current == 'object':
            continue

        if i >= len(colorRange):
            i = 0

        drawClass(current, x, y, colorRange[i])

        if previous is not None:
            drawConnection(current, previous)

        previous = current
        y += HGAP
        i += 1
    return i

def drawConnection(current, previous):
    if sorted([current, previous]) in connections:
        return

    pos0 = drawnclasses[current]
    p0x, p0y = pos0
    pos1 = drawnclasses[previous]
    p1x, p1y = pos1
    context.stroke(blueColor)

    # Determines box entry / exit points.
    if p0y > p1y:
        #print('%s > %s' % (current, previous))
        p0x += WBOX / 2
        p1x += WBOX / 2
        p1y += HBOX
    elif p0y < p1y:
        # Never happens?
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

    # TODO: draw only once for any location.
    context.circle(p0x, p0y, 3)
    context.circle(p1x, p1y, 3)

    # Straight line.
    #context.line((p0x, p0y), (p1x, p1y))

    # Curve.

    path = context.newPath()
    context.moveTo((p0x, p0y))

    cp0x = p0x - OFFSET
    cp0y = p0y - (p0y - p1y) / 3
    context.stroke(greenColor)
    #context.fill(None)
    #context.circle(cp0x, cp0y, 3)

    cp1x = p1x + OFFSET
    cp1y = p1y + (p0y - p1y) / 3
    context.stroke(greenColor)
    #context.fill(None)
    #context.circle(cp1x, cp1y, 3)
    context.fill(None)
    context.stroke((1, 0, 1, 0.5))
    context.curveTo((cp0x, cp0y), (cp1x, cp1y), (p1x, p1y))
    drawPath(path)

    #cp1x = p1x
    #path.moveTo((p0x, p0y))
    connections.append(sorted([current, previous]))
    #print(connections)

def drawClass(name, x, y, color):
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
    #color = Color(0.6, 1, 0.6)
    context.fill(color)
    context.rect(pt(boxx), pt(boxy), pt (WBOX), pt(HBOX))
    context.fill(blackColor)
    context.text(name, (pt(textx), pt(texty)))
    drawnclasses[name] = pos
    positions.append(pos)

def getColorRange(l):
    colorRange = []
    for i in range(l):
        v = i * 1.0 / l
        c = Color(0.7, 0.7, v)
        colorRange.append(c)
    return colorRange

def drawClasses(inspected):
    classes = []

    for _, obj in inspected:
        if inspect.isclass(obj):
            classes.append(obj)

    l = len(classes)
    colorRange = getColorRange(l)

    i = 0

    for o in classes:
        i = drawClassHierarchy(o, colorRange, i)

#size('A1')

def title(name):
    context.fill(0)
    context.stroke(None)
    context.fontSize(42)
    context.text(name, (100, HEIGHT - 100))

import pagebot.contexts.drawbotcontext
import pagebot.contexts.flatcontext

context.newPage(WIDTH, HEIGHT)
title('PageBot Contexts')

connections = []
drawnclasses = {}
positions = []
classes = []
classes.extend(inspect.getmembers(sys.modules['pagebot.contexts.drawbotcontext']))
classes.extend(inspect.getmembers(sys.modules['pagebot.contexts.flatcontext']))
drawClasses(classes)

context.newPage(WIDTH, HEIGHT)
title('PageBot Units')

connections = []
drawnclasses = {}
positions = []
classes = []
classes.extend(inspect.getmembers(sys.modules['pagebot.toolbox.units']))
drawClasses(classes)

from pagebot.document import *
from pagebot.elements import *
from pagebot.elements.views import *

context.newPage(WIDTH, HEIGHT)
title('PageBot Elements')

connections = []
drawnclasses = {}
positions = []
classes = []
classes.extend(inspect.getmembers(sys.modules['pagebot.elements']))
classes.extend(inspect.getmembers(sys.modules['pagebot.elements.views']))
classes.extend(inspect.getmembers(sys.modules['pagebot.document']))
drawClasses(classes)
