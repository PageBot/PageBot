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
import os, copy

from pagebot.contexts import defaultContext as context
from pagebot.style import INCH
from pagebot.document import Document
from pagebot.fonttoolbox.objects.family import getFamily, getFamilies
from pagebot.elements import newTextBox, newRect, newText, newImage
from pagebot.toolbox.transformer import int2Color
from pagebot.conditions import *

W = 7.3*INCH
H = 11*INCH
PADDING = 36, 30, 72, 72 # Page padding top, right, bottom, left
COLUMNS = 4
G = 8
GRID_X = ((200, G), (150, G), (150, G))

# 1923 American Type Founders Specimen Book & Catalog
ATF_PATH = 'images/ATFArtcraftBold.png'

# Build the specimen pages for the font names that include these patterns.
FAMILIES = (getFamily('Bungee'), getFamily('AmstelvarAlpha'))

# Export in _export folder that does not commit in Git. Force to export PDF.
DO_OPEN = False
EXPORT_PATH = '_export/ATFSpecimen-%s.pdf' 

# Some parameters from the original book
PAPER_COLOR = int2Color(0xF4EbC9) # Approximation of paper color of original specimen.
RED_COLOR = int2Color(0xAC1E2B) # Red color used in the original specimen
  
def buildSpecimenPages(doc, family, pn):
    for font in family.getFonts():
        page = doc[pn]
        page.padding = PADDING
        page.gridX = GRID_X
        pageTitle = font.info.familyName + ' ' + font.info.styleName
        # Add filling rectangle for background color of the old paper book.
        newRect(z=-1, w=W, h=H, parent=page, fill=PAPER_COLOR)
        # During development, draw the template scan as background
        newImage(ATF_PATH, x=0, y=0, w=W, parent=page)
        
        # Centered title: family name and style name of the current font.
        titleBs = context.newString(pageTitle, style=dict(font=font.path, w=W-120, textFill=0))
        newText(titleBs, x=50, y=100, parent=page, w=400, conditions=[Top2Top(), Fit2Width()])
        pn += 1
    return pn
    
def makeDocument(families):
    u"""Create the main document in the defined size with a couple of automatic empty pages."""
    # Calculate the amount of pages to create
    numPages = 0
    for family in families:
        numPages += len(family) # Length of the family is the amount of fonts.
        
    doc = Document(w=W, h=H, title='Variable Font Sample Page', originTop=False, startPage=0, 
        autoPages=numPages, context=context, gridX=GRID_X)

    pn = 0
    page = doc[pn]
    page.padding = PADDING
    page.gridX = GRID_X
    newImage(ATF_PATH, x=0, y=0, w=W, parent=page)
    # Get default view from the document and set the viewing parameters.
    view = doc.view
    view.padding = INCH/2 # To show cropmarks and such, make >=20*MM or INCH.
    view.showPageCropMarks = True # Won't show if there is not padding in the view.
    view.showPageFrame = True # No frame in case PAPER_COLOR exists to be shown.
    view.showPagePadding = True # No frame in case PAPER_COLOR exists to be shown.
    view.showPageRegistrationMarks = True
    view.showGrid = False
    view.showPageNameInfo = True # Show file name and date of the document
    view.showTextOverflowMarker = False # Don't show marker in case Filibuster blurb is too long.

    # Build the pages for all fonts that include one of these patterns.
    for family in families:
        pn = buildSpecimenPages(doc, family, pn)

    # Solve remaining layout and size conditions.
    score = doc.solve()
    if score.fails:
        print 'Conditiond failed', score.fails 

    return doc

doc = makeDocument(FAMILIES)
doc.export(EXPORT_PATH) 
if DO_OPEN:
    os.system(u'open "%s"' % EXPORT_PATH)
  
print 'Done'
