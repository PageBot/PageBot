# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
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

# by Petr van Blokland @petrvanblokland
# https://twitter.com/petrvanblokland/status/860610270410018817

import sys
from pagebot.contexts.platform import getContext
from pagebot.toolbox.units import *
from pagebot.toolbox.color import Color

context = getContext()

if not context.isDrawBot:
    print('Example only runs on DrawBot.')
    sys.exit()
    
MAX_I = 5

def drawSierpinskiSquare(px, py, w, maxW, i):
    if i >= MAX_I:
        return

    i += 1
        
    if w < 1:
        return
        
    for x in range(3):
        for y in range(3):
            if x == 1 and y == 1:
                col = Color(max(0, 0.75 - w/100))
                context.fill(col)
                context.rect(pt(px+w), pt(py+w), pt(w), pt(w))
            elif px <= maxW and py <= maxW:
                drawSierpinskiSquare(px+x*w, py+y*w, w/3, maxW, i)

if __name__ == '__main__':
    canvasSize = 500
    numFrames = 40
    factor = 3 ** (1/numFrames)

    for frame in range(numFrames):
        context.newPage(pt(canvasSize), pt(canvasSize))
        context.frameDuration(1/20)
        col = Color(1)
        context.fill(col)
        context.rect(pt(0), pt(0), pt(canvasSize), pt(canvasSize))
        w = canvasSize * factor ** frame
        #print(w)
        #print(canvasSize)
        i = 0
        drawSierpinskiSquare(0, 0, w, canvasSize, i)

    #DrawBotContext can save as animated gif
    context.saveDocument("_export/SierpinskiSquare.gif")
    print('Done')
