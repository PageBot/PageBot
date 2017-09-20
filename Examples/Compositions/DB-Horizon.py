from random import choice
from pagebot.builders import drawBotBuilder as b
if b is None:
    print 'Example runs only in DrawBot'.
else:
    LETTERS = 'ABCEFGHIJKLMNOPQTSTIVWXUZ'

    Frames = 100

    W = H = 500
    IMAGE_PATH = '_export/HorizonWorld.gif'
    if not 'BitcountMonoDouble-RegularCircle' in b.installedFonts():
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
        b.newPage(W, H)
        b.fill(0.8)
        b.rect(0, 0, W, H)
        for c, f, x, y, z, (r, g, b) in letters:
            #y = y/z
            b.fill(r, g, b)
            b.font(f)
            b.stroke(None)
            fSize = min(200, 40000/z)
            b.fontSize(fSize)
            b.text(c, (x+250, y+250-fSize/2))

            b.fill(None)
            b.strokeWidth(0.5)
            b.stroke(0.5)
            b.line((0, 250), (500, 250))
        
            b.fill(1, 1, 1, 0.4)
            b.rect(0, 0, W, H/2-1)
        
            for n in range(0, 500, 10):
                b.fill(None)
                b.stroke(1)
                y = W/2-2 - n*0.4
                lineThickness = (random()*3+0.5) * (H/2 - y)/10
                b.strokeWidth(lineThickness)
                b.line((0, y-lineThickness/2), (W, y-lineThickness/2))
        
    b.saveImage(IMAGE_PATH)

