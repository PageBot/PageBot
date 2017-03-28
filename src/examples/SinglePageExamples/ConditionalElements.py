# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     ValidatingElements.py
#
#     This script generates a fake article on a single page, using Filibuster text,
#     automatic layout template, Galley, Typesetter and Composer classes.
#     Its purpose is to show the use of Validator
#
import pagebot # Import to know the path of non-Python resources.
from pagebot import getFormattedString, textBoxBaseLines

# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, LEFT_ALIGN, A4
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
from pagebot.elements.document import Document
from pagebot.elements.galley import Galley
from pagebot.composer import Composer
from pagebot.typesetter import Typesetter
from pagebot.conditions import Condition, CenterX, LeftAligned, RightAligned, CenterY, TopAligned, BottomAligned

class FontSizeWidthRatio(Condition):
    def evaluate(self, e):
        if abs(e.x) <= self.tolerance and e.style.get('fontSize') < 20:
            return self.value
        return self.value * self.errorFactor
		
    def solve(self, e):
        if self.evaluate(e) < 0:
            e.style['fontSize'] = 19
            return self.value
        return self.value * self.errorFactor
	    
# For clarity, most of the OneValidatingPage.py example documenet is setup as a sequential excecution of
# Python functions. For complex documents this is not the best method. More functions and classes
# will be used in the real templates, which are available from the OpenSource PageBotTemplates repository.
    
W, H = A4
# The standard PageBot function getRootStyle() answers a standard Python dictionary, 
# where all PageBot values are filled by their default values. The root style is kept in RS
# as reference to for all ininitialzaiton of elements. 
# Each element uses the root style as copy and then modifies the values it needs. 
# Note that the use of style dictionaries is fully recursive in PageBot, implementing a cascading structure
# that is very similar to what happens in CSS.

RS = getRootStyle(
    conditions = [],
    fontSize = 10,
    rLeading = 0,
)

EXPORT_PATH = '_export/ValidatingElements.pdf' # Export in folder that does not commit un Git. Force to export PDF.

def makeDocument(rs):
    u"""Demo page composer."""
    
    # Create new document with (w,h) and fixed amount of pages.
    # Make number of pages with default document size.
    # Initially make all pages default with template
    doc = Document(rs, pages=1) 
 
    w = 400

    colorCondition = [
        #CenterX(),
        CenterY(),
        TopAligned(),
        #LeftAligned(), 
        #RightAligned(),
        #FontSizeWidthRatio(verbose=True)
    ]
    textCondition = [ # Center text in middle of the page, independent from size.
        CenterX(),
        CenterY(),
        #LeftAligned(), 
        #RightAligned(),
        #TopAligned(),
        #FontSizeWidthRatio(verbose=True)
    ]
    #point = (0, 0)
    #point = (W/2-w/2, 0)
    #point = (W-w, 0)
    point = (0, 0)
    
    # Change template of page 1
    page = doc[1]

    page.rect(point=point, style=rs, w=w, h=300, conditions=colorCondition, 
        fill=(1, 0.5, 0.5))
    page.rect(point=point, style=rs, w=w, h=100, conditions=colorCondition+[BottomAligned()], 
        fill=(1, 1, 0))
    eTextBox = page.textBox('', point=point, style=dict(fontSize=20), w=w, h=300, vacuumH=True, 
        conditions=textCondition)
      
    g = Galley() 
    t = Typesetter(doc, g)                
    blurbNames = (('h3', 'article_ankeiler'), ('h2', 'article_summary'), ('p', 'article'))
    blurbNames = (('h3', 'article_ankeiler'), ('p', 'article'))
    t.typesetFilibuster(blurbNames)
    
    # Fill the main flow of text boxes with the ML-->XHTML formatted text. 
    c = Composer(doc)
    c.compose(g, page, eTextBox.eId) # Use the eTextBox as target for the text.
        
    pageValue = page.evaluate()
    print 'Page value on evaluation:', pageValue
    # Try to solve the problems if evaluation < 0
    if pageValue < 0:
        page.solve()
    # Evaluate again, result should now be >= 0
    print 'Page value after solving the problems:', page.evaluate()
    
    return doc
        
d = makeDocument(RS)
d.export(EXPORT_PATH) 

    