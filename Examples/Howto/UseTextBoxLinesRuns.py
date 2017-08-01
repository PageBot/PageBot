# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     UseTextFlows.py
#
#     If a TextBox as self.nextElement defined as name for another text box on the
#     same page, then overflow of self will go into the other text box.

from __future__ import division # Make integer division result in float.
import pagebot # Import to know the path of non-Python resources.

from pagebot import x2cx, y2cy
# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, A4, CENTER, RIGHT, LEFT, NO_COLOR,TOP, BOTTOM, MM
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
from pagebot import newFS
from pagebot.fonttoolbox.objects.font import getFontPathOfFont, getFontByName
from pagebot.fonttoolbox.analyzers.glyphanalyzer import GlyphAnalyzer

from pagebot.conditions import *
from pagebot.elements import *
from pagebot.document import Document

DoTextFlow = False   
PagePadding = 32
W = H = 500
BoxWidth = W

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/useTextBoxLinesRuns.png' 

def makeDocument():
    u"""Make a new document."""


    # Create a new document, default to the defined page size. 
    doc = Document(w=W, h=H, originTop=False, title='Text Flow', autoPages=2)
    
    view = doc.getView()
    view.padding = 30 # Aboid showing of crop marks, etc.
    view.showPageCropMarks = True
    view.showPageRegistrationMarks = True
    view.showPageFrame = True
    view.showPagePadding = True
    view.showElementOrigin = True
    view.showElementDimensions = False
    view.showElementInfo = False
    
    # Get list of pages with equal y, then equal x.    
    #page = doc[0][0] # Get the single page from te document.
    page0 = doc.getPage(0) # Get page on pageNumber, first in row (this is only one now).
    page0.name = 'Page 1'
    page0.padding = PagePadding
    
    s = newFS('', style=dict(font='Verdana', fontSize=10, textFill=0))
    for n in range(10):
        s += newFS('(Line %d) Volume of text defines the box height.' % (n+1), style=dict(fontSize=10+n*2, textFill=0))
        s += newFS('Volume', style=dict(textFill=(1, 0, 0), font='Verdana', fontSize=10+n*2))
        s += newFS(' of text defines the box height. \n', style=dict(textFill=0, font='Verdana', fontSize=10+n*2))
          
    e1 = newTextBox(s, 
        parent=page0, padding=4, x=100, w=BoxWidth, font='Verdana', h=None,
        maxW=W-2*PagePadding, minW=100, mb=20, mr=10,       # Conditions make the element move to top-left of the page.
        # And the condition that there should be no overflow, otherwise the text box
        # will try to solve it.     
        conditions=[Left2Left(), Float2Top(), Overflow2Next()],
        # Position of the origin of the element. Just to show where it is.
        # Has no effect on the position conditions. 
        yAlign=BOTTOM, xAlign=LEFT,
        leading=5, fontSize=9, textFill=0, strokeWidth=0.5, fill=0.9, stroke=None,
    )
    """
    for line in e1.textLines:
        print line, line.x, line.y
    for foundPattern in e1.findPattern('Line 5'):
        print foundPattern.x, foundPattern.y, foundPattern.line, foundPattern.line.runs
    """
    font = getFontByName(e1.textLines[0].runs[1].displayName)
    c = 'hyphen'
    g = font[c]
    print g.pointContexts[0].p.x
    save()
    scale(0.3)
    path = font[c].path
    fill(1, 0, 0)
    drawPath(path)
    ga = GlyphAnalyzer(font, c)
    for x, vertical in ga.verticals.items():
        stroke(0)
        strokeWidth(1)
        fill(None)
        line((x, 0), (x, 3000))
    print ga.horizontals    
    for y, horizontal in ga.horizontals.items():
        stroke(0)
        strokeWidth(1)
        fill(None)
        line((0, y), (2000, y))
    restore()
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
        fill(0)
        drawPath(path)   
            #oval(p.x/2, p.y/2, 4, 4)
            #print index, pc   
    """
    
    score = doc.solve() # Try to solve all pages.
    if score.fails:
        print score.fails

    return doc # Answer the doc for further doing.
 
if __name__ == '__main__':
           
    d = makeDocument()
    d.export(EXPORT_PATH) 

