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

class Float2SideLeft(Condition):
    """Align the element.left with max of all placed element.right or
    parent.sideLeft. Positioning includes the margin of all elements."""
    def test(self, e):
        return e.isFloatOnSideLeft(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2SideLeft(), e, score)

class Float2SideRight(Condition):
    """Align the element.right with min of all placed element.left or
    parent.sideRight. Positioning includes the margin of all elements."""
    def test(self, e):
        return e.isFloatOnSideRight(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2SideRight(), e, score)

class Float2SideTop(Condition):
    """Align the element.top with max of all placed element.bottom or
    parent.sideTop. Positioning includes the margin of all elements."""
    def test(self, e):
        return e.isFloatOnSideTop(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2SideTop(), e, score)

class Float2SideBottom(Condition):
    """Align the element.bottom with max of all placed element.top or
    parent.sideBottom. Positioning includes the margin of all elements."""
    def test(self, e):
        return e.isFloatOnSideBottom(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2SideBottom(), e, score)

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

class Float2SideLeftTops(Condition):
    def test(self, e):
        return e.isFloatOnSideLeft(self.tolerance) and e.isFloatOnSideTop(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2SideLeft() and e.float2SideTop(), e, score)

class Float2TopSideLefts(Condition):
    def test(self, e):
        return e.isFloatOnSideTop(self.tolerance) and e.isFloatOnSideLeft(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2SideTop() and e.float2SideLeft(), e, score)

class Float2SideRightTops(Condition):
    def test(self, e):
        return e.isFloatOnSideRight(self.tolerance) and e.isFloatOnSideTop(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2SideRight() and e.float2SideTop(), e, score)

class Float2TopSideRights(Condition):
    def test(self, e):
        return e.isFloatOnSideTop(self.tolerance) and e.isFloatOnSideRight(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2SideTop() and e.float2SideRight(), e, score)

class Float2SideLeftBottoms(Condition):
    def test(self, e):
        return e.isFloatOnSideLeft(self.tolerance) and e.isFloatOnSideBottom(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2SideLeft() and e.float2SideBottom(), e, score)

class Float2BottomSideLefts(Condition):
    def test(self, e):
        return e.isFloatOnSideBottom(self.tolerance) and e.isFloatOnSideLeft(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2SideBottom() and e.float2SideLeft(), e, score)

class Float2SideRightBottoms(Condition):
    def test(self, e):
        return e.isFloatOnSideRight(self.tolerance) and e.isFloatOnSideBottom(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2SideRight() and e.float2SideBottom(), e, score)

class Float2BottomSideRights(Condition):
    def test(self, e):
        return e.isFloatOnSideBottom(self.tolerance) and e.isFloatOnSideRight(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.float2SideBottom() and e.float2SideRight(), e, score)
