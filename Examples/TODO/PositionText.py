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
#     PositionText.py
#
#     Hard position a text box on an (x, y) position.
#
import os
from random import choice
from pagebot.elements import newText
from pagebot import getContext
from pagebot.constants import LEFT, BOTTOM
# Document is the main instance holding all information
# about the document togethers (pages, styles, etc.)
from pagebot.document import Document
from pagebot.toolbox.hyphenation import words

context = getContext()

USE_FLAT = True
EXPORT_PATH = '_export/PositionText.png'
W, H = 500, 500
C = 40 # Column
G = 10
M = 20 # Margin

def makeDocument():
    """Create new document with (w,h) and fixed amount of pages.
    Make number of pages with default document size.
    Initially make all pages default with template."""

    smallWords = []
    for word in words(): # Get all English hyphenating words.
      if len(word) in (4,5,6):
        smallWords.append(word)

    title = 'Position Text Box Example' # Using plain string, style values

    doc = Document(originTop=False, title=title,
                   w=W, h=H,
                   autoPages=1,
                   context=context)

    page = doc[1] # Get the first/single page of the document.
    page.size = W, H

    view = doc.view
    view.w = view.h = W, H
    view.padding = 40
    view.showFrame = True
    view.showCropMarks = True
    view.showOrigin = True # Show the alignment position
                                  # of elements as plus-mark.
    fontSize = 18
    cellHeight = int(fontSize*4)
    for cx in range(0, W-2*M, C):
      for cy in range(0, H-2*M, cellHeight):
        newText(choice(smallWords), # Random small word
                   x=cx, y=cy, # Position from left-bottom of page side
                                 # (not page padding)
                   parent=page,
                   w=C-G, h=cellHeight, # Size of the element.
                   padding=5, # Padding inside text box for all 4 sides equal.
                   fill=color(0.4, 0.6, 1), # Rectangle fill color
                   stroke=color(1, 0, 0), # Rectangle stroke color
                   strokeWidth=10,
                   # Below style values that apply to the content
                   font='Verdana',
                   fontSize=fontSize,
                   leading=em(1), # Absolute and relative leading.
                   xAlign=LEFT, yAlign=BOTTOM, # Set origin of element to left-bottom
                   textFill=(0, 0, 1)) # Color of the text.
    # Return the generated document to the caller.
    return doc

d = makeDocument()
d.export(EXPORT_PATH)

if USE_FLAT:
    os.system(u'open "%s"' % EXPORT_PATH)

print('Done')

