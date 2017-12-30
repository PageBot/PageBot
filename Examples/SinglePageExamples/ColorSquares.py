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
#     ColorSquares.py
#
#     This script generates a page with random color squares, indicating where their position is.
#     This script is using the style parameters "originTop", making the coordinate system run downwards.
#
from __future__ import division # Make integer division result in float.
#import pagebot # Import to know the path of non-Python resources.

from random import random
from drawBot import Variable
from pagebot import x2cx, y2cy
from pagebot.elements import *
from pagebot.document import Document
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
    
ElementOrigin = True
CropMarks = True
RegistrationMarks = True
PageFrame = True
PageNameInfo = True
ViewPadding = 64
PageSize = 500

GUTTER = 8 # Distance between the squares.
SQUARE = 10 * GUTTER # Size of the squares

EXPORT_PATH = '_export/ColorSquares.pdf' # Export in _export folder that does not commit in Git. Force to export PDF.

def makeDocument():
    u"""Make a new document, using the rs as root style."""

    #W = H = 120 # Get the standard a4 width and height in points.
    W = H = PageSize

    # Hard coded SQUARE and GUTTE, just for simple demo, instead of filling padding an columns in the root style.
    # Page size decides on the amount squares that is visible.
    # Page padding is centered then.
    sqx = int(W/(SQUARE + GUTTER)) # Whole amount of squares that fit on the page.
    sqy = int(H/(SQUARE + GUTTER))
    # Calculate centered paddings for the amount of fitting squares.
    # Set values in the rootStyle, so we can compare with column calculated square position and sizes.
    #rs['colH'] = rs['colW'] = SQUARE  # Make default colW and colH square.

    padX = (W - sqx*(SQUARE + GUTTER) + GUTTER)/2
    my = (H - sqy*(SQUARE + GUTTER) + GUTTER)/2


    doc = Document(w=W, h=H, title='Color Squares', originTop=False, autoPages=1)
    
    view = doc.getView()
    
    view.showElementOrigin = ElementOrigin
    view.showPageCropMarks = CropMarks
    view.showPageRegistrationMarks = RegistrationMarks
    view.showPageFrame = PageFrame
    view.showPageNameInfo = PageNameInfo
    view.padding = ViewPadding # Space around the view to accommodate cropmarks and registration marks.

    # Get list of pages with equal y, then equal x.    
    #page = doc[0][0] # Get the single page from te document.
    page = doc.getPage(0) # Get page on pageNumber, first in row (this is only one now).
    page.name = 'This demo page'
    
    page.w = W
    page.h = H
 
    page.padding3D = padX # Set all 3 paddings to same value
    page.gutter3D = GUTTER # Set all 3 gutters to same value

    #newRect((0, 0), w=square, h=square, parent=page, fill=(1, 0, 0), stroke=None) 

    for ix in range(sqx): # Run through the range of (0, 1, ...) number of horizontal squares
        for iy in range(sqy): # Same with vertical squares  
            # Place squares in random colors
            color1 = (random(), 0.1, 0.6)
            color2 = (random(), 0.1, 0.6)
            # Calculate the position for each square as combination of paddings and (ix, iy)
            p = padX + ix * (SQUARE + GUTTER), my + iy * (SQUARE + GUTTER) # Make 2-dimensional point tuple.
            # Create Rect object and place it in the page on position p
            e = newRect(p, w=SQUARE, h=SQUARE, parent=page, fill=color1, stroke=None) 
            # Create Rect object and place it in the page on position p
            newOval(p, w=SQUARE, h=SQUARE, parent=page, fill=color2, stroke=None)    
            # Now drawing with columns needs to align with the plain coordinate drawing.         
            newColRect(ix, iy, 1, 1,  fill=None, parent=page, stroke=0, strokeWidth=0.5)
            # Show coordinate and column/row index value. Don't show origin of the text box, by resetting
            # its style flag showElementOrigin=False 
            # Show coordinate and column/row index value
            # It may seem funny to beginning programmers to have a column/row index as zero
            # for the first column/row, but that is how counters work in Python.
            # The first element in a list has index 0.
            newText('%d, %d Column: %d, %d' % (p[0], p[1], 
                x2cx(p[0], e), # Calculate back to column index for checking.
                y2cy(p[1], e)), 
                # Position of the coordinate with a bit of offset.
                (p[0], p[1] + e.css('colH') + e.gh/4), 
                parent=page, textFill=0, fontSize=4, leading=0, 
                fill=None, stroke=None)

    # Note that in this stage nothing is drawn yet in DrawBot. Potentionally all element can still be moved around
    # added or deleted or moved to other pages.  
    return doc # Answer the doc for further doing.
 

if __name__ == '__main__': # If running from DrawBot
    Variable([
        dict(name='ElementOrigin', ui='CheckBox', args=dict(value=False)),
        dict(name='CropMarks', ui='CheckBox', args=dict(value=True)),
        dict(name='RegistrationMarks', ui='CheckBox', args=dict(value=True)),
        dict(name='PageFrame', ui='CheckBox', args=dict(value=True)),
        dict(name='PageNameInfo', ui='CheckBox', args=dict(value=True)),
        dict(name='ViewPadding', ui='Slider', args=dict(minValue=0, value=64, maxValue=200)),
        dict(name='PageSize', ui='Slider', args=dict(minValue=100, value=400, maxValue=800)),
    ], globals())
    d = makeDocument()
    d.export(EXPORT_PATH) 

