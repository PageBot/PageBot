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
#     SierpinskiSquare.py
#
# by Petr van Blokland @petrvanblokland
# https://twitter.com/petrvanblokland/status/860610270410018817
#
#     Run as cmd-line:
#     --> python SierpinskiSquare.py

import os, os.path

from random import random
from pagebot.contexts.flatcontext import FlatContext

context = FlatContext()
print('Context class is %s' % type(context).__name__)
W = H = 500

def drawSierpinskiSquare(px, py, w, maxW):
    if w < 1:
        return
    for x in range(3):
        for y in range(3):
            if x == 1 and y == 1:
                c = max(0, 0.5 - 0.5*w/W)
                context.fill((random(), c, c))
                #print(x, y, w, 0.5*w/W)
                context.rect(px+w, py+w, w, w)
            elif px <= maxW and py <= maxW:
                drawSierpinskiSquare(px+x*w, py+y*w, w/3.0, maxW)


context.newDocument(w=W, h=H)
context.newPage(W, H)
context.fill((1, 1, 1))
context.rect(0, 0, W, H)
drawSierpinskiSquare(0, 0, W, W)

# TODO: Check on sensitivity of Flat for color types in relation to document types
# Gray scale does not work for .svg
# Opaque does not work for .pdf
# Context should hide that problem.
for extension in ('pdf', 'jpg'):
    if not os.path.exists('_export'):
        os.mkdir('_export')
    exportPath = "_export/SierpinskiSquare." + extension
    context.saveDocument(exportPath)
    os.system(u'open "%s"' % exportPath)

print(('Done'))

