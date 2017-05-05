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
#     This script generates a page with random color squares, indicating where their position is.
#     This script is using the style parameters "originTop", making the coordinate system run downwards.
#
from __future__ import division # Make integer division result in float.
import pagebot # Import to know the path of non-Python resources.

# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, A4, CENTER, NO_COLOR,TOP_ALIGN, BOTTOM_ALIGN
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
from pagebot.document import Document
from pagebot.elements.rect import Rect
# Import all layout condition classes
from pagebot.conditions import *
  
W = H = 500

G = 8 # Distance between the squares.
SQ = 4 * G # Size of the squares
ORIGIN_TOP = True

# The standard PageBot function getRootStyle() answers a standard Python dictionary, 
# where all PageBot style entries are filled by their default values. The root style is kept in RS
# as reference for the ininitialization of all elements. 
# Each element uses the root style as copy and then modifies the values it needs. 
# Note that the use of style dictionaries is fully recursive in PageBot, implementing a cascading structure
# that is very similar to what happens in CSS.

RS = getRootStyle(w=W, h=H,
    showElementOrigin = True, # Show origin marker on element, to see their alignments.
    originTop = ORIGIN_TOP,
)
#for key, value in RS.items():
#    print key, value

EXPORT_PATH = '_export/AlignElements.pdf' # Export in _export folder that does not commit in Git. Force to export PDF.

def makeDocument(rs):
    u"""Make a new document, using the rs as root style."""

    # Hard coded padding, just for simple demo, instead of filling padding an columns in the root style.
    rs['pl'] = rs['pr'] = rs['pt'] = rs['pb'] = SQ
    rs['cw'] = rs['ch'] = SQ
    rs['gw'] = rs['gh'] = G # Gutter width and gutter height.

    doc = Document(rs, pages=1)
    
    page = doc[1] # Get the single page from te document.
    
    # Position square in the 4 corners of the page area.
    # Notice that their alignment (left) does not matter for the conditions.
    page.rect(w=SQ, h=SQ, conditions=(Right2Right(),Top2Top()), fill=0.7)
    page.rect(w=SQ, h=SQ, conditions=(Left2Left(),Bottom2Bottom()), fill=0.7)
    page.rect(w=SQ, h=SQ, conditions=(Left2Left(),Top2Top()), fill=0.7)
    page.rect(w=SQ, h=SQ, conditions=(Right2Right(),Bottom2Bottom()), fill=0.7)

    # Make new container for adding elements inside with alignment.
    cnt = page.container(w=W-6*SQ, h=H-6*SQ, fill=(0.8,0.8,0.8,0.8), margin=SQ, vAlign=BOTTOM_ALIGN, stroke=0,
        conditions=(Center2Center(), Top2Top()))

    r = Rect(w=SQ, h=SQ, stroke=None, 
        conditions=(Bottom2BottomSidex(),Left2Left()), fill=(1, 1, 0))
    cnt.append(r)
    print r.parent
    # Solve the layout placement conditions on the page by moving the
    # elements that are not on the right positions (which is all of them,
    # because we did not add point attributes when creating them.
    page.solve() 
    
    return doc # Answer the doc for further doing.
        
d = makeDocument(RS)
d.export(EXPORT_PATH) 

