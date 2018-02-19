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
#     testFormattedStringMarkers.py
#
import re
import sys
from pagebot.contexts import defaultContext as context
if not context.isDrawBot:
    sys.exit('Example only runs on DrawBot.')

from pagebot.style import getRootStyle
from pagebot.contexts import defaultContext as context

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
    stroke(0)
    strokeWidth(0.5)
    line((10, n*rs['leading']), (500, n*rs['leading']))

print textBox(a, (10, 10, 300, 800))
print textBox(fs, (320, 10, 300, 800))

