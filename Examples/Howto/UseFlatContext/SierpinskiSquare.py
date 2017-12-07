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
#     SierpinskySquare.py

# by Petr van Blokland @petrvanblokland
# https://twitter.com/petrvanblokland/status/860610270410018817
#
#     Run as cmd-line:
#     --> python SierpinskiSquare.py 

from random import random
from pagebot.contexts import defaultContext as context

W = H = 500

def drawSierpinskiSquare(px, py, w, maxW):
    if w < 1:
        return
    for x in range(3):
        for y in range(3):
            if x == 1 and y == 1:
                c = max(0, 0.5 - 0.5*w/W)
                context.fill((random(), c, c))
                #print x, y, w, 0.5*w/W
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
    context.saveDocument("_export/SierpinskiSquare."+extension)
print 'Done'