# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     AlignElements.py
#
#     This script generates a page with aligned square, showing how conditional placement works.
#
import pagebot # Import to know the path of non-Python resources.

# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, A4, CENTER, NO_COLOR,TOP, BOTTOM
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
from pagebot.document import Document
from pagebot.elements import *
# Import all layout condition classes
from pagebot.conditions import *
  
W = H = 500

G = 8 # Distance between the squares.
SQ = 8 * G # Size of the squares

# The standard PageBot function getRootStyle() answers a standard Python dictionary, 
# where all PageBot style entries are filled by their default values. The root style is kept in RS
# as reference for the ininitialization of all elements. 
# Each element uses the root style as copy and then modifies the values it needs. 
# Note that the use of style dictionaries is fully recursive in PageBot, implementing a cascading structure
# that is very similar to what happens in CSS.

RS = getRootStyle(w=W, h=H,
    originTop = False,
    yAlign = BOTTOM,
)
#for key, value in RS.items():
#    print key, value

EXPORT_PATH = '_export/AlignElements.pdf' # Export in _export folder that does not commit in Git. Force to export PDF.

def makeDocument(rs):
    u"""Make a new document, using the rs as root style."""

    doc = Document(rs, pages=1)
    
    page = doc[0] # Get the single page from te document.
    
    # Hard coded padding, just for simple demo, instead of filling padding an columns in the root style.
    page.padding = SQ
    #page.cw = page.ch = SQ
    #page.gw = page.gh = G
    
    # Make new container for adding elements inside with alignment.
    cnt = newRect(w=W-2*SQ, h=H-2*SQ, fill=(0.8, 0.8, 0.8, 0.4), parent=page, margin=SQ, yAlign=BOTTOM, 
        xAlign=CENTER, stroke=None, conditions=(Center2Center(), Middle2Middle()))

    page.solve()
    newRect(w=30, h=30, name='RedRect', parent=cnt, fill=(1, 0, 0), yAlign=TOP,
        conditions=(Center2Center(), Bottom2Bottom()))
    print cnt.solve() 
   
    view = doc.getView()
    view.padding = 0 # Don't show cropmarks and such.
    view.showElementOrigin = True
    view.showElementInfo = False
       
    return doc # Answer the doc for further doing.
        
d = makeDocument(RS)
d.export(EXPORT_PATH) 

