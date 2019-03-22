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
#     MoodColorMatrix.py
#
#     Display the collection of available themes-->moods-->keys
#
from pagebot.themes import ThemeClasses
from pagebot.themes.basetheme import BaseTheme
from pagebot.constants import A4, CENTER
from pagebot.toolbox.units import upt
from pagebot.contexts.drawbotcontext import DrawBotContext
from pagebot.toolbox.color import rgb, color, spot

context = DrawBotContext()

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

def makeThemeMoodPage(themeClass):
    theme = themeClass()
    cIndex = 0
    context.fill(0)
    
    theme = themeClass()
    for moodName in theme.MOODS.keys(): 
        theme.selectMood(moodName)       

        context.newPage(W, H)
        bs = context.newString('PageBot Theme “%s” Mood “%s”' % (theme.name, moodName),
            style=dict(font='Upgrade-Medium', fontSize=32))
        context.text(bs, (PADDING, H-2*PADDING*2/3))

        y = 0
        x = 0

        prevMoodKeyParts = None
        for moodKey, moodColor in sorted(theme.mood.attributes.items()):
            clr = color(moodColor)
            drawColor(moodKey, PADDING + x*(CW+G), H - 2*PADDING - y*(CH+G)-CH, clr)
            x += 1
            moodKeyParts = moodKey.split('.')
            if x >= 7 or (len(moodKeyParts) > 1 and prevMoodKey not in (None, moodKeyParts[0])):
                if y > 5:
                    context.newPage(W, H)
                    y = 0
                else:
                    y += 1
                x = 0
                prevMoodKeyParts = moodKeyParts

    """
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
    """
    
for themeName, themeClass in ThemeClasses.items():
    makeThemeMoodPage(themeClass)
    break
        
#context.b.frameDuration(10)
context.saveImage('_export/MoodColorMatrix.pdf')
#context.saveImage('_export/ThemeColorMatrix.mov')