#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
from pagebot import getContext

c = getContext()

c.newPage(1000, 1000)
fs = c.newString("b", style=dict(lineHeight=74,
                                 font="Times",
                                 fontSize=38))
fs += c.newString("hello world ",
                  style=dict(font="Helvetica",
                             fontSize=10,
                             lineHeight=12))
fs += c.newString("hi agian " * 10)

r = (10, 10, 200, 200)
c.textBox(fs, r)

c.fill(None)
c.stroke(1, 0, 0)
c.rect(*r)

positions = c.textBoxBaseLines(fs, r)

s = 2
for x, y in positions:
    c.oval(x-s, y-s, s*2, s*2)
