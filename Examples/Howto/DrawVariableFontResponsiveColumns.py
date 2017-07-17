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
#     DrawVariableFontResponsiveColumns.py
#
#     Note: the type of animation used in this example is self-contained:
#     all code for for FontIcon class and KeyFrame class is here.
#     In the future these classes will be part of the main PageBot library,
#     which may make them incompatible with this particular example.
#     
import pagebot
from pagebot.fonttoolbox.objects.font import Font, getFontByName
from pagebot import newFS
from pagebot.fonttoolbox.variablefontbuilder import getVariableFont, fitWidth
from pagebot.style import CENTER

W = 600
H = 300

FRAMES = 30
PADDING = 10

ROOT_PATH = pagebot.getRootPath()
FONT_PATH = ROOT_PATH + '/Fonts/fontbureau/AmstelvarAlpha-VF.ttf'
f = Font(FONT_PATH, install=True) # Get PageBot Font instance of Variable font.

ULTRALIGHT_CONDENSED = getVariableFont(FONT_PATH, dict(wght=0.9, wdth=0.7), styleName='Utrla Light Condensed')
ULTRALIGHT = getVariableFont(FONT_PATH, dict(wght=1, wdth=0), styleName='Ultra Light')
LIGHT_CONDENSED = getVariableFont(FONT_PATH, dict(wght=0.9, wdth=0.7), styleName='Light Condensed')
LIGHT = getVariableFont(FONT_PATH, dict(wght=0.9, wdth=0), styleName='Light')
THIN_CONDENSED = getVariableFont(FONT_PATH, dict(wght=0.8, wdth=0.7), styleName='Thin Condensed')
THIN = getVariableFont(FONT_PATH, dict(wght=0.8, wdth=0), styleName='Thin')
BOOK_CONDENSED = getVariableFont(FONT_PATH, dict(wght=0.7, wdth=0.7), styleName='Book Condensed')
BOOK = getVariableFont(FONT_PATH, dict(wght=0.7, wdth=0), styleName='Book')
REGULAR_CONDENSED = getVariableFont(FONT_PATH, dict(wght=0.6, wdth=0.7), styleName='Regular Condensed')
REGULAR = getVariableFont(FONT_PATH, dict(wght=0.6, wdth=0), styleName='Regular')
MEDIUM_CONDENSED = getVariableFont(FONT_PATH, dict(wght=0.5, wdth=0.7), styleName='Medium Condensed')
MEDIUM = getVariableFont(FONT_PATH, dict(wght=0.5, wdth=0), styleName='Medium')
SEMIBOLD_CONDENSED = getVariableFont(FONT_PATH, dict(wght=0.30, wdth=0.7), styleName='Semibold Condensed')
SEMIBOLD = getVariableFont(FONT_PATH, dict(wght=0.30, wdth=0), styleName='Semibold')
BOLD_CONDENSED = getVariableFont(FONT_PATH, dict(wght=0.0, wdth=0.7), styleName='Bold Condensed')
BOLD = getVariableFont(FONT_PATH, dict(wght=0.0, wdth=0), styleName='Bold')


HEAD_SIZE = 36
BODY_SIZE = 12
HEADLINE_FONT = getVariableFont(FONT_PATH, dict(wght=0.5, wdth=0, opsz=HEAD_SIZE), styleName='Medium')
HEADLINE_COND_FONT = getVariableFont(FONT_PATH, dict(wght=0.5, wdth=0.5, opsz=HEAD_SIZE), styleName='Medium')


BODY_FONT = getVariableFont(FONT_PATH, dict(wght=0.8, wdth=0, opsz=BODY_SIZE), styleName='Medium')

HEADLINE = """When fonts started a new world"""

BODY = """The advent of variable fonts means doing nothing, or everything, or something in between for font users and type designers. Superficially, everything that worked before, works now. All existing fonts retain their quality, functionality and performance, but deep down, OpenType variations technology can change everything about type. Here we’re putting this historic development into some perspective, looking both backward at how type technology has evolved, and forward toward where the new tools may take us. As described in the introduction, variations technology superficially changes nothing about the “workings” of older fonts or applications. Users still begin their work by selecting the keyboard and input method associated with their script and language, or just by clicking an icon of their national flag. From there, the OS maps the characters it’ll show on the screen to match those on the keyboard, and turns on any required OpenType features for that script and language. All the individual font files are sorted for presentation by family name, with a hyphen somewhere separating the family name from the style, treatment, and/or effect name."""

def drawAnimation():
    for frame in [0]*10+range(int(FRAMES/2))+[FRAMES/2]*10+range(int(FRAMES/2),FRAMES):
        newPage(W, H)
        fs = newFS(HEADLINE+'\n', style=dict(font=HEADLINE_FONT.installedName, fontSize=HEAD_SIZE, textFill=0, paragraphBottomSpacing=10, rLeading=1.05))
        #fs += newFS(BODY, style=dict(font=BODY_FONT.installedName, fontSize=BODY_FONT, textFill=0))
        if frame < FRAMES/2:
            w = 400 + float(W-2*PADDING)*frame/FRAMES
        else:
            f = FRAMES-frame
            w = 400 + float(W-2*PADDING)*f/FRAMES

        tw, th = textSize(fs, width=w)                
        fill(0.9)
        rect(PADDING, -th+H-PADDING, w, th)
        textBox(fs, (PADDING, -th+H-PADDING, w, th))

        fs = newFS(HEADLINE+'\n', style=dict(font=HEADLINE_COND_FONT.installedName, fontSize=HEAD_SIZE, textFill=0, paragraphBottomSpacing=10, rLeading=1.05))
        #fs += newFS(BODY, style=dict(font=BODY_FONT.installedName, fontSize=BODY_FONT, textFill=0))
        if frame < FRAMES/2:
            w = 400 + float(W-2*PADDING)*frame/FRAMES
        else:
            f = FRAMES-frame
            w = 400 + float(W-2*PADDING)*f/FRAMES

        tw, th = textSize(fs, width=w)                
        fill(0.9)
        rect(PADDING, -th+H/2-PADDING, w, th)
        textBox(fs, (PADDING, -th+H/2-PADDING, w, th))

    saveImage('_export/varFontResponsiveColumns.gif')    

drawAnimation()
   
    