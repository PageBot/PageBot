
import sys
from pagebot import getContext
from pagebot.toolbox.units import *
from pagebot.toolbox.color import Color

context = getContext()

for p in range(10):
    context.newPage(pt(1000), pt(1000))
    for n in range(50):
        col = Color(random(), 0, random(), 0.5 +random()*0.2)
        context.fill(col)
        ch = random()
        x = 20 + random()*800
        y = 20 + random()*800
        

        if ch < 0.2:
            context.oval(pt(x), pt(y), pt(80), pt(80))
        elif ch < 0.4:
            context.rect(pt(x), pt(y), pt(80), pt(80))
        else:
            context.fontSize(pt(24))
            context.text('Hello world on %d,%d' % (x, y), (x, y))
            
context.saveImage('_export/HelloCircleSquare.gif')

