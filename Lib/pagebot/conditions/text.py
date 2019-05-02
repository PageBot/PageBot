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
            index=0, index2=0, style=None):
        self.value = value # Value to answer if the condition is valid
        self.tolerance = tolerance
        self.error = error
        self.verbose = verbose
        self.index = index
        self.index2 = index2
        self.style = style

# Fitting text

class Shrink2TextBounds(Condition):
    def test(self, e):
        return e.isShrunkOnTextHeight(self.tolerance) and e.isShrunkOnTextWidth(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.shrink2TextHeight(), e, score)
            self.addScore(e.shrink2TextWidth(), e, score)
        
class Shrink2TextHeight(Condition):
    def test(self, e):
        return e.isShrunkOnTextHeight(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.shrink2TextHeight(), e, score)
        
class Shrink2TextWidth(Condition):
    def test(self, e):
        return e.isShrunkOnTextWidth(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.shrink2TextWidth(), e, score)
        
# Baseline alignmenets

class Baseline2Grid(BaselineCondition):

    def test(self, e):
        return e.isBaselineOnGrid(self.tolerance, index=self.index)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.baseline2Grid(index=self.index), e, score)

class BaselineUp2Grid(BaselineCondition):

    def test(self, e):
        return e.isBaselineOnGrid(self.tolerance, index=self.index)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.baselineUp2Grid(index=self.index), e, score)

class BaselineDown2Grid(BaselineCondition):
    def test(self, e):
        return e.isBaselineOnGrid(self.tolerance, index=self.index)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.baselineDown2Grid(index=self.index), e, score)

class Baseline2Top(BaselineCondition):
    """Place the first baseline on the parent top padding position. Use the
    regular Top2Top() to place the top of the text on the parent top
    padding position."""
    def test(self, e):
        return e.isBaselineOnTop(self.tolerance, index=self.index)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.baseline2Top(index=self.index), e, score)

class Baseline2Bottom(BaselineCondition):
    def test(self, e):
        return e.isBaselineOnBottom(self.tolerance, index=self.index)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.baseline2Bottom(index=self.index), e, score)

# Capheight alignments

class CapHeight2Top(BaselineCondition):
    def test(self, e):
        return e.isCapHeightOnTop(self.tolerance, index=self.index)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.capHeight2Top(index=self.index), e, score)

class CapHeight2Bottom(BaselineCondition):
    def test(self, e):
        return e.isCapHeightOnBottom(self.tolerance, index=self.index)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.capHeight2Bottom(index=self.index), e, score)

# xHeight alignments

class XHeight2Top(BaselineCondition):
    def test(self, e):
        return e.isXHeightOnTop(self.tolerance, index=self.index)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.xHeight2Top(index=self.index), e, score)

class XHeight2Bottom(BaselineCondition):
    def test(self, e):
        self.addScore(e.isXHeightOnBottom(self.tolerance, index=self.index))

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.xHeight2Bottom(index=self.index), e, score)



''' 

class Baseline2Bottom(Condition):
    def test(self, e):
        return e.isBaselineOnBottom(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.baseline2Bottom(), e, score)

#   Floating

class FloatBaseline2Top(Condition):
    """Try to do `Baseline2Top()` or position just under – truncated locked
    on parent baseline – if there are already elements in the same
    z-layer."""
    def test(self, e):
        return e.isBaselineOnTop(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.floatBaseline2Top(), e, score)

class FloatAscender2Top(Condition):
    """Try to place the ascender of the first line on the parent top
    padding position. Or just under – truncated locked on parent baseline –
    if there are already elements in the same z-layer."""
    def test(self, e):
        return e.isAscenderOnTop(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.floatAscender2Top(), e, score)

class FloatCapHeight2Top(Condition):
    """Try to place the CapHeight of the first line on the parent top
    padding position. Or just under – truncated locked on parent baseline –
    if there are already elements in the same z-layer."""
    def test(self, e):
        return e.isCapHeightOnTop(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.floatCapHeight2Top(), e, score)

class FloatXHeight2Top(Condition):
    """Try to place the xHeight of the first line on the parent top padding
    position. Or just under – truncated locked on parent baseline – if
    there are already elements in the same z-layer."""
    def test(self, e):
        return e.isXHeightOnTop(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.floatXHeight2Top(), e, score)

'''

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
