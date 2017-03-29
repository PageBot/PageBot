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
#     condition.py
#
from __future__ import division
from condition import Condition

class CenterX(Condition):
	def evaluate(self, e):
		u"""Answer the value between 0 and 1 to the level where the element
		is horizontally centered on its parent."""
		parent = e.parent
		if parent is not None:
			if parent.w/2 - (e.w/2 + e.x) <= self.tolerance:
				return self.value
		return self.value * self.errorFactor	

	def solve(self, e):	
		parent = e.parent
		if self.evaluate(e) < 0 and parent is not None:
			e.x = parent.w/2 - e.w/2
			return self.value
		return self.value * self.errorFactor


class LeftAligned(Condition):
	def evaluate(self, e):
		u"""Answer the value between 0 and 1 to the level where the element
		is left aligned with parent."""
		if abs(e.x) <= self.tolerance:
			return self.value
		return self.value * self.errorFactor

	def solve(self, e):
		if self.evaluate(e) < 0:
			e.x = 0
			return self.value
		return self.value * self.errorFactor


class RightAligned(Condition):
	def evaluate(self, e):
		u"""Answer the value between 0 and 1 to the level where the element
		is left aligned with parent."""
		parent = e.parent
		if parent is not None:
			if parent.w - e.w - e.x <= self.tolerance:
				return self.value
		return self.value * self.errorFactor

	def solve(self, e):
		parent = e.parent
		if self.evaluate(e) < 0 and parent is not None:
			e.x = parent.w - e.w
			return self.value
		return self.value * self.errorFactor

class MaxWidthByFontSize(Condition):
	def __init__(self, value=1, tolerance=1, errorFactor=-10, verbose=False, ratio=200):
		Condition.__init__(self, value=1, tolerance=1, errorFactor=-10, verbose=False)
		self.ratio = ratio

	def evaluate(self, e):
		u"""Answer the value between -10 and 1 to the level where the fontSize/width ratio
		fits the self.ratio value."""
		if not e.style.get('fontSize') or abs(e.w/e.style['fontSize'] - self.ratio) <= self.tolerance:
				return self.value
		return self.value * self.errorFactor

	def solve(self, e):
		if e.style.get('fontSize'):
			e.w = e.style['fontSize'] * self.ratio
		return self.value


