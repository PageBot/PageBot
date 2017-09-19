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
#     UseGlyphPathElement.py
#
import pagebot # Import to know the path of non-Python resources.

# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, A4, CENTER, RIGHT, LEFT, NO_COLOR,TOP, BOTTOM, MM
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
from pagebot import newFS
from pagebot.fonttoolbox.objects.font import Font

from pagebot.conditions import *
from pagebot.elements import *
from pagebot.document import Document

PagePadding = 32
PageSize = 500

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/UseGlyphPathElement.pdf' 

def pathFilter(e, path):
    r = 18
    for x in range(0, e.iw, 20):
        for y in range(0, e.ih, 20):
            if e.glyph.onBlack((x, y)):
                fill(random(), random(), random())
                oval(x-r/2, y-r/2, r, r)
            else:
                fill(0, 1, 0)
                rect(x-r/4, y-r/4, r/2, r/2)
    
def makeDocument():
    u"""Make a new document."""

    #W = H = 120 # Get the standard a4 width and height in points.
    W = H = PageSize
    #W, H = A4

    doc = Document(w=W, h=H, originTop=False, autoPages=1)
    
    view = doc.getView()
    view.padding = 40 # Aboid showing of crop marks, etc.
    view.showPageCropMarks = True
    view.showPageRegistrationMarks = True
    view.showPageFrame = True
    view.showElementOrigin = True
    view.showElementDimensions = False
    
    # Get list of pages with equal y, then equal x.    
    #page = doc[0][0] # Get the single page from te document.
    page = doc.getPage(0) # Get page on pageNumber, first in row (this is only one now).
    page.name = 'This is a demo page for floating child elements'

    PATH = u"/Library/Fonts/F5MultiLanguageFontVar.ttf"
    f = Font(PATH, install=False)
    #pathFilter = None
    glyphName = 'e'#'cid05405.1'
    
    e1 = GlyphPath(f[glyphName], stroke=None, h=600,
        fill=None, pathFilter=pathFilter,
        parent=page, font='Verdana',       
        conditions=[Left2Left(), Float2Top()])
    """
    e2 = GlyphPath(f[glyphName], stroke=(1, 0, 0), h=600,
        fill=None, strokeWidth=20, 
        parent=page, font='Verdana',       
        conditions=[Left2Left(), Float2Top()])
    """
    score = page.solve()
    if score.fails:
        print score.fails
    e1.y += 100
    #e2.y += 100

    return doc # Answer the doc for further doing.
 
if __name__ == '__main__':

    Variable([
        dict(name='PageSize', ui='Slider', args=dict(minValue=200, value=500, maxValue=PageSize)),
    ], globals())
           
    d = makeDocument()
    d.export(EXPORT_PATH) 

