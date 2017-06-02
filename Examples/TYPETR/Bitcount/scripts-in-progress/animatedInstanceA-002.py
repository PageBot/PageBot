bitcountNames = []
for fontName in installedFonts():
    if 'Bitcount' in fontName and not 'Italic' in fontName:
        bitcountNames.append(fontName)

FRAMES = 400
H = 150
W = 600

colors = [[1, 0.1, 0, 1], [0, 1, 1, 1], [0.2, 0.3, 1, 1]]
colorDirs = [10/FRAMES, -14/FRAMES, 18/FRAMES]   
fontNames = [choice(bitcountNames), choice(bitcountNames), choice(bitcountNames)]

for frame in range(FRAMES):
    newPage(W, H)
    fill(0)
    rect(0, 0, W, H)
    for cIndex in range(len(colors)):
        colors[cIndex][cIndex] += colorDirs[cIndex]
        colors[cIndex][3] += colorDirs[cIndex]
        if colors[cIndex][cIndex] < 0.5:
            fontNames[cIndex] = choice(bitcountNames)
            colorDirs[cIndex] = -colorDirs[cIndex]
            colors[cIndex][cIndex] += colorDirs[cIndex]
            colors[cIndex][3] = 0.5
        elif colors[cIndex][cIndex] > 1:
            colors[cIndex][cIndex] -= colorDirs[cIndex]
            colors[cIndex][3] = 1
            colorDirs[cIndex] = -colorDirs[cIndex]
        

        offset = 0 #cIndex*2
        r, g, b, t = colors[cIndex]
        fill(r, g, b, t)
        font(fontNames[cIndex])
        fontSize(H)
        text('Typetr', (H/8*2-offset, H/8*2+offset))
saveImage('animatedInstanceA.gif')