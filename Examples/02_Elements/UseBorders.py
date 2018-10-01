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
#     UseBorders.py
#
from random import random
from drawBot import Variable
from drawBot.misc import DrawBotError

import pagebot # Import to know the path of non-Python resources.
# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle
from pagebot.constants import (A4, CENTER,TOP, BOTTOM, INLINE, OUTLINE, ONLINE)
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
from pagebot.elements import *
from pagebot.document import Document
from pagebot.toolbox.color import color, noColor
from pagebot.toolbox.units import pt

ViewPadding = 64
PageSize = 500

GUTTER = 24 # Distance between the squares.
SQUARE = 3 * GUTTER # Size of the squares

DashWhite = 4
DashBlack = 4
LineType = ONLINE

EXPORT_PATH = '_export/UseBorders.pdf' # Export in _export folder that does not commit in Git. Force to export PDF.

def makeDocument():
    """Make a new document, using the rs as root style."""

    #W = H = 120 # Get the standard a4 width and height in points.
    W = H = PageSize

    # Hard coded SQUARE and GUTTE, just for simple demo, instead of filling padding an columns in the root style.
    # Page size decides on the amount squares that is visible.
    # Page padding is centered then.
    sqx = int(W/(SQUARE + GUTTER)) # Whole amount of squares that fit on the page.
    sqy = int(H/(SQUARE + GUTTER))
    # Calculate centered paddings for the amount of fitting squares.
    # Set values in the rootStyle, so we can compare with column calculated square position and sizes.
    #rs['colH'] = rs['colW'] = SQUARE  # Make default colW and colH square.

    padX = (W - sqx*(SQUARE + GUTTER) + GUTTER)/2
    my = (H - sqy*(SQUARE + GUTTER) + GUTTER)/2


    doc = Document(title='Color Squares', w=W, h=H, originTop=False, autoPages=1)

    doc.view.padding = 0 # Don't show cropmarks in this example.

    # Get list of pages with equal y, then equal x.
    #page = doc[1][0] # Get the single page from te document.
    page = doc.getPage(1) # Get page on pageNumber, first in row (this is only one now).
    page.name = 'This demo page'

    page.w = W
    page.h = H

    page.padding3D = padX # Set all 3 paddings to same value
    page.gutter3D = GUTTER # Set all 3 gutters to same value

    #newRect((0, 0), w=square, h=square, parent=page, fill=color(1, 0, 0), stroke=noColor)

    for ix in range(sqx): # Run through the range of (0, 1, ...) number of horizontal squares
        for iy in range(sqy): # Same with vertical squares
            # Place squares in random colors
            color1 = color(random()*0.5+0.5, 0.1, 0.6)
            color2 = color(random()*0.5+0.5, 0.1, 0.6)
            # Calculate the position for each square as combination
            # of paddings and (ix, iy)
            p = padX + ix * (SQUARE + GUTTER), my + iy * (SQUARE + GUTTER) # Make 2-dimensional point tuple.
            # Create Rect object and place it in the page on position p
            # Initialize the borders dicts on lineWidth == 0
            e = newRect(xy=p, w=SQUARE, h=SQUARE, parent=page,
                fill=color1, stroke=noColor, borders=1) # border=1 also works, identical.
            lineType = {-1:ONLINE, 0:INLINE, 1:ONLINE, 2:OUTLINE}[LineType]
            e.borderLeft['strokeWidth'] = pt((ix+1)*4)
            e.borderLeft['line'] = lineType
            e.borderLeft['stroke'] = color(0, 0, 0, 0.5)
            e.borderLeft['dash'] = (DashWhite, DashBlack)

            e.borderBottom['strokeWidth'] = pt((ix+1)*4)
            e.borderBottom['line'] = lineType
            e.borderBottom['stroke'] = color(0, 1, 0)
            e.borderBottom['dash'] = (DashWhite, DashBlack)

            e.borderTop['strokeWidth'] = pt((iy+1)*4)
            e.borderTop['line'] = lineType
            e.borderTop['stroke'] = color(1, 1, 0, 0.5)

            e.borderRight['strokeWidth'] = pt((iy+1)*4)
            e.borderRight['line'] = lineType
            e.borderRight['stroke'] = color(0, 0, 1, 0.5)

            # Create Rect object and place it in the page on position p
    return doc # Answer the doc for further doing.


if __name__ == '__main__': # If running from DrawBot
    Variable([
	     dict(name="LineType", ui="RadioGroup", args=dict(titles=[INLINE, ONLINE, OUTLINE],
	        isVertical=True)),
        dict(name='DashWhite', ui='Slider', args=dict(minValue=0, value=8, maxValue=8)),
        dict(name='DashBlack', ui='Slider', args=dict(minValue=0, value=0, maxValue=8)),
        dict(name='PageSize', ui='Slider', args=dict(minValue=100, value=400, maxValue=800)),
    ], globals())
    d = makeDocument()
    d.export(EXPORT_PATH)

