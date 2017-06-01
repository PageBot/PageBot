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
from pagebot.conditions import *

class Row(Element):
    pass

class Header(Row):
    u"""The Table header is a special kind of row."""
    pass

class Cell(Element):
   def __init__(self, fs, colSpan=1, rowSpan=1, **kwargs):
        Element.__init__(self,  **kwargs)
        self.colSpan = colSpan
        self.rowSpan = rowSpan
   
class EmptyCell(Element):
    u"""Placeholder cell to make index of columns match up if there are empty areas,
    such as colspan and rowspan."""
    pass

class Table(Element):

    HEADER_CLASS = Header
    ROW_CLASS = Row
    CELL_CLASS = Cell
    EMPTYCELL_CLASS = EmptyCell

    def __init__(self, fs, cols=1, rows=1, **kwargs):
        Element.__init__(self,  **kwargs)
        # Make the column/row/cell dictionary
        self.initCells(cols, rows)

    def initCells(self, cols, rows):
        self.HEADER_CLASS(parent=self)
        for col in range(cols):
            for rowIndex in range(rows):
                row = self.ROW_CLASS(parent=self, conditions=[Fit2Width()])
                for colIndex in range(cols):
                    cell = self.CELL_CLASS(parent=row)

    def solve(self):
        u"""The solve will align all rows and cells to the available space in Table,
        and taking into account what the volume is that cells need and how they align
        in columns and rows."""

    def draw(self, origin, view):
        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(p)    
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        for e in self.elements:
            # TODO: Needs updated x/y value
            e.draw(origin, view)

