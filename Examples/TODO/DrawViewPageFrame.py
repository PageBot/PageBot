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
#     DrawViewPageFrame.py
#
#     Needs debug in view dimension showing.
#
from pagebot.style import getRootStyle
from pagebot.constants import CENTER
from pagebot import getContext
# Document is the main instance holding all information about
# the document togethers (pages, styles, etc.)
from pagebot.document import Document
from pagebot.elements import *
from pagebot.conditions import *

W, H = 500, 500 #A5

OriginTop = False

def makeDocument():
    # Create new document with (w,h) and fixed amount of pages.
    # Make number of pages with default document size.
    # Initially make all pages default with template
    doc = Document(originTop=OriginTop, w=W, h=H, autoPages=1)

    page = doc[1] # Get the first/single page of the document.
    page.size = W, H
    #print(page.originTop)
    if OriginTop:
        s = u'Origin on top'
        conditions = (Center2Center(), Top2Top())
    else:
        s = u'Origin on bottom'
        conditions = (Center2Center(), Bottom2Bottom())

    bs = doc.context.newString(s, style=dict(fontSize=30,
                                             textFill=(1, 0, 0),
                                             xTextAlign=CENTER))
    nt = newTextBox(bs, x=100, y=100, conditions=conditions, parent=page, fill=color(1, 1, 0))
    print(bs.s)
    #print(nt.x, nt.y, nt.w, nt.h)
    score = page.solve()
    #if score.fails:
    #    print(score.fails)
    #print(nt.x, nt.y, nt.w, nt.h)

    # Set the view parameters for the required output.
    view = doc.getView()
    view.w = view.h = W, H
    view.padding = 100 # Make view padding to show crop marks and frame
    view.showFrame = True
    view.showCropMarks = True
    view.showOrigin = False
    view.showDimensions = True

    return doc

if __name__ == '__main__':

    context.Variable([
        #dict(name='ElementOrigin', ui='CheckBox', args=dict(value=False)),
        dict(name='OriginTop', ui='CheckBox', args=dict(value=False)),
    ], globals())

    d = makeDocument()
    d.export('_export/DrawViewPageFrame.pdf')

