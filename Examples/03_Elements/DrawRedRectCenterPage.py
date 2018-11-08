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
#     DrawRedRectCenterPage.py
#
#     Needs debugging in dimension showing of views.
#
from pagebot.style import getRootStyle
from pagebot.constants import A5, CENTER, MIDDLE
# Document is the main instance holding all information about
# the document togethers (pages, styles, etc.)
from pagebot.document import Document
from pagebot.elements import newRect
from pagebot.conditions import *
from pagebot.toolbox.color import Color


W, H = A5
W = 400
H = 480
ShowOrigins = False
ShowElementInfo = False
RedRect = True # Show red or gray
RectSize = 300

def makeDocument():
    # Create new document with (w,h) size and fixed amount of pages.
    # Note that most of the rootStyle is cascading through the e.css('name') call,
    # except that values of x, y, z, w, h, d

    # Just to show here how to get the root style. If not altered, it can be omitted.
    # as Document( ) will create a RootStyle by default.
    rootStyle = getRootStyle()

    doc = Document(rootStyle, originTop=False, w=W, h=H, autoPages=1)
    page = doc[1] # Get the first/single page of the document.
    page.padding = 40 # TODO: order if 4 values?

    # Make rect as page element centered with centered origin.
    if RedRect:
        c = Color(1, 0, 0)
    else:
        c = Color(0.5)

    conditions = (Center2Center(), Middle2Middle())
    newRect(fill=c, parent=page, w=RectSize, h=RectSize,
            conditions=conditions, xAlign=CENTER, yAlign=MIDDLE)
    # Solve the layout conditions of the red rectangle.
    # Show if one of the conditions failed to solve.
    score = page.solve()
    if score.fails:
        print('Failed conditions', score.fails)

    # Set the view parameters for the required output.
    view = doc.getView()
    view.w = view.h = W, H
    view.padding = 40 # Make view padding to show crop marks and frame
    view.showFrame = True # Show frame of the page in blue
    view.showPadding = False
    view.showCropMarks = True # Show crop marks
    view.showOrigin = ShowOrigins # Show origin alignment markers on each element.
    view.showDimensions = ShowOrigins
    view.showElementInfo = ShowElementInfo # Show baxes with element info element.

    return doc

if __name__ == '__main__':
    d = makeDocument()
    d.context.Variable([
        #dict(name='ElementOrigin', ui='CheckBox', args=dict(value=False)),
        dict(name='ShowOrigins', ui='CheckBox', args=dict(value=True)),
        dict(name='ShowElementInfo', ui='CheckBox', args=dict(value=False)),
        dict(name='RedRect', ui='CheckBox', args=dict(value=True)),
        dict(name='RectSize', ui='Slider', args=dict(minValue=10, value=W/2, maxValue=W)),
    ], globals())
    d.export('_export/DrawRedRectCenterPage.pdf')

