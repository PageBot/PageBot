#!/usr/bin/env python3
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Example written by Frederik Berlaen
#
#     Supporting DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     testFSBaselineCalculation.py
#
import sys
from pagebot import getContext
context = getContext()
if not context.isDrawBot:
    print('Example only runs on DrawBot.')
    sys.exit()

b = context.b # Builder is DrawBot
b.size(200, 200)
t = "hello world "
fs = b.FormattedString(t, font="Times", fontSize=17, lineHeight=28)
fs.fontLineHeight()


b.font("Times")
b.lineHeight(28)
b.fontSize(17) 

b.text(fs, (10, 100))

r = (66, 0, 100, 100 + b.fontLineHeight()+b.fontDescender())

fs = b.FormattedString(t * 10, font="Times", fontSize=17, lineHeight=28)
fs.fontLineHeight()

b.textBox(fs, r)


b.stroke(0)

b.line((0, 100), (200, 100))

b.stroke(1, 0, 0)
b.fill(None)
b.rect(*r)
