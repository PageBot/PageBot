# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     FloatTextOnTopOfElement.py
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
from pagebot import newFS

from pagebot.conditions import *
from pagebot.elements import *
from pagebot.document import Document
    
RedSize = 100
YellowSize = 30
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
EXPORT_PATH = '_export/FloatTextOnTopOfElement.pdf' 


def makeDocument():
    u"""Make a new document."""

    W = H = PageSize

    doc = Document(w=W, h=H, originTop=False, title='Color Squares', autoPages=1)
    
    view = doc.getView()
    view.padding = 0 # Aboid showing of crop marks, etc.
    view.showElementOrigin = False
    view.showTextOverflowMarker = False
    
    # Get list of pages with equal y, then equal x.    
    #page = doc[0][0] # Get the single page from te document.
    page = doc.getPage(0) # Get page on pageNumber, first in row (this is only one now).
    page.name = 'This is a demo page for floating child elements'
    page.padding = PagePadding
    
    # Show margin of page, can also be done by
    # view.showPagePadding = True
    newRect(fill=0.9, parent=page, margin=0, 
        conditions=(Left2Left(), Fit2Right(), Bottom2Bottom(), Fit2Height()))
    
    redContainer = newRect(fill=(1, 0, 0), pb=10, w=RedSize, h=RedSize, 
        padding=10, conditions=(Left2Left(), Bottom2Bottom()), parent=page) 
    
    # Yellow square
    yellowSquare = newRect(fill=(1, 1, 0), z=8, w=YellowSize, 
        h=YellowSize, parent=redContainer, xAlign=CENTER, yAlign=TOP,
        conditions=(Center2Center(), Bottom2Bottom()))
         
    # Blue square in different z=layer. No interaction with Floating on other z-layers.
    blueSquare = newRect(fill=(0, 1, 1), z=10, w=50, h=50, 
        parent=redContainer, xAlign=CENTER, 
        conditions=(Top2Top(), Center2Center(),)) 
   
    # Centered string
    fs = newFS('Float on top of yellow', 
        style=dict(font='Verdana', fontSize=7, xTextAlign=CENTER,
        textFill=0))
    # Text falls through the yr2 (with differnt z) and lands on yellowSquare by Float2BottomSide()    
    newTextBox(fs, name='Caption', parent=redContainer, z=8,
        fill=(0, 1, 0), strokeWidth=0.5, stroke=(1, 1, 0),
        conditions=[ Fit2Width(), Float2BottomSide()], 
        padding=3,
    )    
    score = page.solve()
    if score.fails:
        print score.fails
        
    return doc # Answer the doc for further doing.
   
Variable([
    #dict(name='ElementOrigin', ui='CheckBox', args=dict(value=False)),
    dict(name='RedSize', ui='Slider', args=dict(minValue=100, value=100, maxValue=500)),
    dict(name='YellowSize', ui='Slider', args=dict(minValue=10, value=30, maxValue=500)),
    dict(name='PagePadding', ui='Slider', args=dict(minValue=10, value=30, maxValue=100)),
    dict(name='PageSize', ui='Slider', args=dict(minValue=100, value=400, maxValue=800)),
], globals())

d = makeDocument()
d.export(EXPORT_PATH) 

