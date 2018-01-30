#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#       from https://github.com/fonttools/fonttools/blob/master/Lib/fontTools/varLib/mutator.py
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
from pagebot.contexts import defaultContext as c

def appendS(fs1, fs2, w, baselineGrid):
    u"""Append fs2 to fs2, while keeping baseline grid locked.
    Assumed is that the top fs1 textBox is already on the baseline grid."""
    h = 1000
    box = 0, 0, w, h
    # Get the status of of the target string. We need to know the position of the last line.
    baselines = c.textBoxBaseLines(fs2, box)
    if baselines:
        print 1000-baselines[0][1], 1000-baselines[-1][1]
    return fs1


c.newPage(1000, 1000)

leading = 24
for n in range(0, 1000, leading):
    c.stroke(1, 0, 0)
    c.fill(None)
    c.line((0, n),(1000,n))
   
fs1 = c.newString('')   
fs2 = c.newString('aaa vvv bbbbbb\nss' * 5,
                  style=dict(fontSize=14,
                             lineHeight=24))
appendS(fs1, fs2, 300, 24)

bx, by, bw, bh = 50, 50, leading*3, 200#, leading*20
c.stroke(0)
c.fill(None)
c.rect(bx, by, bw, bh)

#FIXME: either use or delete the following codeblock:
"""
Y = 100
bx, by, bw, bh = box = (100, Y, 400, 500)
baselines = c.textBoxBaseLines(fs, box)
for x, y in baselines:
    c.stroke(0, 1, 0)
    c.fill(None)
    c.line((x-10, y), (400+10, y))
dy = round(baselines[0][1]/leading)*leading - baselines[0][1]
print dy
box2 = (bx,by+dy, 400, 500)
c.textBox(fs, box2)
c.rect(bx, by+dy, bw, bh)
"""
