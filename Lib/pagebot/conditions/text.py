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
#     text.py
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


class EqualizeFlow2Height(Condition):
	u"""Test if all elements in the flow the same height and/or same amount text lines."""
	# TODO
