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
#     testFSFontMetrics.py
#
import sys
from pagebot import getContext
context = getContext()
if not context.isDrawBot:
    print('Example only runs on DrawBot.')
    sys.exit()

W, H = 1000, 500
newPage(W, H)
b = context.b # Builder is DrawBot

# Using global typographic settings in DrawBot by calling separate functions
txt = "Hellog World"
x, y = W/100, H/4

# set a font
b.font("Verdana")
# set a font size
b.fontSize(300)
# draw the text
b.text(txt, (x, y))

# calculate the size of the text
textWidth, textHeight = b.textSize(txt)

# set a red stroke color
b.stroke(1, 0, 0)
# loop over all font metrics
for metric in (0, b.fontDescender(), b.fontAscender(), b.fontXHeight(), b.fontCapHeight()):
    # draw a red line with the size of the drawn text
    b.line((x, y+metric), (x+textWidth, y+metric))

# Using context.newString, which creates a FsString, embedding DrawBot FormattedString
y += W/2

fs = context.newString(txt, style=dict(font='Verdana', fontSize=300))
