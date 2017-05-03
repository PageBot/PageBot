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
from pagebot.style import TOP, BOTTOM, CENTER
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
				if abs(mt + (mb - mt)/2 - e.yCenter) <= self.tolerance:
					return self.value
			else:
				if abs(mb + (mt - mb)/2 - c.yCenter) <= self.tolerance:
					return self.value
		return self.error

	def solve(self, e):	
		parent = e.parent
		if self.evaluate(e) < 0 and parent is not None:
			mt = parent.css('ml')
			mb = parent.css('mb')
			if parent.originTop:			
				e.yCenter = mt + (mb - mt)/2
			else:
				e.yCenter = mb + (mt - mb)/2
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
			if abs(parent.h/2 - e.yCenter) <= self.tolerance:
				return self.value
		return self.error

	def solve(self, e):	
		parent = e.parent
		if parent is not None and self.evaluate(e) < 0:
			e.yCenter = parent.h/2
			return 
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

class AlignTop(Condition):
	u"""Align with top margin of the parent."""
	def evaluate(self, e):
		u"""Answer the value between 0 and 1 to the level where the element
		is top aligned with the top-margin of the parent."""
		parent = e.parent
		if parent is not None:
			mt = parent.css('mt')
			if parent.originTop:
				if abs(mt - e.top) <= self.tolerance:
					return self.value
			else:
				if abs(parent.h - mt - e.top) <= self.tolerance:
					return self.value
		return self.error

	def solve(self, e):
		parent = e.parent
		if parent is not None and self.evaluate(e) < 0:
			mt = e.css('mt')
			if parent.originTop:
				e.top = mt
			else:
				e.top = parent.h - mt
			return self.value
		return self.error

class AlignOriginTop(Condition):
	def evaluate(self, e):
		u"""Answer the value between 0 and 1 to the level where the element
		is origin aligned with the top-margin of the parent."""
		parent = e.parent
		if parent is not None:
			mt = parent.css('mt')
			if parent.originTop:
				if abs(mt - e.y) <= self.tolerance:
					return self.value
			else:
				if abs(parent.h - mt - e.y) <= self.tolerance:
					return self.value
		return self.error

	def solve(self, e):
		parent = e.parent
		if parent is not None and self.evaluate(e) < 0:
			mt = e.css('mt')
			if parent.originTop:
				e.y = mt
			else:
				e.y = parent.h - mt
			return self.value
		return self.error

class AlignTopSide(Condition):
	u"""Align with top margin of the parent."""
	def evaluate(self, e):
		u"""Answer the value between 0 and 1 to the level where the element
		is top aligned with the top-margin of the parent."""
		parent = e.parent
		if parent is not None:
			if parent.originTop:
				if abs(e.top) <= self.tolerance:
					return self.value
			else:
				if abs(parent.h - e.top) <= self.tolerance:
					return self.value
		return self.error

	def solve(self, e):
		parent = e.parent
		if parent is not None and self.evaluate(e) < 0:
			if parent.originTop:
				e.top = 0
			else:
				e.top = parent.h
			return self.value
		return self.error

class AlignOriginTopSide(Condition):
	u"""Align with top margin of the parent."""
	def evaluate(self, e):
		u"""Answer the value between 0 and 1 to the level where the element
		is top aligned with the top-margin of the parent."""
		parent = e.parent
		if parent is not None:
			if parent.originTop:
				if abs(e.y) <= self.tolerance:
					return self.value
			else:
				if abs(parent.h - e.y) <= self.tolerance:
					return self.value
		return self.error

	def solve(self, e):
		parent = e.parent
		if parent is not None and self.evaluate(e) < 0:
			if parent.originTop:
				e.y = 0
			else:
				e.y = parent.h
			return self.value
		return self.error

#	B O T T O M

class AlignBottom(Condition):
	u"""Align with bottom margin of the parent."""
	def evaluate(self, e):
		u"""Answer the value if the element is bottom aligned with the bottom-margin of the parent."""
		parent = e.parent
		if parent is not None:
			mt = parent.css('mt')
			if parent.originTop:
				if abs(mt - e.top) <= self.tolerance:
					return self.value
			else:
				if abs(parent.h - mt - e.top) <= self.tolerance:
					return self.value
		return self.error

	def solve(self, e):
		parent = e.parent
		if parent is not None and self.evaluate(e) < 0:
			mt = e.css('mt')
			if parent.originTop:
				e.top = mt
			else:
				e.top = parent.h - mt
			return self.value
		return self.error

class AlignOriginBottom(Condition):
	def evaluate(self, e):
		u"""Answer the value between 0 and 1 to the level where the element
		is origin aligned with the top-margin of the parent."""
		parent = e.parent
		if parent is not None:
			mt = parent.css('mt')
			if parent.originTop:
				if abs(mt - e.y) <= self.tolerance:
					return self.value
			else:
				if abs(parent.h - mt - e.y) <= self.tolerance:
					return self.value
		return self.error

	def solve(self, e):
		parent = e.parent
		if parent is not None and self.evaluate(e) < 0:
			mt = e.css('mt')
			if parent.originTop:
				e.y = mt
			else:
				e.y = parent.h - mt
			return self.value
		return self.error

class AlignBottomSide(Condition):
	u"""Align with top margin of the parent."""
	def evaluate(self, e):
		u"""Answer the value between 0 and 1 to the level where the element
		is top aligned with the top-margin of the parent."""
		parent = e.parent
		if parent is not None:
			if parent.originTop:
				if abs(e.top) <= self.tolerance:
					return self.value
			else:
				if abs(parent.h - e.top) <= self.tolerance:
					return self.value
		return self.error

	def solve(self, e):
		parent = e.parent
		if parent is not None and self.evaluate(e) < 0:
			if parent.originTop:
				e.top = 0
			else:
				e.top = parent.h
			return self.value
		return self.error

class AlignOriginBottomSide(Condition):
	u"""Align with top margin of the parent."""
	def evaluate(self, e):
		u"""Answer the value between 0 and 1 to the level where the element
		is top aligned with the top-margin of the parent."""
		parent = e.parent
		if parent is not None:
			if parent.originTop:
				if abs(e.y) <= self.tolerance:
					return self.value
			else:
				if abs(parent.h - e.y) <= self.tolerance:
					return self.value
		return self.error

	def solve(self, e):
		parent = e.parent
		if parent is not None and self.evaluate(e) < 0:
			if parent.originTop:
				e.y = 0
			else:
				e.y = parent.h
			return self.value
		return self.error

