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
#     text.py
#
#     These conditions define the state of flow between elements. If the
#     element with this condition as unmatched overflow, then it needs to try
#     to solve it. Otherwise a fail remains after self.solve()
#
from pagebot.conditions.condition import Condition

# Margins

class Overflow2Next(Condition):
    """If there is overflow in the element, then try to solve it. Note that
    when used in a Composer-typesetter environment, this will not update the
    `globals['page']` value. In that case it is better to call the
    `Element.overflow2Next()` directly at the start of a new chapter."""
	def test(self, e):
		return e.isOverflow(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails.
			self.addScore(e.overflow2Next(), e, score)

# Columns

class EqualizeFlow2Height(Condition):
        """Test if all elements in the flow the same height and/or same amount
        text lines."""
	# TODO

class BaselineCondition(Condition):

    def __init__(self, value=1, tolerance=1, error=-10, verbose=False,
            index=None, style=None):
        self.value = value # Value to answer if the condition is valid
        self.tolerance = tolerance
        self.error = error
        self.verbose = verbose
        self.index = index
        self.style = style

# Baseline alignmenets

class Baseline2Grid(BaselineCondition):

	def test(self, e):
		return e.isBaselineOnGrid(self.tolerance, index=self.index, style=self.style)

	def solve(self, e, score):
		return e.baseline2Grid(index=self.index, style=self.style)

class BaselineUp2Grid(BaselineCondition):

	def test(self, e):
		return e.isBaselineOnGrid(self.tolerance, index=self.index, style=self.style)

	def solve(self, e, score):
		return e.baselineUp2Grid(index=self.index, style=self.style)

class BaselineDown2Grid(BaselineCondition):
	def test(self, e):
		return e.isBaselineOnGrid(self.tolerance, index=self.index, style=self.style)

	def solve(self, e, score):
		return e.baselineDown2Grid(index=self.index, style=self.style)

class Baseline2Top(BaselineCondition):
	def test(self, e):
		return e.isBaselineOnTop(self.tolerance, index=self.index, style=self.style)

	def solve(self, e, score):
		return e.baseline2Top(index=self.index, style=self.style)

class Baseline2Bottom(BaselineCondition):
	def test(self, e):
		return e.isBaselineOnBottom(self.tolerance, index=self.index, style=self.style)

	def solve(self, e, score):
		return e.baseline2Bottom(index=self.index, style=self.style)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
