#!/usr/bin/env python
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Example written by Frederik Berlaen
#
#     Supporting usage of DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     testFSBaselineCalculation.py
#
import sys
from pagebot.contexts.platform import getContext
context = getContext()
if not context.isDrawBot:
    sys.exit('Example only runs on DrawBot.')
"""
b = context.b # Builder is DrawBot
spacer = b.FormattedString('a\n', lineHeight=1, fontSize=2)

t = spacer + b.FormattedString('Hello', font='Verdana', lineHeight=110, fontSize=100)

b.textBox(t, (10, 10, 500, 500))

b.stroke(0)
b.fill(None)
b.rect(10, 10, 300, 500)



spacer = b.FormattedString('a\nb', lineHeight=1, fontSize=2)

t = spacer + b.FormattedString('Hello', font='Verdana', lineHeight=110, fontSize=100)

b.textBox(t, (320, 10, 300, 500))

b.stroke(0)
b.fill(None)
b.rect(320, 10, 300, 500)

"""