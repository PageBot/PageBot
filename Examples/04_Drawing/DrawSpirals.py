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
#     drawSpirals.py
#

from pagebot.toolbox.units import pt
from pagebot.toolbox.color import noColor, blackColor
from pagebot import getContext
c = getContext()
#import pagebot # Import to know the path of non-Python resources.

X = 0
Y = 0
N = 8*8
Sx = 10
Sy = 10
Exy = 0.58
D = 0.5

# hardcoded constants:
W = H = 1000
M = 20
w = W - 2*M
h = H - 2*H

#dict(name='ElementOrigin', ui='CheckBox', args=dict(value=False)),
c.Variable(
  [dict(name='X', ui='Slider',
        args=dict(minValue=-W/2, value=0, maxValue=W/2)),
   dict(name='Y', ui='Slider',
        args=dict(minValue=-H/2, value=0, maxValue=H/2)),
   dict(name='N', ui='Slider',
        args=dict(minValue=8*2, value=8*8, maxValue=8*32)),
   dict(name='Sx', ui='Slider',
        args=dict(minValue=2, value=10, maxValue=40)),
   dict(name='Sy', ui='Slider',
        args=dict(minValue=2, value=10, maxValue=40)),
   dict(name='Exy', ui='Slider',
        args=dict(minValue=0.01, value=0.58, maxValue=1)),
   dict(name='D', ui='Slider',
        args=dict(minValue=0.1, value=0.5, maxValue=5))
  ], globals())

def drawSpiral():
    mx = W/2+X
    my = H/2+Y
    runs = False
    c.newPath()
    c.moveTo((pt(mx), pt(my)))

    for n in range(0, int(N), 4):
        dx1 = n*Sx*D
        dy1 = n*Sy*D
        dx2 = (n+1)*Sx*D
        dy2 = (n+1)*Sy*D
        dx3 = (n+2)*Sx*D
        dy3 = (n+2)*Sy*D
        dx4 = (n+3)*Sx*D
        dy4 = (n+3)*Sy*D
        #dx5 = (n+4)*Sx*D
        #dy5 = (n+4)*Sy*D
        if not runs:
            c.moveTo((pt(mx), pt(my)))
        else:
            c.curveTo((pt(mx-dx1*Exy), pt(my-dy1)),
                (pt(mx-dx1), pt(my-dy1*Exy)), (pt(mx-dx1), pt(my)))
            c.curveTo((pt(mx-dx2), pt(my+dy2*Exy)),
            (pt(mx-dx2*Exy), pt(my+dy2)), (pt(mx), pt(my+dy2)))
            c.curveTo((pt(mx+dx3*Exy), pt(my+dy3)),
                (pt(mx+dx3), pt(my+dy3*Exy)), (pt(mx+dx3), pt(my)))
            c.curveTo((pt(mx+dx4), pt(my-dy4*Exy)), (pt(mx+dx4*Exy), pt(my-dy4)),
                (pt(mx), pt(my-dy4)))
        runs = True

    c.fill(noColor)
    c.stroke(blackColor)
    c.drawPath()

c.newPage(pt(W), pt(H))
drawSpiral()
c.saveImage("_export/Spiral.pdf")
