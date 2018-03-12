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
#     MakeABookCover.py
#
#     Needs filling in with content.
#
from pagebot.contexts import defaultContext as context
from random import random # Used for random color palet.

# Create random title and names
from pagebot.contributions.filibuster.blurb import blurb

from pagebot.toolbox.transformer import darker
# Get function to find the Roboto family (in this case installed in the PageBot repository
from pagebot.fonttoolbox.objects.family import getFamily
# Creation of the RootStyle (dictionary) with all
# available default style parameters filled.
from pagebot.style import getRootStyle, B4, CENTER, MIDDLE, TOP 

# Document is the main instance holding all information
# about the document togethers (pages, styles, etc.)
from pagebot.document import Document

# Import element layout conditions.
from pagebot.conditions import *
from pagebot.elements import newRect, newTextBox
   
# For clarity, most of the MakeABookCover.py example document is setup
# as a sequential excecution of Python functions. For complex documents
# this is not the best method. More functions and classes will be used in the
# real templates, which are available from the PageBotTemplates repository.

W, H = B4
W -= 48 # Make a bit more narrow format.

# Export in folder that does not commit to Git. Force to export PDF.
EXPORT_PATH = '_export/ABookCover.pdf'

family = getFamily('Roboto')
fontRegular = family.findFont('Regular')
fontBold = family.findFont('Bold')
fontItalic = family.findFont('Italic')

def makeDocument():
    u"""Demo random book cover generator."""

    # Create new document with (w,h) and fixed amount of pages.
    # Make number of pages with default document size.
    # Initially make all pages default with template
    doc = Document(w=W, h=H, title='A Demo Book Cover', autoPages=1, context=context,
        originTop=False) # One page, just the cover.

    page = doc[1] # Get the first/single page of the document.
    page.name = 'Cover'
    
    # Get the current view of the document. This allows setting of
    # parameters how the document is represented on output.
    view = doc.view
    view.w, view.h = W, H
    # Set view options. Full list is in elements/views/baseviews.py
    view.padding = 40 # Showing cropmarks and registration marks
                      # need >= 20 padding of the view.
    view.showPageRegistrationMarks = True
    view.showPageCropMarks = True
    view.showPageFrame = True
    view.showPagePadding = False
    view.showPageNameInfo = True
    view.showTextOverflowMarker = False
    
    C1 = (random()*0.2, random()*0.2, random()*0.9)

    # Make background element, filling the page color and bleed.
    colorRect1 = newRect(z=-10, name='Page area', parent=page,
                         conditions=[Top2TopSide(),
                                     Left2LeftSide(),
                                     Fit2RightSide(),
                                     Fit2BottomSide()],
                         fill=C1)
    colorRect1.bleed = 0 #(0, 0, 0, 40) # TODO: Fix Bleed function
    colorRect1.solve() # Solve element position, before we can make
                       # other elements depend on position and size.

    M = 64
    newRect(z=-10, name='Frame 2', parent=colorRect1, 
            conditions=[Center2Center(), Middle2Middle()],
            fill=darker(C1, 0.5), # Default parameter:
                                  # 50% between background color and white
            stroke=None,
            w=colorRect1.w-M, h=colorRect1.h-M,
            xAlign=CENTER, yAlign=MIDDLE)

    # Make random blurb name and titles
    title = blurb.getBlurb('book_phylosophy_title')
    subTitle = blurb.getBlurb('book_pseudoscientific').capitalize()
    if random() < 0.2: # 1/5 chance to add editions text
        subTitle += '\nEdition '+blurb.getBlurb('edition')
    authorName = blurb.getBlurb('name', noTags=True)
    if random() < 0.33: # 1/3 chance for a second author name
        authorName += '\n' + blurb.getBlurb('name')
        
    page.pt = 120 # Now the rectangles positioned automatic, alter the paddings
    page.pl = page.pr = 80
    page.pb = 30
    # Add some title (same width, different height) at the "wrongOrigin" position.
    # They will be repositioned by solving the colorConditions.
    title = context.newString(title+'\n\n', style=dict(font=fontBold.path, fontSize=40, rLeading=1.2, xAlign=CENTER, textFill=1))
    title += context.newString(subTitle + '\n\n', style=dict(font=fontRegular.path, fontSize=32, xAlign=CENTER, textFill=(1, 1, 1,0.5)))
    title += context.newString(authorName, style=dict(font=fontItalic.path, fontSize=24, rTracking=0.025, xAlign=CENTER, textFill=(1, 0.5, 1,0.7)))
    newTextBox(title, parent=page, name='Other element',
            conditions=[Fit2Width(), Center2Center(), Top2Top()],
            xAlign=CENTER, yAlign=TOP)
    
    typoIllustration = context.newString('&', style=dict(font='Georgia', fontSize=400, xAlign=CENTER, textFill=(1, 0.5, 1,0.7)))
    newTextBox(typoIllustration, parent=page,
            conditions=[Fit2Width(), Center2Center(), Bottom2Bottom()],
            xAlign=CENTER, yAlign=TOP)

    score = page.evaluate()
    if score.fails:
        page.solve()

    # Evaluate again, result should now be >= 0
    return doc

d = makeDocument()
d.export(EXPORT_PATH)

