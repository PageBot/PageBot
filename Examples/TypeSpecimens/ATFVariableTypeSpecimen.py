# -*- coding: UTF-8 -*-
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
#     ATFVariableTypeSpecimen.py
#
#     This scripts generates a look-alike revival type specimen with an interpretation
#     of the 1923 American Type Founders Specimen Book & Catalog.
#
#     For educational purpose in using PageBot, almost every line of code has been commented.
#

import os # Import standard libary for accessing the file system.
from random import choice # Used for random selection of sample words

from pagebot.contexts import defaultContext as context # Decide if running in DrawBot or Linux-Flat
from pagebot.style import INCH, CENTER, INLINE # Import some measure and alignments constants.
from pagebot.document import Document # Overall container class of any PageBot script
from pagebot.fonttoolbox.objects.family import getFamily, getFamilies # Access to installed fonts
from pagebot.elements import newTextBox, newRect, newTextBox, newImage # Used elements in this specimen
from pagebot.toolbox.transformer import int2Color # Convenient CSS color to PageBot color conversion
from pagebot.toolbox.hyphenation import wordsByLength # Use English hyphenation dictionary as word selector
from pagebot.conditions import * # Import layout conditions for automatic layout.

# Debugging switches
SHOW_FRAMES = False # True shows page and padding frames.
SHOW_TEMPLATE = False # True shows the ATF scan at the back of every page to show alignment.
SHOW_GRID = True # Show page grid and elements backgrounds in opaque colors.

if SHOW_GRID: # Some debugging colors, used when SHOW_GRID is on.
    DEBUG_COLOR0 = (0.7, 0.3, 0.7, 0.2)
    DEBUG_COLOR1 = (0.3, 0.3, 0.7, 0.2)
    DEBUG_COLOR2 = (0.7, 0.3, 0.3, 0.2)
    DEBUG_COLOR3 = (0.3, 0.7, 0.3, 0.2)    
else: # Otherwise ignore the background colors of the column elements.
    DEBUG_COLOR0 = DEBUG_COLOR1 = DEBUG_COLOR2 = DEBUG_COLOR3 = None
    
# Basic page metrics.
U = 8 # Page layout units, to unite baseline grid and gutter.
W = 7.3*INCH # Copy size from original (?) ATF specimen.
H = 11*INCH
# Hard coded padding sizes derived from the scan.
PT, PR, PB, PL = PADDING = 36, 34, 75, 70 # Page padding top, right, bottom, left
L = 2*U # Baseline leading
G = 3*U # Default gutter = space between the columns

# Hard coded column sizes derived from the scan.
C1, C2, C3 = (150, 112, 112)
# Construct the grid pattern. 
# Last value None means that there is no gutter running inside the right padding.
GRID_X = ((C1, G), (C2, G), (C3, None))
GRID_Y = ((H - PT - PB, None),)

# 1923 American Type Founders Specimen Book & Catalog
# Path to the scan, used to show at first page of this document.
ATF_PATH = 'images/ATFArtcraftBold.png'

# Build the specimen pages for the font names that include these patterns.
FAMILIES = (
    #getFamily('Upgrade'),
    getFamily('Bungee'), 
    #getFamily('Roboto'), 
    #getFamily('AmstelvarAlpha')
)
labelFamily = getFamily('Roboto')
labelFont = labelFamily.findRegularFont() # Ask family to find the most regular font.
labelStyle = dict(font=labelFont.path, fontSize=7, paragraphTopSpacing=9, paragraphBottomSpacing=3)

# Sample glyphs set in bottom right frame. Automatic add a spacing between all characters.
GLYPH_SET = ' '.join(u'ABCDEFGHIJKLMNOPQRSTUVWXYZ&$1234567890abcdefghijklmnopqrstuvwxyz.,-‘:;!?')

# Export in _export folder that does not commit in Git. Force to export PDF.
DO_OPEN = False
if SHOW_GRID:
    EXPORT_PATH = '_export/ATFSpecimen-Grid.pdf' 
else:
    EXPORT_PATH = '_export/ATFSpecimen.pdf' 

# Some parameters from the original book
PAPER_COLOR = int2Color(0xFBF6F1) # Approximation of paper color of original specimen.
RED_COLOR = int2Color(0xAC1E2B) # Red color used in the original specimen

# Get the dictionary of English ("en" is default language), other choice is Dutch ("nl").
# Danish could be made available for PageBot if requested.
# Other hyphenation tables are appreciated to be added to PageBot.
# WORDS key is the word length in character count and the values are lists words of
# equal length.
WORDS = wordsByLength('nl')

def getWord(l):
    u"""Select a random word from the hyphenation dictionary for this language."""
    return choice(WORDS[l]).capitalize()
    
def buildSpecimenPages(doc, family, pn):
    for font in family.getFonts():
        page = doc[pn]
        page.padding = PADDING
        page.gridX = GRID_X
        pageTitle = font.info.familyName + ' ' + font.info.styleName
        # Add filling rectangle for background color of the old paper book.
        # Set z-azis != 0, to make floating elements not get stuck at the background
        newRect(z=-10, w=W, h=H, parent=page, fill=PAPER_COLOR)
        # During development, draw the template scan as background
        # Set z-azis != 0, to make floating elements not get stuck at the background
        if SHOW_TEMPLATE:
            newImage(ATF_PATH, x=0, y=0, z=-10, w=W, parent=page)
        
        # Centered title: family name and style name of the current font.
        titleBs = context.newString(pageTitle, 
                                    style=dict(font=font.path, xTextAlign=CENTER, textFill=0))
        titleBox = newTextBox(titleBs, parent=page, h=2*L,  
                   conditions=[Top2Top(), Fit2Width()],
                   fill=DEBUG_COLOR0)
        titleBox.solve()
        
        largeSampleBox = newTextBox('', parent=page, w=C1+G/2, 
                   conditions=[Float2Top(), Left2Left(), Fit2Bottom()],
                   fill=DEBUG_COLOR1)
        largeSampleBox.solve()
               
        largeSample = None
        previousPointSize = 0
        for wordLength in range(3, 20):
            sample = context.newString(getWord(wordLength)+'\n', style=dict(font=font.path), w=C1, pixelFit=False)
            newPointSize = int(round(sample.fontSize))
            if newPointSize == previousPointSize:
                continue 
            label = context.newString('%d Points\n' % newPointSize, style=labelStyle)
            newSample = label + sample
            if largeSample is None:
                largeSample = newSample
            elif largeSample.h + newSample.h > largeSampleBox.h:
                break
            else:
                largeSample += newSample  
            previousPointSize = newPointSize
            
        largeSampleBox.setText(largeSample)
        
        for n in range(3):        
            smallSamples = context.newString('AAA\n', style=dict(font=font.path, fontSize=24))
            newTextBox(smallSamples, parent=page, w=C2, h=80, ml=G/2, mb=L,
                       conditions=[Right2Right(), Float2Top(), Float2Left()],
                       fill=DEBUG_COLOR1)
        
            smallSamples = context.newString('AAA\n', style=dict(font=font.path, fontSize=24))
            newTextBox(smallSamples, parent=page, w=C2-2, h=80, mb=L,
                       conditions=[Right2Right(), Float2Top()], 
                       fill=DEBUG_COLOR1)

        glyphSetFrame = newRect(parent=page, mb=L, ml=G/2, padding=L,
                             borders=dict(line=INLINE, stroke=0, strokeWidth=0.5), 
                             conditions=[Right2Right(), Float2Top(), Float2Left(), 
                                 Fit2Right(), Fit2Bottom()], 
                             fill=DEBUG_COLOR2)
        
        glyphSet = context.newString('Subset of characters in Complete Font\n', 
            style=dict(font=font.path, fontSize=8, xTextAlign=CENTER,
            rParagraphTopSpacing=0.25,
            rParagraphBottomSpacing=0.5))
        glyphSet += context.newString(GLYPH_SET, 
            style=dict(font=font.path, fontSize=20, xTextAlign=CENTER, leading=32))
        newTextBox(glyphSet, parent=glyphSetFrame, padding=(1.5*L, L, L, L),
                             borders=dict(line=INLINE, stroke=0, strokeWidth=0.25), 
                             conditions=[Left2Left(), Fit2Right(), Top2Top(), 
                             Fit2Bottom() ], 
                             fill=DEBUG_COLOR3)
        
        pn += 1
    return pn
    
def makeDocument(families):
    u"""Create the main document in the defined size with a couple of automatic empty pages."""
    # Calculate the amount of pages to create
    numPages = 1 # Add one of the original page scan.
    for family in families:
        numPages += len(family) # Length of the family is the amount of fonts.
        
    doc = Document(w=W, h=H, title='Variable Font Sample Page', originTop=False, startPage=0, 
        autoPages=numPages, context=context, gridX=GRID_X, gridY=GRID_Y)

    pn = 0
    page = doc[pn]
    page.ch = 0 # No vertical grid
    page.padding = PADDING
    page.gridX = GRID_X
    newImage(ATF_PATH, x=0, y=0, w=W, parent=page)
    
    # Get default view from the document and set the viewing parameters.
    view = doc.view
    view.padding = INCH/2 # For showing cropmarks and such, make >=20*MM or INCH.
    view.showPageCropMarks = True # Won't show if there is not padding in the view.
    view.showPageFrame = SHOW_FRAMES # No frame in case PAPER_COLOR exists to be shown.
    view.showPagePadding = SHOW_FRAMES # No frame in case PAPER_COLOR exists to be shown.
    view.showPageRegistrationMarks = True
    view.showGrid = SHOW_GRID # Show GRID_X lines
    view.showPageNameInfo = True # Show file name and date of the document
    view.showTextOverflowMarker = False # Don't show marker in case Filibuster blurb is too long.

    # Build the pages for all fonts that include one of these patterns.
    pn += 1
    for family in families:
        pn = buildSpecimenPages(doc, family, pn)

    doc.solve()
    
    return doc

doc = makeDocument(FAMILIES)
doc.export(EXPORT_PATH) 
if DO_OPEN:
    os.system(u'open "%s"' % EXPORT_PATH)
  
print 'Done'
