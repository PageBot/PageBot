# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     PositionText.py
#
import pagebot # Import to know the path of non-Python resources.
from pagebot import newFS

# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, B4, CENTER, LEFT, TOP, BOTTOM, RIGHT
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
from pagebot.document import Document
from pagebot.elements import *
    
W, H = 500, 500 

OriginTop = False

def makeDocument():
    # Create new document with (w,h) and fixed amount of pages.
    # Make number of pages with default document size.
    # Initially make all pages default with template
    rootStyle = getRootStyle()
    
    doc = Document(rootStyle, originTop=OriginTop, w=W, h=H, pages=1) 

    page = doc[0] # Get the first/single page of the document.
    page.size = W, H
    
    view = doc.getView()
    view.w = view.h = W, H
    view.padding = 300
    view.showPageFrame = True
    view.showPageCropMarks = True
    view.showElementOrigin = True
    
    title = 'Book Cover'
    fontSize = 40
    t1 = newTextBox(title, x=100, y=100, parent=page, w=400, h=200, 
    name='Other element', font='Verdana', 
        fontSize=fontSize, leading=0, rLeading=1, xAlign=LEFT, yAlign=BOTTOM,
        fill=(0, 1, 0), stroke=(0, 1, 0), textFill=(0, 0, 1))

    return doc

if __name__ == '__main__': 
    Variable([
        #dict(name='ElementOrigin', ui='CheckBox', args=dict(value=False)),
        dict(name='OriginTop', ui='CheckBox', args=dict(value=False)),
    ], globals())
           
    d = makeDocument()
    d.drawPages()
        
