#
#    Typetr logo animation
#
bitcountNames = []
for fontName in installedFonts():
    if 'Bitcount' in fontName and not 'Italic' in fontName and not 'Prop' in fontName:
        bitcountNames.append(fontName)

FRAMES = 300
H = 100
W = 400

colors = [[1, 0.1, 0, 1], [0, 1, 1, 1], [0.2, 0.3, 1, 1], [0.2, 1, 0.1, 1]]
colorDirs = [10/FRAMES, -14/FRAMES, 18/FRAMES, 22/FRAMES]   
fontNames = [choice(bitcountNames), choice(bitcountNames), choice(bitcountNames), choice(bitcountNames)]

for frame in range(FRAMES):
    newPage(W, H)
    fill(1)
    #fill(48.0/255, 10.0/255, 181.0/255)
    rect(0, 0, W, H)
    for cIndex in range(len(colors)):
        colors[cIndex][cIndex] += colorDirs[cIndex]
        colors[cIndex][3] += colorDirs[cIndex]
        if colors[cIndex][cIndex] < 0.2:
            fontNames[cIndex] = choice(bitcountNames)
            colorDirs[cIndex] = -colorDirs[cIndex]
            colors[cIndex][cIndex] += colorDirs[cIndex]
            colors[cIndex][3] = 0.2
        elif colors[cIndex][cIndex] > 1:
            colors[cIndex][cIndex] -= colorDirs[cIndex]
            colors[cIndex][3] = 1
            colorDirs[cIndex] = -colorDirs[cIndex]
        

        offsetX = offsetY = 0 #cIndex*2
        #if not 'Prop' in fontNames[cIndex]: # Compensate for extra pixel on left of T
        #    offsetX = H/10
        r, g, b, t = colors[cIndex]
        fill(r, g, b, t)
        font(fontNames[cIndex])
        fontSize(H)
        text('Typetr', (H/8+offsetX+10, H/8*2+offsetY))
        
saveImage('stills/animatedInstanceA36.png', FRAMES)