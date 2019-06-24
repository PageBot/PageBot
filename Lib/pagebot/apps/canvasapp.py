# -*- coding: UTF-8 -*-
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
#     canvasapp.py
#
from vanilla import Window
from pagebot.apps.baseapp import BaseApp
from pagebot import getContext
from pagebot.toolbox.units import pt
from pagebot.toolbox.color import blueColor, blackColor, color, noColor 

W = H = 1000
M = 20
X = 0
Y = 0
N = 8*8
Sx = 10
Sy = 10
Exy = 0.58
D = 0.5

class CanvasApp(BaseApp):
    """Wrapper class to bundle all document page typesetter and composition
    functions, generating export document."""

    def __init__(self):
        """
        Connects main window and output window for errors.
        """
        super(CanvasApp, self).__init__()
        self.window = Window((800, 600), minSize=(1, 1), closable=True)
        self.context = getContext('Canvas')
        self.window.open()
        self.run()

    def run(self):
        self.window.page = self.context.newPage(1000, 800)
        self.context.stroke(None)
        self.context.fill(blueColor)
        self.context.rect(100, 100, 100, 100)
        self.context.fill(color('red'))
        self.context.oval(200, 100, 100, 100)
        self.drawSpiral()
        self.context.update()

    def drawSpiral(self):
        c = self.context
        mx = W/2+X
        my = H/2+Y
        runs = False
        c.fill(noColor)
        c.strokeWidth(0.5)
        c.stroke(blackColor)

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

if __file__ == '__main__':
    app = CanvasApp()
