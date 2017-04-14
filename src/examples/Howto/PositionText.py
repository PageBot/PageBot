# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     MakeABookCover.py
#
import myglobals 
import pagebot # Import to know the path of non-Python resources.
from pagebot import getFormattedString

# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, B4, CENTER, LEFT_ALIGN, TOP_ALIGN, BOTTOM_ALIGN, RIGHT_ALIGN
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
from pagebot.elements.document import Document
    
W, H = B4 

RS = getRootStyle(
    w = W,
    h = H,
    ml = 64,
    mt = 64,
    mr = 64,
    mb = 80,
    showElementInfo = False,
    showElementOrigin = True,
    originTop = False,
)

def makeDocument(rootStyle):
    u"""Demo random book cover generator."""
    
    # Create new document with (w,h) and fixed amount of pages.
    # Make number of pages with default document size.
    # Initially make all pages default with template
    doc = Document(rootStyle, pages=1) # One page, just the cover.
 
    page = doc[1] # Get the first/single page of the document.

    p = (400, 400, 0)
    
    fontSize = 40
    t1 = page.text('Book CoverSSS\nAAAA\nMMMM\nBook CoverSSS\nAAAA\nMMMM\n', point=p, style=rootStyle, name='Other element', font='Verdana', 
        fontSize=fontSize, leading=0, rLeading=1, align=LEFT_ALIGN,
        fill=(0, 1, 0), stroke=(0, 1, 0), textFill=(0, 0, 1))
    # Use text elemennt size as reference.
    e1 = page.rect(p, w=t1.w, h=t1.h, fill=(1, 0, 0), align=RIGHT_ALIGN, vAlign=BOTTOM_ALIGN)

    #e1.top = 400
    #t1.top = 400
    #e1.top = 400
    t1.y = 400
    #print e1.top, t1.top
    print t1.fs.fontAscender() - t1.fs.fontDescender()
    print t1.css('fontSize')
    print t1.w, t1.h
    print t1.getTextSize()
    return doc
        
d = makeDocument(RS)
d.drawPages()
    
