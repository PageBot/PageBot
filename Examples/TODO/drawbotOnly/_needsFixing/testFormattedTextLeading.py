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
#     testFormattedStringMarkers.py
#
import re
import sys
from pagebot import getContext
context = getContext()
if not context.isDrawBot:
    print('Example only runs on DrawBot.')
    sys.exit()

from pagebot.style import getRootStyle

rs = {} # Make a style
rs['leading'] = 10
rs['fontSize'] = 9
rs['font'] = 'Verdana'
fs = context.newString('aaa', style=rs)

a = context.newString('',
                      style=dict(lineHeight=rs['leading'],
                                 fontSize=rs['fontSize'],
                                 font='Verdana'))
for n in range(100):
    a += 'AAA%s\n' % n
    fs += 'RS%s\n' % n
    fs += context.newString('SSSS', style=dict(fontSize=18, lineHeight=20))
    fs += context.newString('DDDD\n', style=dict(fontSize=9, lineHeight=10))
    context.stroke(0)
    context.strokeWidth(0.5)
    context.line((10, n*rs['leading']), (500, n*rs['leading']))

print(context.textBox(a, (10, 10, 300, 800)))
print(context.textBox(fs, (320, 10, 300, 800)))

