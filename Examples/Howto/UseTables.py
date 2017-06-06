# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     UseTables.py
#

from __future__ import division # Make integer division result in float.
import pagebot # Import to know the path of non-Python resources.

from pagebot.style import getRootStyle, A4, CENTER, RIGHT, LEFT, NO_COLOR,TOP, BOTTOM, MM
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
from pagebot import newFS

from pagebot.conditions import *
from pagebot.elements import *
from pagebot.document import Document

PagePadding = 32
PageSize = 500

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/UseTables.pdf' 

def makeDocument():
    u"""Make a new document."""

    W = H = PageSize

    # Create a new document, default to the defined page size. 
    doc = Document(w=W, h=H, originTop=False, title='Text Flow', autoPages=2)
    
    view = doc.getView()
    view.padding = 40 # Aboid showing of crop marks, etc.
    view.showPageCropMarks = True
    view.showPageRegistrationMarks = True
    view.showPageFrame = False
    view.showPagePadding = False # Table already has background color
    view.showElementOrigin = False
    view.showElementDimensions = False
    
    # Get list of pages with equal y, then equal x.    
    #page = doc[0][0] # Get the single page from te document.
    page0 = doc.getPage(0) # Get page on pageNumber, first in row (this is only one now).
    page0.name = 'Page 1'
    page0.padding = PagePadding
    
    t = newTable(cols=6, rows=62, borders=0.5, parent=page0, 
        fill=0.85, conditions=[Fit(), Overflow2Next()],
        nextElement='nextTable', nextPage='Page 2')
    
    page1 = doc.getPage(1)
    page1.name = 'Page 2'
    page1.padding = PagePadding
    
    t = newTable(cols=0, rows=0, borders=0.5, parent=page1, 
        name='nextTable', fill=0.85, conditions=[Fit()])
        
    score = doc.solve() # Try to solve all pages.
    if score.fails:
        print score.fails

    #print t.w, t.h, t.elements, t.borders

    return doc # Answer the doc for further doing.
 
if __name__ == '__main__':

    Variable([
        dict(name='PagePadding', ui='Slider', args=dict(minValue=0, value=30, maxValue=100)),
        dict(name='PageSize', ui='Slider', args=dict(minValue=200, value=500, maxValue=PageSize)),
    ], globals())
           
    d = makeDocument()
    d.export(EXPORT_PATH) 

