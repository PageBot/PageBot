#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
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
#     pbtable.py
#
from pagebot.constants import CENTER, ORIGIN, MIDDLE
from pagebot.elements.element import Element
from pagebot.toolbox.units import pointOffset
from pagebot.conditions import *
from pagebot.elements.pbtextbox import TextBox
from pagebot.toolbox.color import whiteColor, blackColor, color

class Row(Element):
    def __init__(self, **kwargs):
        Element.__init__(self,  **kwargs)

    def getCell(self, index):
        return self.elements[index]

class Header(Row):
    """The Table header is a special kind of row. The header holds the titles
    of the columns and is reference for their widthts."""
    pass

class Cell(TextBox):
    def __init__(self, fs, minW=None, w=None, h=None, colSpan=1, rowSpan=1, **kwargs):
        TextBox.__init__(self,  fs, minW=minW, w=w, h=h, **kwargs)
        self.colSpan = colSpan
        self.rowSpan = rowSpan

class HeaderCell(Cell):
    pass

class EmptyCell(Element):
    """Placeholder cell to make index of columns match up if there are empty
    areas, such as colspan and rowspan."""
    pass

class Table(Element):

    DEFAULT_H = 12
    DEFAULT_W = DEFAULT_H*4

    HEADER_CLASS = Header
    HEADERCELL_CLASS = HeaderCell
    ROW_CLASS = Row
    CELL_CLASS = Cell
    EMPTYCELL_CLASS = EmptyCell

    COLNAMES = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def __init__(self, colNames=None, cols=1, rows=1, fillHeader=0.8, **kwargs):
        Element.__init__(self,  **kwargs)
        # Make the column/row/cell dictionary
        self.initCells(colNames, cols, rows, fillHeader)

    def _get_colNames(self):
        return self._colNames
    def _set_colNames(self, colNames):
        self._colNames = colNames or self.COLNAMES
    colNames = property(_get_colNames, _set_colNames)

    def initCells(self, colNames, cols, rows, fillHeader):
        self.colNames = colNames
        cellConditions = [Float2Left(), Top2Top(), Fit2Bottom()]
        rowConditions = [Fit2Width(), Float2Top()]

        header = self.HEADER_CLASS(parent=self, h=self.DEFAULT_H, fill=fillHeader, conditions=rowConditions) # Header as first row element.
        for colIndex, col in enumerate(range(cols)):
            bs = self.newString(self.colNames[colIndex], style=dict(font='Verdana-Bold', textFill=whiteColor, fontSize=10))
            if colNames is not None:
                colName = colNames[colIndex]
            else:
                colName = None
            self.HEADERCELL_CLASS(bs, parent=header, w=self.DEFAULT_W, h=self.DEFAULT_H,
                xTextAlign=CENTER, yTextAlign=MIDDLE, name=colName,
                borders=self.borders, fill=color(0.4), conditions=cellConditions)

        bs = self.newString('abc', style=dict(font='Verdana', textFill=blackColor, fontSize=10))
        for rowIndex in range(rows):
            row = self.ROW_CLASS(parent=self, h=self.DEFAULT_H, conditions=rowConditions)
            for colIndex in range(cols):
                self.CELL_CLASS(bs, parent=row, w=self.DEFAULT_W, h=self.DEFAULT_H, borders=self.borders,
                    xTextAlign=CENTER, yTextAlign=MIDDLE, conditions=cellConditions)

    def getHeader(self):
        return self.elements[0]

    def setHeader(self, header):
        self.elements[0] = header

    def getRow(self, index):
        """Answers the Row instance at index. Same as self.elements[index].
        Raise an index error if the row index does not exist."""
        return self.elements[index]

    def getColumn(self, index):
        """Answers a list if cells (including the header) of the indexed column."""
        column = []
        for row in self.elements:
            column.append(row.getCell(index))
        return column

    #   F L O W

    def getOverflow(self):
        overflow = []
        for row in self.elements:
            if row.y < 0:
                overflow.append(row)
        return overflow

    def isOverflow(self, tolerance):
        """Answers if this element needs overflow to be solved. This method is
        typically called by conditions such as Overflow2Next."""
        return self.nextElement is None or not self.getOverflow()

    def overflow2Next(self):
        """Try to fix if there is overflow."""
        result = True
        overflow = self.getOverflow()
        if overflow and self.nextElement: # If there is text overflow and there is a next element?
            result = False
            # Find the page of self
            page = self.getElementPage()
            if page is not None:
                # Try next page
                nextElement = page.getElementByName(self.nextElement) # Optional search  next page too.
                if nextElement is None or nextElement.fs and self.nextPage:
                    # Not found or not empty, search on next page.
                    page = self.doc.getPage(self.nextPage)
                    nextElement =  page.getElementByName(self.nextElement)
                if nextElement is not None and not nextElement.bs:
                    # Finally found one empty box on this page or next page?
                    nextElement.fs = overflow
                    nextElement.prevPage = page.name
                    nextElement.prevElement = self.name # Remember the back link
                    score = nextElement.solve() # Solve any overflow on the next element.
                    result = not score.fails # Test if total flow placement succeeded.
        return result

    #   D R A W B O T / F L A T  S U P P O R T

    def build(self, view, origin=ORIGIN, drawElements=True, **kwargs):

        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        self.drawFrame(view, p) # Draw optional frame or borders.

        # Let the view draw frame info for debugging, in case view.showFrame == True
        view.drawElementFrame(self, p)

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        if drawElements:
            self.buildChildElements(view, p, **kwargs)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreScale(view)
        view.drawElementInfo(self, origin) # Depends on css flag 'showElementInfo'

    #   H T M L  /  S A S S  S U P P O R T

    def build_html(self, view, origin=None, drawElements=True, **kwargs):

        p = pointOffset(self.origin, origin)
        p = self._applyScale(p)
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        if drawElements:
            self.buildChildElements(view, p, **kwargs)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreScale(view)
        view.drawElementInfo(self, origin) # Depends on css flag 'showElementInfo'



