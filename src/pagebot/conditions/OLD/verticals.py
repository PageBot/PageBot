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
#     verticals.py
#
from __future__ import division
from condition import Condition

#	F I T T I N G 

"""
Fitting

Fit
FitSides

FitTop
FitBottom
FitLeft
FitRight

FitTopSide
FitBottomSide
FitLeftSide
FitRightSide


Horizontal

Center2Center
Left2Center
Right2Center
Origin2Center

Center2CenterSides
Left2CenterSides
Right2CenterSides
Origin2CenterSides

Center2Left
Left2Left
Right2Left
Origin2Left

Center2LeftSide
Left2LeftSide
==NOT Right2LeftSide
Origin2LeftSide

Center2Right
Left2Right
Right2Right
Origin2Right

Center2RightSide
==NOT Left2LRightSide
Right2RightSide
Origin2RightSide

Vertical

Center2YCenter
Left2YCenter
Right2YCenter
Origin2YCenter

Center2YCenterSides
Left2YCenterSides
Right2YCenterSides
Origin2YCenterSides

Center2Top
Left2Top
Right2Top
Origin2Top

Center2TopSide
Top2TopSide
==NOT Bottom2TopSide
Origin2TopSide

Center2Bottom
Top2Bottom
Bottom2Bottom
Origin2Bottom

Center2BottomSide
==NOT Top2BottomSide
Bottom2BottomSide
Origin2BottomSide

FloatTopLeft
FloatTopRight
FloatBottomLeft
FloatBottomRight



"""
class Center2YCenterMargins(Condition):
	u"""Center e bounding box between parent vertical margins."""
	def test(self, e):
		return e.isCenteredVertical(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.alignCenterVertical(), e, score)

class CenterVerticalOriginOnMargins(Condition):
	u"""Center e origin between parent vertical margins."""
	def test(self, e):
		return e.isCenteredOrigin(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.alignVCenterOrigin(), e, score)

class CenterVerticalOnSides(Condition):
	u"""Center e bounding box vertical between parent sides."""
	def test(self, e):
		return e.isCenteredVerticalOnSides(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.centerVerticalOnSides(), e, score)

class CenterOriginVerticalSide(Condition):
	u"""Center e bounding box between parent sides."""
	def test(self, e):
		return e.isCenteredOriginVerticalSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.alignCenterOriginVerticalSide(), e, score)

#	T O P

class AlignTop(Condition):
	u"""Align e.top on top margin of parent."""
	def test(self, e):
		return e.isAlignedTop(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.alignTop(), e, score)

class AlignTopSide(Condition):
	u"""Align e.top on top side of parent."""
	def test(self, e):
		return e.isAlignedTopSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.alignTopSide(), e, score)

class AlignOriginTop(Condition):
	u"""Align e.y on top margin of parent."""
	def test(self, e):
		return e.isAlignedOriginTop(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.alignLeftOrigin(), e, score)

class OriginTopSide(Condition):
	u"""Align e.y on top side of parent."""
	def test(self, e):
		return e.isAlignedOriginTopSide(self.tolerance)

	def solve(self, e, score):
		self.transform(not self.test(e) and e.alignOriginTopSide(), e, score)

#   B O T T O M

class Bottom2Bottom(Condition):
	u"""Align e.bottom on bottom margin of parent."""
	def test(self, e):
		return e.isAlignedBottom(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.alignBottom(), e, score)

class Bottom2BottomSide(Condition):
	u"""Align e.bottom on bottom side of parent."""
	def test(self, e):
		return e.isAlignedBottomSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.alignBottomSide(), e, score)

class Origin2Bottom(Condition):
	u"""Align e.y on right margin of parent."""
	def test(self, e):
		return e.isAlignedOriginBottom(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.alignBottomOrigin(), e, score)

class Origin2BottomSide(Condition):
	u"""Align e.x on right side of parent."""
	def test(self, e):
		return e.isAlignedOriginBottomSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.alignOriginBottomSide(), e, score)



