# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#     
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     columns.py
#
from __future__ import division
from pagebot.conditions.condition import Condition

#	F I T T I N G  C O L U M N S

class ColCondition(Condition):
    def __init__(self, col=0, row=0, colSpan=1, rowSpan=1, value=1, tolerance=1, error=-10, verbose=False):
    	Condition.__init__(self, value=value, tolerance=tolerance, error=-error, verbose=verbose)
    	self.col = col
    	self.row = row
    	self.colSpan = colSpan
    	self.rowSpan = rowSpan

class RowCondition(Condition):
    def __init__(self, col=0, row=0, colSpan=1, rowSpan=1, value=1, tolerance=1, error=-10, verbose=False):
    	Condition.__init__(self, value=value, tolerance=tolerance, error=-error, verbose=verbose)
    	self.col = col
    	self.row = row
    	self.colSpan = colSpan
    	self.rowSpan = rowSpan

class Left2Col(ColCondition):
	u"""Fit the left of the element on the column index #, as defined in self.col."""
	def test(self, e):
		return e.isLeftOnCol(self.col, self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.left2Col(self.col), e, score)

class Right2Col(ColCondition):
	u"""Fit the left of the element on the column index #, as defined in self.col."""
	def test(self, e):
		return e.isRightOnCol(self.col, self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.right2Col(self.col), e, score)

class Fit2Colspan(ColCondition):
	u"""Fit the left of the element on the column index #, as defined in self.col."""
	def test(self, e):
		return e.isLefOnCol(self.col, self.tolerance) and e.isFitOnColspan(self.col, self.colSpan, self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.left2Col(self.col), e, score)
			self.addScore(e.fit2Colspan(self.col, self.colSpan), e, score)

class Top2Row(RowCondition):
	u"""Fit the left of the element on the column index #, as defined in self.col."""
	def test(self, e):
		return e.isTopOnRow(self.row, self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.top2Row(self.row), e, score)

class Bottom2Row(RowCondition):
	u"""Fit the left of the element on the column index #, as defined in self.col."""
	def test(self, e):
		return e.isBottomOnRow(self.row, self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.bottom2Row(self.row), e, score)

class Fit2Rowspan(RowCondition):
	u"""Fit the left of the element on the column index #, as defined in self.col."""
	def test(self, e):
		return e.isTopOnCol(self.row, self.tolerance) and e.isFitOnRowspan(self.row, self.rowSpan, self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.top2Row(self.row), e, score)
			self.addScore(e.fit2Rowspan(self.row, self.rowSpan), e, score)

