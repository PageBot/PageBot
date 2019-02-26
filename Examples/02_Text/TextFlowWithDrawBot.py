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
#     TextFlowWithDrawBot.py
#
#     Calculate the overflowing text and add it to another column.
#
#     This example shows the most basic version, using only DrawBot functions.
#     The overflow text takes the same parameters for the Formatted String as the 
#     original text had.
#
W = H = 500
PADDING = 30
CW = (W - 3*PADDING)/2
CH = H - 2*PADDING

newPage(W, H)

fs = FormattedString('AAA '*300, font='Verdana', fill=(1, 0, 0), fontSize=14, lineHeight=16,
    firstLineIndent=20)

box = (PADDING, PADDING, CW, CH)
tb = textBox(fs, box)
overflow = textOverflow(fs, box)
print('Has overflow:', overflow)
textBox(overflow, (PADDING + CW + PADDING, PADDING, CW, CH))