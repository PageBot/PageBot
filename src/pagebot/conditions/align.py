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
		return [Left2Left, Top2Top, Fit2Right, Fit2Bottom]

	def evaluate(self, e, score):
		u"""Fit the element on all margins of the parent. First align left and top,
		then fit right and bottom. This order to avoid that element temporary
		get smaller than their minimum size, if the start position is wrong."""
		self.evaluateAll(e, self._getConditions(), score)

	def solve(self, e, score):	
		self.solveAll(e, self._getConditions(), score)

class Fit2Sides(Condition):
	u"""Fit the element on all sides of the parent sides."""

	def _getConditions(self):
		return [Left2LeftSide, Top2TopSide, Fit2RightSide, Fit2BottomSide]

	def evaluate(self, e, score):
		self.evaluateAll(e, self._getConditions(), score)

	def solve(self, e, score):	
		self.solveAll(e, self._getConditions(), score)

# There are no "FitOrigin" condition, as these may result is extremely large scalings.

class Fit2Left(Condition):
	def test(self, e):
		return e.isLeftOnLeft(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.fit2Left(), e, score)

class Fit2Right(Condition):
	def test(self, e):
		return e.isRightOnRight(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.fit2Right(), e, score)

class Fit2Width(Condition):
	def test(self, e):
		return e.isLeftOnLeft(self.tolerance) and e.isRightOnRight(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.left2Left() and e.fit2Right(), e, score)
		
class Fit2Height(Condition):
	def test(self, e):
		return e.isTopOnTop(self.tolerance) and e.isBottomOnBottom(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.top2Top() and e.fit2Bottom(), e, score)
		
class Fit2Top(Condition):
	def test(self, e):
		return e.isTopOnTop(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.fit2Top(), e, score)

class Fit2Bottom(Condition):
	def test(self, e):
		return e.isBottomOnBottom(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.fit2Bottom(), e, score)

#	F I T T I N G  S I D E S

# There are no "FitOrigin" condition, as these mau result is extremely large scalings.

class Fit2WidthSide(Condition):
	def test(self, e):
		return e.isLeftOnLeftSide(self.tolerance) and e.isRightOnRightSide(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.left2LeftSide() and e.fit2RightSide(), e, score)
		
class Fit2LeftSide(Condition):
	def test(self, e):
		return e.isLeftOnLeftSide(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.fitLeftSide(), e, score)

class Fit2RightSide(Condition):
	def test(self, e):
		return e.isRightOnRightSide(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.fitRightSide(), e, score)

class Fit2HeightSide(Condition):
	def test(self, e):
		return e.isTopOnTopSide(self.tolerance) and e.isBottomOnBottomSide(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.top2Top() and e.fit2BottomSide(), e, score)
		
class Fit2TopSide(Condition):
	def test(self, e):
		return e.isTopOnTopSide(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.fitTopSide(), e, score)

class Fit2BottomSide(Condition):
	def test(self, e):
		return e.isBottomOnBottomSide(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.fitBottomSide(), e, score)

#	C E N T E R  H O R I Z O N T A L

#	Center Horizontal Margins

class Center2Center(Condition):
	u"""Center e bounding box horizontal between parent margins."""
	def test(self, e):
		return e.isCenterOnCenter(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.center2Center(), e, score)

class Left2Center(Condition):
	u"""Align left of e bounding box horizontal between parent margins."""
	def test(self, e):
		return e.isLeftOnCenter(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.left2Center(), e, score)

class Right2Center(Condition):
	u"""Align right of e bounding box horizontal between parent margins."""
	def test(self, e):
		return e.isRightOnCenter(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.right2Center(), e, score)

class Origin2Center(Condition):
	u"""Align left of e bounding box horizontal between parent margins."""
	def test(self, e):
		return e.isOriginOnCenter(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.origin2Center(), e, score)

#	Center Horizontal Sides

class Center2CenterSides(Condition):
	u"""Center e bounding box horizontal between parent sides."""
	def test(self, e):
		return e.isCenterOnCenterSides(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.center2CenterSides(), e, score)

class Left2CenterSides(Condition):
	u"""Align left of e bounding box horizontal between parent sides."""
	def test(self, e):
		return e.isLeftOnCenterSides(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.left2CenterSides(), e, score)

class Right2CenterSides(Condition):
	u"""Align right of e bounding box horizontal between parent margins."""
	def test(self, e):
		return e.isRightOnCenterSides(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.right2CenterSides(), e, score)

class Origin2CenterSides(Condition):
	u"""Align left of e bounding box horizontal between parent margins."""
	def test(self, e):
		return e.isOriginOnCenterSides(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.origin2CenterSides(), e, score)

#   L E F T / R I G H T

class Center2Left(Condition):
	u"""Move center of e bounding box on parent left margin."""
	def test(self, e):
		return e.isCenterOnLeft(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.center2Left(), e, score)

class Left2Left(Condition):
	u"""Align left of e bounding box on parent left margin."""
	def test(self, e):
		return e.isLeftOnLeft(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.left2Left(), e, score)

class Right2Left(Condition):
	u"""Align right of e bounding box to parent left margin."""
	def test(self, e):
		return e.isRightOnLeft(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.right2Left(), e, score)

class Origin2Left(Condition):
	u"""Align left of e bounding box horizontal between parent margins."""
	def test(self, e):
		return e.isOriginOnLeft(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.origin2Left(), e, score)

class Center2LeftSide(Condition):
	u"""Move center of e bounding box on parent left side."""
	def test(self, e):
		return e.isCenterOnLeftSide(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.center2LeftSide(), e, score)

class Left2LeftSide(Condition):
	u"""Align left of e bounding box on parent left side."""
	def test(self, e):
		return e.isLeftOnLeftSide(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.left2LeftSide(), e, score)

# Missing on purpose: Right2LeftSide(Condition). Element is not visible.

class Origin2LeftSide(Condition):
	u"""Align left of e bounding box horizontal between parent left side."""
	def test(self, e):
		return e.isOriginOnLeftSide(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.origin2LeftSide(), e, score)

class Center2Right(Condition):
	u"""Move center of e bounding box on parent right margin."""
	def test(self, e):
		return e.isCenterOnRight(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.center2Right(), e, score)

class Left2Right(Condition):
	u"""Align left of e bounding box on parent right margin."""
	def test(self, e):
		return e.isLeftOnRight(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.left2Right(), e, score)

class Right2Right(Condition):
	u"""Align right of e bounding box to parent right margin."""
	def test(self, e):
		return e.isRightOnRight(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.right2Right(), e, score)

class Origin2Right(Condition):
	u"""Align origin of e bounding box to parent right margin."""
	def test(self, e):
		return e.isOriginOnRight(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.origin2Right(), e, score)

#	Left Horizontal Sides

class Center2RightSide(Condition):
	u"""Move center of e bounding box on parent right side."""
	def test(self, e):
		return e.isCenterOnRightSide(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.center2RightSide(), e, score)

# Missing on purpose: Left2RightSide(Condition). Element is not visible.

class Right2RightSide(Condition):
	u"""Align left of e bounding box on parent right side."""
	def test(self, e):
		return e.isRightOnRightSide(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.right2RightSide(), e, score)

class Origin2RightSide(Condition):
	u"""Align origin of e bounding box horizontal between parent right side."""
	def test(self, e):
		return e.isOriginOnRightSide(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.origin2RightSide(), e, score)

#	V E R T I C A L S

#	Middle Vertical Margins (vertical center, following CSS naming convention)

class Middle2Middle(Condition):
	u"""Middle (vertical center) e bounding box vertical between parent margins."""
	def test(self, e):
		return e.isMiddleOnMiddle(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.middle2Middle(), e, score)

class Middle2MiddleSides(Condition):
	u"""Middle e bounding box vertical between parent vertical sides."""
	def test(self, e):
		return e.isMiddleOnMiddleSides(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.middle2MiddleSides(), e, score)

class Top2Middle(Condition):
	u"""Align top of e bounding box vertical middle between parent margins."""
	def test(self, e):
		return e.isTopOnMiddle(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.top2Middle(), e, score)

class Top2MiddleSides(Condition):
	u"""Align top of e bounding box on vertical middle between parent sides."""
	def test(self, e):
		return e.isTopOnMiddleSides(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.top2MiddleSides(), e, score)

class Bottom2Middle(Condition):
	u"""Align bottom of e bounding box on vertical middle between parent margins."""
	def test(self, e):
		return e.isBottomOnMiddle(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.bottom2Middle(), e, score)

class Bottom2MiddleSides(Condition):
	u"""Align right of e bounding box on vertical middle between parent sides."""
	def test(self, e):
		return e.isBottomOnMiddleSides(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.bottom2MiddleSides(), e, score)

class Origin2Middle(Condition):
	u"""Align origin of e bounding box to vertical middle between parent margin."""
	def test(self, e):
		return e.isOriginOnMiddle(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.origin2Middle(), e, score)

class Origin2MiddleSides(Condition):
	u"""Align origin of e bounding box to vertical middle between parent sides."""
	def test(self, e):
		return e.isOriginOnMiddleSides(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.origin2MiddleSides(), e, score)

class Origin2Top(Condition):
	u"""Align left of e bounding box horizontal between parent margins."""
	def test(self, e):
		return e.isOriginOnTop(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.origin2Top(), e, score)

class Middle2Top(Condition):
	u"""Move middle (vertical center) of e bounding box on parent top margin."""
	def test(self, e):
		return e.isMiddleOnTop(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.middle2Top(), e, score)

class Middle2TopSide(Condition):
	u"""Move middle (vertical center) of e bounding box on parent top side."""
	def test(self, e):
		return e.isMiddleOnTopSide(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.middle2TopSide(), e, score)

class Top2TopSide(Condition):
	u"""Align left of e bounding box on parent top side."""
	def test(self, e):
		return e.isTopOnTopSide(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.top2TopSide(), e, score)

class Top2Top(Condition):
	u"""Align top of e bounding box on parent top margin."""
	def test(self, e):
		return e.isTopOnTop(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.top2Top(), e, score)

class Bottom2Top(Condition):
	u"""Align bottom of e bounding box on parent top margin."""
	def test(self, e):
		return e.isBottomOnTop(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.bottom2Top(), e, score)

# Missing on purpose: Bottom2TopSide(Condition). Element is not visible.

class Origin2TopSide(Condition):
	u"""Align left of e bounding box horizontal between parent top side."""
	def test(self, e):
		return e.isOriginOnTopSide(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.origin2TopSide(), e, score)

class Middle2Bottom(Condition):
	u"""Move middle (vertical center) of e bounding box on parent bottom margin."""
	def test(self, e):
		return e.isMiddleOnBottom(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.middle2Bottom(), e, score)

class Top2Bottom(Condition):
	u"""Align top of e bounding box on parent bottom margin."""
	def test(self, e):
		return e.isTopOnBottom(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.top2Bottom(), e, score)

class Bottom2Bottom(Condition):
	u"""Align bottom of e bounding box to parent bottom margin."""
	def test(self, e):
		return e.isBottomOnBottom(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.bottom2Bottom(), e, score)

class Origin2Bottom(Condition):
	u"""Align origin of e bounding box to parent bottom margin."""
	def test(self, e):
		return e.isOriginOnBottom(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.origin2Bottom(), e, score)

#	Left Horizontal Sides

class Middle2BottomSide(Condition):
	u"""Move middle (vertical center) of e bounding box on parent bottom side."""
	def test(self, e):
		return e.isMiddleOnBottomSide(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.middle2BottomSide(), e, score)

# Missing on purpose: TopBottomSide(Condition). Element is not visible.

class Bottom2BottomSide(Condition):
	u"""Align bottom of e bounding box on parent bottom side."""
	def test(self, e):
		return e.isBottomOnBottomSide(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.bottom2BottomSide(), e, score)

class Origin2BottomSide(Condition):
	u"""Align origin of e bounding box horizontal between parent bottom side."""
	def test(self, e):
		return e.isOriginOnBottomSide(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.origin2BottomSide(), e, score)


