# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     flow.py
#
# 	  These conditions define the state of flow between elements.
#     If the element with this condition as unmatched overflow, then it
#     needs to try to solve it. Otherwise a fail remains after self.solve()
#
from pagebot.conditions.condition import Condition

# Text overflow

class Overflow2Next(Condition):
	"""If there is overflow in the element, then try to solve it.

	>>> from pagebot.elements import newTextBox, Element
	>>> e1 = newTextBox('ABC ' * 4, w=200, h=200 )
	>>> e2 = Element(x=10, y=10, w=200, h=200, name='Root', elements=[e1])
	>>> e1.parent.name
	'Root'
	>>> #e1.isOverflow()
	#True
	"""
	def test(self, e):
		return e.isOverflow(self.tolerance)

	def solve(self, e, score):
		if not self.test(e): # Only try to solve if condition test fails.
			self.addScore(e.overflow2Next(), e, score)

class EqualizeFlow2Height(Condition):
        """Test if all elements in the flow have the same height and/or same
        amount of text lines."""
	# TODO

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

