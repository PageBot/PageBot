bitcountNames = []
for fontName in installedFonts():
    if 'Bitcount' in fontName and not 'Italic' in fontName:
        bitcountNames.append(fontName)

FRAMES = 400
W = H = 300
colorSteps = [FRAMES/2000, FRAMES/2200, FRAMES/2400]
colors = [[1, 0.1, 0, 0.5], [0.1, 0.6, 0, 1], [0.2, 0, 0.6, 0.5]]
colorDirs = [colorSteps[0], -colorSteps[1], colorSteps[2]]   
fontNames = [choice(bitcountNames), choice(bitcountNames), choice(bitcountNames)]

for frame in range(FRAMES):
    newPage(W, H)
    fill(0)
    rect(0, 0, W, H)
    for cIndex in range(len(colors)):
        r, g, b, t = colors[cIndex]
        fill(r, g, b, t)
        font(fontNames[cIndex])
        fontSize(W*3/2)
        text('a', (W/8-cIndex*2, H/8+cIndex*2))
        colors[cIndex][2] += colorDirs[cIndex]
        if colors[cIndex][2] < 0:
            fontNames[cIndex] = choice(bitcountNames)
        if colors[cIndex][2] < 0 or colors[cIndex][2] > 1:
            colorDirs[cIndex] = -colorDirs[cIndex]
            
saveImage('animatedInstanceA.gif')