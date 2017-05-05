
from __future__ import division

W = H = 600
def drawSquare(px, py, w):
    if w < 1:
        return
    for x in range(3):
        for y in range(3):
            if x == 1 and y == 1:
                fill(max(0, 0.75-w/100))
                stroke(None)
                rect(px+w, py+w, w, w)
            #elif x != y:
            #    continue
            elif px <= W and py <= H:
                drawSquare(px+x*w, py+y*w, w/3)

minW = w = 600
maxW = 1800
step = 22
while w < maxW:
    newPage(W, H)                
    drawSquare(0, 0, w)    
    w += step
    step *= 1.048
saveImage('_export/SierpinskiSquare.gif')