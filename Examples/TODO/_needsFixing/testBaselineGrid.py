#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#       from https://github.com/fonttools/fonttools/blob/master/Lib/fontTools/varLib/mutator.py
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
from pagebot.contexts.drawbotcontext import DrawBotContext
from pagebot.contexts.flatcontext import FlatContext


def appendS(fs1, fs2, w, baselineGrid):
    """Append fs2 to fs2, while keeping baseline grid locked.
    Assumed is that the top fs1 textBox is already on the baseline grid."""
    h = 1000
    box = 0, 0, w, h
    # Get the status of of the target string. We need to know the position of the last line.
    baselines = context.textBoxBaseLines(fs2, box)
    if baselines:
        print(1000-baselines[0][1], 1000-baselines[-1][1])
    return fs1

testContexts = (
    (DrawBotContext(), '_export/testFlatString.pdf'),
    # TODO: Get this to work with Flat
    #(FlatContext(), '_export/testDrawBotString.pdf'),
)
for context, path in testContexts:

    context.newPage(1000, 1000)

    leading = 24
    for n in range(0, 1000, leading):
        context.stroke(1, 0, 0)
        context.fill(None)
        context.line((0, n),(1000,n))
   
    fs1 = context.newString('')   
    fs2 = context.newString('aaa vvv bbbbbb\nss' * 5,
                      style=dict(fontSize=14,
                                 lineHeight=24))
    appendS(fs1, fs2, 300, 24)

    bx, by, bw, bh = 50, 50, leading*3, 200#, leading*20
    context.stroke(0)
    context.fill(None)
    context.rect(bx, by, bw, bh)

    Y = 100
    bx, by, bw, bh = box = (100, Y, 400, 500)
    baselines = context.textBoxBaseLines(fs, box)
    for x, y in baselines:
        context.stroke(0, 1, 0)
        context.fill(None)
        context.line((x-10, y), (400+10, y))
    dy = round(baselines[0][1]/leading)*leading - baselines[0][1]
    print(dy)
    box2 = (bx,by+dy, 400, 500)
    context.textBox(fs, box2)
    context.rect(bx, by+dy, bw, bh)
    context.saveImage(path)
