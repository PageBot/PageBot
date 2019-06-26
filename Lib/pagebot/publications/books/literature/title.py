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
#     MakeABookCover.py
#
#     Needs filling in with content.
#
from random import random # Used for random color palet.

# Create random title and names
from pagebot.contributions.filibuster.blurb import blurb
from pagebot.toolbox.color import color, noColor, whiteColor

# Get function to find the Roboto family (in this case installed in the
# PageBot repository).
from pagebot.fonttoolbox.objects.family import getFamily
from pagebot.fonttoolbox.objects.font import findFont

# Get the constants that we need
from pagebot.constants import B4, CENTER, MIDDLE, TOP

# Document is the main instance holding all information
# about the document togethers (pages, styles, etc.)
from pagebot.document import Document

# Import element layout conditions.
from pagebot.conditions import *
from pagebot.elements import newRect, newTextBox
from pagebot.toolbox.units import em

# For clarity, most of the MakeABookCover.py example document is setup
# as a sequential excecution of Python functions. For complex documents
# this is not the best method. More functions and classes will be used in the
# real templates, which are available from the PageBotTemplates repository.

W, H = B4
#W -= 48 # Make a bit more narrow format.

BLEED = 8

# Export in folder that does not commit to Git. Force to export PDF.
EXPORT_PATH = '_export/ABookCover.pdf'

family = getFamily('Roboto')
fontRegular = family.findFont('Regular')
fontBold = family.findFont('Bold')
fontItalic = family.findFont('Italic')
ampersandFont = findFont('Georgia')

def makeDocument():
    """Demo random book cover generator."""

    # Create new document with (w,h) and fixed amount of pages.
    # Make number of pages with default document size.
    # Initially make all pages default with template
    # One page, just the cover.
    doc = Document(w=W, h=H, title='A Demo Book Cover', autoPages=1, originTop=False)

    page = doc[1] # Get the first/single page of the document.
    page.name = 'Cover'

    # Get the current view of the document. This allows setting of
    # parameters how the document is represented on output.
    view = doc.view
    view.w, view.h = W, H
    # Set view options. Full list is in elements/views/baseviews.py
    view.padding = 40 # Showing cropmarks and registration marks
                      # need >= 20 padding of the view.
    view.showRegistrationMarks = True
    view.showCropMarks = True
    view.showFrame = True
    view.showPadding = False
    view.showNameInfo = True
    view.showTextOverflowMarker = False

    context = view.context

    C1 = color(r=random()*0.2, g=random()*0.2, b=random()*0.9)

    # Make background element, filling the page color and bleed.
    colorRect1 = newRect(z=-10, name='Page area', parent=page,
                         conditions=[Top2TopSide(),
                                     Left2LeftSide(),
                                     Fit2RightSide(),
                                     Fit2BottomSide()],
                         fill=C1)
    colorRect1.bleed = BLEED
    colorRect1.solve() # Solve element position, before we can make
                       # other elements depend on position and size.

    M = BLEED + 64
    colorRect2 = newRect(z=-10, name='Frame 2', parent=colorRect1,
            conditions=[Center2Center(), Middle2Middle()],
            fill=C1.darker(0.5), # Default parameter:
                                  # 50% between background color and white
            stroke=noColor,
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

    titleStyle = dict(font=fontBold.path, fontSize=40, leading=em(1.2),
        xTextAlign=CENTER, textFill=whiteColor, hyphenation=False)
    subTitleStyle = dict(font=fontRegular.path, fontSize=32,
        xTextAlign=CENTER, textFill=(1, 1, 1, 0.5), hyphenation=False)
    authorStyle = dict(font=fontItalic.path, fontSize=24, tracking=em(0.025),
        xTextAlign=CENTER, textFill=(1, 0.5, 1,0.7))

    # Add some title (same width, different height) at the "wrongOrigin" position.
    # They will be repositioned by solving the colorConditions.
    title = context.newString(title+'\n\n', style=titleStyle)
    title += context.newString(subTitle + '\n\n', style=subTitleStyle)
    title += context.newString(authorName, style=authorStyle)
    newTextBox(title, parent=colorRect2, name='Other element',
            conditions=[Fit2Width(), Center2Center(), Top2Top()],
            xAlign=CENTER, yAlign=TOP)

    typoIllustration = context.newString('&', style=dict(font=ampersandFont.path, fontSize=300, xTextAlign=CENTER, textFill=(1, 0.5, 1,0.7)))
    newTextBox(typoIllustration, parent=page,
            conditions=[Fit2Width(), Center2Center(), Bottom2Bottom()],
            xAlign=CENTER, yAlign=TOP)

    # Evaluate again, result should now be >= 0
    score = page.evaluate()
    if score.fails: # There is new "failing" elements. Solve their layout.
        page.solve()

    return doc

d = makeDocument()
d.export(EXPORT_PATH)
