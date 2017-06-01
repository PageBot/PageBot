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
    def __init__(self, **kwargs):
        Element.__init__(self,  **kwargs)


    def solve(self, score=None):
        u"""The solve will align all rows and cells to the available space in Table,
        and taking into account what the volume is that cells need and how they align
        in columns and rows."""
        if score is None:
            score = Score()
        if self.conditions: # Can be None or empty
            for condition in self.conditions: # Skip in case there are no conditions in the style.
                condition.solve(self, score)

class Header(Row):
    u"""The Table header is a special kind of row. The header holds the titles of 
    the columns and is reference for their widthts."""
    pass

class Cell(Element):
    def __init__(self, colSpan=1, rowSpan=1, **kwargs):
        Element.__init__(self,  **kwargs)
        self.colSpan = colSpan
        self.rowSpan = rowSpan

    def getCell(self, index):
        return self.elements[index]

class HeaderCell(Cell):
    pass

class EmptyCell(Element):
    u"""Placeholder cell to make index of columns match up if there are empty areas,
    such as colspan and rowspan."""
    pass

class Table(Element):

    DEFAULT_H = 18
    DEFAULT_W = DEFAULT_H*4

    HEADER_CLASS = Header
    HEADERCELL_CLASS = HeaderCell
    ROW_CLASS = Row
    CELL_CLASS = Cell
    EMPTYCELL_CLASS = EmptyCell

    def __init__(self, colNames=None, cols=1, rows=1, **kwargs):
        Element.__init__(self,  **kwargs)
        # Make the column/row/cell dictionary
        self.initCells(colNames, cols, rows)

    def initCells(self, colNames, cols, rows):
        cellConditions = [Float2Left(), Top2Top(), Fit2Bottom()]
        rowConditions = [Fit2Width(), Float2Top()]
 
        header = self.HEADER_CLASS(parent=self, fill=(0, 1, 0), borders=6, conditions=rowConditions) # Header as first row element.
        for colIndex, col in enumerate(range(cols)):
            if colNames is not None:
                colName = colNames[colIndex]
            else:
                colName = None
            self.HEADERCELL_CLASS(parent=header, w=self.DEFAULT_W, h=self.DEFAULT_H, name=colName, 
                conditions=cellConditions)

        for rowIndex in range(rows):
            row = self.ROW_CLASS(parent=self, h=self.DEFAULT_H, conditions=rowConditions)
            for colIndex in range(cols):
                self.CELL_CLASS(parent=row, w=self.DEFAULT_W, h=self.DEFAULT_H, fill=(1, 0, 0), 
                    conditions=cellConditions)

    def getHeader(self):
        return self.elements[0]

    def setHeader(self, header):
        self.elements[0] = header

    def getRow(self, index):
        u"""Answer the Row instance at index. Same as self.elements[index]. Raise an index error
        if the row index does not exist."""
        return self.elements[index]

    def getColumn(self, index):
        u"""Answer a list if cells (including the header) of the indexed column."""
        column = []
        for row in self.elements:
            column.append(row.getCell(index))
        return column

    def draw(self, origin, view):
        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(p)    
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        self.drawFrame(p, view) # Draw optional frame or borders.

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, p, view)

        # If there are child elements, draw them over the text.
        # TODO: Needs updated x/y value
        self._drawElements(p, view)
 
        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, p, view)

        self._restoreScale()
        view.drawElementMetaInfo(self, origin) # Depends on css flag 'showElementInfo'

