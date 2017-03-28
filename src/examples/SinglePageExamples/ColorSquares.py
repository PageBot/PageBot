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
import pagebot # Import to know the path of non-Python resources.
from pagebot import getFormattedString, textBoxBaseLines

# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, A4
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
from pagebot.elements.document import Document
    
W, H = A4 # Get the standard a4 width and height in points.

# The standard PageBot function getRootStyle() answers a standard Python dictionary, 
# where all PageBot values are filled by their default values. The root style is kept in RS
# as reference to for all ininitialzaiton of elements. 
# Each element uses the root style as copy and then modifies the values it needs. 
# Note that the use of style dictionaries is fully recursive in PageBot, implementing a cascading structure
# that is very similar to what happens in CSS.

RS = getRootStyle()

EXPORT_PATH = '_export/OnePageSquares.pdf' # Export in folder that does not commit in Git. Force to export PDF.

def makeDocument(rs):
    u"""Demo page composer."""

    doc = Document(rs, pages=1)

    mx = 25
    my = 20
    onePage = doc[1]
    for ix in range(5):
        for iy in range(7):
            # Place squares in random colors
            color = (random(), 0.1, 0.6)
            onePage.rect(mx+ix*110, my+iy*110, 100, 100, fill=color)
    
    print 'Positions:', onePage.getPositions().keys()
    #print onePage.getElementsPosition()  
    
    return doc
        
d = makeDocument(RS)
d.export(EXPORT_PATH) 

