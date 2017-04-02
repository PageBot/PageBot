# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
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
from pagebot.style import getRootStyle, A4, CENTER, NO_COLOR,TOP_ALIGN, BOTTOM_ALIGN
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
from pagebot.elements.document import Document
    
W = H = 120 # Get the standard a4 width and height in points.
W = H = 500

GUTTER = 8 # Distance between the squares.
SQUARE = 10 * GUTTER # Size of the squares

# The standard PageBot function getRootStyle() answers a standard Python dictionary, 
# where all PageBot style entries are filled by their default values. The root style is kept in RS
# as reference for the ininitialization of all elements. 
# Each element uses the root style as copy and then modifies the values it needs. 
# Note that the use of style dictionaries is fully recursive in PageBot, implementing a cascading structure
# that is very similar to what happens in CSS.

RS = getRootStyle()
RS['w'] = W
RS['h'] = H

# Setting value for demo purpose, it is style default, using the elements origin as top-left. 
# Change to False will show origin of elements in their bottom-left corner.
if 1: # TOP
    RS['originTop'] = True
    RS['vAlign'] = TOP_ALIGN 
else:
    RS['originTop'] = False 
    RS['vAlign'] = BOTTOM_ALIGN 
#for key, value in RS.items():
#    print key, value

EXPORT_PATH = '_export/ColorSquares.pdf' # Export in _export folder that does not commit in Git. Force to export PDF.

def makeDocument(rs):
    u"""Make a new document, using the rs as root style."""

    # Hard coded margins, just for simple demo, instead of filling margins an columns in the root style.
    square = SQUARE # Size of a square. Page margins are calculated from the amount that fit on the page.
    gutter = GUTTER
    sqx = int(W/(square + gutter)) # Whole amount of squares that fit on the page.
    sqy = int(H/(square + gutter))
    # Calculate centered margins for the amount of fitting squares.
    # Set values in the rootStyle, so we can compare with column calculated square position and sizes.
    rs['ml'] = mx = (W - sqx*(square + gutter) + gutter)/2
    rs['mt'] = rs['mb'] = my = (H - sqy*(square + gutter) + gutter)/2
    rs['cw'] = rs['ch'] = square
    rs['g'] = gutter

    doc = Document(rs, pages=1)
    
    page = doc[1] # Get the single page from te document.
    for ix in range(sqx): # Run through the range of (0, 1, ...) number of horizontal squares
        for iy in range(sqy): # Same with vertical squares
            # Place squares in random colors
            color1 = (random(), 0.1, 0.6)
            color2 = (random(), 0.1, 0.6)
            # Calculate the position for each square as combination of margins and (ix, iy)
            p = mx + ix * (square + gutter), my + iy * (square + gutter) # Make 2-dimensional point tuple.
            # Create Rect object and place it in the page on position p
            page.rect(p, w=square, h=square, fill=color1, stroke=None) 
            # Create Rect object and place it in the page on position p
            page.oval(p, w=square, h=square, fill=color2, stroke=None)    
            # Now drawing with columns needs to align with the plain coordinate drawing.         
            e = page.cRect(ix, iy, 1, 1, fill=None, stroke=0, strokeWidth=0.5)
            # Mark the origin coordinate 
            page.oval(p, w=gutter, h=gutter, fill=None, stroke=0, align=CENTER, vAlign=CENTER)
            page.text('%d, %d (%d, %d)' % (p[0], p[1], 
                x2cx(p[0], page), # Calculate back to column index for checking.
                y2cy(p[1], page)), 
                (p[0]+6, p[1]+6), # Position of the coordinate with a bit of offset.
                textFill=0, fontSize=5, leading=0)

            #page.rect((10, 10), w=mx, h=my, fill=(0, 1, 0))
    # Note that in this stage nothing is drawn yet in DrawBot. Potentionally all element can still be moved around
    # added or deleted or moved to other pages.  
    return doc # Answer the doc for further doing.
        
d = makeDocument(RS)
d.export(EXPORT_PATH) 

