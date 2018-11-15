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
#     Shows how to start a document and export it to PNG and PDF in the simplest steps.
#
#     TODO: Floating on second line does not seem to work currently

from pagebot.toolbox.color import color

EXPORT_PATH = '_export/Start'

# Export in _export folder that does not commit in Git.
# Force to export to a few file formats:
EXPORT_PATH_PDF = EXPORT_PATH + '.pdf'
EXPORT_PATH_JPG = EXPORT_PATH + '.jpg'
EXPORT_PATH_PNG = EXPORT_PATH + '.png'
EXPORT_PATH_SVG = EXPORT_PATH + '.svg'

# Document is the main instance holding all information about the document
# together (pages, styles, etc.)
from pagebot.document import Document
from pagebot.elements import newRect
from pagebot.conditions import *
from pagebot.toolbox.color import Color

W, H = 500, 400

def makeDocument():
    # Creates the publication/document that holds the pages.
    doc = Document(w=W, h=H, originTop=False, autoPages=1)
    print(doc.view)
    print(doc.pages)
    
    doc.view.padding = 200 # Don't show cropmarks in this example.
    #doc.margin = 0
    doc.view.showPadding = True

    # Gets page by pageNumber, first in row (at this point there is only one in
    # this row).
    page = doc[1]
    page.padding = 18
    page.showPadding = True

    conditions = [Right2Right(), Float2Top(), Float2Left()]
    # TODO: Solve this bug, does not mirror.
    #conditions = [Left2Left(), Float2Top(), Float2Right()]
    numberOfSquares = 88
    ratio = 1 / numberOfSquares

    for n in range(numberOfSquares):
        
        newRect(w=40, h=42, mr=4, mt=4, parent=page,
                fill=color(1 - n*ratio, 0, 0.5),
                conditions=conditions, margin=0)

    # Recursively solve the conditions in all pages.
    # If there are failing conditions, then the status
    # is returned in the Score instance.
    score = doc.solve()
    print(score)

    doc.export(EXPORT_PATH_SVG)
    doc.export(EXPORT_PATH_JPG)
    doc.export(EXPORT_PATH_PNG)
    doc.export(EXPORT_PATH_PDF)
    print('Done making document %s' % doc)

makeDocument()
