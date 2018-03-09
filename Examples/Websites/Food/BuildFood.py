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
#     Build automatic website for designdesign.space, hosted in github.
#
#     http://designdesign.space
#     http://localhost:8888/designdesignspace/index.html
#
#
# 
import os

from pagebot.contexts import HtmlContext

from pagebot.typesetter import Typesetter
from pagebot.composer import Composer
from pagebot.publications.publication import Publication 
from pagebot.elements import *
from pagebot.conditions import *

# Path to markdown file, including Python code blocks.
MD_PATH = u"Content.md"
NAME = 'foodsite'
DOMAIN = 'foodsite'

DO_GIT = True
DO_MAMP = not DO_GIT

from pagebot.publications import Website

doc = Website(autoPages=0)

# Create a Typesetter for this document, then create pages and fill content. 
# As no Galley instance is supplied to the Typesetter, it will create one,
# or put the current page/box variables to where the MarkDown file indicates.
t = Typesetter(doc, tryExcept=False, verbose=False)
# Parse the markdown content and execute the embedded Python code blocks.
# The blocks, global defined feedback variables and text content are in the 
# typesetter t.galley.
# By default, the typesetter produces a single Galley with content and code blocks.
# In this case it directly writes into the boxes on the Website template pages.
t.typesetFile(MD_PATH)

if DO_MAMP:
    # Internal CSS file may be switched of for development.
    t.doc.info.cssPath = 'sources/pagebot.css'
    view = t.doc.newView('Mamp')

    if not os.path.exists(view.MAMP_PATH):
        print 'The local MAMP server application does not exist. Download and in stall from %s.' % view.MAMP_SHOP_URL 
        os.system(u'open %s' % view.MAMP_SHOP_URL)
    else:
        t.doc.build(path=NAME)
        #t.doc.export('_export/%s.pdf' % NAME, multiPages=True)
        os.system(u'open "%s"' % view.getUrl(NAME))
elif DO_GIT:
    # Make sure outside always has the right generated CSS
    t.doc.info.cssPath = 'sources/pagebot.css'
    view = t.doc.newView('Git')
    t.doc.build(path=NAME)
    # Open the css file in the default editor of your local system.
    os.system('git pull; git add *;git commit -m "Updating website changes.";git pull; git push')
    os.system(u'open "%s"' % view.getUrl(DOMAIN))
else:
    print 'Select DO_MAMP or DO_GIT'
print 'Done' 


