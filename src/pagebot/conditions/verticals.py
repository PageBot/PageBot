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

class CenterOriginY(Condition):
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
		of where the top of the element bounding box is vertical top aligned on its parent.
		This way of positioning is compensating for the alignment of e"""
		parent = e.parent
		if parent is not None:
			if e.originTop:
				if e.css('vAlign') == CENTER and abs(e.y - e.h/2) <= self.tolerance:
					return value
				if e.css('vAlign') == TOP_ALIGN and abs(e.y) <= self.tolerance:
					return self.value
				if e.css('vAlign') == BOTTOM_ALIGN and abs(e.y - e.h) <= self.tolerance:
					return self.value
			else:
				if e.css('vAlign') == CENTER and abs(parent.h - e.y + e.h/2) <= self.tolerance:
					return value
				if e.css('vAlign') == TOP_ALIGN and abs(parent.h - e.y) <= self.tolerance:
					return self.value
				if e.css('vAlign') == BOTTOM_ALIGN and abs(parent.h - e.y + e.h) <= self.tolerance:
					return self.value
		return self.value * self.errorFactor

	def solve(self, e):
		result = None
		parent = e.parent
		if parent is not None:
			if e.originTop:
				if e.css('vAlign') == CENTER:
					e.y = -e.h/2
					result = self.value
				elif e.css('vAlign') == TOP_ALIGN:
					e.y = 0
					result = self.value
				elif e.css('vAlign') == BOTTOM_ALIGN:
					e.y = -e.h
					result = self.value
			else:
				if e.css('vAlign') == CENTER:
					e.y = parent.h - e.h/2
					result = self.value
				elif e.css('vAlign') == TOP_ALIGN:
					e.y = parent.h
					result = self.value
				if e.css('vAlign') == BOTTOM_ALIGN:
					e.y = parent.h - e.h
					result = self.value
		if result is None:
			return self.value * self.errorFactor
		return self.value

class TopOriginAligned(Condition):
	def evaluate(self, e):
		u"""Answer the value between 0 and self.value, representing the level 
		of where the top of the element bounding box is vertical top aligned on its parent.
		This way of positioning is ignoring the alignment of e."""
		parent = e.parent
		if parent is not None:
			if e.originTop and abs(e.y) <= self.tolerance:
				return self.value
			elif not e.originTop and abs(parent.h - e.y) <= self.tolerance:
				return self.value
		return self.value * self.errorFactor

	def solve(self, e):
		result = None
		parent = e.parent
		if parent is not None:
			if e.originTop:
				e.y = 0
				result = self.value
			else:
				e.y = parent.h
				result = self.value
		if result is None:
			return self.value * self.errorFactor
		return self.value

class BottomAligned(Condition):
	def evaluate(self, e):
		u"""Answer the value between 0 and self.value, representing the level 
		of where the top of the element bounding box is vertical top aligned on its parent.
		This way of positioning is compensating for the alignment of e"""
		parent = e.parent
		if parent is not None:
			if e.originTop:
				if e.css('vAlign') == CENTER and abs(-parent.h + e.h/2 - e.y) <= self.tolerance:
					return value
				if e.css('vAlign') == TOP_ALIGN and abs(-parent.h + e.y) <= self.tolerance:
					return self.value
				if e.css('vAlign') == BOTTOM_ALIGN and abs(e.y - e.h) <= self.tolerance:
					return self.value
			else:
				if e.css('vAlign') == CENTER and abs(parent.h - e.y + e.h/2) <= self.tolerance:
					return value
				if e.css('vAlign') == TOP_ALIGN and abs(parent.h - e.y) <= self.tolerance:
					return self.value
				if e.css('vAlign') == BOTTOM_ALIGN and abs(parent.h - e.y + e.h) <= self.tolerance:
					return self.value
		return result * self.errorFactor

	def solve(self, e):
		result = None
		parent = e.parent
		if parent is not None:
			if e.originTop:
				if e.css('vAlign') == CENTER:
					e.y = -e.h/2
					result = self.value
				elif e.css('vAlign') == TOP_ALIGN:
					e.y = 0
					result = self.value
				elif e.css('vAlign') == BOTTOM_ALIGN:
					e.y = -e.h
					result = self.value
			else:
				if e.css('vAlign') == CENTER:
					e.y = parent.h - e.h/2
					result = self.value
				elif e.css('vAlign') == TOP_ALIGN:
					e.y = parent.h
					result = self.value
				if e.css('vAlign') == BOTTOM_ALIGN:
					e.y = parent.h - e.h
					result = self.value
		if result is None:
			return self.value * self.errorFactor
		return self.value

class BottomOriginAligned(Condition):
	def evaluate(self, e):
		u"""Answer the value between 0 and self.value, representing the level 
		of where the origin of the element e is vertical bottom aligned on its parent.
		This way of positioning is ignoring the alignment of e."""
		parent = e.parent
		if parent is not None:
			if e.originTop and abs(parent.h - e.y) <= self.tolerance:
				return self.value
			elif not e.originTop and abs(e.y) <= self.tolerance:
				return self.value
		return self.value * self.errorFactor

	def solve(self, e):
		result = None
		parent = e.parent
		if parent is not None:
			if e.originTop:
				e.y = parent.h
				result = self.value
			else:
				e.y = 0
				result = self.value
		if result is None:
			return self.value * self.errorFactor
		return self.value

