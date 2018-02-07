#!/usr/bin/env python
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
from random import random
from pagebot.contexts import defaultContext as c

for p in range(20):
    c.newPage(1000, 1000)
    for n in range(50):
        c.fill(random(), 0, random(), 0.5 + random()*0.2)
        ch = random()
        x = 20 + random()*800
        y = 20 + random()*800
        if ch < 0.2:
            c.oval(x, y, 80, 80 )
        elif ch < 0.4:
            c.rect(x, y, 80, 80 )
        else:
            fs = c.newString('Hello world on %d,%d' % (x, y),
                             style=dict(fontSize=24))
            c.text(fs, (x, y))

c.saveImage('_export/OurNiceDrawing.pdf')
