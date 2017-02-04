LETTERS = 'ABCEFGHIJKLMNOPQTSTIVWXUZ'
size(500, 500)
for n in range(10):
    c = choice(LETTERS)
    x = 0    
    y = 10    
    z = 20+int(random()*1000)
    
    x = 1/z + random()*100-100
    #y = y/z
    fill(0.5, 0.5, 0.5, 0.5)
    stroke(None)
    fSize = 20000/z
    fontSize(fSize)
    text(c, (x+250, y+250-fSize/2))
    
    fill(None)
    stroke(0)
    line((0, 250), (500, 250))