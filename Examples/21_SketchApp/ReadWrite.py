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

path = '/Users/petr/Dropbox/Production_TYPE-3/3_Pages_TYPE-3/Sketch/Noordzij_Layout-02_rb_TYPE-3.sketch'
path = '/Users/petr/Dropbox/Production_TYPE-3/3_Pages_TYPE-3/Sketch/TestImage.sketch'
doc = context.readDocument(path, w=W, h=H, originTop=True)

view = doc.view
view.padding = 30
view.showCropMarks = True
#view.showPadding = True
view.showOrigin = False
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
        print('=====', artboard.gridX, artboard.gridY)


doc.export('_export/TestImage.pdf')