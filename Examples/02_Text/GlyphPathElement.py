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
from random import random
import pagebot # Import to know the path of non-Python resources.

from pagebot.fonttoolbox.fontpaths import getTestFontsPath
from pagebot import getContext
# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle
from pagebot.constants import A4, CENTER, RIGHT, LEFT,TOP, BOTTOM
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
from pagebot.fonttoolbox.objects.font import getFont

from pagebot.conditions import *
from pagebot.elements import *
from pagebot.document import Document
from pagebot.toolbox.color import color, noColor, blackColor
from pagebot.toolbox.units import pt

context = getContext()

PAGE_PADDING = 32
W, H = A4
W, H = 500, 500

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/GlyphPathElement.pdf'

def pathFilter(e, glyph, view):
    r = pt(24)
    grid = 30
    path = context.getGlyphPath(glyph)
    for x in range(0, int(e.w)*4, grid):
        for y in range(0, int(e.h)*2, grid):
            # Use the glyph to query for color at this position.
            if e.glyph is not None:
                if context.onBlack((x, y), path):
                    context.fill(color(random(), random(), random())) # Color as one tuple, in context API
                    context.oval(pt(x-r/4), pt(y-r/4), r/2, r/2)
                else:
                    context.fill(color(0, 1, 0)) # Color as one tuple, in context API
                    context.oval(pt(x-r/8), pt(y-r/8), r/4, r/4)

                if context.onBlack((x, y), path) and (
                        not context.onBlack((x+grid, y), path) or
                        not context.onBlack((x+grid, y-grid), path)
                    ):
                    context.fill(0)
                    context.oval(pt(x-r/2), pt(y-r/2), r, r)

    context.stroke((1, 0, 0))
    context.fill(noColor)
    context.drawPath(path)
    context.stroke((0, 1, 0), 5)
    context.rect(e.x, e.y, e.w, e.h)

fontPath = getTestFontsPath() + '/djr/bungee/Bungee-Regular.ttf'
font = getFont(fontPath)
glyphName = 'e'#'cid05405.1'

doc = Document(w=W, h=H, originTop=False, autoPages=1)

view = doc.getView()
view.padding = 40 # Aboid showing of crop marks, etc.
view.showCropMarks = True
view.showRegistrationMarks = True
view.showFrame = True
view.showOrigin = True
view.showDimensions = False
view.showFrame = True

# Get list of pages with equal y, then equal x.
#page = doc[1][0] # Get the single page from te document.
page = doc.getPage(1) # Get page on pageNumber, first in row (this is only one now).
page.name = 'This is a demo page for floating child elements'
page.padding = PAGE_PADDING

e1 = GlyphPath(font[glyphName], stroke=noColor,
    fill=noColor, pathFilter=pathFilter,
    parent=page, font='Verdana',
    conditions=[Left2Left(), Top2Top()])


#score = page.solve()

doc.export(EXPORT_PATH)
