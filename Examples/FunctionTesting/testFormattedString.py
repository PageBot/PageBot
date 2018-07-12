#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     testFormattedString.py
#

from pagebot.contexts.platform import getContext

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

EXPORT_PATH = '_export/testFormattedStringBounds.pdf'
D = 2
W = H = 1000
newPage(W, H)
x = y = 60

for ix in range(3):
    for iy in range(4):
        bs = context.newString(TEXTS[(iy, ix)], style=dict(font='Georgia', fontSize=100))
        #Same as bx, by, bw, bh = pixelBounds(bs.s)
        bx, by, bw, bh = bs.bounds()
        xx, yy = x+ix*W/3, y+iy*H/4
        context.text(bs, (xx, yy))
        context.stroke((1, 0, 0), 0.5)
        context.fill(None)
        rect(xx+bx, yy+by, bw, bh)
        rect(xx-D, yy-D, 2*D, 2*D)

saveImage(EXPORT_PATH)
