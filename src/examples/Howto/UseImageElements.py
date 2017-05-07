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
from pagebot.style import getRootStyle, A4, CENTER, NO_COLOR,TOP, BOTTOM, MM
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
from pagebot import getFormattedString

from pagebot.conditions import *
from pagebot.elements import *
from pagebot.document import Document
    
ElementOrigin = True
CropMarks = True
RegistrationMarks = True
PageFrame = True
PageNameInfo = True
PagePadding = 64
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
  
# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/UseImages.pdf' 


Variable([
    #dict(name='ElementOrigin', ui='CheckBox', args=dict(value=False)),
    dict(name='CropMarks', ui='CheckBox', args=dict(value=True)),
    dict(name='RegistrationMarks', ui='CheckBox', args=dict(value=True)),
    dict(name='PageFrame', ui='CheckBox', args=dict(value=True)),
    dict(name='PageNameInfo', ui='CheckBox', args=dict(value=True)),
    dict(name='PagePadding', ui='Slider', args=dict(minValue=-10, value=64, maxValue=200)),
    dict(name='ViewPadding', ui='Slider', args=dict(minValue=0, value=64, maxValue=200)),
    dict(name='PageSize', ui='Slider', args=dict(minValue=100, value=400, maxValue=800)),
], globals())

def makeDocument(rs):
    u"""Make a new document, using the rs as root style."""

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
    rs['colH'] = rs['colW'] = SQUARE  # Make default colW and colH square.

    #padX = (W - sqx*(SQUARE + GUTTER) + GUTTER)/2
    my = (H - sqy*(SQUARE + GUTTER) + GUTTER)/2

    doc = Document(rootStyle=rs, title='Color Squares', autoPages=1)
    
    view = doc.getView()
    
    view.showElementOrigin = ElementOrigin
    view.showPageCropMarks = CropMarks
    view.showPageRegistrationMarks = RegistrationMarks
    view.showPageFrame = PageFrame
    view.showPageNameInfo = PageNameInfo
    print view.style
    view.padding = ViewPadding # Space around the view to accommodate cropmarks and registration marks.

    # Get list of pages with equal y, then equal x.    
    #page = doc[0][0] # Get the single page from te document.
    page = doc.getPage(0) # Get page on pageNumber, first in row (this is only one now).
    page.name = 'This demo page'
    page.padding = PagePadding
    
    page.w = W
    page.h = H
 
    page.padding3D = PagePadding # Set all 3 paddings to same value
    page.gutter3D = GUTTER # Set all 3 gutters to same value
    """
    im = newImage('images/cookbot10.jpg', (50, 50, 10), padding=0, parent=page, w=200, conditions=(Top2Top(), Fit2Width()), elasticH=True, yAlign=BOTTOM,
        frameFill=(0, 1, 0, 0.3), 
        frameStroke=(1, 0, 0)
    )
    if im.image:
        print im.image.size
    # Give parent on creation, to have the css chain working.
    """
    rr = newRect(fill=(1, 0, 0), parent=page) # conditions=(Top2Top(), Fit2Width()), parent=page)
    
    cap = newTextBox('This is the caption. ', w=rr.w, name='Caption', parent=rr,
        font='Verdana', conditions=[Left2LeftSide(), Fit2Width(), Float2TopSide()], elasticH=True,
        fontSize=8, textFill=0, frameFill=(0, 0, 1, 0.3), frameStroke=(0, 0, 1),
    )
    
    print rr.elements
    rr.solve()
    #print cap.evaluate()
    #print cap.isFloatOnBottom(1)
    #score = page.solve()
    #if score.fails:
    #    print 'Failed solving conditions', score.fails
    #print im.x, im.y, im.getVacuumElementsBox(), im.left, im.top, im.right, im.bottom
    #print cap.evaluate()
    #print im.x, im.y, im.getVacuumElementsBox()
    
    return doc # Answer the doc for further doing.
        
d = makeDocument(RS)
d.export(EXPORT_PATH) 

