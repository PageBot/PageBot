# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#     
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     flow.py
#
# 	  These conditions define the state of flow between elements.
#     If the element with this condition as unmatched overflow, then it
#     needs to try to solve it. Otherwise a fail remains after self.solve()
#
from __future__ import division
from pagebot.conditions.condition import Condition

# Margins

class Overflow2Next(Condition):
	u"""If there is overflow in the element, then try to solve it."""
	def test(self, e):
		return e.isOverflow(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.overflow2Next(), e, score)

class EqualizeFlow22Height(Condition):
	u"""Test if all elements in the flow have the same height and/or same amount of text lines."""
	# TODO

class Baseline2Top(Condition):
	u"""Place the first baseline on the parent top padding position. Use the regular Top2Top() to place
	the top of the text on the parent top padding position."""
	def test(self, e):
		return e.isBaselineOnTop(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.baseline2Top(), e, score)

class Baseline2Bottom(Condition):
	def test(self, e):
		return e.isBaselineOnBottom(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.baseline2Bottom(), e, score)

#	Floating

class FloatBaseline2Top(Condition):
	u"""Try to do Baseline2Top() or position just under – truncated locked on parent baseline – if there 
	are already elements in the same z-layer."""
	def test(self, e):
		return e.isBaselineOnTop(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.floatBaseline2Top(), e, score)

class FloatAscender2Top(Condition):
	u"""Try to place the ascender of the first line on the parent top padding position. Or just under
	– truncated locked on parent baseline – if there are already elements in the same z-layer."""
	def test(self, e):
		return e.isAscenderOnTop(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.floatAscender2Top(), e, score)

class FloatCapHeight2Top(Condition):
	u"""Try to place the CapHeight of the first line on the parent top padding position. Or just under
	– truncated locked on parent baseline – if there are already elements in the same z-layer."""
	def test(self, e):
		return e.isCapHeightOnTop(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.floatCapHeight2Top(), e, score)

class FloatXHeight2Top(Condition):
	u"""Try to place the xHeight of the first line on the parent top padding position. Or just under
	– truncated locked on parent baseline – if there are already elements in the same z-layer."""
	def test(self, e):
		return e.isXHeightOnTop(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails. 
			self.addScore(e.floatXHeight2Top(), e, score)

