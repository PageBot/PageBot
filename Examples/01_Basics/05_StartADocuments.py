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
#     05_Document.py
#
#     Shows how to start a document and export it to PNG and 
#     PDF in the simplest steps.
#
#     TODO: Floating on second line does not seem to work currently

from pagebot.toolbox.color import color
from pagebot.toolbox.units import pt

EXPORT_PATH = '_export/StartADocument'

# Export in _export folder that does not commit in Git.
# Force to export to a few file formats:
EXPORT_PATHS = (
    EXPORT_PATH + '.pdf',
    EXPORT_PATH + '.jpg',
    EXPORT_PATH + '.png',
    EXPORT_PATH + '.svg'
)

# Document is the main instance holding all information about the document
# together (pages, styles, etc.)
from pagebot.document import Document
from pagebot.elements import *
from pagebot.conditions import *
from pagebot.toolbox.color import Color

W, H = pt(500, 400)
RW = RH = pt(40)
PADDING = pt(28)

def makeDocument():
    # Creates the publication/document that holds the pages.
    doc = Document(w=W, h=H, originTop=False, autoPages=1)

    # Gets page by pageNumber, first in row (at this point there is only one in
    # this row).
    page = doc[1]
    page.padding = PADDING
    page.showPadding = True

    
    conditions = [Right2Right(), Float2Top(), Float2Left()]
    # TODO: Solve this bug, does not mirror.
    conditions = (
        Left2Left(), 
        Float2Top(), 
        Float2Right()
    )
    numberOfSquares = 88
    ratio = 1 / numberOfSquares

    for n in range(numberOfSquares):
        newRect(w=RW, h=RH, parent=page,
                fill=color(1 - n*ratio, 0, 0.5),
                conditions=conditions, margin=0)

    # Recursively solve the conditions in all page child elements..
    # If there are failing conditions, then the status
    # is returned in the Score instance.
    score = doc.solve()
    # Export to various export formats
    for exportPath in EXPORT_PATHS:
        doc.export(exportPath)

makeDocument()