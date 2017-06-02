LETTERS = 'ABCEFGHIJKLMNOPQTSTIVWXUZ'

W = H = 500
fontName = 'BitcountMonoDouble-RegularCircle'
if not fontName in installedFonts():
    fontName = 'Georgia-Bold'
size(W, H)
for n in range(10):
    c = choice(LETTERS)
    x = 0    
    y = 10    
    z = 20+int(random()*2000)
    
    x = 1/z + random()*100-100
    #y = y/z
    fill(0.1, 0.1, 0.1)
    font(fontName)
    stroke(None)
    fSize = min(200, 40000/z)
    fontSize(fSize)
    text(c, (x+250, y+250-fSize/2))
    
    fill(None)
    strokeWidth(0.5)
    stroke(0.5)
    line((0, 250), (500, 250))
    
fill(1, 1, 1, 0.4)
rect(0, 0, W, H/2-1)
    
for n in range(0, 500, 10):
    fill(None)
    stroke(1)
    strokeWidth(random()*3+0.5)
    y = W/2-2 - n*0.4
    line((0, y), (W, y))