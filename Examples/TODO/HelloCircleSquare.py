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
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     HelloCircleSquare.py
#
#     Example to run in plain Python.
#     Dependencies: pabebot, flat, fonttools.
#
#     xxyxyz.org/flat#tutorial
#
#     Run as cmd-line:
#     --> python HelloCircleSquare.py

import os

from random import random
from pagebot.contexts.flatcontext import FlatContext
context = FlatContext()
print('Context class is %s' % type(context).__name__)

from pagebot.fonttoolbox.objects.font import findFont

font = findFont('Amstelvar-Roman-VF')

TITLE = 'HelloCircleSquare'
EXPORT_PATH = '_export/%s.pdf' % TITLE

W = H = 500
PAGES = 3
RECTS = 150
R = 20 # Diameter of circle or square
M = 20 # Page margin

context.newDocument(w=W, h=H, title=TITLE, pageCount=3)

for p in range(PAGES):
    context.newPage(W, H)
    for n in range(RECTS):
        # Compatible to DrawBot: color values between (0, 1)
        red, green, blue = random(), random(), random()
        #a = 0.5 + random()*0.5
        #context.fill((red, green, blue, a))
        context.fill((red, green, blue))
        ch = random()
        x = M + random()*(W-2*M-R) # Only in available space
        y = M + random()*(H-2*M-R)
        if ch < 0.2:
            context.oval(x, y, R, R)
        elif ch < 0.4:
            context.rect(x, y, R, R)
        else:
            # Make formatted Flat flavor BabelString instance.
            bs = context.newString('Hello world on %d,%d' % (x, y),
                                   style=dict(font=font,
                                              fontSize=10))
            context.text(bs, (x, y))

#context.saveImage('_export/HelloCircleSquare.gif')
# PDF does not support alpha colors.
#context.saveDocument('_export/HelloCircleSquare.pdf')
# Does not support alpha colors
#context.saveDocument('_export/HelloCircleSquare.jpg')
context.saveDocument(EXPORT_PATH)

os.system(u'open "%s"' % EXPORT_PATH)
print('Done')

