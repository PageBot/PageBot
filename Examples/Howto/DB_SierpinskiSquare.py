# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     ScalingAnImage.py

# by Petr van Blokland @petrvanblokland
# https://twitter.com/petrvanblokland/status/860610270410018817

def drawSierpinskiSquare(px, py, w, maxW):
    if w < 1:
        return
    for x in range(3):
        for y in range(3):
            if x == 1 and y == 1:
                fill(max(0, 0.75 - w/100))
                rect(px+w, py+w, w, w)
            elif px <= maxW and py <= maxW:
                drawSierpinskiSquare(px+x*w, py+y*w, w/3, maxW)

if __name__ == '__main__':
    canvasSize = 500
    numFrames = 40
    factor = 3 ** (1/numFrames)

    for frame in range(numFrames):
        newPage(canvasSize, canvasSize)
        frameDuration(1/20)
        fill(1)
        rect(0, 0, canvasSize, canvasSize)
        w = canvasSize * factor ** frame
        drawSierpinskiSquare(0, 0, w, canvasSize)

    saveImage("_export/SierpinskiSquare.gif")
    print 'Done'