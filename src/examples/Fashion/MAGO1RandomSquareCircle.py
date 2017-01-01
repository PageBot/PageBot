
s = 0.3
for frame in range(30):
    newPage(1000*s,1000*s)
    for n in range(50):
        fill(random(), random()*0.7, random()*0.2, random()*0.3+0.1)
        x = random()*800*s+50*s # Horizontal position
        y = random()*800*s+50*s # Vertical position
        if random() < 0.9:
            rect(x, y, 40*s, 40*s)
        else:
            oval(x, y, 40*s, 40*s)
        
saveImage('myDrawing.gif')