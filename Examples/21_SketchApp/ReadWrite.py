# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     ReadWrite.py
#
from pagebot import getResourcesPath
from pagebot.toolbox.finder import Finder
from pagebot.document import Document
from pagebot.contexts.sketchcontext import SketchContext
from pagebot.constants import *

context = SketchContext()

W, H = inch(8, 10.875)

path = 'TestImage.sketch'

doc = context.readDocument(path, w=W, h=H, originTop=True)

view = doc.view
view.padding = 30
view.showCropMarks = True
#view.showPadding = True
view.showOrigin = False
view.showRegistrationMarks = True
view.showGrid = [GRID_COL, GRID_ROW]
view.showCropMarks = True
view.showFrame = True
#view.showDimensions = True

for pn, pages in doc.pages.items():
    page = pages[0]
    for artboard in page.elements:
        page.gridX = artboard.gridX
        page.gridY = artboard.gridY
        print(artboard.xy, artboard.size)
        for e in artboard.elements:
            print(e)
            for e1 in e.elements:
                print('\t', e)
        #print('=====', artboard.gridX, artboard.gridY)


EXPORT_PATH = '_export/TestImage.pdf'
doc.export(EXPORT_PATH)
