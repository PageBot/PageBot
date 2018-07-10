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
#     UseFormattedStringFlows.py
#
#     If a TextBox as self.nextElement defined as name for another text box on the
#     same page, then overflow of self will go into the other text box.
from __future__ import division # Make integer division result in float.
#import pagebot # Import to know the path of non-Python resources.

from pagebot.style import LEFT, BOTTOM, TOP
from pagebot.conditions import *
from pagebot.elements import *
from pagebot.document import Document

DoTextFlow = True
BoxWidth = 500
PagePadding = 30
PageSize = 500

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/UseTextFlows.pdf'

def makeDocument():
    """Make a new document."""

    W = H = PageSize

    # Create a new document, default to the defined page size.
    doc = Document(w=W, h=H, originTop=False, title='Text Flow', autoPages=2)

    view = doc.view
    c = view.context
    view.padding = 0 # Aboid showing of crop marks, etc.
    view.showPageCropMarks = True
    view.showPageRegistrationMarks = True
    view.showPageFrame = True
    view.showPagePadding = True
    view.showElementOrigin = True
    view.showElementDimensions = False

    # Get list of pages with equal y, then equal x.
    #page = doc[1][0] # Get the single page from te document.
    page0 = doc[1] # Get page on pageNumber, first in row (this is only one now).
    page0.name = 'Page 1'
    page0.padding = PagePadding

    bs = c.newString('')
    for n in range(10):
        bs += c.newString('(Line %d) ' % (n+1), style=dict(font='Verdana-Bold', fontSize=9, leading=10, textFill=0))
        bs += c.newString('Volume of text defines the box height. Volume of text defines the box height. \n', style=dict(font='Verdana', fontSize=9, leading=10, textFill=0))

    if DoTextFlow:
        h1 = 120 # Fox on a given height, to show the text flowing to the e2 element.
    else:
        h1 = None

    e1 = newTextBox(bs,
        name='ElasticTextBox1',
        nextElement='ElasticTextBox2', # Overflow goes here.
        parent=page0, padding=4, x=100, w=BoxWidth, font='Verdana', h=h1,
        maxW=W-2*PagePadding, minW=100, mb=20, mr=10,       # Conditions make the element move to top-left of the page.
        # And the condition that there should be no overflow, otherwise the text box
        # will try to solve it.
        conditions=[Left2Left(), Float2Top(), Overflow2Next()],
        # Position of the origin of the element. Just to show where it is.
        # Has no effect on the position conditions.
        yAlign=BOTTOM, xAlign=LEFT,
        strokeWidth=0.5, fill=0.9, stroke=None,
    )
    e2 = newTextBox('', # Empty box, will get the overflow from e1, if there is any.
        name='ElasticTextBox2', # Flow reference by element.name
        nextElement='ElasticTextBox3', nextPage='Page 2',
        parent=page0, padding=4, x=100, w=BoxWidth, h=200,
        maxW=W-2*PagePadding, minW=100,
        conditions=[Right2Right(), Float2Top(), Fit2Bottom(), Overflow2Next()], yAlign=TOP,  fill=1, stroke=None,
    )
    # Get next page, to show flow running over page breaks.
    page1 = doc[1]
    page1.name = 'Page 2'
    page1.padding = PagePadding

    e3 = newTextBox('', # Empty box, will get the overflow from e2, if there is any.
        name='ElasticTextBox3', # Flow reference by element.name
        parent=page1, padding=4, w=BoxWidth,
        maxW=W-2*PagePadding, minW=100,
        conditions=[Right2Right(), Float2Top(), Fit2Bottom()],
        yAlign=TOP,  fill=1, stroke=None)

    score = doc.solve() # Try to solve all pages.
    if score.fails:
        print(score.fails)

    return doc # Answer the doc for further doing.

if __name__ == '__main__':
    d = makeDocument()
    d.context.Variable([
        #dict(name='ElementOrigin', ui='CheckBox', args=dict(value=False)),
        dict(name='DoTextFlow', ui='CheckBox', args=dict(value=True)),
        dict(name='BoxWidth', ui='Slider', args=dict(minValue=100, value=500, maxValue=PageSize)),
        dict(name='PagePadding', ui='Slider', args=dict(minValue=0, value=30, maxValue=100)),
        dict(name='PageSize', ui='Slider', args=dict(minValue=200, value=500, maxValue=PageSize)),
    ], globals())
    d.export(EXPORT_PATH)

