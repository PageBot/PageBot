from pagebot.contexts import defaultContext as c

for p in range(10):
    c.newPage(1000, 1000)
    for n in range(50):
        c.fill((random(), 0, random(), 0.5 +random()*0.2))
        ch = random()
        x = 20 + random()*800
        y = 20 + random()*800
        if ch < 0.2:
            c.oval(x, y, 80, 80 )
        elif ch < 0.4:
            c.rect(x, y, 80, 80 )
        else:
            c.fontSize(24)
            c.text('Hello world on %d,%d' % (x, y), (x, y))



c.saveImage('_export/HelloCircleSquare.gif')