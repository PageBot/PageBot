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
#     AlignElements.py
#
#     This script generates a page with aligned square, showing how conditional placement works.
#     Interactive Variable() only works in DrawBot context.
#
# Creation of the RootStyle (dictionary) with all available default style parameters filled.
#TODO from pagebot.contexts.flatcontext import FlatContext
from pagebot.contexts.drawbotcontext import DrawBotContext
from pagebot.constants import CENTER
# Document is the main instance holding all information about
# the document togethers (pages, styles, etc.)
from pagebot.document import Document
from pagebot.elements import newRect
from pagebot.toolbox.color import blueColor, darkGrayColor, redColor, Color, noColor, color
from pagebot.conditions import *

# Variables used as interactive globals in DrawBot context.
ShowOrigins = False
ShowElementInfo = False
ShowDimensions = False
PageSize = 500

W = H = PageSize

G = 8 # Distance between the squares.
SQ = 8 * G # Size of the squares

def makeDocument(context):
    """Make a new document."""

    doc = Document(w=W, h=H, originTop=False, autoPages=1, context=context)
    page = doc[1] # Get the single page from te document.

    # Hard coded padding, just for simple demo,
    # instead of filling padding and columns in the root style.
    page.padding = SQ

    # Position square in the 4 corners of the page area.
    # Notice that their alignment (left) does not matter for the conditions.
    newRect(w=SQ, h=SQ, parent=page,
            conditions=(Right2Right(), Top2Top()), fill=darkGrayColor)
    newRect(w=SQ, h=SQ, parent=page,
            conditions=(Left2Left(), Bottom2Bottom()), fill=darkGrayColor)
    newRect(w=SQ, h=SQ, parent=page,
            conditions=(Left2Left(), Top2Top()), fill=darkGrayColor)
    newRect(w=SQ, h=SQ, parent=page,
            conditions=(Right2Right(), Bottom2Bottom()), fill=darkGrayColor)

    # Make new container for adding elements inside with alignment.
    # cnt = newRect(w=W-2*SQ, h=H-2*SQ,
    #               fill=color(0.8, 0.8, 0.8, 0.4),
    #               parent=page, margin=SQ, yAlign=BOTTOM,
    #               xAlign=CENTER, stroke=noColor,
    #               conditions=(Center2Center(), Middle2Middle()))

    # Add rectangles to the page,
    # using alignment conditions to position rules.
    newRect(w=SQ, h=SQ, stroke=noColor, parent=page, xAlign=CENTER,
            conditions=(Center2Center(), Middle2Middle()), fill=redColor)

    conditions = [(Center2Center(), Top2Top()),
                  (Center2Center(), Bottom2Bottom()),
                  (Left2Left(), Middle2Middle()),
                  (Right2Right(), Middle2Middle())]

    for condition in conditions:
        newRect(w=SQ, h=SQ, stroke=noColor, parent=page, xAlign=CENTER,
                conditions=condition, fill=color(1, 1, 0))

    sideConditions = [(Center2Center(), Top2TopSide()),
                      (Center2Center(), Bottom2BottomSide()),
                      (Left2LeftSide(), Middle2Middle()),
                      (Right2RightSide(), Middle2Middle())]
    for condition in sideConditions:
        newRect(w=SQ, h=SQ, stroke=noColor, parent=page, xAlign=CENTER,
                conditions=condition, fill=color(0.5, 1, 0))

    cornerConditions = [(Left2LeftSide(), Top2TopSide()),
                        (Right2RightSide(), Top2TopSide()),
                        (Left2LeftSide(), Bottom2BottomSide()),
                        (Right2RightSide(), Bottom2BottomSide())]
    for condition in cornerConditions:
        newRect(w=SQ, h=SQ, stroke=noColor, parent=page, xAlign=CENTER,
                conditions=condition, fill=blueColor)
    # Solve the layout placement conditions on the page by moving the
    # elements that are not on the right positions (which is all of them,
    # because we did not add point attributes when creating them.

    score = page.solve()
    if score.fails:
        print('Failed to solve %d conditions:' % len(score.fails))
    for condition, e in score.fails:
        print(e.bottom2BottomSide())
        print(condition, e, e.bottom,
              Bottom2BottomSide().test(e),
              e.isBottomOnBottomSide(), e.bottom)

    # Get the current view of the document. This allows setting of
    # parameters how the document is represented on output.
    view = doc.view
    view.w, view.h = W, H
    # Set view options. Full list is in elements/views/baseviews.py
    view.padding = 30 # Showing cropmarks and registration marks
                      # need >= 20 padding of the view.
    view.showRegistrationMarks = True
    view.showCropMarks = True
    view.showFrame = True
    view.showPadding = True
    view.showNameInfo = True

    # These values can be changed in the Variable window,
    # when in DrawBot context.
    view.showOrigin = ShowOrigins # Show origin alignment
                                         # markers on each element.
    view.showDimensions = ShowDimensions
    view.showElementInfo = ShowElementInfo # Show boxes with element info

    return doc # Answer the doc.

if __name__ == '__main__':

    # May contain NoneDrawBotBuilder if not running on a DrawBot platform
    context = DrawBotContext() 
    d = makeDocument(context)
    # Make interactive global controls. Only works in DrawBot context. Otherwise 
    # Export in _export folder that does not commit in Git. Force to export PDF.
    EXPORT_PATH = '_export/AlignElements.png'
    d.export(EXPORT_PATH)

    # FIX: F L A T
    #context = FlatContext()
    #d = makeDocument(context)
    # Export in _export folder that does not commit in Git. Force to export PDF.
    #EXPORT_PATH = '_export/AlignElements_F.pdf'
    #d.export(EXPORT_PATH)
