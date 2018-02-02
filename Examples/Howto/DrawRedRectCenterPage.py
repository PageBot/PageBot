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
#     DrawRedRectCenterPage.py
#
#     Needs debugging in dimension showing of views.
#
from pagebot.style import getRootStyle, A5, CENTER, MIDDLE
# Document is the main instance holding all information about
# the document togethers (pages, styles, etc.)
from pagebot.document import Document
from pagebot.elements import newRect
from pagebot.conditions import *

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

    page = doc[0] # Get the first/single page of the document.
    page.padding = 40 # TODO: order if 4 values?

    # Make rect as page element centered with centered origin.
    if RedRect:
        c = 1, 0, 0
    else:
        c = 0.5
    conditions = (Center2Center(), Middle2Middle())
    newRect(fill=c, parent=page, w=RectSize, h=RectSize,
            conditions=conditions, xAlign=CENTER, yAlign=MIDDLE)
    # Solve the layout conditions of the red rectangle.
    # Show if one of the conditions failed to solve.
    score = page.solve()
    if score.fails:
        print 'Failed conditions', score.fails

    # Set the view parameters for the required output.
    view = doc.getView()
    view.w = view.h = W, H
    view.padding = 0 # Make view padding to show crop marks and frame
    view.showPageFrame = True # Show frame of the page in blue
    view.showPagePadding = True
    view.showPageCropMarks = True # Show crop marks
    view.showElementOrigin = ShowOrigins # Show origin alignment markers on each element.
    view.showElementDimensions = ShowOrigins
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

