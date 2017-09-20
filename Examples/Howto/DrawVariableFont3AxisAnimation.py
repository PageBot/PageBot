# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     DrawVariableFont3AxisAnimation.py
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

LIGHT72 = getVariableFont(FONT_PATH, dict(wght=0.5, wdth=0.6, opsz=72), styleName='Light72')
BOOK_LIGHT = getVariableFont(FONT_PATH, dict(wght=0.5, wdth=0.7), styleName='Book Light')
BOOK_CONDENSED = getVariableFont(FONT_PATH, dict(wght=0.6, wdth=0.7), styleName='Book Condensed')
BOOK = getVariableFont(FONT_PATH, dict(wght=0.6, wdth=0), styleName='Book')
LIGHT_CONDENSED = getVariableFont(FONT_PATH, dict(wght=0.9, wdth=0.7), styleName='Light Condensed')
LIGHT = getVariableFont(FONT_PATH, dict(wght=0.9, wdth=0), styleName='Light')
BOOK_ITALIC = getVariableFont(FONT_PATH, dict(wght=0.25, wdth=1), styleName='Book Italic')
MEDIUM = getVariableFont(FONT_PATH, dict(wght=0.40, wdth=0), styleName='Medium')
SEMIBOLD = getVariableFont(FONT_PATH, dict(wght=0.40, wdth=1), styleName='Semibold')
SEMIBOLD_CONDENSED = getVariableFont(FONT_PATH, dict(wght=0.40, wdth=0.5), styleName='Semibold Condensed')
BOLD = getVariableFont(FONT_PATH, dict(wght=0.0, wdth=0), styleName='Bold')
BOLD_CONDENSED = getVariableFont(FONT_PATH, dict(wght=0.0, wdth=0.7), styleName='Bold Condensed')
BOLD_ITALIC = getVariableFont(FONT_PATH, dict(wght=0.7, wdth=0), styleName='Bold Italic')

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
        if drawBackground is not None:
            self.drawBacktround = drawBackground
    
    def drawBackground(self):
        fill(1)
        rect(0, 0, W, H)
            
    def draw(self):
        for n in range(self.steps):
            newPage(W, H)
            self.drawBackground()
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

lightIcon = FontIcon(LIGHT, 'Light', eId='Light', s=S, label='50K', labelFont=LABEL_FONT)
lightCondensedIcon = FontIcon(LIGHT_CONDENSED, 'Light Condensed', eId='LightCondensed', s=S, label='50K', labelFont=LABEL_FONT)
boldIcon = FontIcon(BOLD, 'Bold', eId='Bold', s=S, label='50K', labelFont=LABEL_FONT)
boldCondensedIcon = FontIcon(BOLD_CONDENSED, 'Bold Condensed', eId='BoldCondensed', s=S, label='50K', labelFont=LABEL_FONT)
varFontIcon = FontIcon(BOOK, 'Variable Font', eId='VarFont', s=S, label='0K', labelFont=LABEL_FONT, title='No axes')

fontIcons = [varFontIcon, lightIcon, boldIcon, lightCondensedIcon, boldCondensedIcon]
id2FontIcon = {}
for fontIcon in fontIcons:
    id2FontIcon[fontIcon.eId] = fontIcon
    
def positionFontIcons():
    y = H - 110
    for iconId in ('Light', 'LightCondensed', 'Bold', 'BoldCondensed'):
        fontIcon = id2FontIcon[iconId]
        fontIcon.x = 50
        fontIcon.y = y
        y -= fontIcon.h*1.1

    varFontIcon = id2FontIcon['VarFont']
    varFontIcon.x = W/2-varFontIcon.w/2
    varFontIcon.y = H/2-varFontIcon.ih/2

def drawBackground(keyFrame, frame):
    fill(1)
    rect(0, 0, W, H)
    
def drawAnimation():
    positionFontIcons()
    varFontIcon = id2FontIcon['VarFont']

    KeyFrame(fontIcons, {}, 8,
        drawBackground=drawBackground
    ).draw()

    KeyFrame(fontIcons, 
        {'Light': (varFontIcon.x, varFontIcon.y), 'Bold': (varFontIcon.x, varFontIcon.y)}, 14,
        drawBackground=drawBackground
    ).draw()
    id2FontIcon['Light'].show = False
    id2FontIcon['Bold'].show = False
    varFontIcon.title = '1 axis [Weight]'
    varFontIcon.label = '75K'
    
    KeyFrame(fontIcons, 
        {'LightCondensed': (varFontIcon.x, varFontIcon.y), 'BoldCondensed': (varFontIcon.x, varFontIcon.y)}, 14,
        drawBackground=drawBackground
    ).draw()
    id2FontIcon['LightCondensed'].show = False
    id2FontIcon['BoldCondensed'].show = False
    varFontIcon.title = '2 axis [Weight, Width]'
    varFontIcon.label = '90K'

    KeyFrame(fontIcons, {}, 14,
        drawBackground=drawBackground
    ).draw()

    saveImage('_export/VarFont2Axes.gif')    

drawAnimation()
   
    