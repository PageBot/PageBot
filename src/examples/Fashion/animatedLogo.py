
speed = 12
f = 0
FRAMES = 40
W = H = 600
for frame in range(40):
    newPage(W, H)
    fill(0)
    rect(0, 0, W, H)
    f = f + speed
    if f > FRAMES/4:
        speed = -speed
    newPath()
    moveTo((250, 508))
    curveTo((-108, 612+f), (120, 120), (238, 476))
    lineTo((96, 200))
    lineTo((400, 200))
    closePath()
    fill(1, 0, 0)
    drawPath()
    print frame
    
saveImage('myLogo.gif')