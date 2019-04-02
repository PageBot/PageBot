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
#     columns.py
#
from pagebot.conditions.condition import Condition

#	F I T T I N G  C O L U M N S

class ColCondition(Condition):
    def __init__(self, col=0, colSpan=1, row=0, rowSpan=1, value=1, tolerance=1, error=-10, verbose=False):
    	Condition.__init__(self, value=value, tolerance=tolerance, error=-error, verbose=verbose)
    	self.col = col
    	self.row = row
    	self.colSpan = colSpan
    	self.rowSpan = rowSpan

class RowCondition(Condition):
    def __init__(self, row=0, rowSpan=1, col=0, colSpan=1, value=1, tolerance=1, error=-10, verbose=False):
    	Condition.__init__(self, value=value, tolerance=tolerance, error=-error, verbose=verbose)
    	self.col = col
    	self.row = row
    	self.colSpan = colSpan
    	self.rowSpan = rowSpan

class Left2Col(ColCondition):
	"""Fit the left of the element on the column index #, as defined in self.col.

	>>> from pagebot.elements import Element
	>>> from pagebot.constants import mm
	>>> C, G, PAD = mm(50), mm(5), mm(20) # Column width, gutter and element paddig
	>>> gridX = [(C, G), (C, G), (C, G), (C, G), (C, G)] # Create the column grid
	>>> W = len(gridX) * (C + G) + 2 * PAD
	>>> e1 = Element(w=W, h=500, gridX=gridX, padding=PAD)
	>>> e2 = Element(parent=e1, conditions=[Left2Col(1)])
	>>> e2.x # Original default position
	0pt
	>>> result = e1.solve() # Solve the conditions
	>>> e2.x # Solved position
	75mm
	>>> e2.conditions = [Left2Col(2)] # Change condition and solve again
	>>> result = e1.solve()
	>>> e2.x # Solved position
	130mm
	>>> e2.conditions = [Left2Col(3)] # Change condition and solve again
	>>> result = e1.solve()
	>>> e2.x # Solved position
	185mm
	"""
	def test(self, e):
		return e.isLeftOnCol(self.col, self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails.
			self.addScore(e.left2Col(self.col), e, score)

class Right2Col(ColCondition):
	"""Fit the left of the element on the column index #, as defined in self.col.

	>>> from pagebot.elements import Element
	>>> from pagebot.constants import mm
	>>> C, G, PAD = mm(50), mm(5), mm(20) # Column width, gutter and element paddig
	>>> gridX = [(C, G), (C, G), (C, G), (C, G), (C, G)] # Create the column grid
	>>> W = len(gridX) * (C + G) + 2 * PAD
	>>> e1 = Element(w=W, h=500, gridX=gridX, padding=PAD)
	>>> e2 = Element(parent=e1, conditions=[Right2Col(2)])
	>>> e2.x # Original default position
	0pt
	>>> result = e1.solve() # Solve the conditions
	>>> e2.x # Solved position
	130mm
	>>> e2.conditions = [Right2Col(3)] # Change condition and solve again
	>>> result = e1.solve()
	>>> e2.x # Solved position
	185mm
	>>> e2.conditions = [Right2Col(4)] # Change condition and solve again
	>>> result = e1.solve()
	>>> e2.x # Solved position
	240mm
	"""
	def test(self, e):
		return e.isRightOnCol(self.col, self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails.
			self.addScore(e.right2Col(self.col), e, score)

class Fit2ColSpan(ColCondition):
	u"""Fit the width of the element to the col spans self.colSpan starting at self.col."""
	def test(self, e):
		return e.isLeftOnCol(self.col, self.tolerance) and e.isFitOnColSpan(self.col, self.colSpan, self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails.
			self.addScore(e.left2Col(self.col), e, score)
			self.addScore(e.fit2ColSpan(self.col, self.colSpan), e, score)

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

class Fit2RowSpan(RowCondition):
	u"""Fit the left of the element on the column index #, as defined in self.col."""
	def test(self, e):
		return e.isTopOnCol(self.row, self.tolerance) and e.isFitOnRowSpan(self.row, self.rowSpan, self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails.
			self.addScore(e.top2Row(self.row), e, score)
			self.addScore(e.fit2RowSpan(self.row, self.rowSpan), e, score)


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

