# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     HandleDocWithPages.py
#
#     Test handling of pages in a doc.
#
import pagebot # Import to know the path of non-Python resources.

from pagebot.document import Document
from pagebot.elements import *
from pagebot.conditions import *

W, H = 100, 130

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/HandleDocWithPages.pdf' 

def makeDocument():
    u"""Make a new document."""

    doc = Document(w=W, h=H, originTop=False, autoPages=1)
    print doc.pages
    
    page = doc[0] # Get the single page from te document.
    page.name = 'First page'
    
    # Position square in the 4 corners of the page area.
    # Notice that their alignment (left) does not matter for the conditions.
    newTextBox(page.name, w=30, h=30, parent=page, pl=3,pt=3,    
        conditions=(Center2Center(),Middle2Middle()), fill=0.7)

    page.solve()
       
    view = doc.getView()
    view.w, view.h = W, H
    view.padding = 0 # Don't show cropmarks and such.
       
    return doc # Answer the doc for further doing.
        
d = makeDocument()
d.export(EXPORT_PATH) 

