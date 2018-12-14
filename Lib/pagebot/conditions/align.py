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
#     align.py
#
from pagebot.conditions.condition import Condition

class SolveBlock(Condition):
    """Used as a condition in the sequence of conditions, to fix the block of
    child elements first."""

    def evaluate(self, e, score):
        for child in e.elements:
            child.evaluate(score)

    def solve(self, e, score):
        for child in e.elements:
            child.solve(score)

#    F I T T I N G  P A G E  P A D D I N G

#   By fitting conditions, elements grow to match the size of parents.

class Fit(Condition):
    """Fit the element on all sides of the parent paddings.

    >>> from pagebot.elements import Element
    >>> conditions = [Fit()]
    >>> e1 = Element(x=20, y=20, w=50, h=50, conditions=conditions)
    >>> e2 = Element(w=300, h=300, elements=[e1], padding=12)
    >>> e1.x, e1.y, e1.w, e1.h # Default position and size
    (20pt, 20pt, 50pt, 50pt)
    >>> e1.solve() # Solve position and size from conditions on 4 sides
    Score: 4 Fails: 0
    >>> e1.x, e1.y, e1.w, e1.h # Position and size, solved by position, fitting parent
    (12pt, 12pt, 276pt, 276pt)
    """

    def _getConditions(self):
        return [Left2Left, Top2Top, Fit2Right, Fit2Bottom]

    def evaluate(self, e, score):
        """Fit the element on all paddings of the parent. First align left and top,
        then fit right and bottom. This order to make sure size fitting is based on
        the right position on the parent."""
        self.evaluateAll(e, self._getConditions(), score)

    def solve(self, e, score):
        self.solveAll(e, self._getConditions(), score)

class Fit2Sides(Condition):
    """Fit the element on all sides of the parent sides.

    >>> from pagebot.elements import Element
    >>> conditions = [Fit2Sides()]
    >>> e1 = Element(x=20, y=20, w=50, h=50, conditions=conditions)
    >>> e2 = Element(w=300, h=300, elements=[e1])
    >>> e1.x, e1.y, e1.w, e1.h # Default position and size
    (20pt, 20pt, 50pt, 50pt)
    >>> e1.solve() # Solve position and size from conditions on 4 sides
    Score: 4 Fails: 0
    >>> e1.x, e1.y, e1.w, e1.h # Position and size, solved by position, fitting parent
    (0pt, 0pt, 300pt, 300pt)
    """
    def _getConditions(self):
        return [Left2LeftSide, Top2TopSide, Fit2RightSide, Fit2BottomSide]

    def evaluate(self, e, score):
        self.evaluateAll(e, self._getConditions(), score)

    def solve(self, e, score):
        self.solveAll(e, self._getConditions(), score)

class Fit2Bleed(Condition):
    def _getConditions(self):
        return [Left2LeftBleed, Top2TopBleed, Fit2RightBleed, Fit2BottomBleed]

    def evaluate(self, e, score):
        """Fit the element on all bleeds of the parent. First align left and top,
        then fit right and bottom. This order to make sure size fitting is based on
        the right position on the parent."""
        self.evaluateAll(e, self._getConditions(), score)

    def solve(self, e, score):
        self.solveAll(e, self._getConditions(), score)

# There are no "FitOrigin" condition, as these may result is extremely large scalings.

class Fit2Left(Condition):
    """Grow the element to the left side, until it fits the parent element padding.

    >>> from pagebot.elements import Element
    >>> conditions = [Fit2Left()]
    >>> e1 = Element(x=20, y=20, w=50, h=50, conditions=conditions)
    >>> e2 = Element(w=300, h=300, elements=[e1], padding=12)
    >>> e1.x, e1.y, e1.w, e1.h # Default position and size
    (20pt, 20pt, 50pt, 50pt)
    >>> e1.solve() # Solve position and size from conditions.
    Score: 1 Fails: 0
    >>> e1.x, e1.y, e1.w, e1.h # Position and size, solved by position, fitting parent on padding
    (12pt, 20pt, 58pt, 50pt)
    """
    def test(self, e):
        return e.isLeftOnLeft(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.fit2Left(), e, score)

class Fit2Right(Condition):
    """Grow the element to the right side, until it fits the parent element padding.

    >>> from pagebot.elements import Element
    >>> conditions = [Fit2Right()]
    >>> e1 = Element(x=20, y=20, w=50, h=50, conditions=conditions)
    >>> e2 = Element(w=300, h=300, elements=[e1], padding=12)
    >>> e1.x, e1.y, e1.w, e1.h # Default position and size
    (20pt, 20pt, 50pt, 50pt)
    >>> e1.solve() # Solve position and size from conditions.
    Score: 1 Fails: 0
    >>> e1.x, e1.y, e1.w, e1.h # Position and size, solved by position, fitting parent on padding
    (20pt, 20pt, 268pt, 50pt)
    """
    def test(self, e):
        return e.isRightOnRight(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.fit2Right(), e, score)

class Fit2Width(Condition):
    """Grow the element to left and right side, until it fits the parent element.

    >>> from pagebot.elements import Element
    >>> conditions = [Fit2Width()]
    >>> e1 = Element(x=20, y=20, w=50, h=50, conditions=conditions)
    >>> e2 = Element(w=300, h=400, elements=[e1])
    >>> e1.x, e1.y, e1.w, e1.h # Default position and size
    (20pt, 20pt, 50pt, 50pt)
    >>> e1.solve() # Solve position and size from conditions.
    Score: 1 Fails: 0
    >>> e1.x, e1.y, e1.w, e1.h # Position and size, solved by position, fitting parent
    (0pt, 20pt, 300pt, 50pt)
    """
    def test(self, e):
        return e.isLeftOnLeft(self.tolerance) and e.isRightOnRight(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.left2Left() and e.fit2Right(), e, score)

class Scale2Width(Condition):
    """Grow the element to left and right side, until it fits the parent element.
    The scale vertical to the original ratio.

    >>> from pagebot.elements import Element
    >>> conditions = [Scale2Width()]
    >>> e1 = Element(x=20, y=20, w=50, h=50, conditions=conditions)
    >>> e2 = Element(w=300, h=400, elements=[e1])
    >>> e1.x, e1.y, e1.w, e1.h # Default position and size
    (20pt, 20pt, 50pt, 50pt)
    >>> e1.solve() # Solve position and size from conditions.
    Score: 1 Fails: 0
    >>> e1.x, e1.y, e1.w, e1.h # Position and size, solved by position, fitting parent
    (0pt, 20pt, 300pt, 300pt)
    """
    def test(self, e):
        return e.isLeftOnLeft(self.tolerance) and e.isRightOnRight(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.left2Left() and e.scale2Right(), e, score)

class Fit2Height(Condition):
    """Grow the element to top and bottom side, until it fits the parent element.

    >>> from pagebot.elements import Element
    >>> conditions = [Fit2Height()]
    >>> e1 = Element(x=20, y=20, w=50, h=50, conditions=conditions)
    >>> e2 = Element(w=300, h=400, elements=[e1])
    >>> e1.x, e1.y, e1.w, e1.h # Default position and size
    (20pt, 20pt, 50pt, 50pt)
    >>> e1.solve() # Solve position and size from conditions.
    Score: 1 Fails: 0
    >>> e1.x, e1.y, e1.w, e1.h # Position and size, solved by position, fitting parent
    (20pt, 0pt, 50pt, 400pt)
    """
    def test(self, e):
        return e.isTopOnTop(self.tolerance) and e.isBottomOnBottom(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.top2Top() and e.fit2Bottom(), e, score)

class Fit2Top(Condition):
    """Grow the element to top side, until it fits the parent element.

    >>> from pagebot.elements import Element
    >>> conditions = [Fit2Top()]
    >>> e1 = Element(x=20, y=20, w=50, h=50, conditions=conditions)
    >>> e2 = Element(w=300, h=400, elements=[e1])
    >>> e1.x, e1.y, e1.w, e1.h # Default position and size
    (20pt, 20pt, 50pt, 50pt)
    >>> e1.solve() # Solve position and size from conditions.
    Score: 1 Fails: 0
    >>> e1.x, e1.y, e1.w, e1.h # Position and size, solved by position, fitting parent
    (20pt, 20pt, 50pt, 430pt)
    """
    def test(self, e):
        return e.isTopOnTop(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.fit2Top(), e, score)

class Fit2Bottom(Condition):
    """Grow the element to bottom side, until it fits the parent element.

    >>> from pagebot.elements import Element
    >>> conditions = [Fit2Bottom()]
    >>> e1 = Element(x=20, y=20, w=50, h=50, conditions=conditions)
    >>> e2 = Element(w=300, h=400, elements=[e1])
    >>> e1.x, e1.y, e1.w, e1.h # Default position and size
    (20pt, 20pt, 50pt, 50pt)
    >>> e1.solve() # Solve position and size from conditions.
    Score: 1 Fails: 0
    >>> e1.x, e1.y, e1.w, e1.h # Position and size, solved by position, fitting parent
    (20pt, 0pt, 50pt, 20pt)
    """
    def test(self, e):
        return e.isBottomOnBottom(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.fit2Bottom(), e, score)

#    F I T T I N G  S I D E S

# There are no "FitOrigin" condition, as these may result is extremely large scalings.

class Fit2WidthSides(Condition): # Note the plural in the name!
    def test(self, e):
        return e.isLeftOnLeftSide(self.tolerance) and e.isRightOnRightSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.left2LeftSide() and e.fit2RightSide(), e, score)

class Fit2LeftSide(Condition):
    def test(self, e):
        return e.isLeftOnLeftSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.fit2LeftSide(), e, score)

class Fit2RightSide(Condition):
    def test(self, e):
        return e.isRightOnRightSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.fit2RightSide(), e, score)

class Fit2HeightSides(Condition):
    def test(self, e):
        return e.isTopOnTopSide(self.tolerance) and e.isBottomOnBottomSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.top2TopSide() and e.fit2BottomSide(), e, score)

class Fit2TopSide(Condition):
    def test(self, e):
        return e.isTopOnTopSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.fit2TopSide(), e, score)

class Fit2TopBleed(Condition):
    """From the current bottom position, until it fits the parent.top and overshooting bleed."""
    def test(self, e):
        return e.isTopOnTopBleed(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.fit2TopBleed(), e, score)

class Fit2BottomSide(Condition):
    def test(self, e):
        return e.isBottomOnBottomSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.fit2BottomSide(), e, score)

class Fit2BottomBleed(Condition):
    def test(self, e):
        return e.isBottomOnBottomBleed(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.fit2BottomBleed(), e, score)

#   F I T T I N G  B L E E D S

class Fit2WidthBleeds(Condition): # Note the plural in the name!
    def test(self, e):
        return e.isLeftOnLeftBleed(self.tolerance) and e.isRightOnRightBleed(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.left2LeftBleed() and e.fit2RightBleed(), e, score)

class Fit2LeftBleed(Condition):
    def test(self, e):
        return e.isLeftOnLeftBleed(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.fit2LeftBleed(), e, score)

class Fit2RightBleed(Condition):
    def test(self, e):
        return e.isRightOnRightBleed(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.fit2RightBleed(), e, score)

class Fit2HeightBleeds(Condition):
    def test(self, e):
        return e.isTopOnTopBleed(self.tolerance) and e.isBottomOnBottomBleed(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.top2TopBleed() and e.fit2BottomBleed(), e, score)

class Fit2TopBleed(Condition):
    """From the current bottom position, until it fits the parent.top and overshooting bleed."""
    def test(self, e):
        return e.isTopOnTopBleed(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.fit2TopBleed(), e, score)

class Fit2BottomBleed(Condition):
    def test(self, e):
        return e.isBottomOnBottomBleed(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.fit2BottomBleed(), e, score)

#    S H R I N K

#   By shrinking conditions, elements get smaller to match the size of their children.
#   Not only literally ”shrinking”, if self is smaller than the space occupied by
#   the child elements, then it will grow on that side.

class Shrink(Condition):
    """Shrink the element on all sides around the margins of the enclose child elements.
    There should be at least one child element for this to be executed."""

    def _getConditions(self):
        return [Left2Left, Top2Top, Fit2Right, Fit2Bottom]

    def evaluate(self, e, score):
        """Fit the element on all margins of the parent. First align left and top,
        then fit right and bottom. This order to avoid that element temporary
        get smaller than their minimum size, if the start position is wrong."""
        self.evaluateAll(e, self._getConditions(), score)

    def solve(self, e, score):
        self.solveAll(e, self._getConditions(), score)

class Shrink2BlockSides(Condition):
    """Shirink the element on all sides of the children sides. There needs to be at least
    one child element."""

    def _getConditions(self):
        return [Shrink2BlockLeftSide, Shrink2BlockTopSide, Shrink2BlockRightSide, Shrink2BlockBottomSide]

    def evaluate(self, e, score):
        self.evaluateAll(e, self._getConditions(), score)

    def solve(self, e, score):
        self.solveAll(e, self._getConditions(), score)

# There are no "ShrinkOrigin" condition, as these may result is extremely large scalings.

class Shrink2BlockLeft(Condition):
    def test(self, e):
        return e.isShrunkOnBlockLeft(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.shrink2BlockLeft(), e, score)

class Shrink2BlockRight(Condition):
    def test(self, e):
        return e.isShrunkOnBlockRight(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.shrink2BlockRight(), e, score)


class Shrink2BlockTop(Condition):
    def test(self, e):
        return e.isShrunkOnBlockTop(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.shrink2BlockTop(), e, score)

class Shrink2BlockBottom(Condition):
    def test(self, e):
        return e.isShrunkOnBlockBottom(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.shrink2BlockBottom(), e, score)

#    S H R I N K I N G  S I D E S

#   Shrink to sides of the child elements, regardless of their margins or the padding of the parent
#   There are no "Shrink2Origin" conditions, as these may result is extremely large scalings.

class Shrink2BlockWidthSides(Condition): # Note the plural in the name.
    def test(self, e):
        return e.isShrunkOnBlockLeftSide(self.tolerance) and e.isShrunkOnBlockRightSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.shrink2BlockLeftSide() and e.shrink2BlockRightSide(), e, score)

class Shrink2BlockLeftSide(Condition):
    def test(self, e):
        return e.isShrunkOnBlockLeftSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.shrink2BlockLeftSide(), e, score)

class Shrink2BlockRightSide(Condition):
    def test(self, e):
        return e.isShrunkOnBlockRightSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.strink2BlockRightSide(), e, score)

class Shrink2BlockHeightSide(Condition):
    def test(self, e):
        return e.isShrunkOnBlockTopSide(self.tolerance) and e.isShrunkOnBlockBottomSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.shrink2BlockTopSide() and e.shrink2BlockBottomSide(), e, score)

class Shrink2BlockTopSide(Condition):
    def test(self, e):
        return e.isShrunkOnBlockTopSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.shrink2BlockTopSide(), e, score)

class Shrink2BlockBottomSide(Condition):
    def test(self, e):
        return e.isShrunkOnBlockBottomSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.shrink2BlockBottomSide(), e, score)

#    B L O C K  F I T T I N G
#
#    Make the block fit the width/height of the element.

class FitBlock2Width(Condition):
    def test(self, e):
        return e.isBlockFittingWidth(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.fitBlock2Width(), e, score)

class FitBlock2WidthSides(Condition):
    def test(self, e):
        return e.isBlockFittingWidthSides(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.fitBlock2WidthSides(), e, score)

class FitBlock2Height(Condition):
    def test(self, e):
        return e.isBlockFittingHeight(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.fitBlock2Height(), e, score)

class FitBlock2HeightSides(Condition):
    def test(self, e):
        return e.isBlockFittingHeightSides(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.fitBlock2HeightSides(), e, score)

#    C E N T E R  H O R I Z O N T A L

class Center(Condition):
    """Center and Middle e bounding box horizontal and vertical."""
    def test(self, e):
        return e.isCenterOnCenter(self.tolerance) and e.isMiddleOnMiddle(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition text fails.
            self.addScore(e.center2Center() and e.middle2Middle(), e, score)

#    Center Horizontal Margins

class Center2Center(Condition):
    """Center e bounding box horizontal between parent paddings."""
    def test(self, e):
        return e.isCenterOnCenter(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.center2Center(), e, score)

class Left2Center(Condition):
    """Align left of e bounding box horizontal between parent padding."""
    def test(self, e):
        return e.isLeftOnCenter(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.left2Center(), e, score)

class Right2Center(Condition):
    """Align right of e bounding box horizontal between parent paddings."""
    def test(self, e):
        return e.isRightOnCenter(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.right2Center(), e, score)

class Origin2Center(Condition):
    """Align left of e bounding box horizontal between parent paddings."""
    def test(self, e):
        return e.isOriginOnCenter(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.origin2Center(), e, score)

#    Center Horizontal Sides

class Center2CenterSides(Condition):
    """Center e bounding box horizontal between parent sides."""
    def test(self, e):
        return e.isCenterOnCenterSides(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.center2CenterSides(), e, score)

class Left2CenterSides(Condition):
    """Align left of e bounding box horizontal between parent sides."""
    def test(self, e):
        return e.isLeftOnCenterSides(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.left2CenterSides(), e, score)

class Right2CenterSides(Condition):
    """Align right of e bounding box horizontal between parent margins."""
    def test(self, e):
        return e.isRightOnCenterSides(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.right2CenterSides(), e, score)

class Origin2CenterSides(Condition):
    """Align left of e bounding box horizontal between parent margins."""
    def test(self, e):
        return e.isOriginOnCenterSides(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.origin2CenterSides(), e, score)

#   L E F T / R I G H T

class Center2Left(Condition):
    """Move center of e bounding box on parent left margin."""
    def test(self, e):
        return e.isCenterOnLeft(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.center2Left(), e, score)

class Left2Left(Condition):
    """Align left of e bounding box on parent left margin."""
    def test(self, e):
        return e.isLeftOnLeft(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.left2Left(), e, score)

class Right2Left(Condition):
    """Align right of e bounding box to parent left margin."""
    def test(self, e):
        return e.isRightOnLeft(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.right2Left(), e, score)

class Origin2Left(Condition):
    """Align left of e bounding box horizontal between parent margins."""
    def test(self, e):
        return e.isOriginOnLeft(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.origin2Left(), e, score)

class Center2LeftSide(Condition):
    """Move center of e bounding box on parent left side."""
    def test(self, e):
        return e.isCenterOnLeftSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.center2LeftSide(), e, score)

class Left2LeftSide(Condition):
    """Align left of e bounding box on parent left side."""
    def test(self, e):
        return e.isLeftOnLeftSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.left2LeftSide(), e, score)

class Left2LeftBleed(Condition):
    """Align left of e bounding box on parent left bleed side."""
    def test(self, e):
        return e.isLeftOnLeftBleed(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.left2LeftBleed(), e, score)

# Missing on purpose: Right2LeftSide(Condition). Element is not visible.

class Origin2LeftSide(Condition):
    """Align left of e bounding box horizontal between parent left side."""
    def test(self, e):
        return e.isOriginOnLeftSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.origin2LeftSide(), e, score)

class Center2Right(Condition):
    """Move center of e bounding box on parent right margin."""
    def test(self, e):
        return e.isCenterOnRight(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.center2Right(), e, score)

class Left2Right(Condition):
    """Align left of e bounding box on parent right margin."""
    def test(self, e):
        return e.isLeftOnRight(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.left2Right(), e, score)

class Left2RightSide(Condition):
    """Align left of e bounding box on parent right side."""
    def test(self, e):
        return e.isLeftOnRightSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.left2RightSide(), e, score)

class Right2Right(Condition):
    """Align right of e bounding box to parent right margin."""
    def test(self, e):
        return e.isRightOnRight(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.right2Right(), e, score)

class Origin2Right(Condition):
    """Align origin of e bounding box to parent right margin."""
    def test(self, e):
        return e.isOriginOnRight(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.origin2Right(), e, score)

#    Left Horizontal Sides

class Center2RightSide(Condition):
    """Move center of e bounding box on parent right side."""
    def test(self, e):
        return e.isCenterOnRightSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.center2RightSide(), e, score)

# Missing on purpose: Left2RightSide(Condition). Element is not visible.

class Right2RightSide(Condition):
    """Align left of e bounding box on parent right side."""
    def test(self, e):
        return e.isRightOnRightSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.right2RightSide(), e, score)

class Right2RightBleed(Condition):
    """Align left of e bounding box on parent right bleed side."""
    def test(self, e):
        return e.isRightOnRightBleed(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.right2RightBleed(), e, score)

class Origin2RightSide(Condition):
    """Align origin of e bounding box horizontal between parent right side."""
    def test(self, e):
        return e.isOriginOnRightSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.origin2RightSide(), e, score)

#    V E R T I C A L S

#    Middle Vertical Margins (vertical center, following CSS naming convention)

class Middle2Middle(Condition):
    """Middle (vertical center) e bounding box vertical between parent margins."""
    def test(self, e):
        return e.isMiddleOnMiddle(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.middle2Middle(), e, score)

class Middle2MiddleSides(Condition):
    """Middle e bounding box vertical between parent vertical sides."""
    def test(self, e):
        return e.isMiddleOnMiddleSides(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.middle2MiddleSides(), e, score)

class Top2Middle(Condition):
    """Align top of e bounding box vertical middle between parent margins."""
    def test(self, e):
        return e.isTopOnMiddle(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.top2Middle(), e, score)

class Top2MiddleSides(Condition):
    """Align top of e bounding box on vertical middle between parent sides."""
    def test(self, e):
        return e.isTopOnMiddleSides(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.top2MiddleSides(), e, score)

class Bottom2Middle(Condition):
    """Align bottom of e bounding box on vertical middle between parent margins."""
    def test(self, e):
        return e.isBottomOnMiddle(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.bottom2Middle(), e, score)

class Bottom2MiddleSides(Condition):
    """Align right of e bounding box on vertical middle between parent sides."""
    def test(self, e):
        return e.isBottomOnMiddleSides(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.bottom2MiddleSides(), e, score)

class Origin2Middle(Condition):
    """Align origin of e bounding box to vertical middle between parent margin."""
    def test(self, e):
        return e.isOriginOnMiddle(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.origin2Middle(), e, score)

class Origin2MiddleSides(Condition):
    """Align origin of e bounding box to vertical middle between parent sides."""
    def test(self, e):
        return e.isOriginOnMiddleSides(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.origin2MiddleSides(), e, score)

class Origin2Top(Condition):
    """Align left of e bounding box horizontal between parent margins."""
    def test(self, e):
        return e.isOriginOnTop(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.origin2Top(), e, score)

class Middle2Top(Condition):
    """Move middle (vertical center) of e bounding box on parent top margin."""
    def test(self, e):
        return e.isMiddleOnTop(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.middle2Top(), e, score)

class Middle2TopSide(Condition):
    """Move middle (vertical center) of e bounding box on parent top side."""
    def test(self, e):
        return e.isMiddleOnTopSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.middle2TopSide(), e, score)

class Top2Top(Condition):
    """Align top of e bounding box on parent top margin."""
    def test(self, e):
        return e.isTopOnTop(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.top2Top(), e, score)

class Top2TopSide(Condition):
    """Align top of e bounding box on parent top side."""
    def test(self, e):
        return e.isTopOnTopSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.top2TopSide(), e, score)

class Top2TopBleed(Condition):
    """Align top of e bounding box on parent top side, overshooting by bleed."""
    def test(self, e):
        return e.isTopOnTopBleed(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.top2TopBleed(), e, score)

class Bottom2Top(Condition):
    """Align bottom of e bounding box on parent top margin."""
    def test(self, e):
        return e.isBottomOnTop(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.bottom2Top(), e, score)

# Missing on purpose: Bottom2TopSide(Condition). Element is not visible.

class Origin2TopSide(Condition):
    """Align left of e bounding box horizontal between parent top side."""
    def test(self, e):
        return e.isOriginOnTopSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.origin2TopSide(), e, score)

class Middle2Bottom(Condition):
    """Move middle (vertical center) of e bounding box on parent bottom margin."""
    def test(self, e):
        return e.isMiddleOnBottom(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.middle2Bottom(), e, score)

class Top2Bottom(Condition):
    """Align top of e bounding box on parent bottom margin."""
    def test(self, e):
        return e.isTopOnBottom(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.top2Bottom(), e, score)

class Bottom2Bottom(Condition):
    """Align bottom of e bounding box to parent bottom margin."""
    def test(self, e):
        return e.isBottomOnBottom(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.bottom2Bottom(), e, score)

class Origin2Bottom(Condition):
    """Align origin of e bounding box to parent bottom margin."""
    def test(self, e):
        return e.isOriginOnBottom(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.origin2Bottom(), e, score)

#    Left Horizontal Sides

class Middle2BottomSide(Condition):
    """Move middle (vertical center) of e bounding box on parent bottom side."""
    def test(self, e):
        return e.isMiddleOnBottomSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.middle2BottomSide(), e, score)

# Missing on purpose: TopBottomSide(Condition). Element is not visible.

class Bottom2BottomSide(Condition):
    """Align bottom of e bounding box on parent bottom side."""
    def test(self, e):
        return e.isBottomOnBottomSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.bottom2BottomSide(), e, score)

class Bottom2BottomBleed(Condition):
    """Align bottom of e bounding box on parent bottom side, overshooting by the vertical bleed value."""
    def text(self, e):
        return e.isBottomOnBottomBleed(self.tolerance)

    def solve(self, e, score):
        if not self.text(e): # Only try to solve if condition test fails.
            self.addScore(e.bottom2BottomBleed(), e, score)

class Origin2BottomSide(Condition):
    """Align origin of e bounding box horizontal between parent bottom side."""
    def test(self, e):
        return e.isOriginOnBottomSide(self.tolerance)

    def solve(self, e, score):
        if not self.test(e): # Only try to solve if condition test fails.
            self.addScore(e.origin2BottomSide(), e, score)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
