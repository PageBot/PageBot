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
#
from __future__ import division # Make integer division result in float.
import os
import pagebot # Import to know the path of non-Python resources.

from pagebot import x2cx, y2cy
# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, CENTER, RIGHT, LEFT, NO_COLOR,TOP, BOTTOM, perc
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
from pagebot import newFS

from pagebot.conditions import *
from pagebot.elements import *
from pagebot.document import Document

DoTextFlow = False   
padding = 32

# Export in _export folder that does not commit in Git. Force to export PDF.
# The .html and .css extensions triggers the HtmlBuilder and CssBuilder to be used for file export.
# If the MAMP server application not installed, a browser is opened on their website to download it.
MAMP_PATH = '/Applications/MAMP/htdocs/'
MAMP_PAGEBOT_PATH = MAMP_PATH + 'pagebot/designdesignspace/'
EXPORT_PATH_HTML = MAMP_PAGEBOT_PATH + 'index.html'
MAMP_LOCAL_URL = 'http://localhost:8888/pagebot/designdesignspace/index.html'
MAMP_SHOP_URL = 'https://www.mamp.info/en/' # In cade MAMP does not exist, open on their website to download and install.

def makeDocument():
    u"""Make a new document."""

    W = H = 1000, 600

    # Create a new document, default to the defined page size. 
    doc = Document(w=W, h=H, originTop=False, title='Text Flow', autoPages=2)
    
    view = doc.getView()
    print view.viewId, doc.views
    view.padding = 30 # Aboid showing of crop marks, etc.
    view.showPageCropMarks = True
    view.showPageRegistrationMarks = True
    view.showPageFrame = True
    view.showPagePadding = True
    view.showElementOrigin = True
    view.showElementDimensions = False
    view.showElementInfo = False
    
    # Get list of pages with equal y, then equal x.    
    #page = doc[0][0] # Get the single page from te document.
    page0 = doc.getPage(0) # Get page on pageNumber, first in row (this is only one now).
    page0.name = 'Page 1'
    page0.padding = padding
    
    s = ''
    for n in range(10):
        s += '(Line %d) Volume of text defines the box height. Volume of text defines the box height. \n' % (n+1)
    if DoTextFlow:
        h1 = 120 # Fox on a given height, to show the text flowing to the e2 element.
    else:
        h1 = None  
          
    e1 = newTextBox(s, 
        name='ElasticTextBox1',
        nextElement='ElasticTextBox2', # Overflow goes here.
        parent=page0, padding=4, x=100, w=perc(100), font='Verdana', h=h1,
        mb=20, mr=10,       # Conditions make the element move to top-left of the page.
        # And the condition that there should be no overflow, otherwise the text box
        # will try to solve it.     
        conditions=[Left2Left(), Float2Top(), Overflow2Next()],
        # Position of the origin of the element. Just to show where it is.
        # Has no effect on the position conditions. 
        yAlign=BOTTOM, xAlign=LEFT,
        leading=5, fontSize=9, textFill=0, strokeWidth=0.5, fill=0.9, stroke=None,
    )
    e2 = newTextBox('', # Empty box, will get the overflow from e1, if there is any.
        name='ElasticTextBox2', # Flow reference by element.name 
        nextElement='ElasticTextBox3', nextPage='Page 2',
        parent=page0, padding=4, x=100, w=perc(100), h=200, 
        conditions=[Right2Right(), Float2Top(), Fit2Bottom(), Overflow2Next()], yAlign=TOP,  fill=1, stroke=None,
    )
    # Get next page, to show flow running over page breaks.
    page1 = doc[1]
    page1.name = 'Page 2'
    page1.padding = padding

    e3 = newTextBox('', # Empty box, will get the overflow from e2, if there is any.
        name='ElasticTextBox3', # Flow reference by element.name
        parent=page1, padding=4, w=perc(100),  
        conditions=[Right2Right(), Float2Top(), Fit2Bottom()], 
        yAlign=TOP,  fill=1, stroke=None)
        
    score = doc.solve() # Try to solve all pages.
    if score.fails:
        print score.fails

    return doc # Answer the doc for further doing.
 

doc = makeDocument()

if not os.path.exists(MAMP_PATH):
    print 'The local MAMP server application does not exist. Download and in stall from %s.' % MAMP_SHOP_URL 
    os.system(u'open %s' % MAMP_SHOP_URL)
else:
    doc.export(EXPORT_PATH_HTML)
    # Open the css file in the default editor of your local system.
    os.system(u'open "%s"' % MAMP_LOCAL_URL)
    print 'Done' 

