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
#     horizontals.py
#
from __future__ import division
from condition import Condition

#	C E N T E R

class Center2Center(Condition):
	u"""Center e bounding box between parent margins."""
	def test(self, e):
		return e.isCentered(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.alignCenter(), e, score)

class CenterOrigin(Condition):
	u"""Center e origin between parent margins."""
	def test(self, e):
		return e.isCenteredOrigin(self.tolerance)

	def solve(addScore, e, score):
		self.addScore(not self.test(e) and e.alignCenterOrigin(), e, score)

class CenterSide(Condition):
	u"""Center e bounding box between parent sides."""
	def test(self, e):
		return e.isCenteredSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.alignCenterSide(), e, score)

class CenterOriginSide(Condition):
	u"""Center e bounding box between parent sides."""
	def test(self, e):
		return e.isCenteredOriginSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.alignCenterOriginSide(), e, score)


#	L E F T

class AlignLeft(Condition):
	u"""Align e.left on left margin of parent."""
	def test(self, e):
		return e.isAlignedLeft(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.alignLeft(), e, score)

class AlignLeftSide(Condition):
	u"""Align e.left on left side of parent."""
	def test(self, e):
		return e.isAlignedLeftSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.alignLeftSide(), e, score)

class AlignLeftOrigin(Condition):
	u"""Align e.x on left margin of parent."""
	def test(self, e):
		return e.isAlignedLeftOrigin(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.alignLeftOrigin(), e, score)

class AlignLeftOriginSide(Condition):
	u"""Align e.x on left side of parent."""
	def test(self, e):
		return e.isAlignedLeftOriginSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.alignLeftOriginSide(), e, score)

#   R I G H T

class AlignRight(Condition):
	u"""Align e.right on right margin of parent."""
	def test(self, e):
		return e.isAlignedRight(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.alignRight(), e, score)

class AlignRightSide(Condition):
	u"""Align e.right on right side of parent."""
	def test(self, e):
		return e.isAlignedRightSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.alignRightSide(), e, score)

class AlignOriginRight(Condition):
	u"""Align e.x on right margin of parent."""
	def test(self, e):
		return e.isAlignedOriginRight(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.alignOriginRight(), e, score)

class AlignOriginRightSide(Condition):
	u"""Align e.x on right side of parent."""
	def test(self, e):
		return e.isAlignedOriginRightSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.alignOriginRightSide(), e, score)



