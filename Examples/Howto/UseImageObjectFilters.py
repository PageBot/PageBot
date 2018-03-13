#!/usr/bin/env python
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
#     UseImageObjectFilters.py
#
#     This script generates page that show the behavior and working of the DrawBot
#     ImageObject filters.
#
from __future__ import division # Make integer division result in float.

from pagebot.contexts import defaultContext as context
from pagebot.contexts.platform import getResourcesPath
from pagebot.fonttoolbox.objects.family import getFamily
from pagebot.style import TOP, BOTTOM, A4
from pagebot.conditions import *
from pagebot.elements import *
from pagebot.document import Document
# Document is the main instance holding all information about the
# document together (pages, styles, etc.)

W, H = A4

IMAGE_PATH = getResourcesPath() + '/images/peppertom_lowres.png'

family = getFamily('Roboto')
font = family.findFont(weight=400)
fontItalic = family.findFont(weight=400, italic=True)

GUTTER = 8 # Distance between the squares.
SQUARE = 10 * GUTTER # Size of the squares
PADDING = 20

FILTER_TYPES = {
}

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/UseImageElements.pdf' 

def makeDocument():
    u"""Make a new document."""

    # Hard coded SQUARE and GUTTER, just for simple demo, instead of filling padding an columns in the root style.
    # Page size decides on the amount squares that is visible.
    # Page padding is centered then.
    sqx = int(W/(SQUARE + GUTTER)) # Whole amount of squares that fit on the page.
    sqy = int(H/(SQUARE + GUTTER))
    # Calculate centered paddings for the amount of fitting squares.
    # Set values in the rootStyle, so we can compare with column calculated square position and sizes.
    #rs['colH'] = rs['colW'] = SQUARE  # Make default colW and colH square.

    #padX = (W - sqx*(SQUARE + GUTTER) + GUTTER)/2
    my = (H - sqy*(SQUARE + GUTTER) + GUTTER)/2

    doc = Document(w=W, h=H, originTop=False, title='Color Squares', autoPages=1, context=context)
    
    view = doc.getView()
    view.padding = 0 # Aboid showing of crop marks, etc.
    view.showElementOrigin = False
    
    # Get list of pages with equal y, then equal x.    
    #page = doc[1[0] # Get the single page from te document.
    page = doc[1] # Get page on pageNumber, first in row (this is only one now).
    page.name = 'This is a demo page for floating child elements'
    page.padding = PADDING
    
    page.gutter3D = GUTTER # Set all 3 gutters to same value

    for n in range(4):
        img = newImage(IMAGE_PATH, (50, 50, 10), padding=0,
                       parent=page, w=150, h=150, #clipRect=(120, 120, 1440, 440),
                       conditions=(Right2Right(),
                                   Float2Top(),
                                   Float2Left(),
                                   SolveBlock(),
                                   #Shrink2BlockBottom()
                                   ),
                       yAlign=BOTTOM,
                       #fill=(0, 1, 0, 0.3),
                       #stroke=(1, 0, 0)
                       )
        # Give parent on creation, to have the css chain working.
    
        # Caption falls through the yr2 (with differnt z) and lands on yr1 by Float2BottomSide()    
        captionStyle = dict(font=font.path, fontSize=11, textFill=0)
        captionConditions = (Fit2Width(), Float2Top())
        fs = context.newString('Captions float below the image', style=captionStyle)
        img.caption = newTextBox(fs, name='Caption', z=0, conditions=captionConditions, 
            padding=4, yAlign=TOP, 
                #strokeWidth=0.5, 
                #fill=(0, 0, 1, 0.3), 
                #stroke=(0, 0, 1),
            )
    
    score = page.solve()
    if score.fails:
        print score.fails

    #print img.h
    #for e in img.elements:
    #    print e.h

    return doc # Answer the doc for further doing.
 
d = makeDocument()
d.export(EXPORT_PATH) 

