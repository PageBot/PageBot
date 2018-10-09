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
from pagebot import getAllContexts
from pagebot.toolbox.color import Color

W = 1000
H = 800
f = Color(0, 1, 0)
s = Color(1, 0, 0)

def testContexts():
    for c in getAllContexts():
        testContext(c)

def testContext(context):
    print(context)
    print(context.__dict__['b'])
    #for key, value in context.__dict__.items():
    #    print(' * %s: %s' % (key, value))

    try:
    	context.newDrawing()
    	context.newPage(w=W, h=H)
    	context.fill(f)
    	context.stroke(s)
    	context.rect(10, 10, 100, 100)
    	context.oval(10, 10, 100, 100)
    	context.circle(10, 10, 100)
    	bla = context.newString('bla')
    	context.text('bla1', (10, 10))
    	style = {'font': 'Helvetica'}
    	bla = context.newString('bla', style=style)
    	context.text('bla2', (10, 10))
    	context.text(bla, (10, 10))
    except Exception as e:
    	print(e)

testContexts()
