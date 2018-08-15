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
#     UseGlyphPathElement.py
#
#     TODO: Needs some cleaning to get letter better in page, with lifted baseline.
#
import pagebot # Import to know the path of non-Python resources.

from pagebot.fonttoolbox.fontpaths import getTestFontsPath
from pagebot.contexts.platform import getContext
# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, A4, CENTER, RIGHT, LEFT,TOP, BOTTOM, MM
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
from pagebot.fonttoolbox.objects.font import getFont

from pagebot.conditions import *
from pagebot.elements import *
from pagebot.document import Document
from pagebot.toolbox.color import color, noColor, blackColor
from pagebot.toolbox.units import pt

context = getContext()

PagePadding = 32
PageSize = 500

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/GlyphPathElement.pdf'

def pathFilter(e, path, view):
    r = pt(24)
    for x in range(0, int(e.w)*4, 30):
        for y in range(0, int(e.h)*2, 30):
            # Use the glyph to query for color at this position.
            if e.glyph is not None:
                if e.glyph.onBlack((x, y)):
                    context.fill(color(random(), random(), random())) # Color as one tuple, in context API
                    context.oval(pt(x-r/2), pt(y-r/2), r, r)
                else:
                    context.fill(color(0, 1, 0)) # Color as one tuple, in context API
                    context.rect(pt(x-r/4), pt(y-r/4), r/2, r/2)

#W = H = 120 # Get the standard a4 width and height in points.
W = H = PageSize
#W, H = A4

fontPath = getTestFontsPath() + '/djr/bungee/Bungee-Regular.ttf'
font = getFont(fontPath)
glyphName = 'e'#'cid05405.1'

doc = Document(w=W, h=H, originTop=False, autoPages=1)

view = doc.getView()
view.padding = 40 # Aboid showing of crop marks, etc.
view.showPageCropMarks = True
view.showPageRegistrationMarks = True
view.showPageFrame = True
view.showElementOrigin = True
view.showElementDimensions = False

# Get list of pages with equal y, then equal x.
#page = doc[1][0] # Get the single page from te document.
page = doc.getPage(1) # Get page on pageNumber, first in row (this is only one now).
page.name = 'This is a demo page for floating child elements'

e1 = GlyphPath(font[glyphName], stroke=noColor, h=600,
    fill=noColor, pathFilter=pathFilter,
    parent=page, font='Verdana',
    conditions=[Left2Left(), Float2Top()])

score = page.solve()
if score.fails:
    print(score.fails)
e1.y += 100
#e2.y += 100

doc.export(EXPORT_PATH)
