# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
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
#     UseMarkDownText.py
#
from __future__ import print_function
from pagebot.document import Document
from pagebot.elements import *
from pagebot.conditions import *
from pagebot.typesetter import Typesetter


W = 400
H = 480
RectSize = 300
ShadowOffset = 0
ShadowBlur = 10
ShadowTextOffset = 0
ShadowTextBlur = 10

markdownPath = 'TOC.md'

def makeDocument():

    doc = Document(originTop=False, w=W, h=H, autoPages=1)
    print(doc.styles.keys())
    doc.addStyle('h1', dict(textFill=0), force=True)
    doc.addStyle('h2', dict(textFill=0), force=True)
    doc.addStyle('p', dict(textFill=0), force=True)

    page = doc[1] # Get the first/single page of the document.
    page.padding = 40 # TODO: order if 4 values?

    # Make rect as page element centered with centered origin.
    conditions = [Fit()]

    g = Galley(parent=page, conditions=conditions, textFill=0)
    ts = Typesetter(doc, g)
    print(ts)
    ts.typesetFile(markdownPath)

    # Solve the layout conditions of the red rectangle.
    # Show if one of the conditions failed to solve.
    score = page.solve()
    if score.fails:
        print('Failed conditions', score.fails)

    # Set the view parameters for the required output.
    view = doc.getView()
    view.padding = 0 # Make view padding to show crop marks and frame
    view.showPageFrame = True # Show frame of the page in blue
    #view.showPagePadding = True
    view.showPageCropMarks = True # Show crop marks

    return doc

d = makeDocument()
d.export('_export/UseMarkdownText.pdf')

