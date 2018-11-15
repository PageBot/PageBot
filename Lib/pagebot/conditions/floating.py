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
#     floating.py
#
from pagebot.conditions.condition import Condition

# Margins

class Float2Left(Condition):
    """Align the element.left with max of all placed element.right or
    parent.left. Positioning includes the margin of all elements."""
    def test(self, e):
        return e.isFloatOnLeft(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2Left(), e, score)

class Float2Right(Condition):
    """Align the element.right with min of all placed element.left or
    parent.right. Positioning includes the margin of all elements."""
    def test(self, e):
        return e.isFloatOnRight(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2Right(), e, score)

class Float2Top(Condition):
    """Align the `element.top` with max of all placed `element.bottom` or
    `parent.top`. Positioning includes the margin of all elements."""
    def test(self, e):
        return e.isFloatOnTop(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2Top(), e, score)

class Float2Bottom(Condition):
    """Align the element.bottom with max of all placed element.top or
    parent.bottom. Positioning includes the margin of all elements."""
    def test(self, e):
        return e.isFloatOnBottom(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2Bottom(), e, score)

# Sides

class Float2LeftSide(Condition):
    """Align the element.left with max of all placed element.right or
    parent.leftSide. Positioning includes the margin of all elements."""
    def test(self, e):
        return e.isFloatOnLeftSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2LeftSide(), e, score)

class Float2RightSide(Condition):
    """Align the element.right with min of all placed element.left or
    parent.rightSide. Positioning includes the margin of all elements."""
    def test(self, e):
        return e.isFloatOnRightSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2RightSide(), e, score)

class Float2TopSide(Condition):
    """Align the element.top with max of all placed element.bottom or
    parent.topSide. Positioning includes the margin of all elements."""
    def test(self, e):
        return e.isFloatOnTopSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2TopSide(), e, score)

class Float2BottomSide(Condition):
    """Align the element.bottom with max of all placed element.top or
    parent.bottomSide. Positioning includes the margin of all elements."""
    def test(self, e):
        return e.isFloatOnBottomSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2BottomSide(), e, score)

# Combinations

class Float2LeftTop(Condition):
    def test(self, e):
        return e.isFloatOnLeft(self.tolerance) and e.isFloatOnTop(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2Left() and e.float2Top(), e, score)

class Float2TopLeft(Condition):
    def test(self, e):
        return e.isFloatOnTop(self.tolerance) and e.isFloatOnLeft(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2Top() and e.float2Left(), e, score)

class Float2RightTop(Condition):
    def test(self, e):
        return e.isFloatOnRight(self.tolerance) and e.isFloatOnTop(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2Right() and e.float2Top(), e, score)

class Float2TopRight(Condition):
    def test(self, e):
        return e.isFloatOnTop(self.tolerance) and e.isFloatOnRight(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2Top() and e.float2Right(), e, score)

class Float2LeftBottom(Condition):
    def test(self, e):
        return e.isFloatOnLeft(self.tolerance) and e.isFloatOnBottom(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2Left() and e.float2Bottom(), e, score)

class Float2BottomLeft(Condition):
    def test(self, e):
        return e.isFloatOnBottom(self.tolerance) and e.isFloatOnLeft(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2Bottom() and e.float2Left(), e, score)

class Float2RightBottom(Condition):
    def test(self, e):
        return e.isFloatOnRight(self.tolerance) and e.isFloatOnBottom(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2Right() and e.float2Bottom(), e, score)

class Float2BottomRight(Condition):
    def test(self, e):
        return e.isFloatOnBottom(self.tolerance) and e.isFloatOnRight(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2Bottom() and e.float2Right(), e, score)

# Combination sides

class Float2LeftTopSides(Condition):
    def test(self, e):
        return e.isFloatOnLeftSide(self.tolerance) and e.isFloatOnTopSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2LeftSide() and e.float2TopSide(), e, score)

class Float2TopLeftSides(Condition):
    def test(self, e):
        return e.isFloatOnTopSide(self.tolerance) and e.isFloatOnLeftSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2TopSide() and e.float2LeftSide(), e, score)

class Float2RightTopSides(Condition):
    def test(self, e):
        return e.isFloatOnRightSide(self.tolerance) and e.isFloatOnTopSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2RightSide() and e.float2TopSide(), e, score)

class Float2TopRightSides(Condition):
    def test(self, e):
        return e.isFloatOnTopSide(self.tolerance) and e.isFloatOnRightSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2TopSide() and e.float2RightSide(), e, score)

class Float2LeftBottomSides(Condition):
    def test(self, e):
        return e.isFloatOnLeftSide(self.tolerance) and e.isFloatOnBottomSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2LeftSide() and e.float2BottomSide(), e, score)

class Float2BottomLeftSides(Condition):
    def test(self, e):
        return e.isFloatOnBottomSide(self.tolerance) and e.isFloatOnLeftSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2BottomSide() and e.float2LeftSide(), e, score)

class Float2RightBottomSides(Condition):
    def test(self, e):
        return e.isFloatOnRightSide(self.tolerance) and e.isFloatOnBottomSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2RightSide() and e.float2BottomSide(), e, score)

class Float2BottomRightSides(Condition):
    def test(self, e):
        return e.isFloatOnBottomSide(self.tolerance) and e.isFloatOnRightSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2BottomSide() and e.float2RightSide(), e, score)
