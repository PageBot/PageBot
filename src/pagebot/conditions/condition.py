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
class Condition(object):
    def __init__(self, value=1, tolerance=1, errorFactor=-10, verbose=False):
    	self.value = value # Value to answer if the condition is valid
        self.tolerance = tolerance
        self.errorFactor = errorFactor
        self.verbose = verbose

    def __repr__(self):
    	return '<Condition %s>' % self.transformations

class CenterX(Condition):
	def evaluate(self, e):
		u"""Answer the value between 0 and 1 to the level where the elenent
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
			if self.verbose:
				print 'Centered', e
			return self.value
		return self.value * self.errorFactor


class LeftAligned(Condition):
	def evaluate(self, e):
		u"""Answer the value between 0 and 1 to the level where the elenent
		is left aligned with parent."""
		if abs(e.x) <= self.tolerance:
			return self.value
		return self.value * self.errorFactor

	def solve(self, e):
		if self.evaluate(e) < 0:
			e.x = 0
			if self.verbose:
				print 'Left aligned', e
			return self.value
		return self.value * self.errorFactor


class RightAligned(Condition):
	def evaluate(self, e):
		u"""Answer the value between 0 and 1 to the level where the elenent
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
			if self.verbose:
				print 'Right aligned', e
			return self.value
		return self.value * self.errorFactor

