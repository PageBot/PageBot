# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     UseTextFlows.py
#
#     If a TextBox as self.nextElement defined as name for another text box on the
#     same page, then overflow of self will go into the other text box.

from __future__ import division # Make integer division result in float.
import pagebot # Import to know the path of non-Python resources.

from pagebot import x2cx, y2cy
# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, A3, EuropeBusinessCard, INCH, CENTER, RIGHT, LEFT, NO_COLOR,TOP, BOTTOM, MM
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)

PH, PW = A3 # Landscape for collection of pages in thumb view.
W, H = EuropeBusinessCard

ViewPadding = INCH/5
PagePadding = INCH/5

from pagebot.conditions import *
from pagebot.elements import *
from pagebot.document import Document

fontNames = []
for fontName in installedFonts():
    if 'BitcountMonoDouble' in fontName:
        fontNames.append(fontName)
#print fontNames

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/TYPETRBusinessCards.pdf' 

def makeDocument():
    u"""Make a new document."""
    # Create a new document, default to the defined page size. 
    doc = Document(w=W, h=H, originTop=False, title='Text Flow', autoPages=2)
    
    view = doc.getView()
    view.padding = ViewPadding # Aboid showing of crop marks, etc.
    view.showPageCropMarks = True
    view.showPageRegistrationMarks = True
    view.showPageFrame = True
    view.showPagePadding = True
    view.showElementOrigin = True
    view.showElementDimensions = False
    view.showTextOverflowMarker = False
    
    padding = 12
    
    # Get list of pages with equal y, then equal x.    
    #page = doc[0][0] # Get the single page from te document.
    page = doc.getPage(0) # Get page on pageNumber, first in row (this is only one now).
    page.name = 'Page 1'
    page.padding = padding
    
    BODY_FONT = 'BitcountMonoDouble-RegularCircle'
    
    fs = doc.context.newString('TYPETR',
                               w=W-padding*2,
                               style=dict(font=BODY_FONT,
                                          fontSize=56,
                                          leading=0,
                                          textFill=0))
    fs += doc.context.newString("""
Petr van Blokland
Designer|Lecturer|Developer

Rietveld 56 | 2611 LM Delft 
The Netherlands
Email buro@petr.com
typetr.typenetwork.com
Twitter @petrvanblokland
Mobile +31 6 2421 9502""", style=dict(font=BODY_FONT,
                                      fontSize=9,
                                      leading=0,
                                      textFill=0))

    e1 = newTextBox(fs, 
        name='ElasticTextBox1',
        parent=page, font=BODY_FONT, pt=6,
        # And the condition that there should be no overflow, otherwise the text box
        # will try to solve it.     
        conditions=[Left2Left(), Fit2Width(), Float2TopSide()],
        # Position of the origin of the element. Just to show where it is.
        # Has no effect on the position conditions. 
    )
       
    score = doc.solve() # Try to solve all pages.
    if score.fails:
        print score.fails

    return doc # Answer the doc for further doing.
 

       
d = makeDocument()
d.export(EXPORT_PATH) 

