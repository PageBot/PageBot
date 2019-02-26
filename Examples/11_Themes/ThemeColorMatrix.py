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
#     ThemeColorMatrix.py
#
from pagebot.themes import ThemeClasses
from pagebot.themes.basetheme import BaseTheme
from pagebot.constants import A4, CENTER
from pagebot.toolbox.units import upt
from pagebot.contexts.drawbotcontext import DrawBotContext
from pagebot.toolbox.color import rgb, color, spot

context = DrawBotContext()

class FantasyTheme(BaseTheme):
    NAME = 'Fantasy Red'
    BASE_COLORS = dict(
        base2=color(1, 0, 0.2), # Filling 2 base colors as source for range.
        dark3=color(1, 0, 0.5), # Overwriting single slot in the matrix.
        logo=spot(300)
    )

CW = 100
CH = CW*1.5
PADDING = 60
DX = 7
DY = 7
G = 12

W, H = PADDING*2 + CW*DX + G*(DX-1), PADDING*3 + CH*DY + G*(DY-1) 

def drawColor(colorName, x, y, clr):
    
    context.stroke(None)
    context.fill(clr)
    context.rect(x, y+CH-CW, CW, CW)
    context.stroke(0)
    context.strokeWidth(1)
    context.fill(None)
    context.rect(x, y, CW, CH)

    textFill = 0
    bs = context.newString('%s\n#%s' % (colorName, clr.hex), 
        style=dict(font='Upgrade-Regular', fontSize=16, leading=18, xTextAlign=CENTER, textFill=textFill))
    tw, th = bs.size
    context.text(bs, (x+CW/2-tw/2, y+30))

def makeThemePage(themeClass):
    context.newPage(W, H)
    theme = themeClass()
    colorNames = sorted(theme.palette.colorNames)
    cIndex = 0
    context.fill(0)
    bs = context.newString('PageBot Theme “%s”' % theme.name, style=dict(font='Upgrade-Medium', fontSize=32))
    context.text(bs, (PADDING, H-2*PADDING*2/3))
    
    y = 0
    for colorGroup in colorMatrix:
        x = 0
        for colorName in colorGroup:
            try:
                clr = theme.palette[colorName]
                if clr is not None:
                    drawColor(colorName, PADDING + x*(CW+G), H - 2*PADDING - y*(CH+G)-CH, clr)
                cIndex += 1
            except IndexError:
                break
            x += 1
        y += 1

colorMatrix = (
    ('black', 'gray', 'white', 'background', 'logoLight', 'logo', 'logoDark'),
    ('lightest0', 'light0', 'lighter0', 'base0', 'darker0', 'dark0', 'darkest0'),
    ('lightest1', 'light1', 'lighter1', 'base1', 'darker1', 'dark1', 'darkest1'),
    ('lightest2', 'light2', 'lighter2', 'base2', 'darker2', 'dark2', 'darkest2'),
    ('lightest3', 'light3', 'lighter3', 'base3', 'darker3', 'dark3', 'darkest3'),
    ('lightest4', 'light4', 'lighter4', 'base4', 'darker4', 'dark4', 'darkest4'),
    ('lightest5', 'light5', 'lighter5', 'base5', 'darker5', 'dark5', 'darkest5'),
)
for themeName, themeClass in ThemeClasses.items():
    makeThemePage(themeClass)
makeThemePage(FantasyTheme)
        
#context.b.frameDuration(10)
context.saveImage('_export/ThemeColorMatrix.pdf')
#context.saveImage('_export/ThemeColorMatrix.mov')