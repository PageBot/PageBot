# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     DrawRedRectCenterPage.py
#
from pagebot import getFormattedString
from pagebot.style import getRootStyle, A5, BOTTOM, CENTER, MIDDLE
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
from pagebot.document import Document
from pagebot.elements import *
from pagebot.conditions import *
    
W, H = A5 

OriginTop = False

Variable([
    #dict(name='ElementOrigin', ui='CheckBox', args=dict(value=False)),
    dict(name='OriginTop', ui='CheckBox', args=dict(value=False)),
], globals())

def makeDocument():
    # Create new document with (w,h) size and fixed amount of pages.
    # Note that most of the rootStyle is cascading through the e.css('name') call,
    # except that values of x, y, z, w, h, d

    # Just to show here how to get the root style. If not altered, it can be omitted.
    # as Document( ) will create a RootStyle by default.
    rootStyle = getRootStyle()
    
    doc = Document(rootStyle, originTop=OriginTop, w=W, h=H, pages=1) 
    
    page = doc[0] # Get the first/single page of the document.
    
    # Make rect as page element centered with centered origin.
    newRect(fill=(1, 0, 0), parent=page, w=200, h=200,
        conditions=(Center2Center(), Middle2Middle()),
        xAlign=CENTER, yAlign=MIDDLE)
    # Solve the layout conditions of the red rectangle.
    # Show if one of the conditions failed to solve.
    score = page.solve()
    if score.fails:
        print 'Failed conditions', score.fails
        
    # Set the view parameters for the required output.
    view = doc.getView()
    view.w = view.h = W, H
    view.padding = 50 # Make view padding to show crop marks and frame
    view.showPageFrame = True # Show frame of the page in blue
    view.showPageCropMarks = True # Show crop marks
    view.showElementOrigin = True # Show alignment positions of the origin for each element.
    
    return doc
        
d = makeDocument()
d.export('_export/DrawRedRectCenterPage.pdf')
    
