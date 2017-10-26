for p in range(20):
    newPage(1000, 1000)
    for n in range(50):
        fill(random(), 0, random(), 0.5 +random()*0.2)
        ch = random()
        x = 20 + random()*800
        y = 20 + random()*800
        if ch < 0.2:
            oval(x, y, 80, 80 )
        elif ch < 0.4:
            rect(x, y, 80, 80 )
        else:
            fontSize(24)
            text('Hello world on %d,%d' % (x, y), (x, y))



saveImage('/Users/Petr/Desktop/OurNiceDrawing.gif')