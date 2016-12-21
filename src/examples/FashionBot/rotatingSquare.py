
s = 0.3
FRAMES = 200
W = H = 1000
RADIUS = 300*s
# ----------
font("Helvetica")
fontSize(24)
for frame in range(FRAMES):
    newPage(W*s,H*s)
    fill(1, 0, 0)
    #fill(random(), random()*0.7, random()*0.2, random()*0.3+0.1)
    angle = 4*frame*pi*2/FRAMES
    x = W*s/2 + sin(angle)*RADIUS # Horizontal position
    y = H*s/2 + cos(angle)*RADIUS # Horizontal position
    if random() < 0.1:
        oval(x, y, 110*s, 110*s)

    else:
        oval(x, y, 100*s, 100*s)
    fill(0)
    text("Hello %d students" % frame, (x+110*s/2, y+110*s/2))
        
saveImage('myRotatingDrawing.gif')