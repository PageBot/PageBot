# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     OnePageSquares.py
#
#     This script generates a page with random color square. 
#
from __future__ import division # Make integer division result in float.
import pagebot # Import to know the path of non-Python resources.

# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, A4, CENTER, NO_COLOR
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
from pagebot.elements.document import Document
    
W, H = A4 # Get the standard a4 width and height in points.
#W = H = 500

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

EXPORT_PATH = '_export/OnePageSquares.pdf' # Export in _export folder that does not commit in Git. Force to export PDF.

def makeDocument(rs):
    u"""Make a new document, using the rs as root style."""
    doc = Document(rs, pages=1)

    # Hard coded margins, just for simple demo, instead of filling margins an columns in the root style.
    square = SQUARE # Size of a square. Page margins are calculated from the amount that fit on the page.
    gutter = GUTTER
    sqx = int(W/(square + gutter)) # Whole amount of squares that fit on the page.
    sqy = int(H/(square + gutter))
    # Calculate centered margins for the amount of fitting squares.
    mx = (W - sqx*(square + gutter) + gutter)/2
    my = (H - sqy*(square + gutter) + gutter)/2

    page = doc[1] # Get the single page from te document.
    for ix in range(sqx):
        for iy in range(sqy):
            # Place squares in random colors
            color = (random(), 0.1, 0.6)
            p = mx + ix * (square + gutter), my + iy * (square + gutter) # Make 2-dimensional point tuple.
            page.rect(p, w=square, h=square, fill=color, stroke=None) # Create Rect object and place it in the page on position p
            page.oval(p, w=gutter, h=gutter, fill=None, stroke=0, align=CENTER, valign=CENTER)
            page.text('%d,%d' % p, (p[0]+5, p[1]-2), style=rs, textFill=0.5, fontSize=6, scaleX=1)
    # Note that in this stage nothing is drawn yet in DrawBot. Potentionally all element can still be moved around
    # added or deleted or moved to other pages.  
    return doc # Answer the doc for further doing.
        
d = makeDocument(RS)
d.export(EXPORT_PATH) 

