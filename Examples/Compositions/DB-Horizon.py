LETTERS = 'ABCEFGHIJKLMNOPQTSTIVWXUZ'
from random import choice

Frames = 100

W = H = 500
IMAGE_PATH = '_export/HorizonWorld.gif'
if not 'BitcountMonoDouble-RegularCircle' in installedFonts():
    fontNames = ['Georgia-Bold', 'Georgia']
else:
    fontNames = []
    for fontName in installedFonts():
        if 'BitcountMono' in fontName and not 'Italic' in fontName:
            fontNames.append(fontName)
            
letters = []
for n in range(10):
    c = choice(LETTERS)
    x = 0    
    y = 15    
    z = 20+int(random()*500)

    x = 1/z + random()*100-100
    cc = random()*0.8+0.1, random()*0.1, random()*0.8*0.1
    f = choice(fontNames)
    letters.append((c, f, x, y, z, cc))
    
for n in range(Frames):
    newPage(W, H)
    fill(0.8)
    rect(0, 0, W, H)
    for c, f, x, y, z, (r, g, b) in letters:
        #y = y/z
        fill(r, g, b)
        font(f)
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
            y = W/2-2 - n*0.4
            lineThickness = (random()*3+0.5) * (H/2 - y)/10
            strokeWidth(lineThickness)
            line((0, y-lineThickness/2), (W, y-lineThickness/2))
    
saveImage(IMAGE_PATH)

