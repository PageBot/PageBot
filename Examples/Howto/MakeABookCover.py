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
from random import random

# Create random title and names
# from pagebot.contributions.filibuster.blurb import blurb

from pagebot.contexts import defaultContext as context
from pagebot.toolbox.transformer import darker

# Creation of the RootStyle (dictionary) with all
# available default style parameters filled.
from pagebot.style import getRootStyle, B4, CENTER, MIDDLE, TOP 

# Document is the main instance holding all information
# about the document togethers (pages, styles, etc.)
from pagebot.document import Document

# Import element layout conditions.
from pagebot.conditions import *
from pagebot.elements import newRect, newText
   
# For clarity, most of the OneValidatingPage.py example document is setup
# as a sequential excecution of Python functions. For complex documents
# this is not the best method. More functions and classes will be used in the
# real templates, which are available from the PageBotTemplates repository.

W, H = B4
W -= 48 # Make a bit more narrow format.

if 0: # If showing registration/cutting marks, increase side of the document.
    docW = W+200
    docH = H+200
else:
    docW = W
    docH = H

# The standard PageBot function getRootStyle() answers a standard Python
# dictionary, where all PageBot values are filled by their default values.
# The root style is kept in RS as reference to for all ininitialzaiton
# of elements.
#
# Each element uses the root style as copy and then modifies the values
# it needs. Note that the use of style dictionaries is fully recursive
# in PageBot, implementing a cascading structure that is very similar
# to what happens in CSS.

RS = getRootStyle(
    w=W,
    h=H,
    pl=64,
    pt=64,
    pr=64,
    pb=80,
    docW=docW,
    docH=docH,
    showElementInfo=False,
    showElementOrigin=True,
    originTop=True
)

# Export in folder that does not commit to Git. Force to export PDF.
EXPORT_PATH = '_export/ABookCover.pdf'


def makeDocument():
    u"""Demo random book cover generator."""

    # Create new document with (w,h) and fixed amount of pages.
    # Make number of pages with default document size.
    # Initially make all pages default with template
    doc = Document(w=W, h=H, title='A Demo Book Cover', autoPages=1, context=context) # One page, just the cover.

    page = doc[0] # Get the first/single page of the document.
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
    view.showPagePadding = True
    view.showPageNameInfo = True

    C1 = (random()*0.2, random()*0.2, random()*0.9)

    # Make background element, filling the page color and bleed.
    colorRect1 = newRect(z=-10, name='Page area', parent=page,
                         conditions=[Top2TopSide(),
                                     Left2LeftSide(),
                                     Fit2RightSide(),
                                     Fit2BottomSide()],
                         fill=C1)
    
    colorRect1.solve() # Solve element position, before we can make
                       # other elements depend on position and size.

    #colorRect2:
    M = 64
    newRect(z=-10, name='Frame 2', parent=colorRect1, conditions=[Center2Center(),
                                               Middle2Middle()],
            fill=darker(C1, 0.5), # Default parameter:
                                  # 50% between background color and white
            stroke=None,
            w=colorRect1.w-M, h=colorRect1.h-M,
            xAlign=CENTER, yAlign=MIDDLE)

    page.pt = 200
    # Add some title (same width, different height) at the "wrongOrigin" position.
    # They will be repositioned by solving the colorConditions.
    title = context.newString('Book Cover\n', style=dict(font='Georgia', fontSize=40, rLeading=1.2, xAlign=CENTER, textFill=1))
    title += context.newString('Subtitle of the book\n\n', style=dict(font='Georgia', fontSize=32, xAlign=CENTER, textFill=(1, 1, 1,0.5)))
    title += context.newString('Author name & other' + '\n'*8, style=dict(font='Georgia', fontSize=24, xAlign=CENTER, textFill=(1, 0.5, 1,0.7)))
    title += context.newString('&', style=dict(font='Georgia', fontSize=400, xAlign=CENTER, textFill=(1, 0.5, 1,0.7)))
    newText(title, parent=page, name='Other element',
            conditions=[Center2Center(), Top2Top()],
            xAlign=CENTER, yAlign=TOP)
    """
    page.rect(point=wrongOrigin, style=rootStyle, w=W2, h=H2,
              name='Floating element 2',
              conditions=colorCondition2, fill=(1, 1, 0),
              xAlign=LEFT, yAlign=TOP)
    page.rect(point=wrongOrigin, style=rootStyle, w=W3, h=H3,
              name='Floating element 3',
              conditions=colorCondition2, fill=(1, 0, 1),
              xAlign=LEFT, yAlign=TOP)

    # Make text box at wrong origin. Apply same width a the color rect,
    # which may be too wide from typographic point ogf view.
    # The MaxWidthByFontSize will set the self.w to the maximum
    # width for this pointSize.
    if not hasattr(pbglobals, 'blurbText'):
        the_blurb = blurb.getBlurb('article_summary', noTags=True)
        pbglobals.blurbText = doc.context.newString(the_blurb, page,
                                                    style=dict(font='Georgia',
                                                               fontSize=12,
                                                               rLeading=0.2,
                                                               textColor=0))
    page.textBox(pbglobals.blurbText, point=wrongOrigin,
                 style=rootStyle, w=WT,
                 conditions=textCondition,
                 xAlign=CENTER, yAlign=CENTER)

    page.rect(point=wrongOrigin, style=rootStyle, w=W4, h=H4,
              name='Floating element 4',
              conditions=colorCondition2, fill=(0, 1, 1),
              xAlign=LEFT, yAlign=TOP)

    page.rect(point=wrongOrigin, style=rootStyle, w=W5, h=H5,
              name='Floating element 5',
              conditions=[FloatRightTopSides()], fill=(0, 1, 0),
              xAlign=LEFT, yAlign=TOP)
    """
    score = page.evaluate()
    #print 'Page value on evaluation:', score
    #print score.fails
    # Try to solve the problems if evaluation < 0
    if score.fails:
        #print('Solving', score.fails)
        page.solve()
    #print score.fails
    # Evaluate again, result should now be >= 0
    score = page.evaluate()
    #print('Page value after solving the problems:', score)
    #for fail in score.fails:
    #    print(fail)

    return doc

if __name__ == '__main__':
    d = makeDocument()
    d.export(EXPORT_PATH)

