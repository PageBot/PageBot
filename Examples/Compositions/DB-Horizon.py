# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     Horizon.py
#
from random import choice
from pagebot.contexts import defaultContect as context

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
    context.newPage(W, H)
    context.fill(0.8)
    context.rect(0, 0, W, H)
    for c, f, x, y, z, (r, g, b) in letters:
        #y = y/z
        bs = context.newString(c, style=dict(font=f, fontSize=fSize, textFill=(r, g, b)))
        context.text(bs, (x+250, y+250-fSize/2))

        context.fill(None)
        context.stroke(0.5, 0.5)
        context.line((0, 250), (500, 250))
    
        context.fill(1, 1, 1, 0.4)
        context.rect(0, 0, W, H/2-1)
    
        for n in range(0, 500, 10):
            context.fill(None)
            y = W/2-2 - n*0.4
            lineThickness = (random()*3+0.5) * (H/2 - y)/10
            context.stroke(1, lineThickness)
            stroke.line((0, y-lineThickness/2), (W, y-lineThickness/2))
    
context.saveImage(IMAGE_PATH)

