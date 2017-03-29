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
from condition import Condition

class CenterY(Condition):
	def evaluate(self, e):
		u"""Answer the value between 0 and self.value, representing the level 
		of where the element is vertical centered on its parent."""
		parent = e.parent
		if parent is not None:
			if parent.h/2 - (e.h/2 + e.y) <= self.tolerance:
				return self.value
		return self.value * self.errorFactor	

	def solve(self, e):	
		parent = e.parent
		if self.evaluate(e) < 0 and parent is not None:
			e.y = parent.h/2 - e.h/2
			return self.value
		return self.value * self.errorFactor


class TopAligned(Condition):
	def evaluate(self, e):
		u"""Answer the value between 0 and self.value, representing the level 
		of where the element is vertical top aligned on its parent."""
		parent = e.parent
		if parent is not None:
			if parent.h - e.h - e.y <= self.tolerance:
				return self.value
		return self.value * self.errorFactor

	def solve(self, e):
		parent = e.parent
		if self.evaluate(e) < 0 and parent is not None:
			e.y = parent.h - e.h
			return self.value
		return self.value * self.errorFactor

class BottomAligned(Condition):
	def evaluate(self, e):
		u"""Answer the value between 0 and self.value, representing the level 
		of where the element is vertical bottom aligned on its parent."""
		if abs(e.y) <= self.tolerance:
			return self.value
		return self.value * self.errorFactor

	def solve(self, e):
		if self.evaluate(e) < 0:
			e.y = 0
			return self.value
		return self.value * self.errorFactor

