#!/usr/bin/evn python
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
#     ElasticTextBox.py
#

from pagebot import getContext
c = getContext()

from pagebot.constants import A4, LEFT, TOP, BOTTOM
from pagebot.conditions import *
from pagebot.elements import *
from pagebot.document import Document
from pagebot.toolbox.color import color, noColor
from pagebot.toolbox.units import pt, em

DoTextFlow = False
BoxWidth = 500
PagePadding = 30
PageSize = 1000

GUTTER = 8 # Distance between the squares.
SQUARE = 10 * GUTTER # Size of the squares

# The standard PageBot function getRootStyle() answers a standard Python
# dictionary, where all PageBot style entries are filled by their default
# values. The root style is kept in RS as reference for the ininitialization of
# all elements.
# Each element uses the root style as copy and then modifies the values it
# needs. Note that the use of style dictionaries is fully recursive in
# PageBot, implementing a cascading structure that is very similar to what
# happens in CSS.

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/UseElasticTextBox.pdf'


def makeDocument():
    """Make a new document."""

    #W = H = 120 # Get the standard a4 width and height in points.
    W = PageSize
    H = PageSize
    # Hard coded SQUARE and GUTTE, just for simple demo, instead of filling padding an columns in the root style.
    # Page size decides on the amount squares that is visible.
    # Page padding is centered then.
    sqx = int(W/(SQUARE + GUTTER)) # Whole amount of squares that fit on the page.
    sqy = int(H/(SQUARE + GUTTER))
    # Calculate centered paddings for the amount of fitting squares. Set
    # values in the rootStyle, so we can compare with column calculated square
    # position and sizes.
    #rs['colH'] = rs['colW'] = SQUARE  # Make default colW and colH square.

    #padX = (W - sqx*(SQUARE + GUTTER) + GUTTER)/2
    my = (H - sqy*(SQUARE + GUTTER) + GUTTER)/2

    doc = Document(w=W, h=H, originTop=False, title='Color Squares', autoPages=1)

    view = doc.view # Get the current view of the document.
    view.padding = 40 # Aboid showing of crop marks, etc.
    view.showCropMarks = True
    view.showRegistrationMarks = True
    view.showFrame = True
    view.showPadding = True
    view.showOrigin = True
    view.showDimensions = False

    # Get list of pages with equal y, then equal x.
    #page = doc[1][0] # Get the single page from te document.
    page = doc[1] # Get page on pageNumber, first in row (this is only one now).
    page.name = 'This is a demo page for floating child elements'
    page.padding = PagePadding

    page.gutter3D = GUTTER # Set all 3 gutters to same value

    if BoxWidth < 200:
        tColor = color(1, 0, 0)
    else:
        tColor = color(0, 0, 1)

    s = ''
    for n in range(10):
        s += '(%d) Volume of text defines the box height.\n' % (n+1)
    if DoTextFlow:
        h1 = 100
    else:
        h1 = None
    e1 = newTextBox(s,
        name='ElasticTextBox1',
        parent=page, padding=4, x=100, w=min(BoxWidth, page.pw), font='Verdana', h=h1,
        conditions=[Left2Left(), Float2Top()], yAlign=BOTTOM, xAlign=LEFT,
        leading=em(1.4), fontSize=9, textFill=tColor, strokeWidth=pt(0.5), fill=color(0.9), stroke=noColor,
    )
    e2 = newTextBox(s,
        name='ElasticTextBox2',
        parent=page, padding=4, x=100, w=min(BoxWidth, page.pw), font='Verdana',
        conditions=[Right2Right(), Float2Top()], yAlign=TOP, leading=em(1.4),
        fontSize=9, textFill=0.9, strokeWidth=0.5, fill=tColor, stroke=noColor,
    )

    score = page.solve()

    if score.fails:
        print(score.fails)

    return doc # Answer the doc for further doing.

if __name__ == '__main__':

    c.Variable([
        #dict(name='ElementOrigin', ui='CheckBox', args=dict(value=False)),
         dict(name='DoTextFlow', ui='CheckBox', args=dict(value=False)),
         dict(name='BoxWidth', ui='Slider', args=dict(minValue=200, value=500, maxValue=PageSize)),
        dict(name='PagePadding', ui='Slider', args=dict(minValue=0, value=30, maxValue=100)),
        dict(name='PageSize', ui='Slider', args=dict(minValue=200, value=500, maxValue=PageSize)),
    ], globals())

    d = makeDocument()
    d.export(EXPORT_PATH)
