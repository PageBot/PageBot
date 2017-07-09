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
#     PositionText.py
#
#     Hard position a text box on an (x, y) position.
#
import pagebot # Import to know the path of non-Python resources.
from pagebot import newFS

# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, B4, CENTER, LEFT, TOP, BOTTOM, RIGHT
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
from pagebot.document import Document
from pagebot.elements import *
    
W, H = 500, 500 

def makeDocument():
    u"""Create new document with (w,h) and fixed amount of pages.
    Make number of pages with default document size.
    Initially make all pages default with template."""
    
    doc = Document(originTop=False, w=W, h=H, autoPages=1) 

    page = doc[0] # Get the first/single page of the document.
    page.size = W, H
    
    view = doc.getView()
    view.w = view.h = W, H
    view.padding = 40
    view.showPageFrame = True
    view.showPageCropMarks = True
    view.showElementOrigin = True # Show the alignment position of elements as plus-mark.
    
    title = 'Book Cover' # Using plain string, style values from from text box element.
    fontSize = 40
    e = newTextBox(title, # Text inside the text box
        name='Other element', # Optinal (unique) name of element. Otherwise e.eId is used.
        x=100, y=100, # Position from left-bottom of page side (not page padding)
        parent=page,
        w=400, h=200, # Size of the element. Since x = 100 and W = 500, this "manually" fits.
        padding=5, # Padding inside text box for all 4 sides equal.
        fill=(0.4, 0.6, 1), stroke=(1, 0, 0), strokeWidth=13, # Rectangle fill, stroke colors 
        # Below style values that apply to the content
        font='Verdana', 
        fontSize=fontSize, 
        leading=0, rLeading=1, # Absolute and relative leading.
        xAlign=LEFT, yAlign=BOTTOM, # Set origin of element to left-bottom
        textFill=(0, 0, 1) # Color of the text.
    )
    # Return the generated document to the caller.
    return doc

if __name__ == '__main__': 
           
    d = makeDocument()
    d.drawPages()
        
