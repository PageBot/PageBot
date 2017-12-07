#!/usr/bin/env python
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
#     PositionText.py
#
#     Hard position a text box on an (x, y) position.
#
import os
import pagebot # Import to know the path of non-Python resources.

from pagebot.style import LEFT, BOTTOM
# Document is the main instance holding all information
# about the document togethers (pages, styles, etc.)
from pagebot.document import Document

W, H = 500, 500

def makeDocument():
    u"""Create new document with (w,h) and fixed amount of pages.
    Make number of pages with default document size.
    Initially make all pages default with template."""

    doc = Document(originTop=False,
                   w=W, h=H,
                   autoPages=1,
                   context=defaultContext)

    page = doc[0] # Get the first/single page of the document.
    page.size = W, H

    view = doc.view
    view.w = view.h = W, H
    view.padding = 40
    view.showPageFrame = True
    view.showPageCropMarks = True
    view.showElementOrigin = True # Show the alignment position
                                  # of elements as plus-mark.

    title = 'Book Cover' # Using plain string, style values
                         # from text box element.
    fontSize = 40
    newTextBox(title, # Text inside the text box
        name='Other element', # Optinal (unique) name of element.
                              # Otherwise e.eId is used.
        x=100, y=100, # Position from left-bottom of page side
                      # (not page padding)
        parent=page,
        w=400, h=200, # Size of the element.
                      # Since x = 100 and W = 500, this "manually" fits.
        padding=5, # Padding inside text box for all 4 sides equal.
        fill=(0.4, 0.6, 1), # Rectangle fill color
        stroke=(1, 0, 0), # Rectangle stroke color
        strokeWidth=10,
        # Below style values that apply to the content
        font='Verdana',
        fontSize=fontSize,
        leading=0, rLeading=1, # Absolute and relative leading.
        xAlign=LEFT, yAlign=BOTTOM, # Set origin of element to left-bottom
        textFill=(0, 0, 1) # Color of the text.
    )
    # Return the generated document to the caller.
    return doc

d = makeDocument()
d.export(EXPORT_PATH)

if USE_FLAT:
    os.system(u'open "%s"' % EXPORT_PATH)

print('Done')

