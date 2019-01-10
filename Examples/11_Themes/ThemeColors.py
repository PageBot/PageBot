# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     UseThemes.py
#
from pagebot.themes.palette import PALETTES
from pagebot.constants import A4, CENTER
from pagebot.toolbox.units import upt

W, H = upt(A4)

CW = 100
CH = CW*1.5
PADDING = 50
DX = 4
DY = 3
G = (W - PADDING*2 - CW*DX)/(DX - 1)

def drawColor(x, y, clr):
    
    r, g, b = clr.rgb
    fill(r, g, b)
    rect(x, y+CH-CW, CW, CW)
    stroke(0)
    strokeWidth(0.5)
    fill(None)
    rect(x, y, CW, CH)

    textFill = 0
    fs = FormattedString('SPOT\n%s' % clr.spot, 
        font='Upgrade-Regular', fontSize=16, lineHeight=18, align=CENTER, fill=textFill)
    tw, th = textSize(fs)
    text(fs, (x+CW/2-tw/2, y+30))

for name, palette in sorted(PALETTES.items()):
    newPage(W, H)
    cIndex = 0
    fill(0)
    fs = FormattedString(palette.name, font='Upgrade-Medium', fontSize=32)
    text(fs, (PADDING, PADDING))
    
    for x in range(DX):
        for y in range(DY):
            if palette[cIndex] is not None:
                drawColor(PADDING + x*(CW+G), H - PADDING - y*(CH+G)-CH, palette[cIndex])
            cIndex += 1


saveImage('_export/ThemeColors.pdf')