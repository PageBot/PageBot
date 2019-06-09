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
from pagebot.contexts.strings.babelstring import BabelString
from pagebot import getContext
from pagebot.toolbox.units import pt

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
    if context is None:
        print('Context is None')
        return
    print('Context', context)
    print('Context builder', context.b)
    #for key, value in context.__dict__.items():
    #    print(' * %s: %s' % (key, value))

    try:
        context.frameDuration(1)
        context.newDrawing()
        context.newPage(w=W, h=H)
        context.fill(f)
        context.stroke(s)
        x, y = getRandom()
        context.rect(x, y, pt(100), pt(100))
        x, y = getRandom()
        context.oval(x, y, pt(100), pt(100))
        x, y = getRandom()
        context.circle(x, y, pt(100))
        bla = context.newString('BabelString No Style')
        print('String is BabelString', isinstance(bla, BabelString))
        x, y = getRandom()
        context.text(bla, pt(x, y))
        x, y = getRandom()
        context.text('plain string', pt(x, y))
        style = {'font': 'Helvetica', 'textFill': f}
        bla = context.newString('Babel String with Style', style=style)
        x, y = getRandom()
        context.text('bla2', pt(x, y))
        x, y = getRandom()
        context.text(bla, pt(x, y))
        x, y = getRandom()
        path = getResourcesPath() + "/images/cookbot1.jpg"
        context.image(path, p=pt(x, y), w=pt(100), h=pt(100))
        # TODO:
        # - test Bézier path
        # - test glyph path
        # ...
        context.saveImage('_export/%s.pdf' % context.name)
    except Exception as e:
    	    print('Context errors', traceback.format_exc())
def showContexts():
	print('Here are some examples of how to retrieve different kinds of contexts:')
	context = getContext() # Creates a DrawBot context on Mac, Flat on others
	print('Context on Mac', context)
	context = getContext() # Still DrawBot, takes the buffered DEFAULT_CONTEXT.
	print('DrawBot context?', context)
	context = getContext('DrawBot') # Still DrawBot, takes the buffered DEFAULT_CONTEXT.
	print('DrawBot context?', context)
	context = getContext(contextType='Flat') # Force Flat.
	print('Flat context?', context)
	context = getContext(contextType='Flat') # Buffered in DEFAULT_CONTEXT this time.
	print('Flat context?', context)
	context = getContext(contextType='HTML')
	print('HTML context?', context)
	context = getContext(contextType='InDesign') # To be implemented.
	print('InDesign context?', context)
	context = getContext(contextType='IDML') # To be implemented.
	print('IDML context?', context)
	#context = getContext(contextType='SVG') # To be implemented. # Missing valid valid import svgwrite
	#print(context)

showContexts()
testContexts()

