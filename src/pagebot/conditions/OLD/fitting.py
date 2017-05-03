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
#     fitting.py
#
from __future__ import division
from condition import Condition

#	F I T T I N G  

class Fit(Condition):

	def _getConditions(self):
		from horizontals import AlignLeft, AlignTop
		return [AlignLeft, AlignTop, FitRight, FitBottom]

	def evaluate(self, e, score):
		u"""Fit the element on all margins of the parent. First align left and top,
		then fit right and bottom. This order to avoid that element temporary
		get smaller than their minimum size, if the start position is wrong."""
		self.evaluateAll(e, self._getConditions(), score)

	def solve(self, e, score):	
		from horizontals import AlignLeft, AlignTop
		self.solveAll(e, self._getConditions(), score)

class FitSides(Condition):

	def _getConditions(self):
		from horizontals import AlignLeftSide, AlignTopSide
		return [AlignLeftSide, AlignTopSide, FitRightSide, FitBottomSide]

	def evaluate(self, e, score):
		u"""Fit the element on all sides of the parent."""
		self.evaluateAll(e, self._getConditions(), score)

	def solve(self, e, score):	
		self.solveAll(e, self._getConditions(), score)

#	F I T T I N G  M A R G I N

# There are no "FitOrigin" condition, as these mau result is extremely large scalings.

class FitLeft(Condition):
	def test(self, e):
		return e.isAlignedLeft(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.fitLeft(), e, score)

class FitRight(Condition):
	def test(self, e):
		return e.isAlignedRight(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.fitRight(), e, score)

class FitTop(Condition):
	def test(self, e):
		return e.isAlignedTop(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.fitTop(), e, score)

class FitBottom(Condition):
	def test(self, e):
		return e.isAlignedBottom(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.fitBottom(), e, score)

#	F I T T I N G  S I D E S

# There are no "FitOrigin" condition, as these mau result is extremely large scalings.

class FitLeftSide(Condition):
	def test(self, e):
		return e.isAlignedLeftSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.fitLeftSide(), e, score)

class FitRightSide(Condition):
	def test(self, e):
		return e.isAlignedRightSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.fitRightSide(), e, score)

class FitTopSide(Condition):
	def test(self, e):
		return e.isAlignedTopSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.fitTopSide(), e, score)

class FitBottomSide(Condition):
	def test(self, e):
		return e.isAlignedBottomSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.fitBottomSide(), e, score)
