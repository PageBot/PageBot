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
from pagebot.contexts.drawbotcontext import DrawBotContext

context = DrawBotContext()

W = H = upt(A4)[0]

CW = 100
CH = CW*1.5
PADDING = 50
DX = 4
DY = 3
G = (W - PADDING*2 - CW*DX)/(DX - 1)

def drawColor(x, y, clr):
    
    context.stroke(None)
    context.fill(clr)
    context.rect(x, y+CH-CW, CW, CW)
    context.stroke(0)
    context.strokeWidth(2)
    context.fill(None)
    context.rect(x, y, CW, CH)

    textFill = 0
    bs = context.newString('SPOT\n%s' % clr.spot, 
        style=dict(font='Upgrade-Regular', fontSize=16, leading=18, xTextAlign=CENTER, textFill=textFill))
    tw, th = bs.size
    context.text(bs, (x+CW/2-tw/2, y+30))

for name, palette in sorted(PALETTES.items()):
    context.newPage(W, H)
    cIndex = 0
    context.fill(0)
    bs = context.newString(palette.name, style=dict(font='Upgrade-Medium', fontSize=22))
    context.text(bs, (PADDING, H-PADDING*2/3))
    
    for x in range(DX):
        for y in range(DY):
            if palette[cIndex] is not None:
                drawColor(PADDING + x*(CW+G), H - PADDING - y*(CH+G)-CH, palette[cIndex])
            cIndex += 1


context.saveImage('_export/ThemeColors.pdf')