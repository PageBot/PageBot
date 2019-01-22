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
#     TextFlowWithContext.py
#
#     Calculate the overflowing text and add it to another column.
#
#     This example shows the most basic version, using only DrawBot functions.
#     The overflow text takes the same parameters for the Formatted String as the 
#     original text had.
#
from pagebot.contexts.drawbotcontext import DrawBotContext

context = DrawBotContext()

W = H = 500
PADDING = 30
CW = (W - 3*PADDING)/2
CH = H - 2*PADDING

context.newPage(W, H)

style = dict(font='Verdana', textFill=(1, 0, 0), fontSize=14, leading=16, firstLineIndent=20)
bs = context.newString('AAA '*300, style=style)

box = (PADDING, PADDING, CW, CH)
context.textBox(bs, box)
overflow = context.textOverflow(bs, box)
context.textBox(overflow, (PADDING + CW + PADDING, PADDING, CW, CH))