#!/usr/bin/env python3
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
#     ExportCSS.py
#
#     U N D E R  C O N S T R U C T I O N
#
import os
#import pagebot # Import to know the path of non-Python resources.

# Creation of the RootStyle (dictionary) with all
# available default style parameters filled.
from pagebot.constants import LEFT, TOP, BOTTOM

from pagebot.conditions import *
from pagebot.elements import newTextBox
from pagebot.document import Document

DoTextFlow = False
PagePadding = 32
PageSize = 500

# Export in _export folder that does not commit in Git. Force to export PDF.
# The .css extension triggers the CssBuilder to be used for file export.
# Currently a style dumps as CSS comment is exported. Needs to be adjusted
# to filter and translate info real CSS.
EXPORT_PATH = '_export/ExportCSS.css'

def makeDocument():
    """Make a new document."""

    W = H = PageSize

    # Create a new document, default to the defined page size.
    doc = Document(w=W, h=H, originTop=False, title='Text Flow', autoPages=2)

    view = doc.getView()
    view.padding = 0 # Aboid showing of crop marks, etc.
    view.showCropMarks = True
    view.showRegistrationMarks = True
    view.showFrame = True
    view.showPadding = True
    view.showOrigin = True
    view.showDimensions = False

    # Get list of pages with equal y, then equal x.
    #page = doc[1][0] # Get the single page from te document.
    page0 = doc.getPage(1) # Get page on pageNumber,
                           # first in row (this is only one now).
    page0.name = 'Page 1'
    page0.padding = PagePadding

    s = ''
    for n in range(10):
        s += ('(Line %d) Volume of text defines the box height.'
              ' Volume of text defines the box height.\n') % (n+1)
        h1 = None

    newTextBox(s,
               name='CSSTextBox1',
               parent=page0, padding=4, x=100, font='Verdana', h=h1,
               mb=20, mr=10, # Conditions make the
                                       # element move to
                                       # top-left of the page.
               # And the condition that there should be no overflow,
               # otherwise the text box will try to solve it.
               conditions=[Left2Left(), Fit2Width(), Float2Top()],
               # Position of the origin of the element.
               # Just to show where it is.
               # Has no effect on the position conditions.
               yAlign=BOTTOM, xAlign=LEFT,
               leading=5, fontSize=9, textFill=blackColor,
               strokeWidth=0.5, fill=color(9, stroke=noColor)
    newTextBox('', # Empty box, will get the
                   # overflow from e1, if there is any.
               name='CSSTextBox2', # Flow reference by element.name
               parent=page0, padding=4, x=100, h=200,
               conditions=[Left2Left(), Fit2Width(), Float2Top()],
               yAlign=TOP, fill=whiteColor, stroke=noColor)

    score = doc.solve() # Try to solve all pages.
    if score.fails:
        print(score.fails)

    return doc # Answer the doc for further doing.

# Document current view will recognize .css extension to call the CssBuilder.
d = makeDocument()
d.export(EXPORT_PATH)
print('Generated CSS code saved as file', EXPORT_PATH)
# Open the css file in the default editor of your local system.
os.system(u'open "%s"' % EXPORT_PATH)
print('Done')

