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
WBOX = 160

def drawClassHierarchy(obj):
    x = 100
    y = 100
    for c in list(obj.__mro__)[::-1]:
        drawClass(c, x, y)
        y += 100
    print('...')

def drawClass(c, x, y):
    color = Color(0.6, 1, 0.6)
    context.fill(color)
    context.rect(pt(x), pt(y), pt (WBOX), pt(HBOX))
    context.fill(blackColor)
    context.fontSize(pt(20))
    context.text(c.__name__, (x+5, y+5))
    
context.newPage(pt(1000), pt(1000))
#size('A1')
    
classes = inspect.getmembers(sys.modules['pagebot.contexts.drawbotcontext'])

for name, obj in classes:
    if inspect.isclass(obj):
        drawClassHierarchy(obj)