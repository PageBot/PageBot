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
#     TextBoxLinesRuns.py
#
#     If a TextBox as self.nextElement defined as name for another text box on the
#     same page, then overflow of self will go into the other text box.

from pagebot.constants import LEFT, BOTTOM
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.fonttoolbox.analyzers.glyphanalyzer import GlyphAnalyzer
from pagebot.conditions import *
from pagebot.elements import *
from pagebot.document import Document
from pagebot.toolbox.color import color, noColor, blackColor
from pagebot.toolbox.units import pt
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)

DoTextFlow = False
PagePadding = 32
W = H = 500
BoxWidth = W - 2 * PagePadding

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/useTextBoxLinesRuns.png'

def makeDocument():
    """Make a new document."""

    # Create a new document, default to the defined page size.
    doc = Document(w=W, h=H, originTop=False, title='Text Flow', autoPages=2)
    c = doc.context

    view = doc.getView()
    view.padding = 30 # Aboid showing of crop marks, etc.
    view.showCropMarks = True
    view.showRegistrationMarks = True
    view.showFrame = True
    view.showPadding = True
    view.showOrigin = True
    view.showDimensions = False
    view.showElementInfo = False

    # Get list of pages with equal y, then equal x.
    #page = doc[1][0] # Get the single page from te document.
    page0 = doc.getPage(1) # Get page on pageNumber, first in row (this is only one now).
    page0.name = 'Page 1'
    page0.padding = PagePadding

    s = c.newString('', style=dict(font='Verdana', fontSize=pt(10), textFill=blackColor))
    for n in range(10):
        s += c.newString(('(Line %d) '
                          'Volume of text defines the box height.') % (n+1),
                         style=dict(fontSize=10+n*2, textFill=blackColor))
        s += c.newString('Volume', style=dict(textFill=color(1, 0, 0),
                                              font='Verdana',
                                              fontSize=pt(10+n*2)))
        s += c.newString(' of text defines the box height. \n',
                         style=dict(textFill=blackColor,
                                    font='Verdana',
                                    fontSize=pt(10+n*2)))

    e1 = newTextBox(s, parent=page0, padding=pt(4), x=pt(100),
                    w=BoxWidth, font='Verdana', h=None, mb=20, mr=10,
                    #Conditions make the element move to top-left of the page.
                    # And the condition that there should be no overflow,
                    # otherwise the text box will try to solve it.
                    conditions=[Left2Left(),
                                Float2Top(),
                                Overflow2Next()],
                    #Position of the origin of the element. Just to show
                    # where it is. Has no effect on the position conditions.
                    yAlign=BOTTOM, xAlign=LEFT,
                    leading=pt(5), fontSize=pt(9), textFill=color(0),
                    strokeWidth=pt(0.5), fill=color(0.9), stroke=noColor)

    """
    for line in e1.textLines:
        print(line, line.x, line.y)
    for foundPattern in e1.findPattern('Line 5'):
        print(foundPattern.x, foundPattern.y, foundPattern.line, foundPattern.line.runs)
    """

    font = findFont('Roboto-Regular')
    char = 'hyphen'
    g = font[char]
    print(g.pointContexts[0].p.x)
    c.save()

    c.scale(0.3)
    c.fill(color(1, 0, 0))
    c.drawGlyphPath(font[char])
    ga = GlyphAnalyzer(g)


    for x, vertical in ga.verticals.items():
        c.stroke(blackColor, pt(1))
        c.fill(noColor)
        c.line(pt(x, 0), pt(x, 3000))

    print(ga.horizontals)

    for y, horizontal in ga.horizontals.items():
        c.stroke(blackColor, pt(1))
        c.fill(noColor)
        c.line(pt(0, y), pt(2000, y))
    c.restore()

    """
    for contour in ga.glyph.pointContexts:
        path = BezierPath()
        for index, pc in contour.items():
            p = pc[3]
            if index == 0:
                path.moveTo((p.x/2, p.y/2))
            else:
                path.lineTo((p.x/2, p.y/2))
        path.closePath()
        c.fill(0)
        c.drawPath(path)
            #c.oval(p.x/2, p.y/2, 4, 4)
            #print(index, pc   )
    """
    score = doc.solve() # Try to solve all pages.

    if score.fails:
        print(score.fails)

    return doc # Answer the doc for further doing.

if __name__ == '__main__':
    d = makeDocument()
    d.export(EXPORT_PATH)

