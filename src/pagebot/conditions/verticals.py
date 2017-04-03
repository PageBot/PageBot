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
from pagebot.style import TOP_ALIGN, BOTTOM_ALIGN, CENTER
from condition import Condition

#	C E N T E R S

class VCenter(Condition):
	u"""Vertically center the bounding box of element e on the middle 
	between top and bottom margins."""
	def evaluate(self, e):
		u"""Answer the value between 0 and self.value, representing the level 
		of where the element is vertical centered on its parent."""
		parent = e.parent
		if parent is not None:
			mt = parent.css('ml')
			mb = parent.css('mb')
			if parent.originTop:
				if abs(mt + (mb - mt)/2 - e.vCenter) <= self.tolerance:
					return self.value
			else:
				if abs(mb + (mt - mb)/2 - c.vCenter) <= self.tolerance:
					return self.value
		return self.error

	def solve(self, e):	
		parent = e.parent
		if self.evaluate(e) < 0 and parent is not None:
			mt = parent.css('ml')
			mb = parent.css('mb')
			if parent.originTop:			
				e.vCenter = mt + (mb - mt)/2
			else:
				e.vCenter = mb + (mt - mb)/2
			return self.value
		return self.error

class VCenterOrigin(Condition):
	u"""Vertically center the bounding box of element e on the middle 
	between top and bottom margins."""
	def evaluate(self, e):
		u"""Answer the value between 0 and self.value, representing the level 
		of where the element is vertical centered on its parent."""
		parent = e.parent
		if parent is not None:
			mt = parent.css('ml')
			mb = parent.css('mb')
			if parent.originTop:
				if abs(mt + (mb - mt)/2 - e.y) <= self.tolerance:
					return self.value
			else:
				if abs(mb + (mt - mb)/2 - c.y) <= self.tolerance:
					return self.value
		return self.error

	def solve(self, e):	
		parent = e.parent
		if self.evaluate(e) < 0 and parent is not None:
			mt = parent.css('ml')
			mb = parent.css('mb')
			if parent.originTop:			
				e.y = mt + (mb - mt)/2
			else:
				e.y = mb + (mt - mb)/2
			return self.value
		return self.error

class VCenterSide(Condition):
	u"""Vertically center the bounding box of element e on the middle 
	between top and bottom margins."""
	def evaluate(self, e):
		u"""Answer the value between 0 and self.value, representing the level 
		of where the element is vertical centered on its parent."""
		parent = e.parent
		if parent is not None:
			if abs(parent.h/2 - e.vCenter) <= self.tolerance:
				return self.value
		return self.error

		@@@@@ return evaluated result or self.error?
		@@@@@ 
	def solve(self, e):	
		parent = e.parent
		if parent is not None andself.evaluate(e) < 0:
			e.vCenter = parent.h/2
		return self.error

class VCenterOriginSide(Condition):
	u"""Vertically center the bounding box of element e on the middle 
	between top and bottom margins."""
	def evaluate(self, e):
		u"""Answer the value between 0 and self.value, representing the level 
		of where the element is vertical centered on its parent."""
		parent = e.parent
		if parent is not None:
			if abs(parent.h/2 - e.y) <= self.tolerance:
				return self.value
		return self.error

	def solve(self, e):	
		parent = e.parent
		if parent is not None and self.evaluate(e) < 0:
			e.y = parent.h/2
		return self.error

#	T O P

class TopAligned(Condition):
	u"""Align with top margin of the parent."""
	def evaluate(self, e):
		u"""Answer the value between 0 and 1 to the level where the element
		is top aligned with the top-margin of the parent."""
		parent = e.parent
		if parent is not None:
			mt = parent.css('ml')
			mb = parent.css('mb')
			if parent.originTop:
				if abs(mt + (mb - mt)/2 - e.top) <= self.tolerance:
					return self.value
			else:
				if abs(mb + (mt - mb)/2 - e.top) <= self.tolerance:
					return self.value
		return self.error

	def solve(self, e):
		if self.evaluate(e) < 0:
			e.top = e.css('mt')
			return self.value
		return self.value * self.errorFactor

class TopOriginAligned(Condition):
	def evaluate(self, e):
		u"""Answer the value between 0 and 1 to the level where the element
		is left aligned with parent."""
		if abs(e.y) <= self.tolerance:
			return self.value
		return self.value * self.errorFactor

	def solve(self, e):
		if self.evaluate(e) < 0:
			e.y = e.css('mt')
			return self.value
		return self.value * self.errorFactor

class TopBleedAligned(Condition):
	def evaluate(self, e):
		u"""Answer the value between 0 and 1 to the level where the element
		is top aligned with parent."""
		if abs(e.top) <= self.tolerance:
			return self.value
		return self.error

	def solve(self, e):
		if self.evaluate(e) < 0:
			e.top = e.css('bleed') # Set bleed = 0, if element needs to fit
			return self.value
		return self.error

class TopOriginBleedAligned(Condition):
	def evaluate(self, e):
		u"""Answer the value between 0 and 1 to the level where the element
		is left aligned with parent."""
		if abs(e.y) <= self.tolerance:
			return self.value
		return self.error

	def solve(self, e):
		if self.evaluate(e) < 0:
			e.y = 0
			return self.value
		return self.error

class BottomAligned(Condition):
	def evaluate(self, e):
		u"""Answer the value between 0 and 1 to the level where the element
		is left aligned with parent."""
		parent = e.parent
		if parent is not None:
			if abs(parent.h - e.bottom) <= self.tolerance:
				return self.value
		return self.error

	def solve(self, e):
		parent = e.parent
		if self.evaluate(e) < 0 and parent is not None:
			e.bottom = parent.h
			return self.value
		return self.error

class BottomOriginAligned(Condition):
	def evaluate(self, e):
		u"""Answer the value between 0 and 1 to the level where the element
		is left aligned with parent."""
		parent = e.parent
		if parent is not None:
			if abs(parent.h - e.y) <= self.tolerance:
				return self.value
		return self.error

	def solve(self, e):
		parent = e.parent
		if self.evaluate(e) < 0 and parent is not None:
			e.y = parent.h
			return self.value
		return self.error
