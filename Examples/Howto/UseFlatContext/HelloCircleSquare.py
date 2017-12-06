# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     HelloCircleSquare.py
#
#     Example to run in plain Python.
#     Dependencies: pabebot, flat, fonttools.
#
#     http://xxyxyz.org/flat#tutorial
#
from random import random
from pagebot.contexts import defaultContext as context

W = H = 500
PAGES = 3
RECTS = 150
R = 20 # Diameter of circle or square
M = 20 # Page margin

context.newDocument(w=W, h=H)
for p in range(PAGES):
    context.newPage(W, H)
    for n in range(RECTS):
        # Compatible to DrawBot: color values between (0, 1)
        a = 0.5 +random()*0.5
        red, green, blue = random(), random(), random()
        context.fill((red, green, blue, a))
        ch = random()
        x = M + random()*(W-2*M-R) # Only in available space
        y = M + random()*(H-2*M-R)
        if ch < 0.2:
            context.oval(x, y, R, R )
        elif ch < 0.4:
            context.rect(x, y, R, R )
        else:
            # Make formatted Flat flavor BabelString instance.
            #bs = context.newString('Hello world on %d,%d' % (x, y), style=dict(font='Verdana', fontSize=24))
            #context.text(bs, (x, y))
            pass

#c.saveImage('_export/HelloCircleSquare.gif')
context.saveDocument('_export/HelloCircleSquare.png')