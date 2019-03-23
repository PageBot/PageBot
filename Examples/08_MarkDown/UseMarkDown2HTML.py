# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     UseMarkDown2HTML.py
#
#     This example script shows the sequence how to get from a MarkDown
#     file with embedded code blocks, using Typesetter and Composer
#     to create a HTML site, and then fill the pages with the MarkDown text.
#     
#     Also it illustrates how MarkDown code blocks and this calling 
#     applicatin communicate with each other through a shared "targets"
#     dictionary. 
#
import os, shutil

from pagebot.contexts.htmlcontext import HtmlContext
from pagebot.document import Document
from pagebot.elements import *
from pagebot.conditions import *
from pagebot.typesetter import Typesetter
from pagebot.composer import Composer
from pagebot.toolbox.color import color, blackColor, whiteColor
from pagebot.constants import *
from pagebot.toolbox.units import pt, em
from pagebot.elements.web.nanosite.siteelements import *

W, H = A4
PADDING = pt(40) # Simple page padding

# Path to the MarkDown source file
MARKDOWN_PATH = 'EmbeddedPython.md'
EXPORT_PATH = '_export/UseMarkdown2HTML'
MAMP_PATH = '/Applications/MAMP/htdocs/' 
SITE_NAME = 'UseMarkDown'
SITE_PATH = MAMP_PATH + SITE_NAME 

# In this example we'll be using DrawBotContext to write a PDF file of the document.
context = HtmlContext()

# Define the styles for the Typesetter, matching the tags that are using in the
# MarkDown file.
styles = dict(
    body=dict(
        fill=whiteColor,
        ml=9, mr=0, mt=0, mb=0,
        pl=em(3), pr=em(3), pt=em(3), pb=em(3),
        fontSize=pt(12),
        leading=em(1.4)),
    br=dict(leading=em(1.4)),
    h1=dict(textFill=color('red'), fontSize=pt(24), leading=em(1.4), 
        paragraphBottomSpacing=pt(12)),
    h2=dict(textFill=color(0.3), fontSize=pt(18), leading=em(1.4),
        paragraphTopSpacing=pt(12), paragraphBottomSpacing=pt(12)),
    p=dict(textFill=blackColor, fontSize=pt(12), leading=em(1.4)),
    li=dict(textFill=color('green'), tabs=pt(8, 16, 24, 36, 48), 
        fontSize=pt(12), leading=em(1.4), 
        indent=16, firstLineIndent=0)
)

# Create the overall document with the defined size.
viewId = 'Mamp'
site = Site(styles=styles)
doc = site.newDocument(viewId=viewId, autoPages=1, defaultImageWidth=MAX_IMAGE_WIDTH)

# Set the view parameters for the required output.
view = doc.view
view.padding = pt(40) # Make view padding to show crop marks and frame
view.showFrame = True # Show frame of the page in blue
view.showPadding = True
view.showCropMarks = True # Show crop marks
view.showRegistrationMarks = True
view.showNameInfo = True

view.resourcePaths = ('css','fonts','images','js')
view.jsUrls = (
    URL_JQUERY, 
    #URL_MEDIA, 
    'js/sitemain.js', 
    'js/jquery.bbslider.min.js'
)
# SiteView will automatic generate css/style.scss.css from assumed css/style.scss
view.cssUrls = (
    'fonts/webfonts.css', 'css/normalize.css', 
    #'css/nanostyle_css.py' # Will automatic call conversion by the theme.mood.
    'css/nanostyle.css', 
    #'css/style-org.css', 
    'css/jquery.bbslider.css'
)

# Read the markdown file, where all elements (embedded code blocks) are pasted
# on a galley element, in sequential order. No interpreting takes place yet.
t = Typesetter(context, styles=styles)
galley = t.typesetFile(MARKDOWN_PATH)

# Make a simplet template: one page with one column.
page = doc[1] # Get the first/single page of the document.
page.padding = PADDING # Set the padding of this page.

# Make a text box, fitting the page padding on all sides.
# The name "Box" is used to identiify the box that MarkDown text goes into.
newTextBox(parent=page, name='Box', conditions=[Fit()])

page.solve() # Solve the fitting condition.

# Create the Composer instance that will interpret the Typesetter galley.
composer = Composer(doc)

# Create the global targets dictionary with objects that can be used during
# interpretation of the markdown elements on the galley. The composer instance
# will run sequentially through the elements, executing the code blocks. 
# This may cause the shifting of target for the text elements to another block
# or another page.
targets = dict(doc=doc, page=page, box=page.select('Box'), composer=composer)
composer.compose(galley, targets=targets)

# Now the targets dictionary is filled with results that were created during
# execution of the code blocks, such as possible errors and warnings.
# Also it contains the latest “box”
print('Keys in target results:', targets.keys())
print('No errors:', targets['errors'])
print('Number of verbose feedback entries:', len(targets['verbose']))
print('Values created in the code block: aa=%s, bb=%s, cc=%s' % (targets['aa'], targets['bb'], targets['cc']))

if os.path.exists(SITE_PATH):
    shutil.rmtree(SITE_PATH) # Comment this line, if more safety is required. In that case manually delete.
doc.export(SITE_PATH)

if not os.path.exists(SITE_PATH):
    print('The local MAMP server application does not exist. Download and install from %s.' % view.MAMP_SHOP_URL)
    os.system(u'/usr/bin/open %s' % view.MAMP_SHOP_URL)
else:
    #t.doc.export('_export/%s.pdf' % NAME, multiPages=True)
    os.system(u'/usr/bin/open "%s"' % mampView.getUrl(SITE_NAME))
