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
#     ThemeMoodElement.py
#
import copy
# Import the Theme classes from PageBot.
from pagebot.themes import ThemeClasses
from pagebot.themes import BaseTheme, FreshAndShiny
from pagebot.conditions import *
from pagebot.elements import *
from pagebot.contexts.drawbotcontext import DrawBotContext
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.toolbox.color import color, spot
from pagebot.toolbox.units import point2D
from pagebot.document import Document
from pagebot.constants import *

W, H = A4

context = DrawBotContext()

class ThemeSpecimen(Element):
    """Draw an element, showing best of an info-graphic with the 
    content (color palette and mood) of the selected Theme.
    """
    
    def buildElement(self, view, p, drawElements, **kwargs):
        context = self.context
        # Mood: body=dict(color='dark0', bgcolor='lightest0'),

        mood = self.theme.mood
        context.fill(mood.body_bgcolor)
        x, y = point2D(p)
        context.rect(p[0], p[1], self.w, self.h)
        # Theme name header, iterate until it fits.
        tw = XXXL
        styleHead = copy.copy(self.style)
        styleHead['font'] = boldFont = findFont('PageBot-Bold')
        styleHead['textFill'] = mood.body_color
        themeMoodName = '%s:%s' % (self.theme.name, self.theme.mood.name)
        for fontSize in range(24, 0, -1):
            styleHead['fontSize'] = pt(fontSize)
            themeName = context.newString(themeMoodName, style=styleHead)
            tw, th = themeName.size
            if tw < self.pw:
                context.textBox(themeName, 
                    (x+self.pl, y+self.h-th-self.pt, self.pw, th))
                break
        # Theme palette
        
doc = Document(w=W, h=H, context=context, originTop=False)

view = doc.view
view.showPadding = True

page = doc[1]
page.padding = 60
ThemeSpecimen(parent=page, theme=FreshAndShiny('normal'), fill=0.9, 
    padding=12, conditions=[Fit()])
page.solve()

page = page.next
page.padding = 60
ThemeSpecimen(parent=page, theme=FreshAndShiny('dark'), fill=0.9, 
    padding=12, conditions=[Fit()])
page.solve()

doc.export('_export/ThemeMoodElement.pdf')
'''
CW = pt(100) # Width of a color cell
CH = CW*1.5 # Height of a color cell
PADDING = pt(60) # Padding between color matrix and page side.
DX = 7 # Number of matrix colums
DY = 7 # Number of matric rows
G = pt(12) # Gutter in point unit between the color cells.

labelFont = findFont('Roboto-Regular') # Find the font in the PageBot resources.
labelSize = pt(16)
labelLeading = pt(18)

# Calculate the page size, based on size of matrix, cells and gutter.
W, H = PADDING*2 + CW*DX + G*(DX-1), PADDING*3 + CH*DY + G*(DY-1) 

def drawColor(colorName, x, y, clr):
    # Draw the color cell as square with a value label.
    context.stroke(None)
    context.fill(clr)
    context.rect(x, y+CH-CW, CW, CW)
    context.stroke(blackColor)
    context.strokeWidth(1)
    context.fill(None)
    context.rect(x, y, CW, CH)
    textFill = 0
    labelString = context.newString('%s\n#%s' % (colorName, clr.hex), 
        style=dict(font=labelFont, fontSize=labelSize, leading=labelLeading, 
        textFill=textFill))
    tw, th = labelString.size # Get the size of the label to center it
    context.text(labelString, (x+CW/2-tw/2, y+30)) # Position text in cell

def makeThemePage(themeClass):
    context.newPage(W, H)
    theme = themeClass()
    colorNames = sorted(theme.palette.colorNames)
    cIndex = 0
    context.fill(0)
    titleString = context.newString('PageBot Theme “%s”' % theme.name, 
        style=dict(font=labelFont, fontSize=32))
    context.text(titleString, (PADDING, H-2*PADDING*2/3))
    
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

# Define the matrix by theirs palette names.
colorMatrix = (
    ('black', 'gray', 'white', 'background', 'logoLight', 'logo', 'logoDark'),
    ('lightest0', 'light0', 'lighter0', 'base0', 'darker0', 'dark0', 'darkest0'),
    ('lightest1', 'light1', 'lighter1', 'base1', 'darker1', 'dark1', 'darkest1'),
    ('lightest2', 'light2', 'lighter2', 'base2', 'darker2', 'dark2', 'darkest2'),
    ('lightest3', 'light3', 'lighter3', 'base3', 'darker3', 'dark3', 'darkest3'),
    ('lightest4', 'light4', 'lighter4', 'base4', 'darker4', 'dark4', 'darkest4'),
    ('lightest5', 'light5', 'lighter5', 'base5', 'darker5', 'dark5', 'darkest5'),
)
# Make pages for all standard Theme palettes
for themeName, themeClass in ThemeClasses.items():
    makeThemePage(themeClass)
# Add pages for the custom themes that we made.
makeThemePage(FantasyTheme)
makeThemePage(DDSTheme)
      
# Save the first of the pages in different formats.
# Only the PDF will contain all pages create.
context.saveImage('_export/dds453-theme-color-matrix.pdf')
context.saveImage('_export/dds453-theme-color-matrix.png')
context.saveImage('_export/dds453-theme-color-matrix.svg')
'''