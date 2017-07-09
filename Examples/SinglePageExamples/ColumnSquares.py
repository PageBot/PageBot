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
#     ColorSquares.py
#
#     This script generates a page with random color squares, indicating where their position is.
#     This script is using the style parameters "originTop", making the coordinate system run downwards.
#
from __future__ import division # Make integer division result in float.
import pagebot # Import to know the path of non-Python resources.

from pagebot import x2cx, y2cy
# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, A4, CENTER, NO_COLOR,TOP, BOTTOM, MM
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
from pagebot import newFS, setFillColor, setStrokeColor, x2cx, cx2x, y2cy, cy2y, z2cz, cz2z, w2cw, cw2w, h2ch, ch2h, d2cd, cd2d

from pagebot.elements import *
from pagebot.document import Document
    
ElementOrigin = True
CropMarks = True
RegistrationMarks = True
PageFrame = True
PageNameInfo = True
ViewPadding = 64
PageSize = 500

GUTTER = 8 # Distance between the squares.
SQUARE = 10 * GUTTER # Size of the squares

# The standard PageBot function getRootStyle() answers a standard Python dictionary, 
# where all PageBot style entries are filled by their default values. The root style is kept in RS
# as reference for the ininitialization of all elements. 
# Each element uses the root style as copy and then modifies the values it needs. 
# Note that the use of style dictionaries is fully recursive in PageBot, implementing a cascading structure
# that is very similar to what happens in CSS.


RS = getRootStyle(w=PageSize, h=PageSize)
# Setting value for demo purpose, it is style default, using the elements origin as top-left. 
# Change to False will show origin of elements in their bottom-left corner.
if 0: # TOP
    RS['originTop'] = True
    RS['yAlign'] = TOP 
else:
    RS['originTop'] = False 
    RS['yAlign'] = BOTTOM 
  
#for key, value in RS.items():
#    print key, value

EXPORT_PATH = '_export/ColorSquares.pdf' # Export in _export folder that does not commit in Git. Force to export PDF.

def makeDocument(rs):
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
    rs['ch'] = rs['cw'] = SQUARE  # Make default column width and column height square.

    padX = (W - sqx*(SQUARE + GUTTER) + GUTTER)/2
    my = (H - sqy*(SQUARE + GUTTER) + GUTTER)/2


    doc = Document(w=W, h=H, rootStyle=rs, originTop=False, title='Color Squares', autoPages=1)
    
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

    for ix in range(sqx): # Run through the range of (0, 1, ...) number of horizontal squares
        for iy in range(sqy): # Same with vertical squares  
            # Place squares in random colors
            color1 = (0.1, random(), 0.6)
            color2 = (0.1, random(), 0.6)
            # Create Rect object and place it in the page on column/row index posiition
            e = newColRect(ix, iy, 1, 1, parent=page, fill=color1, stroke=None) 
            # Create Rect object and place it in the page on the same column/row index position.
            newColOval(ix, iy, 1, 1, parent=page, fill=color2, stroke=None)    
            # Now drawing with point coordinates needs to align with the column positions. 
            # Test by drawing a rectangle on the same position.        
            # No need to draw the origin marker of each element. That is done by the style flag
            # showElementOrigin = True
            p = padX + ix * (SQUARE + GUTTER), my + iy * (SQUARE + GUTTER) # Make 2-dimensional point tuple.
            newRect(p, w=SQUARE, h=SQUARE, parent=page, fill=None, stroke=0, strokeWidth=0.5)
            # Show coordinate and column/row index value. Don't show origin of the text box, by resetting
            # its style flag showElementOrigin=False 
            newText('%d, %d Column: %d, %d' % (p[0], p[1], 
                x2cx(p[0], e), # Calculate back to column index for checking.
                y2cy(p[1], e)), 
                (p[0], p[1] + e.css('colH') + e.gh/4), # Position of the coordinate with a bit of offset.
                parent=page, textFill=0, fontSize=4, leading=0, 
                fill=None, stroke=None)

    # Note that in this stage nothing is drawn yet in DrawBot. Potentionally all element can still be moved around
    # added or deleted or moved to other pages.  
    return doc # Answer the doc for further doing.
   
if __name__ == '__main__':

    Variable([
        dict(name='ElementOrigin', ui='CheckBox', args=dict(value=False)),
        dict(name='CropMarks', ui='CheckBox', args=dict(value=True)),
        dict(name='RegistrationMarks', ui='CheckBox', args=dict(value=True)),
        dict(name='PageFrame', ui='CheckBox', args=dict(value=True)),
        dict(name='PageNameInfo', ui='CheckBox', args=dict(value=True)),
        dict(name='ViewPadding', ui='Slider', args=dict(minValue=0, value=64, maxValue=200)),
        dict(name='PageSize', ui='Slider', args=dict(minValue=100, value=400, maxValue=800)),
    ], globals())

    d = makeDocument(RS)
    d.export(EXPORT_PATH) 

