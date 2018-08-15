#!/usr/bin/python
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
#     AnimatedGif.py
#
#     Run as cmd-line:
#     --> python AnimatedGif.py


from random import random
from pagebot.contexts.flatcontext import FlatContext

context = FlatContext()
print('Context class is %s' % type(context).__name__)

W = 400
H = 400

context.newDocument(w=W, h=H)

for n in range(1,50):
    context.newPage(W, H)
    context.fill(random(), random(), random())
    context.rect(random()*W, random()*H, 20, 20)

context.saveImage('test.gif')
