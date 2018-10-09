#!/usr/bin/env python3
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
from random import random
from pagebot import getContext

context = getContext()

for p in range(20):
    context.newPage(1000, 1000)
    for n in range(50):
        context.fill((random(), 0, random(), 0.5 + random()*0.2))
        ch = random()
        x = 20 + random()*800
        y = 20 + random()*800
        if ch < 0.2:
            context.oval(x, y, 80, 80 )
        elif ch < 0.4:
            context.rect(x, y, 80, 80 )
        else:
            bs = context.newString('Hello world on %d,%d' % (x, y),
                             style=dict(fontSize=24))
            context.text(bs, (x, y))

context.saveImage('_export/HelloCircleSquare.pdf')
