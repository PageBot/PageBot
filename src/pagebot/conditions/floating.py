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
#     floating.py
#
from __future__ import division
from condition import Condition

# Margins

class FloatLeft(Condition):
	u"""Align the element.left with max of all placed element.right or parent.left."""
	def test(self, e):
		return e.isFloatLeft(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.float2Left(), e, score)

class FloatRight(Condition):
	u"""Align the element.right with min of all placed element.left or parent.right."""
	def test(self, e):
		return e.isFloatRight(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.float2Right(), e, score)

class FloatTop(Condition):
	u"""Align the element.top with max of all placed element.bottom or parent.top."""
	def test(self, e):
		return e.isFloatTop(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.float2Top(), e, score)

class FloatBottom(Condition):
	u"""Align the element.bottom with max of all placed element.top or parent.bottom."""
	def test(self, e):
		return e.isFloatBottom(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.float2Bottom(), e, score)

# Sides

class FloatLeftSide(Condition):
	u"""Align the element.left with max of all placed element.right or parent.leftSide."""
	def test(self, e):
		return e.isFloatLeftSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.float2LeftSide(), e, score)

class FloatRightSide(Condition):
	u"""Align the element.right with min of all placed element.left or parent.rightSide."""
	def test(self, e):
		return e.isFloatRightSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.float2RightSide(), e, score)

class FloatTopSide(Condition):
	u"""Align the element.top with max of all placed element.bottom or parent.topSide."""
	def test(self, e):
		return e.isFloatTopSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.float2TopSide(), e, score)

class FloatBottomSide(Condition):
	u"""Align the element.bottom with max of all placed element.top or parent.bottomSide."""
	def test(self, e):
		return e.isFloatBottomSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.float2Side(), e, score)

# Combinations

class FloatLeftTop(Condition):
	def test(self, e):
		return e.isFloatLeft(self.tolerance) and e.isFloatTop(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.float2Left() and e.float2Top(), e, score)

class FloatTopLeft(Condition):
	def test(self, e):
		return e.isFloatTop(self.tolerance) and e.isFloatLeft(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.float2Top() and e.float2Left(), e, score)

class FloatRightTop(Condition):
	def test(self, e):
		return e.isFloatRight(self.tolerance) and e.isFloatTop(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.float2Right() and e.float2Top(), e, score)

class FloatTopRight(Condition):
	def test(self, e):
		return e.isFloatTop(self.tolerance) and e.isFloatRight(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.float2Top() and e.float2Right(), e, score)

class FloatLeftBottom(Condition):
	def test(self, e):
		return e.isFloatLeft(self.tolerance) and e.isFloatBottom(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.float2Left() and e.float2Bottom(), e, score)

class FloatBottomLeft(Condition):
	def test(self, e):
		return e.isFloatBottom(self.tolerance) and e.isFloatLeft(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.float2Bottom() and e.float2Left(), e, score)

class FloatRightBottom(Condition):
	def test(self, e):
		return e.isFloatRight(self.tolerance) and e.isFloatBottom(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.float2Right() and e.float2Bottom(), e, score)

class FloatBottomRight(Condition):
	def test(self, e):
		return e.isFloatBottom(self.tolerance) and e.isFloatRight(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.float2Bottom() and e.float2Right(), e, score)

# Combination sides

class FloatLeftTopSides(Condition):
	def test(self, e):
		return e.isFloatLeftSide(self.tolerance) and e.isFloatTopSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.float2LeftSide() and e.float2TopSide(), e, score)

class FloatTopLeftSides(Condition):
	def test(self, e):
		return e.isFloatTopSide(self.tolerance) and e.isFloatLeftSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.float2TopSide() and e.float2LeftSide(), e, score)

class FloatRightTopSides(Condition):
	def test(self, e):
		return e.isFloatRightSide(self.tolerance) and e.isFloatTopSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.float2RightSide() and e.float2TopSide(), e, score)

class FloatTopRightSides(Condition):
	def test(self, e):
		return e.isFloatTopSide(self.tolerance) and e.isFloatRightSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.float2TopSide() and e.float2RightSide(), e, score)

class FloatLeftBottomSides(Condition):
	def test(self, e):
		return e.isFloatLeftSide(self.tolerance) and e.isFloatBottomSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.float2LeftSide() and e.float2BottomSide(), e, score)

class FloatBottomLeftSides(Condition):
	def test(self, e):
		return e.isFloatBottomSide(self.tolerance) and e.isFloatLeftSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.float2BottomSide() and e.float2LeftSide(), e, score)

class FloatRightBottomSides(Condition):
	def test(self, e):
		return e.isFloatRightSide(self.tolerance) and e.isFloatBottomSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.float2RightSide() and e.float2BottomSide(), e, score)

class FloatBottomRightSides(Condition):
	def test(self, e):
		return e.isFloatBottomSide(self.tolerance) and e.isFloatRightSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.float2BottomSide() and e.float2RightSide(), e, score)




