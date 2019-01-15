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
#     05_StringFlows.py
#
#     If a TextBox as self.nextElement defined as name for another text box on the
#     same page, then overflow of self will go into the other text box.

from pagebot.constants import LEFT, BOTTOM, TOP
from pagebot.conditions import *
from pagebot.elements import *
from pagebot.document import Document
from pagebot.toolbox.color import color, blackColor, noColor, whiteColor

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
    view.showCropMarks = True
    view.showRegistrationMarks = True
    view.showFrame = True
    view.showPadding = True
    view.showOrigin = True
    view.showDimensions = False

    # Get list of pages with equal y, then equal x.
    #page = doc[1][0] # Get the single page from the document.
    page1 = doc[1] # Get page on pageNumber, first in row (there is only one now).
    page1.name = 'Page 1'
    page1.padding = PagePadding

    bs = c.newString('')
    for n in range(10):
        bs += c.newString('(Line %d) ' % (n+1), style=dict(font='Verdana-Bold', fontSize=9, leading=10, textFill=blackColor))
        bs += c.newString('Volume of text defines the box height. Volume of text defines the box height. \n',
            style=dict(font='Verdana', fontSize=9, leading=10, textFill=blackColor))

    if DoTextFlow:
        h1 = 120 # Fox on a given height, to show the text flowing to the e2 element.
    else:
        h1 = None

    e1 = newTextBox(bs,
        name='ElasticTextBox1',
        nextElement='ElasticTextBox2', # Overflow goes here.
        parent=page0, padding=4, x=100, w=BoxWidth, font='Verdana', h=h1,
        mb=20, mr=10,       # Conditions make the element move to top-left of the page.
        # And the condition that there should be no overflow, otherwise the text box
        # will try to solve it.
        conditions=[Left2Left(), Float2Top(), Overflow2Next()],
        # Position of the origin of the element. Just to show where it is.
        # Has no effect on the position conditions.
        yAlign=BOTTOM, xAlign=LEFT,
        strokeWidth=0.5, fill=color(0.9), stroke=noColor,
    )
    e2 = newTextBox('', # Empty box, will get the overflow from e1, if there is any.
        name='ElasticTextBox2', # Flow reference by element.name
        nextElementName='ElasticTextBox3', nextPageName='Page 2',
        parent=page1, padding=4, x=100, w=BoxWidth, h=200,
        conditions=[Right2Right(), Float2Top(), Fit2Bottom(), Overflow2Next()], yAlign=TOP,  fill=whiteColor, stroke=noColor,
    )
    # Get next page, to show flow running over page breaks.
    page2 = page1.next
    page2.name = 'Page 2'
    page2.padding = PagePadding

    e3 = newTextBox('', # Empty box, will get the overflow from e2, if there is any.
        name='ElasticTextBox3', # Flow reference by element.name
        parent=page1, padding=4, w=BoxWidth,
        conditions=[Right2Right(), Float2Top(), Fit2Bottom()],
        yAlign=TOP,  fill=whiteColor, stroke=noColor)

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

