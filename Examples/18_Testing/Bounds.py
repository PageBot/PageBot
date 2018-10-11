#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
#     Bounds.py
#

from pagebot import getContext
from pagebot.toolbox.color import noColor, color
from pagebot.toolbox.units import pt

context = getContext()

TEXTS = {
    (0, 0): 'ABC',
    (1, 0): u'Ábc',
    (2, 0): 'hpx',
    (3, 0): 'Hyt',
    (0, 1): '(W)',
    (1, 1): u'“Page”',
    (2, 1): '[Bot]',
    (3, 1): u'Abç',
    (0, 2): u'ÅBÇ',
    (1, 2): '[Bot]',
    (2, 2): '$123',
    (3, 2): 'Abc',
}

EXPORT_PATH = '_export/testBounds.pdf'
D = 8 # Size of origin marker
W = H = pt(1000) # Size of export page.
context.newPage(W, H) # Make new DrawBot page.
x = y = pt(60) # Start of (x,y) matrix

for ix in range(3):
    for iy in range(4):
        # Formatted string
        word = TEXTS[(iy, ix)]
        bs = context.newString(word, style=dict(font='Georgia', fontSize=100))
        #Same as bx, by, bw, bh = pixelBounds(bs.s)
        bx, by, bw, bh = bs.bounds()
        xx, yy = x+ix*W/3, y+iy*H/4 # Calculate position in page layout.
        context.text(bs, (xx, yy))
        context.stroke(color(1, 0, 0), 0.5)
        context.fill(noColor) # Equivalent to DrawBot.fill(None)
        context.rect(xx+bx, yy+by, bw, bh)
        context.stroke(color(0, 0.5, 0.5), 0.5)
        context.fill(noColor) # Equivalent to DrawBot.fill(None)
        context.oval(xx-D, yy-D, 2*D, 2*D)
        context.line((xx-D, yy), (xx+D, yy))
        context.line((xx, yy-D), (xx, yy+D))

context.saveImage(EXPORT_PATH)
