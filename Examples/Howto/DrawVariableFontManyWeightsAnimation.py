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
#     DrawVariableFontManyWeightsAnimation.py
#
#     Note: the type of animation used in this example is self-contained:
#     all code for for FontIcon class and KeyFrame class is here.
#     In the future these classes will be part of the main PageBot library,
#     which may make them incompatible with this particular example.
#     
import pagebot
from pagebot.fonttoolbox.objects.font import Font, getFontByName
from pagebot import newFS
from pagebot.fonttoolbox.variablefontbuilder import getVariableFont 
from pagebot.style import CENTER

W = H = 500

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

LABEL_FONT = BOOK

"""
FAMILY = 'Georgia'
for fontName in installedFonts():
    if FAMILY in fontName:
        print fontName
LABEL_FONT = getFontByName('Verdana')
BOOK = getFontByName(FAMILY)
BOOK_ITALIC = getFontByName(FAMILY+'-Italic')
BOLD = getFontByName(FAMILY+'-Bold')
BOLD_ITALIC = getFontByName(FAMILY+'-BoldItalic')
"""
class FontIcon(object):
    W = 30
    H = 40
    L = 2
    E = 8
    LABEL_RTRACKING = 0.02
    LABEL_RLEADING = 1.3

    def __init__(self, f, name=None, label=None, title=None, eId=None, c='F', s=1, line=None, 
            labelFont=None, titleFont=None, x=0, y=0, show=True):
        self.f = f # Font instance
        self.labelFont = labelFont or f
        self.titleFont = titleFont, labelFont or f
        self.title = title
        self.name = name # Name below the icon
        self.label = label # Optiona second label line
        self.c = c # Character(s) in the icon.
        self.scale = s
        self.line = line or self.L
        self.x = x
        self.y = y
        self.show = show
        self.eId = eId

    def _get_w(self):
        return self.W*self.scale
    w = property(_get_w)
    
    def _get_ih(self):
        u"""Answer scaled height of the plain icon without name label."""
        return self.H*self.scale
    ih = property(_get_ih)
    
    def _get_h(self):
        h = self.ih
        if self.name:
            h += self.E*self.scale*1.4 # Extra vertical space to show the name.
        if self.label:
            h += self.E*self.scale*1.4 # Extra vertical space to show the name.
        if self.title:
            h += self.E*self.scale*1.4 # Extra vertical space to show the name.
        return h
    h = property(_get_h)
    
    def draw(self, orgX, orgY):     
        if not self.show:
            return  
        w = self.w # Width of the icon
        h = self.ih # Height of the icon
        e = self.E*self.scale # Ear size
        l = self.L*self.scale # Line
        x = self.x + orgX
        y = self.y + orgY
        
        path = newPath()
        moveTo((0, 0))
        lineTo((0, h))
        lineTo((w-e, h))
        lineTo((w, h-e))
        lineTo((w, 0))
        lineTo((0, 0))
        closePath()
        moveTo((w-e, h))
        lineTo((w-e, h-e))
        lineTo((w, h-e))
    
        save()
        fill(1)
        stroke(0)
        strokeWidth(self.line)
        translate(x, y)
        drawPath(path)
        labelSize = e
        fs = newFS(self.c, style=dict(font=self.f.installedName, textFill=0, fontSize=h*2/3))
        tw, th = textSize(fs)
        text(fs, (w/2-tw/2, h/2-th/3.2))
        
        if self.title:
            fs = newFS(self.title, style=dict(font=self.labelFont.installedName, textFill=0, 
                rTracking=self.LABEL_RTRACKING, fontSize=labelSize))
            tw, th = textSize(fs)
            text(fs, (w/2-tw/2, self.ih+th/2))

        y = -self.LABEL_RLEADING*labelSize
        if self.name:
            fs = newFS(self.name, style=dict(font=self.labelFont.installedName, textFill=0, 
                rTracking=self.LABEL_RTRACKING, fontSize=labelSize))
            tw, th = textSize(fs)
            text(fs, (w/2-tw/2, y))
            y -= self.LABEL_RLEADING*labelSize
        if self.label:
            fs = newFS(self.label, style=dict(font=self.labelFont.installedName, textFill=0, 
                rTracking=self.LABEL_RTRACKING, fontSize=labelSize))
            tw, th = textSize(fs)
            text(fs, (w/2-tw/2, y))
        restore()
    
class KeyFrame(object):
    def __init__(self, objects, positions, steps=None, drawBackground=None):
        self.objects = objects
        self.positions = positions
        self.steps = steps or 1
        self.drawBackgroundHook = drawBackground
    
    def drawBackground(self):
        fill(1)
        rect(0, 0, W, H)
            
    def draw(self):
        for n in range(self.steps):
            newPage(W, H)
            self.drawBackground()
            if self.drawBackgroundHook is not None:
                self.drawBackgroundHook(self, n)
            for o in self.objects:
                offsetX = 0
                offsetY = 0
                if o.eId in self.positions: # Changed target, then calculate new offset
                    tx, ty = self.positions[o.eId]
                    offsetX = (tx-o.x)*1.0*n/self.steps
                    offsetY = (ty-o.y)*1.0*n/self.steps
                o.draw(offsetX, offsetY)
        # Set the new target positions
        for o in self.objects:
            if o.eId in self.positions:
                tx, ty = self.positions[o.eId]
                o.x = tx
                o.y = ty            
S = 1.5
FSIZE = '50k'
ultraLightIcon = FontIcon(ULTRALIGHT, 'Ultra Light', eId='UltraLight', s=S, label=FSIZE, labelFont=LABEL_FONT)
ultraLightCondensedIcon = FontIcon(ULTRALIGHT_CONDENSED, 'UltraLight Condensed', eId='UltraLightCondensed', s=S, label=FSIZE, labelFont=LABEL_FONT)
lightIcon = FontIcon(LIGHT, 'Light', eId='Light', s=S, label=FSIZE, labelFont=LABEL_FONT)
lightCondensedIcon = FontIcon(LIGHT_CONDENSED, 'Light Condensed', eId='LightCondensed', s=S, label=FSIZE, labelFont=LABEL_FONT)
thinIcon = FontIcon(THIN, 'Thin', eId='Thin', s=S, label=FSIZE, labelFont=LABEL_FONT)
thinCondensedIcon = FontIcon(THIN_CONDENSED, 'Thin Condensed', eId='ThinCondensed', s=S, label=FSIZE, labelFont=LABEL_FONT)
bookIcon = FontIcon(BOOK, 'Book', eId='Book', s=S, label=FSIZE, labelFont=LABEL_FONT)
bookCondensedIcon = FontIcon(BOOK_CONDENSED, 'Book Condensed', eId='BookCondensed', s=S, label=FSIZE, labelFont=LABEL_FONT)
regularIcon = FontIcon(REGULAR, 'Regular', eId='Regular', s=S, label=FSIZE, labelFont=LABEL_FONT)
regularCondensedIcon = FontIcon(REGULAR_CONDENSED, 'Regular Condensed', eId='BookCondensed', s=S, label=FSIZE, labelFont=LABEL_FONT)
mediumIcon = FontIcon(MEDIUM, 'Medium', eId='Medium', s=S, label=FSIZE, labelFont=LABEL_FONT)
mediumCondensedIcon = FontIcon(MEDIUM_CONDENSED, 'Medium Condensed', eId='MediumCondensed', s=S, label=FSIZE, labelFont=LABEL_FONT)
semibolIcon = FontIcon(SEMIBOLD, 'Semibold', eId='Semibold', s=S, label=FSIZE, labelFont=LABEL_FONT)
semiboldCondensedIcon = FontIcon(SEMIBOLD_CONDENSED, 'Semibold Condensed', eId='SemiboldCondensed', s=S, label=FSIZE, labelFont=LABEL_FONT)
boldIcon = FontIcon(BOLD, 'Bold', eId='Bold', s=S, label=FSIZE, labelFont=LABEL_FONT)
boldCondensedIcon = FontIcon(BOLD_CONDENSED, 'Bold Condensed', eId='BoldCondensed', s=S, label=FSIZE, labelFont=LABEL_FONT)
varFontIcon = FontIcon(BOOK, 'Variable Font', eId='VarFont', s=S, c='', label='0k', labelFont=LABEL_FONT, title='No axes')

fontIcons = [varFontIcon, ultraLightIcon, lightIcon, thinIcon, bookIcon, regularIcon, mediumIcon, semibolIcon, boldIcon]
id2FontIcon = {}
for fontIcon in fontIcons:
    id2FontIcon[fontIcon.eId] = fontIcon
    
def positionFontIcons():
    y = Y = H - 130
    for iconId in ('UltraLight', 'Thin', 'Regular', 'Semibold'):
        fontIcon = id2FontIcon[iconId]
        fontIcon.x = 50
        fontIcon.y = y
        y -= fontIcon.h*1.1
    y = Y
    for iconId in ('Light', 'Book', 'Medium', 'Bold'):
        fontIcon = id2FontIcon[iconId]
        fontIcon.x = 150
        fontIcon.y = y
        y -= fontIcon.h*1.1

    varFontIcon = id2FontIcon['VarFont']
    varFontIcon.x = W/2-varFontIcon.w/2+40
    varFontIcon.y = H/2-varFontIcon.ih/2

def drawBackground1(keyFrame, frame):
    fs = newFS('8 weight fonts\nTotal 400k', style=dict(font=LABEL_FONT.installedName, rLeading=1.2, fontSize=18, textFill=(1, 0, 0)))
    textBox(fs, (50, H-60, 200, 50))
    
def drawBackground2(keyFrame, frame):
    drawBackground1(keyFrame, frame)
    varFontIcon = id2FontIcon['VarFont']
    fs = newFS('1 axis\nTotal 100k', style=dict(font=LABEL_FONT.installedName, rLeading=1.2, fontSize=18, textFill=(1, 0, 0)))
    textBox(fs, (varFontIcon.x, H-60, 200, 50))
    
def drawBackground3(keyFrame, frame):
    drawBackground1(keyFrame, frame)
    varFontIcon = id2FontIcon['VarFont']
    fs = newFS('Infinite weights\nTotal 100k', style=dict(font=LABEL_FONT.installedName, rLeading=1.2, fontSize=18, textFill=(1, 0, 0)))
    textBox(fs, (varFontIcon.x, H-60, 200, 50))
        
def drawAnimation():
    positionFontIcons()
    varFontIcon = id2FontIcon['VarFont']

    KeyFrame(fontIcons, {}, 15,
        drawBackground=drawBackground1
    ).draw()

    KeyFrame(fontIcons, 
        {'Regular': (varFontIcon.x, varFontIcon.y)}, 10,
        drawBackground=drawBackground1
    ).draw()
    id2FontIcon['Regular'].show = False
    varFontIcon.title = '0 axis'
    varFontIcon.label = FSIZE
    varFontIcon.c = 'F'
    
    KeyFrame(fontIcons, 
        {'Bold': (varFontIcon.x, varFontIcon.y)}, 10,
        drawBackground=drawBackground1
    ).draw()
    id2FontIcon['Bold'].show = False
    varFontIcon.title = '1 axis [Weight]'
    varFontIcon.label = '100k'

    KeyFrame(fontIcons, {}, 10,
        drawBackground=drawBackground2
    ).draw()
    
    KeyFrame(fontIcons, 
        {'UltraLight': (varFontIcon.x, varFontIcon.y), 'Light': (varFontIcon.x, varFontIcon.y), 
         'Thin': (varFontIcon.x, varFontIcon.y), 'Book': (varFontIcon.x, varFontIcon.y), 
         'Medium': (varFontIcon.x, varFontIcon.y), 'Semibold': (varFontIcon.x, varFontIcon.y), 
         'Bold': (varFontIcon.x, varFontIcon.y)}, 10,
        drawBackground=drawBackground2
    ).draw()
    id2FontIcon['UltraLight'].show = False
    id2FontIcon['Light'].show = False
    id2FontIcon['Thin'].show = False
    id2FontIcon['Book'].show = False
    id2FontIcon['Medium'].show = False
    id2FontIcon['Semibold'].show = False
    varFontIcon.label = '100K'

    KeyFrame(fontIcons, {}, 40,
        drawBackground=drawBackground3
    ).draw()

    saveImage('_export/VarFontManyWeights.gif')    

drawAnimation()
   
    