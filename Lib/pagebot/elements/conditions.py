#!/usr/bin/env python3
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
#     conditions.py
#

class Conditions:

    #   C O N D I T I O N S

    def isBottomOnBottom(self, tolerance=0):
        return abs(self.parent.pb - self.mBottom) <= tolerance

    def isBottomOnSideBottom(self, tolerance=0):
        return abs(self.mBottom) <= tolerance

    def isBottomOnBleedBottom(self, tolerance=0):
        return abs(self.mBottom - self.bleedBottom) <= tolerance

    def isBottomOnTop(self, tolerance=0):
        return abs(self.parent.h - self.parent.pt - self.mBottom) <= tolerance

    def isCenterOnCenter(self, tolerance=0):
        pl = self.parent.pl # Get parent padding left
        center = (self.parent.w - self.parent.pr - pl)/2
        return abs(pl + center - self.center) <= tolerance

    def isCenterOnCenterSides(self, tolerance=0):
        return abs(self.parent.w/2 - self.center) <= tolerance

    def isCenterOnLeft(self, tolerance=0):
        return abs(self.parent.pl - self.center) <= tolerance

    def isCenterOnRight(self, tolerance=0):
        return abs(self.parent.w - self.parent.pr - self.center) <= tolerance

    def isCenterOnSideRight(self, tolerance=0):
        return abs(self.parent.w - self.center) <= tolerance

    def isMiddleOnBottom(self, tolerance=0):
        return abs(self.parent.pb - self.middle) <= tolerance

    def isMiddleOnSideBottom(self, tolerance=0):
        return abs(self.middle) <= tolerance

    def isMiddleOnTop(self, tolerance=0):
        return abs(self.parent.h - self.parent.pt - self.middle) <= tolerance

    def isMiddleOnSideTop(self, tolerance=0):
        return abs(self.parent.h - self.middle) <= tolerance

    def isMiddleOnMiddle(self, tolerance=0):
        pt = self.parent.pt # Get parent padding top
        pb = self.parent.pb
        middle = (self.parent.h - pt - pb)/2
        return abs(pb + middle - self.middle) <= tolerance

    def isMiddleOnMiddleSides(self, tolerance=0):
        return abs(self.parent.h - self.middle) <= tolerance

    def isLeftOnCenter(self, tolerance=0):
        pl = self.parent.pl # Get parent padding left
        center = (self.parent.w - self.parent.pr - pl)/2
        return abs(pl + center - self.mLeft) <= tolerance

    def isLeftOnCenterSides(self, tolerance=0):
        return abs(self.parent.w/2 - self.mLeft) <= tolerance

    def isLeftOnLeft(self, tolerance=0):
        return abs(self.parent.pl - self.mLeft) <= tolerance

    def isLeftOnSideLeft(self, tolerance=0):
        return abs(self.mLeft) <= tolerance

    def isLeftOnBleedLeft(self, tolerance=0):
        return abs(self.mLeft + self.bleedLeft) <= tolerance

    def isLeftOnRight(self, tolerance=0):
        return abs(self.parent.w - self.parent.pr - self.mLeft) <= tolerance

    def isLeftOnSideRight(self, tolerance=0):
        return abs(self.parent.w - self.mLeft) <= tolerance

    def isCenterOnSideLeft(self, tolerance=0):
        return abs(self.parent.mLeft - self.center) <= tolerance

    def isTopOnMiddle(self, tolerance=0):
        pt = self.parent.pt # Get parent padding top
        pb = self.parent.pb
        middle = (self.parent.h - pb - pt)/2
        return abs(pb + middle - self.mTop) <= tolerance

    def isTopOnMiddleSides(self, tolerance=0):
        return abs(self.parent.h/2 - self.mTop) <= tolerance

    def isOriginOnBottom(self, tolerance=0):
        pb = self.parent.pb # Get parent padding left
        return abs(pb - self.y) <= tolerance

    def isOriginOnSideBottom(self, tolerance=0):
        return abs(self.y) <= tolerance

    def isOriginOnCenter(self, tolerance=0):
        pl = self.parent.pl # Get parent padding left
        center = (self.parent.w - self.parent.pr - pl)/2
        return abs(pl + center - self.x) <= tolerance

    def isOriginOnCenterSides(self, tolerance=0):
        return abs(self.parent.w/2 - self.x) <= tolerance

    def isOriginOnLeft(self, tolerance=0):
        return abs(self.parent.pl - self.x) <= tolerance

    def isOriginOnSideLeft(self, tolerance=0):
        return abs(self.x) <= tolerance

    def isOriginOnRight(self, tolerance=0):
        return abs(self.parent.w - self.parent.pr - self.x) <= tolerance

    def isOriginOnSideRight(self, tolerance=0):
        return abs(self.parent.w - self.x) <= tolerance

    def isOriginOnTop(self, tolerance=0):
        return abs(self.parent.h - self.parent.pt - self.y) <= tolerance

    def isOriginOnSideTop(self, tolerance=0):
        """Answers if the origin of self is on the top side of self.parent.

        >>> from pagebot.elements.element import Element
        >>> e1 = Element(w=200, h=400)
        >>> e2 = Element(w=50, h=50, parent=e1)
        >>> #FIX e1.isOriginOnSideTop()
        False
        >>> #FIX e2.isOriginOnSideTop()
        False
        >>> e2.y = e1.top
        >>> #FIX e2.isOriginOnSideTop(), e2.y, e1.top
        (True, 500pt, 500pt)
        """
        if self.parent is None:
            return False
        return abs(self.parent.top - self.y) <= tolerance

    def isOriginOnMiddle(self, tolerance=0):
        """Answers if the origin of self is on the top side of self.parent.

        >>> from pagebot.elements.element import Element
        >>> e1 = Element(w=200, h=400)
        >>> e2 = Element(w=50, h=50, parent=e1)
        >>> e1.isOriginOnMiddle()
        False
        >>> #FIX e2.isOriginOnMiddle()
        False
        >>> e2.y = e1.middle
        >>> #FIX e2.isOriginOnMiddle(), e2.y, e1.middle
        (True, 500pt, 500pt)
        """
        if self.parent is None:
            return False
        return abs(self.parent.middle - self.y) <= tolerance

    def isOriginOnMiddleSides(self, tolerance=0):
        return abs(self.parent.h/2 - self.y) <= tolerance

    def isRightOnCenter(self, tolerance=0):
        """Answers if the right size of `self` is on the middle of the parent.

        >>> from pagebot.elements.element import Element
        >>> e1 = Element(x=100, w=200) # e1.right == 300
        >>> e2 = Element(w=600, elements=[e1])

        """
        return abs(self.parent.pl + self.parent.pw/2 - self.mRight) <= tolerance

    def isRightOnCenterSides(self, tolerance=0):
        return abs(self.parent.w/2 - self.mRight) <= tolerance

    def isRightOnLeft(self, tolerance=0):
        return abs(self.parent.pl - self.mRight) <= tolerance

    def isRightOnRight(self, tolerance=0):
        return abs(self.parent.w - self.parent.pr - self.mRight) <= tolerance

    def isRightOnSideRight(self, tolerance=0):
        return abs(self.parent.w - self.mRight) <= tolerance

    def isRightOnBleedRight(self, tolerance=0):
        return abs(self.parent.w + self.bleedLeft) <= tolerance

    def isBottomOnMiddle(self, tolerance=0):
        pt = self.parent.pt # Get parent padding top
        pb = self.parent.pb
        middle = (self.parent.h - pb - pt)/2
        return abs(pb + middle - self.mBottom) <= tolerance

    def isBottomOnMiddleSides(self, tolerance=0):
        return abs(self.parent.h/2 - self.mBottom) <= tolerance

    def isTopOnBottom(self, tolerance=0):
        return abs(self.parent.pb - self.mTop) <= tolerance

    def isTopOnTop(self, tolerance=0):
        return abs(self.parent.h - self.parent.pt - self.mTop) <= tolerance

    def isTopOnSideTop(self, tolerance=0):
        return abs(self.parent.h - self.mTop) <= tolerance

    def isTopOnBleedTop(self, tolerance=0):
        return abs(self.parent.h - self.mTop + self.bleedTop) <= tolerance

    # Shrink block conditions

    def isSchrunkOnBlockLeft(self, tolerance):
        boxX, _, _, _ = self.marginBox
        return abs(self.mLeft + self.pl - boxX) <= tolerance

    def isShrunkOnBlockRight(self, tolerance):
        boxX, _, boxW, _ = self.marginBox
        return abs(self.mRight - self.pr - (boxX + boxW)) <= tolerance

    def isShrunkOnBlockTop(self, tolerance):
        _, boxY, _, boxH = self.marginBox
        return self.mTop - self.pt - (boxY + boxH) <= tolerance

    def isShrunkOnBlockBottom(self, tolerance):
        """Test if the bottom of self is shrunk to the bottom position of the
        block."""
        _, boxY, _, boxH = self.marginBox
        return abs(self.pb - boxY) <= tolerance

    def isShrunkOnBlockSideLeft(self, tolerance):
        boxX, _, _, _ = self.box
        return abs(self.mLeft - boxX) <= tolerance

    def isShrunkOnBlockSideRight(self, tolerance):
        boxX, _, boxW, _ = self.mbox
        return abs(self.mRight - (boxX + boxW)) <= tolerance

    def isShrunkOnBlockSideTop(self, tolerance):
        _, boxY, _, boxH = self.box
        return self.mTop - (boxY + boxH) <= tolerance

    def isShrunkOnBlockSideBottom(self, tolerance):
        _, boxY, _, boxH = self.marginBox
        return abs(self.mBottom - boxY) <= tolerance

    # Unimplemented here for text operations.

    def isShrunkOnTextHeight(self, tolerance=0):
        """For non-text elements, this is always True to satisfy the calling
        condition."""
        return True

    def shrink2TextHeight(self, tolerance=0):
        """For non-text elements, this is always True to satisfy the calling
        condition."""
        return True

    def isShrunkOnTextWidth(self, tolerance=0):
        """For non-text elements, this is always True to satisfy the calling
        condition."""
        return True

    def shrink2TextWidth(self, tolerance=0):
        """For non-text elements, this is always True to satisfy the calling
        condition."""
        return True

    # Float conditions to page padding.

    def isFloatOnTop(self, tolerance=0):
        answer = abs(min(self.getFloatSideTop(), self.parent.h - self.parent.pt) - self.mTop) <= tolerance
        return answer

    def isFloatOnBottom(self, tolerance=0):
        return abs(max(self.getFloatSideBottom(), self.parent.pb) - self.mBottom) <= tolerance

    def isFloatOnLeft(self, tolerance=0):
        answer = abs(max(self.getFloatSideLeft(), self.parent.pl) - self.mLeft) <= tolerance
        return answer

    def isFloatOnRight(self, tolerance=0):
        return abs(min(self.getFloatSideRight(), self.parent.w - self.parent.pr) - self.mRight) <= tolerance

    # Float conditions to page sides

    def isFloatOnSideTop(self, tolerance=0):
        return abs(self.getFloatSideTop() - self.mTop) <= tolerance

    def isFloatOnSideBottom(self, tolerance=0):
        return abs(self.getFloatSideBottom() - self.mBottom) <= tolerance

    def isFloatOnSideLeft(self, tolerance=0):
        return abs(self.getFloatSideLeft() - self.mLeft) <= tolerance

    def isFloatOnSideRight(self, tolerance=0):
        return abs(self.getFloatSideRight() - self.mRight) <= tolerance

    #   Column/Row conditions

    def isLeftOnCol(self, col, tolerance):
        """Move top of the element to col index position."""
        gridColumns = self.getGridColumns()
        if col in range(len(gridColumns)):
            return abs(self.mLeft - gridColumns[col][0]) <= tolerance
        return False # row is not in range of gridColumns

    def isRightOnCol(self, col, tolerance):
        """Move top of the element to col index position."""
        gridColumns = self.getGridColumns()
        if col in range(len(gridColumns)):
            return abs(self.mRight - gridColumns[col][0] - self.gw) <= tolerance
        return False # row is not in range of gridColumns

    def isFitOnColSpan(self, col, colSpan, tolerance):
        """Answers if the self.w is the same as the total of column widths
        between col and col+colSpan.

        >>> from pagebot.toolbox.units import pt
        >>> from pagebot.elements.element import Element
        >>> gridX = (pt(100, 10), pt(200, 20), pt(300, 30), pt(400, 40), pt(500, 50))
        >>> e1 = Element(padding=30, w=600, gridX=gridX)
        >>> e1.getGridColumns()
        [(0, 100pt), (110pt, 200pt), (330pt, 300pt), (660pt, 400pt), (1100pt, 500pt)]
        >>> e2 = Element(w=100, parent=e1)
        >>> e1.getGridColumns()
        [(0, 100pt), (110pt, 200pt), (330pt, 300pt), (660pt, 400pt), (1100pt, 500pt)]
        >>> e2.isFitOnColSpan(0, 1, 0)
        True
        >>> e2.w = 310
        >>> e2.isFitOnColSpan(0, 2, 0)
        True
        >>> e2.w = 950
        >>> e2.isFitOnColSpan(1, 3, 0)
        True
        """
        gridColumns = self.getGridColumns()

        if col >= 0 and col+colSpan <= len(gridColumns):
            c1 = gridColumns[col]
            c2 = gridColumns[col + colSpan - 1]
            return abs(self.w - (c2[0] - c1[0] + c2[1])) <= tolerance

        return False

    def isTopOnRow(self, row, tolerance):
        """Move top of the element to row."""
        gridRows = self.getGridRows()

        if row in range(len(gridRows)):
            return abs(self.mTop - gridRows[row][0]) <= tolerance

        # row is not in range of gridColumns.
        return False

    def isBottomOnRow(self, row, tolerance):
        """Move top of the element to row."""
        gridRows = self.getGridRows()

        if row in range(len(gridRows)):
            return abs(self.mBottom - gridRows[row][0]) <= tolerance

        # row is not in range of gridColumns.
        return False

    def isFitOnRowSpan(self, row, rowSpan, tolerance):
        gridRows = self.getGridRows()
        if row >= 0 and row+rowSpan < len(gridRows):
            r1 = gridRows[row]
            r2 = gridRows[row + rowSpan - 1]
            return abs(self.h - (r2[0] - r1[0] + r2[1])) <= tolerance
        return False

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
