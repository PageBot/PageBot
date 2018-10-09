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
#     FloatTextOnTopOfElement.py
#
#     This script generates a page with random color squares, indicating where
#     their position is.
#
#     This script is using the style parameters "originTop", making the
#     coordinate system run downwards.
#


#import pagebot # Import to know the path of non-Python resources.
from pagebot.constants import CENTER, TOP
from pagebot.conditions import *
from pagebot.elements import *
from pagebot.document import Document
from pagebot.toolbox.units import pt
from pagebot.toolbox.color import color

RedSize = pt(100)
YellowSize = pt(30)
PagePadding = pt(30)
PageSize = pt(400)

GUTTER = pt(8) # Distance between the squares.
SQUARE = 10 * GUTTER # Size of the squares

# The standard PageBot function getRootStyle() answers a standard Python dictionary,
# where all PageBot style entries are filled by their default values. The root style is kept in RS
# as reference for the ininitialization of all elements.
# Each element uses the root style as copy and then modifies the values it needs.
# Note that the use of style dictionaries is fully recursive in PageBot, implementing a cascading structure
# that is very similar to what happens in CSS.

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/FloatTextOnTopOfElement.pdf'


def makeDocument():
    """Make a new document."""

    W = H = PageSize

    doc = Document(w=W, h=H, originTop=False, title='Color Squares', autoPages=1)

    view = doc.getView()
    view.padding = pt(0) # Aboid showing of crop marks, etc.
    view.showOrigin = False
    view.showTextOverflowMarker = False

    # Get list of pages with equal y, then equal x.
    #page = doc[1][0] # Get the single page from te document.
    page = doc.getPage(1) # Get page on pageNumber, first in row (this is only one now).
    page.name = 'This is a demo page for floating child elements'
    page.padding = PagePadding

    # Show margin of page, can also be done by
    # view.showPadding = True
    newRect(fill=color(0.9), parent=page, margin=0,
            conditions=(Left2Left(), Fit2Right(), Bottom2Bottom(), Fit2Height()))

    redContainer = newRect(fill=color(1, 0, 0), pb=pt(10), w=RedSize, h=RedSize, padding=pt(10),
                           conditions=(Left2Left(), Bottom2Bottom()), parent=page)

    # Yellow square
    yellowSquare = newRect(fill=color(1, 1, 0), z=pt(8), w=YellowSize,
                           h=YellowSize, parent=redContainer, xAlign=CENTER, yAlign=TOP,
                           conditions=(Center2Center(), Bottom2Bottom()))

    # Blue square in different z=layer. No interaction with Floating on other z-layers.
    blueSquare = newRect(fill=color(0, 1, 1), z=10, w=50, h=50,
                         parent=redContainer, xAlign=CENTER,
                         conditions=(Top2Top(), Center2Center()))

    # Centered string
    fs = doc.context.newString('Float on top of yellow',
                               style=dict(font='Verdana',
                                          fontSize=7,
                                          xTextAlign=CENTER,
                                          textFill=blackColor))
    # Text falls through the yr2 (with differnt z) and lands on yellowSquare by Float2BottomSide()
    newTextBox(fs, name='Caption', parent=redContainer, z=8,
               fill=color(0, 1, 0), strokeWidth=0.5, stroke=color(1, 1, 0),
               conditions=[Fit2Width(), Float2BottomSide()], padding=3)
    score = page.solve()
    if score.fails:
        print(score.fails)

    return doc # Answer the doc for further doing.

d = makeDocument()
#dict(name='ElementOrigin', ui='CheckBox', args=dict(value=False)),
d.context.Variable(
    [dict(name='RedSize', ui='Slider',
          args=dict(minValue=100, value=100, maxValue=500)),
     dict(name='YellowSize', ui='Slider',
          args=dict(minValue=10, value=30, maxValue=500)),
     dict(name='PagePadding', ui='Slider',
          args=dict(minValue=10, value=30, maxValue=100)),
     dict(name='PageSize', ui='Slider',
          args=dict(minValue=100, value=400, maxValue=800))
    ], globals())
d.export(EXPORT_PATH)

