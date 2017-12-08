#!/usr/bin/env python
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
#     drawSpirals.py
#
from __future__ import division # Make integer division result in float.
#import pagebot # Import to know the path of non-Python resources.
W = H = 1000
X = 0
Y = 0
N = 12*8
Sx = 10
Sy = 10
Ex = 10
Ey = 10
D = 1
M = 20
w = W - 2*M
h = H - 2*H

def drawSpiral():
    mx = W/2+X
    my = H/2+Y
    runs = False
    path = BezierPath()
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
            path.moveTo((mx, my))
        else:
            path.curveTo((mx-dx1*Exy, my-dy1), (mx-dx1, my-dy1*Exy), (mx-dx1, my))
            path.curveTo((mx-dx2, my+dy2*Exy), (mx-dx2*Exy, my+dy2), (mx, my+dy2))
            path.curveTo((mx+dx3*Exy, my+dy3), (mx+dx3, my+dy3*Exy), (mx+dx3, my))
            path.curveTo((mx+dx4, my-dy4*Exy), (mx+dx4*Exy, my-dy4), (mx, my-dy4))
        runs = True
    # close the path
    fill(None)
    stroke(0)
    strokeWidth(2)
    drawPath(path)

#dict(name='ElementOrigin', ui='CheckBox', args=dict(value=False)),
Variable([dict(name='X', ui='Slider',
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
         ],
         globals())

drawSpiral()
