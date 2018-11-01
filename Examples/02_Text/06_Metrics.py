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
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     FormattedStringMetrics.py
#
#     It is possible to measure on the content of FormattedString instances.
#     These show examples how to do that.
#
from pagebot import getContext
from pagebot.toolbox.units import pt, em
from pagebot.toolbox.color import Color, color

context = getContext()

W, H = pt(2000, 400)

def run():
    w, h = pt(1000, 400) # Make a list of Unit pt instances and unpack them.
    context.newPage(W, H)
    txt = "Hello World"
    x, y = pt(10, 100) # Position of the text.

    # draw the text.
    bs = context.newString(txt, style=dict(fontSize=pt(300), font="Verdana"))
    context.text(bs, (x, y))

    # calculate the size of the text.
    textWidth, textHeight = bs.size

    # set a red stroke color
    strokeColor = color(1, 0, 0) # Color instance can translate into any other color type.
    context.stroke(strokeColor)

    # loop over all font metrics
    for metric in (0, bs.fontDescender, bs.fontAscender, bs.fontXHeight, bs.fontCapHeight):
        # Draw a red line with the size of the drawn text
        # Context drawing functions expect measures to be Unit instances.
        p1 = pt(x, y+metric) # Make a list of 2 Pt instances.
        p2 = pt(W-2*x, y+metric)
        context.line(p1, p2)

if __name__ == '__main__':
    run()
