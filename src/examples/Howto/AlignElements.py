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
from pagebot.style import getRootStyle, A4, CENTER, NO_COLOR, TOP, BOTTOM, MIDDLE, RIGHT, LEFT
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
from pagebot.elements.document import Document
from pagebot.elements import Rect, Oval
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
    
    if 0:
        # Position square in the 4 corners of the page area.
        # Notice that their alignment (left) does not matter for the conditions.
        for X in (Right2Right(), Left2Right(), Right2Left(), Left2Left()):
            for Y in (Bottom2Bottom(), Top2Bottom(), Bottom2Top(), Top2Top()):
                for xAlign in (LEFT, RIGHT):
                    for yAlign in (TOP, BOTTOM):
                        page.rect(w=SQ, h=SQ, conditions=(X, Y), align=xAlign, yAlign=yAlign, fill=0.7)

    # Make new container for adding elements inside with alignment.
    cnt = page.container(w=W-6*SQ, h=H-6*SQ, fill=1, margin=SQ, 
        align=LEFT, yAlign=TOP, stroke=0,
        pr=10, pt=10, pb=10, pl=30,
        conditions=(Right2Right(), Top2Top()))
    cnt.solve()
    
    r1 = cnt.oval((0,0), w=SQ, h=SQ, stroke=None, originTop=False, ZZconditions=(Left2Center(),Middle2Middle()), fill=(1, 1, 0))
    cnt.appendElement(r1)
    
    
    cnt2 = cnt.container((0, 0), w=300, h=300, fill=(0.5, 0.5, 0), margin=SQ, 
        align=LEFT, yAlign=TOP, stroke=0,
        pr=10, pt=10, pb=10, pl=30)
    cnt2.solve()

    r2 = Rect((10, 10), w=SQ, h=SQ, originTop=False, stroke=None, XXconditions=(Top2Top(),Left2Left()), fill=(1, 0, 0))
    cnt2.appendElement(r2)

    # Solve the layout placement conditions on the page by moving the
    # elements that are not on the right positions (which is all of them,
    # because we did not add point attributes when creating them.
    #page.solve() 
    print cnt.elements
        
    return doc # Answer the doc for further doing.
        
d = makeDocument(RS)
d.export(EXPORT_PATH) 

