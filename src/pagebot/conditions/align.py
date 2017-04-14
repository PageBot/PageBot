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
#     align.py
#
from __future__ import division
from condition import Condition

#	F I T T I N G 

class Fit(Condition):
	u"""Fit the element on all sides of the parent margins."""

	def _getConditions(self):
		return [Left2Left, Top2Top, FitRight, FitBottom]

	def evaluate(self, e, score):
		u"""Fit the element on all margins of the parent. First align left and top,
		then fit right and bottom. This order to avoid that element temporary
		get smaller than their minimum size, if the start position is wrong."""
		self.evaluateAll(e, self._getConditions(), score)

	def solve(self, e, score):	
		self.solveAll(e, self._getConditions(), score)

class FitSides(Condition):
	u"""Fit the element on all sides of the parent sides."""

	def _getConditions(self):
		return [Left2LeftSide, Top2TopSide, FitRightSide, FitBottomSide]

	def evaluate(self, e, score):
		self.evaluateAll(e, self._getConditions(), score)

	def solve(self, e, score):	
		self.solveAll(e, self._getConditions(), score)

# There are no "FitOrigin" condition, as these may result is extremely large scalings.

class FitLeft(Condition):
	def test(self, e):
		return e.isLeftOnLeft(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.fitLeft(), e, score)

class FitRight(Condition):
	def test(self, e):
		return e.isRightOnRight(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.fitRight(), e, score)

class FitWidth(Condition):
	def test(self, e):
		return e.isLeftOnLeft(self.tolerance) and e.isRightOnRight(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.left2Left() and e.fitRight(), e, score)
		
class FitHeight(Condition):
	def test(self, e):
		return e.isTopOnTop(self.tolerance) and e.isBottomOnBottom(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.top2Top() and e.fitBottom(), e, score)
		
class FitTop(Condition):
	def test(self, e):
		return e.isTopOnTop(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.fitTop(), e, score)

class FitBottom(Condition):
	def test(self, e):
		return e.isBottomOnBottom(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.fitBottom(), e, score)

#	F I T T I N G  S I D E S

# There are no "FitOrigin" condition, as these mau result is extremely large scalings.

class FitLeftSide(Condition):
	def test(self, e):
		return e.isLeftOnLeftSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.fitLeftSide(), e, score)

class FitRightSide(Condition):
	def test(self, e):
		return e.isRightOnRightSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.fitRightSide(), e, score)

class FitTopSide(Condition):
	def test(self, e):
		return e.isTopOnTopSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.fitTopSide(), e, score)

class FitBottomSide(Condition):
	def test(self, e):
		return e.isBottomOnBottomSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.fitBottomSide(), e, score)

#	C E N T E R  H O R I Z O N T A L

#	Center Horizontal Margins

class Center2Center(Condition):
	u"""Center e bounding box horizontal between parent margins."""
	def test(self, e):
		return e.isCenterOnCenter(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.center2Center(), e, score)

class Left2Center(Condition):
	u"""Align left of e bounding box horizontal between parent margins."""
	def test(self, e):
		return e.isLeftOnCenter(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.left2Center(), e, score)

class Right2Center(Condition):
	u"""Align right of e bounding box horizontal between parent margins."""
	def test(self, e):
		return e.isRightOnCenter(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.right2Center(), e, score)

class Origin2Center(Condition):
	u"""Align left of e bounding box horizontal between parent margins."""
	def test(self, e):
		return e.isOriginOnCenter(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.origin2Center(), e, score)

#	Center Horizontal Sides

class Center2CenterSides(Condition):
	u"""Center e bounding box horizontal between parent sides."""
	def test(self, e):
		return e.isCenterOnCenterSides(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.center2CenterSides(), e, score)

class Left2CenterSides(Condition):
	u"""Align left of e bounding box horizontal between parent sides."""
	def test(self, e):
		return e.isLeftOnCenterSides(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.left2CenterSides(), e, score)

class Right2CenterSides(Condition):
	u"""Align right of e bounding box horizontal between parent margins."""
	def test(self, e):
		return e.isRightOnCenterSides(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.right2CenterSides(), e, score)

class Origin2CenterSides(Condition):
	u"""Align left of e bounding box horizontal between parent margins."""
	def test(self, e):
		return e.isOriginOnCenterSides(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.origin2CenterSides(), e, score)

#   L E F T / R I G H T

class Center2Left(Condition):
	u"""Move center of e bounding box on parent left margin."""
	def test(self, e):
		return e.isCenterOnLeft(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.center2Left(), e, score)

class Left2Left(Condition):
	u"""Align left of e bounding box on parent left margin."""
	def test(self, e):
		return e.isLeftOnLeft(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.left2Left(), e, score)

class Right2Left(Condition):
	u"""Align right of e bounding box to parent left margin."""
	def test(self, e):
		return e.isRightOnLeft(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.right2Left(), e, score)

class Origin2Left(Condition):
	u"""Align left of e bounding box horizontal between parent margins."""
	def test(self, e):
		return e.isOriginOnLeft(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.origin2Left(), e, score)

class Center2LeftSide(Condition):
	u"""Move center of e bounding box on parent left side."""
	def test(self, e):
		return e.isCenterOnLeftSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.center2LeftSide(), e, score)

class Left2LeftSide(Condition):
	u"""Align left of e bounding box on parent left side."""
	def test(self, e):
		return e.isLeftOnLeftSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.left2LeftSide(), e, score)

# Missing on purpose: Right2LeftSide(Condition). Element is not visible.

class Origin2LeftSide(Condition):
	u"""Align left of e bounding box horizontal between parent left side."""
	def test(self, e):
		return e.isOriginOnLeftSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.origin2LeftSide(), e, score)

class Center2Right(Condition):
	u"""Move center of e bounding box on parent right margin."""
	def test(self, e):
		return e.isCenterOnRight(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.center2Right(), e, score)

class Left2Right(Condition):
	u"""Align left of e bounding box on parent right margin."""
	def test(self, e):
		return e.isLeftOnRight(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.left2Right(), e, score)

class Right2Right(Condition):
	u"""Align right of e bounding box to parent right margin."""
	def test(self, e):
		return e.isRightOnRight(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.right2Right(), e, score)

class Origin2Right(Condition):
	u"""Align origin of e bounding box to parent right margin."""
	def test(self, e):
		return e.isOriginOnRight(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.origin2Right(), e, score)

#	Left Horizontal Sides

class Center2RightSide(Condition):
	u"""Move center of e bounding box on parent right side."""
	def test(self, e):
		return e.isCenterOnRightSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.center2RightSide(), e, score)

# Missing on purpose: Left2RightSide(Condition). Element is not visible.

class Right2RightSide(Condition):
	u"""Align left of e bounding box on parent right side."""
	def test(self, e):
		return e.isRightOnRightSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.right2RightSide(), e, score)

class Origin2RightSide(Condition):
	u"""Align origin of e bounding box horizontal between parent right side."""
	def test(self, e):
		return e.isOriginOnRightSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.origin2RightSide(), e, score)

#	V E R T I C A L S

#	Center Vertical Margins

class Center2VerticalCenter(Condition):
	u"""Center e bounding box vertical between parent margins."""
	def test(self, e):
		return e.isCenterOnVerticalCenter(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.center2VerticalCenter(), e, score)

class Center2VerticalCenterSides(Condition):
	u"""Center e bounding box vertical between parent vertical sides."""
	def test(self, e):
		return e.isCenterOnVerticalCenterSides(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.center2VerticalCenterSides(), e, score)

class Top2VerticalCenter(Condition):
	u"""Align left of e bounding box vertical between parent margins."""
	def test(self, e):
		return e.isTopOnVerticalCenter(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.top2VerticalCenter(), e, score)

class Top2VerticalCenterSides(Condition):
	u"""Align left of e bounding box vertical between parent sides."""
	def test(self, e):
		return e.isTopOnVerticalCenterSides(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.top2VerticalCenterSides(), e, score)

class Bottom2VerticalCenter(Condition):
	u"""Align right of e bounding box vertical between parent margins."""
	def test(self, e):
		return e.isBottomOnVerticalCenter(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.bottom2VerticalCenter(), e, score)

class Bottom2VerticalCenterSides(Condition):
	u"""Align right of e bounding box vertical between parent vertical sides."""
	def test(self, e):
		return e.isBottomOnVerticalCenterSides(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.bottom2VerticalCenterSides(), e, score)

class Origin2VerticalCenter(Condition):
	u"""Align bottom of e bounding box to parent top margin."""
	def test(self, e):
		return e.isOriginOnVerticalCenter(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.origin2VerticalCenter(), e, score)

class Origin2VerticalCenterSides(Condition):
	u"""Align bottom of e bounding box to parent vertical sides."""
	def test(self, e):
		return e.isOriginOnVerticalCenterSides(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.origin2VerticalCenterSides(), e, score)

class Origin2Top(Condition):
	u"""Align left of e bounding box horizontal between parent margins."""
	def test(self, e):
		return e.isOriginOnTop(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.origin2Top(), e, score)

class Center2Top(Condition):
	u"""Move center of e bounding box on parent top margin."""
	def test(self, e):
		return e.isCenterOnTop(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.center2Top(), e, score)

class Center2TopSide(Condition):
	u"""Move center of e bounding box on parent left side."""
	def test(self, e):
		return e.isCenterOnTopSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.center2TopSide(), e, score)

class Top2TopSide(Condition):
	u"""Align left of e bounding box on parent top side."""
	def test(self, e):
		return e.isTopOnTopSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.top2TopSide(), e, score)

class Top2Top(Condition):
	u"""Align top of e bounding box on parent top margin."""
	def test(self, e):
		return e.isTopOnTop(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.top2Top(), e, score)

# Missing on purpose: Bottom2TopSide(Condition). Element is not visible.

class Origin2TopSide(Condition):
	u"""Align left of e bounding box horizontal between parent top side."""
	def test(self, e):
		return e.isOriginOnTopSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.origin2TopSide(), e, score)

class Center2Bottom(Condition):
	u"""Move center of e bounding box on parent bottom margin."""
	def test(self, e):
		return e.isCenterOnBottom(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.center2Bottom(), e, score)

class Top2Bottom(Condition):
	u"""Align top of e bounding box on parent bottom margin."""
	def test(self, e):
		return e.isTopOnBottom(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.top2Bottom(), e, score)

class Bottom2Bottom(Condition):
	u"""Align bottom of e bounding box to parent bottom margin."""
	def test(self, e):
		return e.isBottomOnBottom(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.bottom2Bottom(), e, score)

class Origin2Bottom(Condition):
	u"""Align origin of e bounding box to parent bottom margin."""
	def test(self, e):
		return e.isOriginOnBottom(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.origin2Bottom(), e, score)

#	Left Horizontal Sides

class Center2BottomSide(Condition):
	u"""Move center of e bounding box on parent bottom side."""
	def test(self, e):
		return e.isCenterOnBottomSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.center2BottomSide(), e, score)

# Missing on purpose: TopBottomSide(Condition). Element is not visible.

class Bottom2BottomSide(Condition):
	u"""Align bottom of e bounding box on parent bottom side."""
	def test(self, e):
		return e.isBottomOnBottomSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.bottom2BottomSide(), e, score)

class Origin2BottomSide(Condition):
	u"""Align origin of e bounding box horizontal between parent bottom side."""
	def test(self, e):
		return e.isOriginOnBottomSide(self.tolerance)

	def solve(self, e, score):
		self.addScore(not self.test(e) and e.origin2BottomSide(), e, score)


