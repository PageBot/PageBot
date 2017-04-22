bitcountNames = []
for fontName in installedFonts():
    if 'Bitcount' in fontName and not 'Italic' in fontName:
        bitcountNames.append(fontName)

FRAMES = 400
W = H = 300
colorSteps = [16/FRAMES, 20/FRAMES, 24/FRAMES]
colors = [[1, 0.1, 0, random()], [0.1, 0.6, 0, 1], [0.2, 0, 0.6, random()]]
colorDirs = [colorSteps[0], -colorSteps[1], colorSteps[2]]   
fontNames = [choice(bitcountNames), choice(bitcountNames), choice(bitcountNames)]

for frame in range(FRAMES):
    newPage(W, H)
    fill(0)
    rect(0, 0, W, H)
    for cIndex in range(len(colors)):
        colors[cIndex][3] += colorDirs[cIndex]
        if colors[cIndex][3] < 0:
            fontNames[cIndex] = choice(bitcountNames)
            colorDirs[cIndex] = -colorDirs[cIndex]
        elif colors[cIndex][3] > 1:
            colors[cIndex][3] = 1
            colorDirs[cIndex] = -colorDirs[cIndex]
        

        r, g, b, t = colors[cIndex]
        fill(r, g, b, t)
        font(fontNames[cIndex])
        fontSize(W*3/2)
        text('a', (W/8-cIndex*2, H/8+cIndex*2))
saveImage('animatedInstanceA.gif')