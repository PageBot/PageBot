# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     AmstelvarSpecimen.py
#
import pagebot # Import to know the path of non-Python resources.

# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, A4, CENTER, RIGHT, LEFT, NO_COLOR,TOP, BOTTOM, MM
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
from pagebot import newFS

from pagebot.conditions import *
from pagebot.elements import *
from pagebot.document import Document
from pagebot.fonttoolbox.objects.font import Font
from pagebot.elements.variablefonts.variablecube import VariableCube
from pagebot.fonttoolbox.variablefontbuilder import getVariableFont

PagePadding = 32
PageSize = 500

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/AmstelvarSpecimen.pdf' 

FONT_PATH = pagebot.getFontPath()
fontPath = FONT_PATH + 'fontbureau/AmstelvarAlpha-Variations.ttf'

GLYPH_NAME = 'B'
CIRCLE_ELEMENT_FILL = 1

def makeDocument(fontPath):
    u"""Make a new document."""

    f = Font(fontPath) # Get PageBot Font instance of Variable font.
   
    W = H = PageSize

    # Create a new document, default to the defined page size. 
    doc = Document(w=W, h=H, originTop=False, title='Text Flow', autoPages=1)
    
    view = doc.getView()
    view.padding = 0 # Aboid showing of crop marks, etc.
    view.showPageCropMarks = True
    view.showPageRegistrationMarks = True
    view.showPageFrame = True
    view.showPagePadding = True
    view.showElementOrigin = False
    view.showElementDimensions = False
    
    # Get list of pages with equal y, then equal x.    
    #page = doc[0][0] # Get the single page from te document.
    page = doc.getPage(0) # Get page on pageNumber, first in row (this is only one now).
    page.name = 'Page 1'
    page.padding = PagePadding
    
    fs = newFS(f.info.familyName + ' ' + f.info.styleName, 
        style=dict(font=f.name, fontSize=18, textFill=0))
    _, th = textSize(fs)
    title = newTextBox(fs, conditions=[Top2Top(), Fit2Width()],
        parent=page, h=th*1.2)
    
    circle = VariableCircle(f, s=GLYPH_NAME, name='VariableCircleSpeciment',
        parent=page, padding=4, x=100, fontSize=84,
        maxW=W-2*PagePadding, minW=100,      
        # Conditions make the element move to top-left of the page.
        # And the condition that there should be no overflow, otherwise the text box
        # will try to solve it.     
        conditions=[Float2Top(), Fit2Bottom(), Center2Center()],
        # Position of the origin of the element. Just to show where it is.
        # Has no effect on the position conditions. 
        yAlign=BOTTOM, xAlign=LEFT, fill=CIRCLE_ELEMENT_FILL, borders=0,
    )
    
    print circle.w, circle.h
    
    score = doc.solve() # Try to solve all pages.
    if score.fails:
        print score.fails

    # To avoid circular dependent conditions, we correct the position of the title
    # on left to that the position of the circle has become.
    title.pl = circle.x - page.pl
    
    return doc # Answer the doc for further doing.
 
       
d = makeDocument(fontPath)
d.export(EXPORT_PATH) 

