# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Free to use. Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     DesignDesignSpace.py
#
#     Build automatic website for designdesign.space
# 
import os
from pagebot.typesetter import Typesetter
from pagebot.composer import Composer
from pagebot.publications.publication import Publication
from pagebot.elements import *
from pagebot.conditions import *

# Path to markdown file, including Python code blocks.
MD_PATH = u"DesignDesignSpace.md"

# Export in _export folder that does not commit in Git. Force to export PDF.
# The .html and .css extensions triggers the HtmlBuilder and CssBuilder to be used for file export.
# If the MAMP server application not installed, a browser is opened on their website to download it.
MAMP_PATH = '/Applications/MAMP/htdocs/'
MAMP_PAGEBOT_PATH = MAMP_PATH + 'pagebot/designdesignspace/'
EXPORT_PATH_HTML = MAMP_PAGEBOT_PATH + 'index.html'
EXPORT_PATH_CSS = MAMP_PAGEBOT_PATH + 'main.css'
MAMP_LOCAL_URL = 'http://localhost:8888/pagebot/designdesignspace/index.html'
MAMP_SHOP_URL = 'https://www.mamp.info/en/' # In cade MAMP does not exist, open on their website to download and install.

# Create an unbound Typesetter instance (trying to find a Poster
# (inheriting from Document) instance in one of the codeblock results. 
# If no Galley instance is supplied to the Typesetter, it will create one.
t = Typesetter()
# Parse the markdown content and execute the embedded Python code blocks.
# The blocks, global defined variables and text content are in the 
# typesetter t.galley.
t.typesetFile(MD_PATH)
#print t.codeBlocks
# The typesetter produced a single Galley with content and code blocks.
# Now use a composer (automatic "designer") to fit the pieces together.
# Takes a galley as soruce and a document for target pages. 
Composer().compose(t.galley, t.doc)

if 0: # Print some results of the typesetter
    # Typesetter found document definition inside content.
    print 'Book title:', t.doc.title, round(t.doc.w), round(t.doc.h)
    # Multiple code blocks found with identical identifier.
    # Added counter 'Views_0' to 'Views' to make it unique. 
    print 'Found code blocks: %d' % len(t.codeBlocks.keys())
    #print t.galley.elements[0].text
    #page = t.doc[0]
    #print page.padding
    #print page.w, page.h

if 1: # Debugging, show the pages with their names.
    print t.doc.css('gridL')
    for templateName, template in t.doc.templates.items():
        print templateName, template.name
    for pn, pages in t.doc.getSortedPages():
        for page in pages:
            print '\t', page, page.w, page.h, page.template.name
            #page.isLeft(), page.isRight(), page.getGridColumns()

if 1:
    # Views define the way documents are exported.
    # Add space for cropmarks and registrations marks
    view = t.doc.getView()
    view.padding = 30
    view.showPageNameInfo = True
    view.showPagePadding = False # No need, as we are drawing the grid
    view.showPageCropMarks = True
    view.showPageRegistrationMarks = True
    view.showPageFrame = True 
    view.showGrid = True
    
    view.style['viewGridStroke'] = (0, 0, 1)
    view.style['viewGridStrokeWidth'] = 0.5

if not os.path.exists(MAMP_PATH):
    print 'The local MAMP server application does not exist. Download and in stall from %s.' % MAMP_SHOP_URL 
    os.system(u'open %s' % MAMP_SHOP_URL)
else:

    t.doc.export(EXPORT_PATH_CSS)
    print 'Generated CSS code saved as file', EXPORT_PATH_CSS
    t.doc.export(EXPORT_PATH_HTML)
    print 'Generated HTML and CSS code saved as files', EXPORT_PATH_HTML
    # Open the css file in the default editor of your local system.
    os.system(u'open "%s"' % MAMP_LOCAL_URL)
    print 'Done' 

