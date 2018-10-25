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
# -----------------------------------------------------------------------------
#
#     Contexts.py
#

import traceback
from random import random
from pagebot import getAllContexts, getResourcesPath
from pagebot.toolbox.color import Color
from pagebot.constants import A4Rounded

H, W = A4Rounded
f = Color(0, 1, 0)
s = Color(1, 0, 0)

def testContexts():
    for c in getAllContexts():
        testContext(c)

def getRandom():
    x = (W-100) * random()
    y = (H-100) * random()
    return x, y

def testContext(context):
    print(context)
    print(context.__dict__['b'])
    #for key, value in context.__dict__.items():
    #    print(' * %s: %s' % (key, value))

    try:
        context.frameDuration(1)
        context.newDrawing()
        context.newPage(w=W, h=H)
        context.fill(f)
        context.stroke(s)
        x, y = getRandom()
        context.rect(x, y, 100, 100)
        x, y = getRandom()
        context.oval(x, y, 100, 100)
        x, y = getRandom()
        context.circle(x, y, 100)
        bla = context.newString('BabelString No Style')
        x, y = getRandom()
        context.text(bla, (x, y))
        x, y = getRandom()
        context.text('plain string', (x, y))
        style = {'font': 'Helvetica', 'textFill': f}
        bla = context.newString('Babel String with Style', style=style)
        x, y = getRandom()
        context.text('bla2', (x, y))
        x, y = getRandom()
        context.text(bla, (x, y))
        x, y = getRandom()
        path = getResourcesPath() + "/images/cookbot1.jpg"
        context.image(path, (x, y), w=100, h=100)

        context.saveImage('_export/%s.pdf' % context.name)
    except Exception as e:
    	    print('!!! %s' % e)
    	    print(traceback.format_exc())

testContexts()
