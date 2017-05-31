# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     pbtextbox.py
#
import re
import CoreText
import Quartz

from drawBot import textOverflow, hyphenation, textBox, rect, textSize, FormattedString, line

from pagebot.style import LEFT, RIGHT, CENTER, NO_COLOR, MIN_WIDTH, MIN_HEIGHT, makeStyle
from pagebot.elements.element import Element
from pagebot.toolbox.transformer import pointOffset
from pagebot import newFS, setStrokeColor, setFillColor
from pagebot.fonttoolbox.objects.glyph import Glyph

          
class Table(Element):

    def __init__(self, fs, cols=1, rows=1, **kwargs):
        Element.__init__(self,  **kwargs)
        # Make the column/row/cell dictionary
        self.initCells(cols, rows)

    def initCells(self):
        self.cells = {} # Key is col/row index.
        for col in range(cols):
            for row in range(rows):
                self.cells[(col, row)] = Cell(row=row, row=row, conditions=[])

    def draw(self, origin, view):
        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(p)    
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        columnWidths = self._getColumnWidths()
        rowHeights = self._getRowHeights()
        for (x, y), cell in self.cells.items():
            cell.draw((px+columWidth[x], py+rowHeights[y]), view)




