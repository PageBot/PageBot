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
#     TextWidthTracking.py
#

from pagebot import getContext
from pagebot.toolbox.units import em
from pagebot.toolbox.color import blackColor


context = getContext()

W = 600
H = 400

HEAD_LINE = """When fonts started a new world"""

context.newPage(W, H)


w = 500
x = 20
y = 20

def textBounds(s, x, y, w):
    bs = context.newString(s, w=w,
                           style=dict(font='Georgia',
                                      tracking=em(0.02),
                                      textFill=blackColor))

    tw, th = bs.size
    bx, by, bw, bh = bs.bounds()
    context.text(bs, (x-bx, y-by))

    # Red rectangle shows context.textSize bounding box.
    # Green rectangle shows pixel bounds.
    # TODO: context.textSize should draw lower fitting ascender and descender.
    # Not start on baseline.
    context.fill(None)
    context.stroke((1, 0, 0), 0.5)
    context.rect(x, y, bw, bh)
    context.stroke((0, 0.5, 0), 0.5)
    context.rect(x, y, tw, th)

    return bs
    
y = 100
bs = textBounds(HEAD_LINE, x, y, w)
#print('%s %s %s' % (bs, bs.fittingFontSize, bs.bounds()))
y += 50
bs = textBounds('When fonts...', x, y, w)
#print('%s %s %s' % (bs, bs.fittingFontSize, bs.bounds()))
y += 80
bs = textBounds('Fonts...', x, y, w)
#print('%s %s %s' % (bs, bs.fittingFontSize, bs.bounds()))

