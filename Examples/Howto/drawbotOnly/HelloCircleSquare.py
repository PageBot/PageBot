
import sys
from pagebot.contexts import defaultContext as context
if not context.isDrawBot:
    sys.exit('Example only runs on DrawBot.')

for p in range(10):
    context.newPage(1000, 1000)
    for n in range(50):
        context.fill((random(), 0, random(), 0.5 +random()*0.2))
        ch = random()
        x = 20 + random()*800
        y = 20 + random()*800
        if ch < 0.2:
            context.oval(x, y, 80, 80 )
        elif ch < 0.4:
            context.rect(x, y, 80, 80 )
        else:
            context.fontSize(24)
            context.text('Hello world on %d,%d' % (x, y), (x, y))



context.saveImage('_export/HelloCircleSquare.gif')