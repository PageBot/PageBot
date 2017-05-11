# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#Z
#     UseElasticTextBox.py
#
from __future__ import division # Make integer division result in float.
import pagebot # Import to know the path of non-Python resources.

from pagebot import x2cx, y2cy
# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, A4, CENTER, NO_COLOR,TOP, BOTTOM, MM
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
from pagebot import getFormattedString

from pagebot.conditions import *
from pagebot.elements import *
from pagebot.document import Document
    
PagePadding = 64
PageSize = 500

GUTTER = 8 # Distance between the squares.
SQUARE = 10 * GUTTER # Size of the squares

# The standard PageBot function getRootStyle() answers a standard Python dictionary, 
# where all PageBot style entries are filled by their default values. The root style is kept in RS
# as reference for the ininitialization of all elements. 
# Each element uses the root style as copy and then modifies the values it needs. 
# Note that the use of style dictionaries is fully recursive in PageBot, implementing a cascading structure
# that is very similar to what happens in CSS.

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/UseElasticTextBox.pdf' 

BoxWidth = 200

def makeDocument():
    u"""Make a new document."""

    #W = H = 120 # Get the standard a4 width and height in points.
    W = PageSize
    H = PageSize

    # Hard coded SQUARE and GUTTE, just for simple demo, instead of filling padding an columns in the root style.
    # Page size decides on the amount squares that is visible.
    # Page padding is centered then.
    sqx = int(W/(SQUARE + GUTTER)) # Whole amount of squares that fit on the page.
    sqy = int(H/(SQUARE + GUTTER))
    # Calculate centered paddings for the amount of fitting squares.
    # Set values in the rootStyle, so we can compare with column calculated square position and sizes.
    #rs['colH'] = rs['colW'] = SQUARE  # Make default colW and colH square.

    #padX = (W - sqx*(SQUARE + GUTTER) + GUTTER)/2
    my = (H - sqy*(SQUARE + GUTTER) + GUTTER)/2

    doc = Document(w=W, h=H, originTop=False, title='Color Squares', autoPages=1)
    
    view = doc.getView()
    view.padding = 0 # Aboid showing of crop marks, etc.
    view.showElementOrigin = True
    view.showElementDimensions = True
    
    # Get list of pages with equal y, then equal x.    
    #page = doc[0][0] # Get the single page from te document.
    page = doc.getPage(0) # Get page on pageNumber, first in row (this is only one now).
    page.name = 'This is a demo page for floating child elements'
    page.padding = PagePadding
    
    page.gutter3D = GUTTER # Set all 3 gutters to same value

    tb = newTextBox('Volume of text defines the box height. ' * 10+'\n\n', 
        name='ElasticTextBox', 
        parent=page, padding=4, x=100, w=BoxWidth, font='Verdana',         
        conditions=[Left2Left(), Float2Top()], yAlign=TOP, leading=5, 
        fontSize=9, textFill=0, strokeWidth=0.5, fill=0.85, stroke=None,
    )
    tb = newTextBox('Volume of text defines the box height. ' * 10+'\n\n', 
        name='ElasticTextBox', 
        parent=page, padding=4, x=100, w=BoxWidth, font='Verdana',         
        conditions=[Right2Right(), Float2Top()], yAlign=TOP, leading=5, 
        fontSize=9, textFill=0, strokeWidth=0.5, fill=0.65, stroke=None,
    )
    score = page.solve()
    if score.fails:
        print score.fails

    return doc # Answer the doc for further doing.
 
if __name__ == '__main__':


    Variable([
        #dict(name='ElementOrigin', ui='CheckBox', args=dict(value=False)),
         dict(name='BoxWidth', ui='Slider', args=dict(minValue=50, value=300, maxValue=800)),
        dict(name='PageSize', ui='Slider', args=dict(minValue=100, value=400, maxValue=800)),
    ], globals())
           
    d = makeDocument()
    d.export(EXPORT_PATH) 

