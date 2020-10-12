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
#     alignments.py
#

class Alignments:

    #   Column/Row alignment

    def left2Col(self, col):
        """Move top of the element to col index position."""
        gridColumns = self.getGridColumns()

        if col in range(len(gridColumns)):
            self.mLeft = self.parent.pl + gridColumns[col][0] # @@@ FIX GUTTER
            return True

        # Row is not in range of available gridColumns.
        return False

    def right2Col(self, col):
        """Move right of the element to col index position."""
        gridColumns = self.getGridColumns()

        if col in range(len(gridColumns)):
            self.mRight = self.parent.pl + gridColumns[col][0] - self.gw
            return True

        # Row is not in range of available gridColumns.
        return False

    def fit2ColSpan(self, col, colSpan):
        """Fit the width of self to colSpan (can run over several columns),
        starting at column index col.

        >>> from pagebot.toolbox.units import pt
        >>> from pagebot.elements.element import Element
        >>> gridX = (pt(100, 10), pt(200, 20), pt(300, 30), pt(400, 40), pt(500, 50))
        >>> e1 = Element(padding=30, w=600, gridX=gridX)
        >>> e1.getGridColumns()
        [(0, 100pt), (110pt, 200pt), (330pt, 300pt), (660pt, 400pt), (1100pt, 500pt)]
        >>> e2 = Element(w=100, parent=e1)
        >>> e2.isFitOnColSpan(1, 3, 0), e2.w
        (False, 100pt)
        >>> e2.fit2ColSpan(1, 3)
        True
        >>> e2.isFitOnColSpan(1, 3, 0), e2.w
        (True, 950pt)
        """
        gridColumns = self.getGridColumns()
        if col >= 0 and col+colSpan <= len(gridColumns):
            c1 = gridColumns[col]
            c2 = gridColumns[col + colSpan - 1]
            self.w = c2[0] - c1[0] + c2[1]
            return True
        return False

    def top2Row(self, row):
        """Move top of the element to row."""
        gridRows = self.getGridRows()
        if row in range(len(gridRows)):
            self.mTop = self.parent.pb + gridRows[row][0] # @@@ FIX GUTTER
            return True
        return False # row is not in range of gridColumns

    def bottom2Row(self, row):
        """Move top of the element to row."""
        gridRows = self.getGridRows()
        if row in range(len(gridRows)):
            self.mBottom = self.parent.pb + gridRows[row][0] # @@@ FIX GUTTER
            return True
        return False # row is not in range of gridColumns

    def fit2RowSpan(self, row, rowSpan):
        gridRows = self.getGridRows()
        indices = range(len(gridRows))
        if row in indices and row + rowSpan in indices:
            r1 = gridRows[row]
            r2 = gridRows[row + rowSpan - 1]
            self.h = r2[0] - r1[0] + r2[1]
            return True
        return False

    def top2Grid(self):
        """Move the top of self to rounded grid

        >>> from pagebot.elements.element import Element
        >>> e1 = Element(baselineGridStart=100, baselineGrid=10, h=1000)
        >>> e2 = Element(y=105, h=200, parent=e1)
        >>> e2.top
        305pt
        >>> e2.top2Grid()
        >>> e2.y
        100pt
        >>> e2.y = 101
        >>> e2.top2Grid()
        >>> e2.y
        100pt
        >>> e2.y = 106
        >>> e2.top2Grid()
        >>> e2.y
        110pt
        """
        self.top += self.getDistance2Grid(self.top)

    def bottom2Grid(self):
        """Move the top of self to rounded grid

        >>> from pagebot.elements.element import Element
        >>> e1 = Element(baselineGridStart=100, baselineGrid=10, h=1000)
        >>> e2 = Element(y=105, h=200, parent=e1)
        >>> e2.bottom
        105pt
        >>> e2.bottom2Grid()
        >>> e2.y
        100pt
        >>> e2.y = 101
        >>> e2.bottom2Grid()
        >>> e2.y
        100pt
        >>> e2.y = 106
        >>> e2.bottom2Grid()
        >>> e2.y
        110pt
        """
        self.bottom += self.getDistance2Grid(self.bottom)

    def _get_distance2Grid(self):
        """Answer the distance to the parent grid, where vertical alignment
        decides where is measured.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.toolbox.units import pt
        >>> e1 = Element(baselineGridStart=100, baselineGrid=50, h=1000)
        >>> e2 = Element(y=130, h=200, parent=e1)
        >>> e2.distance2Grid
        20pt
        >>> e2.y = pt(140)
        >>> e2.distance2Grid
        10pt
        >>> e2.y = pt(150)
        >>> e2.distance2Grid
        0pt
        """
        return self.parent.getDistance2Grid(self.y)
    distance2Grid = property(_get_distance2Grid)

    #   Page block and Page side alignments

    #   Horizontal alignments

    def center2Center(self):
        """Move center of self to padding center position of parent.
        Note that this different from self.center2CenterSides if the left
        and right padding of parent is not identical.
        The position of e2 element origin depends on the horizontal
        alignment type.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import LEFT, CENTER, RIGHT
        >>> e1 = Element(w=500, pl=30, pr=80) # Force non-symmetry
        >>> e1.center2Center() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.center2Center()
        >>> e2.x, 30 + (500 - 30 - 80)/2 - 120/2
        (165pt, 165.0)
        >>> e2.xAlign = CENTER
        >>> success = e2.center2Center()
        >>> e2.x, 30 + (500 - 30 - 80)/2
        (225pt, 225.0)
        >>> e2.xAlign = RIGHT
        >>> success = e2.center2Center()
        >>> e2.x, 30 + (500 - 30 - 80)/2 + 120/2
        (285pt, 285.0)
        """
        if self.parent is None:
            return False
        self.center = self.parent.pl + self.parent.pw/2
        return True

    def center2CenterSides(self):
        """Move center of self to center of sides of parent.
        Note that this different from self.center2Center if the left
        and right padding of parent is not identical.
        The position of e2 element origin depends on the horizontal
        alignment type.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import LEFT, CENTER, RIGHT
        >>> e1 = Element(w=500, pl=30, pr=80) # Force non-symmetry
        >>> e1.center2CenterSides() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.center2CenterSides()
        >>> e2.x, 500/2 - 120/2
        (190pt, 190.0)
        >>> e2.xAlign = CENTER
        >>> success = e2.center2CenterSides()
        >>> e2.x, 500/2
        (250pt, 250.0)
        >>> e2.xAlign = RIGHT
        >>> success = e2.center2CenterSides()
        >>> e2.x, 500/2 + 120/2
        (310pt, 310.0)
        """
        if self.parent is None:
            return False
        self.center = self.parent.w/2
        return True

    def center2Left(self):
        """Move center of self to left padding of parent.
        The position of e2 element origin depends on the horizontal
        alignment type.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import LEFT, CENTER, RIGHT
        >>> e1 = Element(w=500, pl=30, pr=80) # Force non-symmetry
        >>> e1.center2Left() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.center2Left()
        >>> e2.x, 30 - 120/2
        (-30pt, -30.0)
        >>> e2.xAlign = CENTER
        >>> success = e2.center2Left()
        >>> e2.x, 30
        (30pt, 30)
        >>> e2.xAlign = RIGHT
        >>> success = e2.center2Left()
        >>> e2.x, 30 + 120/2
        (90pt, 90.0)
        """
        if self.parent is None:
            return False
        self.center = self.parent.pl # Padding left
        return True

    def center2SideLeft(self):
        """Move center of self to left side of parent.
        The position of e2 element origin depends on the horizontal
        alignment type.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import LEFT, CENTER, RIGHT
        >>> e1 = Element(w=500, pl=30, pr=80) # Force non-symmetry
        >>> e1.center2SideLeft() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.center2SideLeft()
        >>> e2.x, -120/2
        (-60pt, -60.0)
        >>> e2.xAlign = CENTER
        >>> success = e2.center2SideLeft()
        >>> e2.x
        0pt
        >>> e2.xAlign = RIGHT
        >>> success = e2.center2SideLeft()
        >>> e2.x, 120/2
        (60pt, 60.0)
        """
        if self.parent is None:
            return False
        self.center = 0
        return True

    def center2Right(self):
        """Move center of self to the right padding of parent.
        The position of e2 element origin depends on the horizontal
        alignment type.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import LEFT, CENTER, RIGHT
        >>> e1 = Element(w=500, pl=30, pr=80) # Force non-symmetry
        >>> e1.center2Right() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.center2Right()
        >>> e2.x, 500 - 80 - 120/2
        (360pt, 360.0)
        >>> e2.xAlign = CENTER
        >>> success = e2.center2Right()
        >>> e2.x, 500 - 80
        (420pt, 420)
        >>> e2.xAlign = RIGHT
        >>> success = e2.center2Right()
        >>> e2.x, 500 - 80 + 120/2
        (480pt, 480.0)
        """
        if self.parent is None:
            return False
        self.center = self.parent.w - self.parent.pr
        return True

    def center2SideRight(self):
        """Move center of self to the right side of parent.
        The position of e2 element origin depends on the horizontal
        alignment type.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import LEFT, CENTER, RIGHT
        >>> e1 = Element(w=500, pl=30, pr=80) # Force non-symmetry
        >>> e1.center2SideRight() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.center2SideRight()
        >>> e2.x, 500 - 120/2
        (440pt, 440.0)
        >>> e2.xAlign = CENTER
        >>> success = e2.center2SideRight()
        >>> e2.x, 500
        (500pt, 500)
        >>> e2.xAlign = RIGHT
        >>> success = e2.center2SideRight()
        >>> e2.x, 500 + 120/2
        (560pt, 560.0)
        """
        if self.parent is None:
            return False
        self.center = self.parent.w
        return True

    def left2Center(self):
        """Move left of self to the padding center of parent.
        The position of e2 element origin depends on the horizontal
        alignment type.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import RIGHT, CENTER, LEFT
        >>> e1 = Element(w=500, pl=30, pr=80) # Force non-symmetry
        >>> e1.left2Center() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.left2Center()
        >>> e2.x, 30 + (500 - 30 - 80)/2
        (225pt, 225.0)
        >>> e2.xAlign = CENTER
        >>> success = e2.left2Center()
        >>> e2.x, 30 + (500 - 30 - 80)/2 + 120/2
        (285pt, 285.0)
        >>> e2.xAlign = RIGHT
        >>> success = e2.left2Center()
        >>> e2.x, 30 + (500 - 30 - 80)/2 + 120
        (345pt, 345.0)
        """
        if self.parent is None:
            return False
        self.mLeft = self.parent.pl + self.parent.pw/2
        return True

    def left2CenterSides(self):
        """Move left of self to the sides center of parent.
        The position of e2 element origin depends on the horizontal
        alignment type.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import RIGHT, CENTER, LEFT
        >>> e1 = Element(w=500, pl=30, pr=80) # Force non-symmetry
        >>> e1.left2Center() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.left2CenterSides()
        >>> e2.x, 500/2
        (250pt, 250.0)
        >>> e2.xAlign = CENTER
        >>> success = e2.left2CenterSides()
        >>> e2.x, 500/2 + 120/2
        (310pt, 310.0)
        >>> e2.xAlign = RIGHT
        >>> success = e2.left2CenterSides()
        >>> e2.x, 500/2 + 120
        (370pt, 370.0)
        """
        if self.parent is None:
            return False
        self.mLeft = self.parent.w/2
        return True

    def left2Left(self):
        """Move left of self to padding left position of parent.
        The position of e2 element origin depends on the horizontal
        alignment type.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import RIGHT, CENTER, LEFT
        >>> e1 = Element(w=500, pl=50)
        >>> e1.left2Left() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.left2Left()
        >>> e2.x
        50pt
        >>> e2.xAlign = CENTER
        >>> success = e2.left2Left()
        >>> e2.x
        110pt
        >>> e2.xAlign = RIGHT
        >>> success = e2.left2Left()
        >>> e2.x
        170pt
        """
        if self.parent is None:
            return False
        self.mLeft = self.parent.pl # Padding left
        return True

    def left2SideLeft(self):
        """Move left of self to left position of parent.
        The position of e2 element origin depends on the horizontal
        alignment type.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import RIGHT, CENTER, LEFT
        >>> e1 = Element(w=500, pl=50)
        >>> e1.left2SideLeft() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.left2SideLeft()
        >>> e2.x
        0pt
        >>> e2.xAlign = CENTER
        >>> success = e2.left2SideLeft()
        >>> e2.x
        60pt
        >>> e2.xAlign = RIGHT
        >>> success = e2.left2SideLeft()
        >>> e2.x
        120pt
        """
        if self.parent is None:
            return False
        self.mLeft = 0
        return True

    def left2BleedLeft(self):
        """Move left of self to left bleed position of parent.
        The position of e2 element origin depends on the horizontal
        alignment type.
        """
        if self.parent is None:
            return False
        self.mLeft = -self.bleedLeft
        return True

    def left2Right(self):
        """Move left of self to padding right position of parent.
        The position of e2 element origin depends on the horizontal
        alignment type.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import RIGHT, CENTER, LEFT
        >>> e1 = Element(w=500, padding=50)
        >>> e1.left2Right() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=RIGHT)
        >>> success = e2.left2Right()
        >>> e2.x
        570pt
        >>> e2.xAlign = CENTER
        >>> success = e2.left2Right()
        >>> e2.x
        510pt
        >>> e2.xAlign = LEFT
        >>> success = e2.left2Right()
        >>> e2.x
        450pt
        """
        if self.parent is None:
            return False
        self.mLeft = self.parent.w - self.parent.pr
        return True

    def left2SideRight(self):
        """Move left of self to full width (right position) of parent.
        The position of e2 element origin depends on the horizontal
        alignment type.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import RIGHT, CENTER, LEFT
        >>> e1 = Element(w=500, padding=50)
        >>> e1.left2SideRight() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=RIGHT)
        >>> success = e2.left2SideRight()
        >>> e2.x
        620pt
        >>> e2.xAlign = CENTER
        >>> success = e2.left2SideRight()
        >>> e2.x
        560pt
        >>> e2.xAlign = LEFT
        >>> success = e2.left2SideRight()
        >>> e2.x
        500pt
        """
        if self.parent is None:
            return False
        self.mLeft = self.parent.w
        return True

    def right2Center(self):
        """Position the right side centered on the padding of the parent.
        Note that this different from self.right2Center if the left
        and right padding of parent is not identical.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import LEFT, CENTER, RIGHT
        >>> e1 = Element(w=500, pl=30, pr=80) # Force non-symmetric padding
        >>> e1.right2Center() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.right2Center()
        >>> e2.x, e1.pl, e1.pw/2, 30 + (500 - 30 - 80)/2 - 120
        (105pt, 30pt, 195pt, 105.0)
        >>> e2.xAlign = CENTER
        >>> success = e2.right2Center()
        >>> e2.x, 30 + (500 - 30 - 80)/2 - 120/2
        (165pt, 165.0)
        >>> e2.xAlign = RIGHT
        >>> success = e2.right2Center()
        >>> e2.x, 30 + (500 - 30 - 80)/2
        (225pt, 225.0)
        """
        if self.parent is None:
            return False
        self.mRight = self.parent.pl + self.parent.pw/2
        return True

    def right2CenterSides(self):
        """Position the right side centered on the sides of the parent.
        Note that this different from self.right2Center if the left
        and right padding of parent is not identical.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import LEFT, CENTER, RIGHT
        >>> e1 = Element(w=500, pl=30, pr=80) # Force non-symmetric padding
        >>> e1.right2CenterSides() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.right2CenterSides()
        >>> e2.x # 500/2 - 120
        130pt
        >>> e2.xAlign = CENTER
        >>> success = e2.right2CenterSides()
        >>> e2.x # 500/2 - 120/2
        190pt
        >>> e2.xAlign = RIGHT
        >>> success = e2.right2CenterSides()
        >>> e2.x # 500/2
        250pt
        """
        if self.parent is None:
            return False
        self.mRight = self.parent.w/2
        return True

    def right2Left(self):
        """Move right of self to padding left position of parent.
        The position of e2 element origin depends on the horizontal
        alignment type.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import LEFT, CENTER, RIGHT
        >>> e1 = Element(w=500, padding=50)
        >>> e1.right2Left() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.right2Left()
        >>> e2.x # 50 - 120
        -70pt
        >>> e2.xAlign = CENTER
        >>> success = e2.right2Left()
        >>> e2.x # 50 - 120/2
        -10pt
        >>> e2.xAlign = RIGHT
        >>> success = e2.right2Left()
        >>> e2.x
        50pt
        """
        if self.parent is None:
            return False
        self.mRight = self.parent.pl # Padding left
        return True

    def right2SideLeft(self):
        """Move right of self to left position of parent. The position of e2
        element origin depends on the horizontal alignment type.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import LEFT, CENTER, RIGHT
        >>> e1 = Element(w=500, padding=50)
        >>> e1.right2SideLeft() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.right2SideLeft()
        >>> e2.x
        -120pt
        >>> e2.xAlign = CENTER
        >>> success = e2.right2SideLeft()
        >>> e2.x, -120/2
        (-60pt, -60.0)
        >>> e2.xAlign = RIGHT
        >>> success = e2.right2SideLeft()
        >>> e2.x
        0pt
        """
        if self.parent is None:
            return False
        self.mRight = 0 # Left side of parent position
        return True

    def right2Right(self):
        """Move right of self to padding right position of parent.
        The position of e2 element origin depends on the horizontal
        alignment type.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import LEFT, CENTER, RIGHT
        >>> e1 = Element(w=500, pl=30, pr=80)
        >>> e1.right2Right() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.right2Right()
        >>> e2.x, 500 - 80 - 120
        (300pt, 300)
        >>> e2.xAlign = CENTER
        >>> success = e2.right2Right()
        >>> e2.x, 500 - 80 - 120/2
        (360pt, 360.0)
        >>> e2.xAlign = RIGHT
        >>> success = e2.right2Right()
        >>> e2.x, 500 - 80
        (420pt, 420)
        """
        if self.parent is None:
            return False
        self.mRight = self.parent.w - self.parent.pr
        return True

    def right2SideRight(self):
        """Move right of self to right width position of parent.
        The position of e2 element origin depends on the horizontal
        alignment type.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import LEFT, CENTER, RIGHT
        >>> e1 = Element(w=500, padding=50)
        >>> e1.right2SideRight() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.right2SideRight()
        >>> e2.x, 500 - 120
        (380pt, 380)
        >>> e2.xAlign = CENTER
        >>> success = e2.right2SideRight()
        >>> e2.x, 500 - 120/2
        (440pt, 440.0)
        >>> e2.xAlign = RIGHT
        >>> success = e2.right2SideRight()
        >>> e2.x
        500pt
        """
        if self.parent is None:
            return False
        self.mRight = self.parent.w
        return True

    def right2BleedRight(self):
        """Move right of self to right bleed width position of parent. The
        position of e2 element origin depends on the horizontal alignment
        type."""
        if self.parent is None:
            return False
        self.mRight = self.parent.w + self.bleedRight
        return True

    def origin2Center(self):
        """Move origin of the element to the padding center of the parent.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import LEFT
        >>> e1 = Element(w=500, pl=30, pr=80)
        >>> e1.origin2Center() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.origin2Center()
        >>> e2.x, 30 + (500 - 30 - 80)/2
        (225pt, 225.0)
        """
        if self.parent is None:
            return False
        self.x = self.parent.pl + self.parent.pw/2
        return True

    def origin2CenterSides(self):
        """Move origin of the element to the sides center of the parent.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import LEFT
        >>> e1 = Element(w=500, pl=30, pr=80)
        >>> e1.origin2CenterSides() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.origin2CenterSides()
        >>> e2.x, 500/2
        (250pt, 250.0)
        """
        if self.parent is None:
            return False
        self.x = self.parent.w/2
        return True

    def origin2Left(self):
        """Move origin of the element to the padding left of the parent.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import LEFT
        >>> e1 = Element(w=500, pl=30, pr=80)
        >>> e1.origin2Left() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.origin2Left()
        >>> e2.x, 30
        (30pt, 30)
        """
        if self.parent is None:
            return False
        self.x = self.parent.pl # Padding left
        return True

    def origin2SideLeft(self):
        """Move origin of the element to the left side of the parent.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import LEFT
        >>> e1 = Element(w=500, pl=30, pr=80)
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.origin2SideLeft()
        >>> e2.x
        0pt
        """
        self.x = 0
        return True

    def origin2Right(self):
        """Move origin of the element to the right padding of the parent.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import LEFT
        >>> e1 = Element(w=500, pl=30, pr=80)
        >>> e1.origin2Right() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.origin2Right()
        >>> e2.x, 500 - 80
        (420pt, 420)
        """
        if self.parent is None:
            return False
        self.x = self.parent.w - self.parent.pr
        return True

    def origin2SideRight(self):
        """Move origin of the element to the right padding of the parent.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import LEFT
        >>> e1 = Element(w=500, pl=30, pr=80)
        >>> e1.origin2SideRight() # Element without parent answers False
        False
        >>> e2 = Element(w=120, parent=e1, xAlign=LEFT)
        >>> success = e2.origin2SideRight()
        >>> e2.x, 500
        (500pt, 500)
        """
        if self.parent is None:
            return False
        self.x = self.parent.w
        return True


    #   Vertical alignments

    def bottom2Bottom(self):
        """Move bottom of the element to the bottom of the parent block.
        The position of e2 element origin depends on the vertical
        alignment type.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import TOP, MIDDLE, BOTTOM
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.bottom2Bottom() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.bottom2Bottom()
        >>> e2.y, 80 + 120
        (200pt, 200)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.bottom2Bottom()
        >>> e2.y, 80 + 120/2, e1.pb + e2.h/2
        (140pt, 140.0, 140pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.bottom2Bottom()
        >>> e2.y, 80
        (80pt, 80)
        """

        """
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.bottom2Bottom() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.bottom2Bottom()
        >>> e2.y, 500 - 80 - 120
        (300pt, 300)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.bottom2Bottom()
        >>> e2.y, 500 - 80 - 120/2, e1.h - e1.pb - e2.h/2
        (360pt, 360.0, 360pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.bottom2Bottom()
        >>> e2.y, 500 - 80
        (420pt, 420)
        """
        if self.parent is None:
            return False

        self.mBottom = self.parent.pb
        return True

    def bottom2SideBottom(self):
        """Move bottom of the element to the bottom side of the parent.
        The position of e2 element origin depends on the vertical
        alignment type.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import TOP, MIDDLE, BOTTOM
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> # Element without parent answers False.
        >>> e1.bottom2SideBottom()
        True
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> # Inherited property.
        >>> success = e2.bottom2SideBottom()
        >>> e2.y, 120
        (120pt, 120)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.bottom2SideBottom()
        >>> e2.y, 120/2, e2.h/2
        (60pt, 60.0, 60pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.bottom2SideBottom()
        >>> e2.y, 0
        (0pt, 0)
        """

        """
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> # Element without parent answers False.
        >>> e1.bottom2SideBottom()
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> # Inherited property.
        >>> success = e2.bottom2SideBottom()
        >>> e2.y, 500 - 120
        (380pt, 380)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.bottom2SideBottom()
        >>> e2.y, 500 - 120/2, e1.h - e2.h/2
        (440pt, 440.0, 440pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.bottom2SideBottom()
        >>> e2.y, 500
        (500pt, 500)
        """
        self.mBottom = 0
        return True

    def bottom2BleedBottom(self):
        """Move bottom of the element to the bottom side of the parent,
        overshooting by bleed. The position of e2 element origin depends on
        the vertical alignment type.
        """
        self.mBottom = -self.bleedBottom
        return True

    def bottom2Top(self):
        """Move bottom of the element to the top padding of the parent.
        The position of e2 element origin depends on the vertical
        alignment type.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import TOP, MIDDLE, BOTTOM
        >>> e1 = Element(h=500, pt=30, pb=80,)
        >>> e1.bottom2Top() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.bottom2Top()
        >>> e2.y, 500 - 30 + 120, e1.h - e1.pt + e2.h
        (590pt, 590, 590pt)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.bottom2Top()
        >>> e2.y, 500 - 30 + 120/2, e1.h - e1.pt + e2.h/2
        (530pt, 530.0, 530pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.bottom2Top()
        >>> e2.y, 500 - 30, e1.h - e1.pt
        (470pt, 470, 470pt)
        """

        """
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.bottom2Top() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.bottom2Top()
        >>> e2.y, 30 - 120
        (-90pt, -90)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.bottom2Top()
        >>> e2.y, 30 - 120/2
        (-30pt, -30.0)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.bottom2Top()
        >>> e2.y, 30
        (30pt, 30)
        """

        if self.parent is None:
            return False
        self.mBottom = self.parent.h - self.parent.pt
        return True

    def middle2Bottom(self):
        """Move middle of the element to the bottom padding of the parent.
        The position of e2 element origin depends on the vertical
        alignment type.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import TOP, MIDDLE, BOTTOM
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.middle2Bottom() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.middle2Bottom()
        >>> e2.y, 80 + 120/2, e1.pb + e2.h/2
        (140pt, 140.0, 140pt)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.middle2Bottom()
        >>> e2.y, 80, e1.pb
        (80pt, 80, 80pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.middle2Bottom()
        >>> e2.y, 80 - 120/2, e1.pb - e2.h/2
        (20pt, 20.0, 20pt)
        """

        """
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.middle2Bottom() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.middle2Bottom()
        >>> e2.y, 500 - 80 - 120/2
        (360pt, 360.0)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.middle2Bottom()
        >>> e2.y, 500 - 80
        (420pt, 420)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.middle2Bottom()
        >>> e2.y, 500 - 80 + 120/2
        (480pt, 480.0)
        """

        if self.parent is None:
            return False
        self.middle = self.parent.pb
        return True

    def middle2SideBottom(self):
        """Move middle of the element to the bottom side of the parent.
        The position of e2 element origin depends on the vertical
        alignment type.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import TOP, MIDDLE, BOTTOM
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.middle2SideBottom() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.middle2SideBottom()
        >>> e2.y, 120/2, e2.h/2
        (60pt, 60.0, 60pt)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.middle2SideBottom()
        >>> e2.y, 0
        (0pt, 0)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.middle2SideBottom()
        >>> e2.y, -120/2, -e2.h/2
        (-60pt, -60.0, -60pt)
        """

        """
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.middle2SideBottom() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.middle2SideBottom()
        >>> e2.y, 500 - 120/2
        (440pt, 440.0)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.middle2SideBottom()
        >>> e2.y, 500
        (500pt, 500)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.middle2SideBottom()
        >>> e2.y, 500 + 120/2
        (560pt, 560.0)
        """

        if self.parent is None:
            return False
        self.middle = 0
        return True


    def middle2Top(self):
        """Move middle of the element to the top side of the parent.
        The position of e2 element origin depends on the vertical
        alignment type.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import TOP, BOTTOM, MIDDLE
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.middle2Top() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.middle2Top()
        >>> e2.y, 500 - 30 + 120/2, e1.h - e1.pt + e2.h/2
        (530pt, 530.0, 530pt)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.middle2Top()
        >>> e2.y, 500 - 30, e1.h - e1.pt
        (470pt, 470, 470pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.middle2Top()
        >>> e2.y, 500 - 30 - 120/2, e1.h - e1.pt - e2.h/2
        (410pt, 410.0, 410pt)
        """

        """
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.middle2Top() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.middle2Top()
        >>> e2.y, 30 - 120/2
        (-30pt, -30.0)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.middle2Top()
        >>> e2.y, 30
        (30pt, 30)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.middle2Top()
        >>> e2.y, 30 + 120/2
        (90pt, 90.0)
        """

        if self.parent is None:
            return False
        self.middle = self.parent.h - self.parent.pt
        return True

    def middle2SideTop(self):
        """Move middle of the element to the top side of the parent.
        The position of e2 element origin depends on the vertical
        alignment type.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import TOP, MIDDLE, BOTTOM
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.middle2SideTop() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.middle2SideTop()
        >>> e2.y, 500 + 120/2, e1.h + e2.h/2
        (560pt, 560.0, 560pt)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.middle2SideTop()
        >>> e2.y, 500, e1.h
        (500pt, 500, 500pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.middle2SideTop()
        >>> e2.y, 500 - 120/2, e1.h - e2.h/2
        (440pt, 440.0, 440pt)
        """

        """
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.middle2SideTop() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.middle2SideTop()
        >>> e2.y, -120/2
        (-60pt, -60.0)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.middle2SideTop()
        >>> e2.y
        0pt
        >>> e2.yAlign = BOTTOM
        >>> success = e2.middle2SideTop()
        >>> e2.y, 120/2
        (60pt, 60.0)
        """

        if self.parent is None:
            return False
        self.middle = self.parent.h
        return True

    def middle2Middle(self): # Vertical center, following CSS naming.
        """Move middle of the element to the padding middle of the parent.
        The position of e2 element origin depends on the vertical
        alignment type.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import TOP, MIDDLE, BOTTOM
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.middle2Middle() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.middle2Middle()
        >>> e2.y, 80 + (500 - 30 - 80)/2 + 120/2, e1.pb + (e1.h - e1.pb - e1.pt)/2 + e2.h/2
        (335pt, 335.0, 335pt)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.middle2Middle()
        >>> e2.y, 80 + (500 - 30 - 80)/2, e1.pb + (e1.h - e1.pb - e1.pt)/2
        (275pt, 275.0, 275pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.middle2Middle()
        >>> e2.y, 80 + (500 - 30 - 80)/2 - 120/2, e1.pb + (e1.h - e1.pb - e1.pt)/2 - e2.h/2
        (215pt, 215.0, 215pt)
        """

        """
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.middle2Middle() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.middle2Middle()
        >>> e2.y, 30 + (500 - 30 - 80)/2 - 120/2
        (165pt, 165.0)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.middle2Middle()
        >>> e2.y, 30 + (500 - 30 - 80)/2
        (225pt, 225.0)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.middle2Middle()
        >>> e2.y, 30 + (500 - 30 - 80)/2 + 120/2
        (285pt, 285.0)
        """

        if self.parent is None:
            return False
        self.middle = self.parent.pb + self.parent.ph/2
        return True

    def middle2MiddleSides(self):
        """Move middle of the element to the sides middle of the parent.
        The position of e2 element origin depends on the vertical
        alignment type.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import TOP, MIDDLE, BOTTOM
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.middle2MiddleSides() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.middle2MiddleSides()
        >>> e2.y, 500/2 + 120/2, e1.h/2 + e2.h/2
        (310pt, 310.0, 310pt)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.middle2MiddleSides()
        >>> e2.y, 500/2, e1.h/2
        (250pt, 250.0, 250pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.middle2MiddleSides()
        >>> e2.y, 500/2 - 120/2, e1.h/2 - e2.h/2
        (190pt, 190.0, 190pt)
        """

        """
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.middle2MiddleSides() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.middle2MiddleSides()
        >>> e2.y, 500/2 - 120/2
        (190pt, 190.0)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.middle2MiddleSides()
        >>> e2.y, 500/2
        (250pt, 250.0)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.middle2MiddleSides()
        >>> e2.y, 500/2 + 120/2
        (310pt, 310.0)
        """

        if self.parent is None:
            return False
        self.middle = self.parent.h/2
        return True


    def top2Middle(self):
        """Move top of the element to the padding middle of the parent.
        The position of e2 element origin depends on the vertical
        alignment type.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import BOTTOM, TOP, MIDDLE
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.top2Middle() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.top2Middle()
        >>> e2.y, 80 + (500 - 30 - 80)/2, e1.pb + (e1.h - e1.pb - e1.pt)/2
        (275pt, 275.0, 275pt)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.top2Middle()
        >>> e2.y, 80 + (500 - 30 - 80)/2 - 120/2, e1.pb + (e1.h - e1.pb - e1.pt)/2 - e2.h/2
        (215pt, 215.0, 215pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.top2Middle()
        >>> e2.y, 80 + (500 - 30 - 80)/2 - 120, e1.pb + (e1.h - e1.pb - e1.pt)/2 - e2.h
        (155pt, 155.0, 155pt)
        """

        """
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.top2Middle() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.top2Middle()
        >>> e2.y, 30 + (500 - 30 - 80)/2
        (225pt, 225.0)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.top2Middle()
        >>> e2.y, 30 + (500 - 30 - 80)/2 + 120/2
        (285pt, 285.0)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.top2Middle()
        >>> e2.y, 30 + (500 - 30 - 80)/2 + 120
        (345pt, 345.0)
        """

        if self.parent is None:
            return False
        self.mTop = self.parent.pb + self.parent.ph/2
        return True

    def top2MiddleSides(self):
        """Move top of the element to the middle between sides of the parent.
        The position of e2 element origin depends on the vertical alignment
        type.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import BOTTOM, TOP, MIDDLE
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.top2MiddleSides() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.top2MiddleSides()
        >>> e2.y, 500/2
        (250pt, 250.0)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.top2MiddleSides()
        >>> e2.y, 500/2 - 120/2, e1.h/2 - e2.h/2
        (190pt, 190.0, 190pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.top2MiddleSides()
        >>> e2.y, 500/2 - 120, e1.h/2 - e2.h
        (130pt, 130.0, 130pt)
        """
        """
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.top2MiddleSides() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.top2MiddleSides()
        >>> e2.y, 500/2
        (250pt, 250.0)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.top2MiddleSides()
        >>> e2.y, 500/2 + 120/2
        (310pt, 310.0)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.top2MiddleSides()
        >>> e2.y, 500/2 + 120
        (370pt, 370.0)
        """

        if self.parent is None:
            return False
        self.mTop = self.parent.h/2
        return True

    def origin2Bottom(self):
        """Move origin of the element to the padding bottom of the parent.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import TOP, MIDDLE, BOTTOM
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.origin2Bottom() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.origin2Bottom()
        >>> e2.y, 80, e1.pb
        (80pt, 80, 80pt)
        """

        """
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.origin2Bottom() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.origin2Bottom()
        >>> e2.y, 500 - 80
        (420pt, 420)
        """

        if self.parent is None:
            return False
        self.y = self.parent.pb
        return True

    def origin2SideBottom(self):
        """Move origin of the element to the padding bottom of the parent.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import TOP
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.origin2SideBottom() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.origin2SideBottom()
        >>> e2.y, 0
        (0pt, 0)
        """

        """
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.origin2SideBottom() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.origin2SideBottom()
        >>> e2.y
        500pt
        """

        if self.parent is None:
            return False
        self.y = 0
        return True

    def origin2Top(self):
        """Move origin of the element to the top padding of the parent.
        """

        """
        >>> from pagebot.elements.element import Element
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.origin2Top() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1)
        >>> success = e2.origin2Top()
        >>> e2.y, 30
        (30pt, 30)

        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.origin2Top() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1)
        >>> success = e2.origin2Top()
        >>> e2.y, 30
        (30pt, 30)

        """
        if self.parent is None:
            return False
        self.y = self.parent.h - self.parent.pt
        return True

    def origin2SideTop(self):
        """Move origin of the element to the top side of the parent.

        >>> from pagebot.elements.element import Element
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.origin2SideTop() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1)
        >>> success = e2.origin2SideTop()
        >>> e2.y, e1.h
        (500pt, 500pt)
        """

        """
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.origin2SideTop() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1)
        >>> success = e2.origin2SideTop()
        >>> e2.y
        0pt
        """

        if self.parent is None:
            return False
        self.y = self.parent.h
        return True

    def origin2Middle(self):
        """Move origin of the element to the top side of the parent.

        >>> from pagebot.elements.element import Element
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.origin2Middle() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1)
        >>> success = e2.origin2Middle()
        >>> e2.y, 80 + (500 - 30 - 80)/2
        (275pt, 275.0)
        """

        """
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.origin2Middle() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1)
        >>> success = e2.origin2Middle()
        >>> e2.y, 30 + (500 - 30 - 80)/2
        (225pt, 225.0)
        """

        if self.parent is None:
            return False
        self.y = self.parent.pb + self.parent.ph/2
        return True

    def origin2MiddleSides(self):
        """Move origin of the element to the sides middle of the parent.

        >>> from pagebot.elements.element import Element
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.origin2MiddleSides() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1)
        >>> success = e2.origin2MiddleSides()
        >>> e2.y, 500/2
        (250pt, 250.0)

        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.origin2MiddleSides() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1)
        >>> success = e2.origin2MiddleSides()
        >>> e2.y, 500/2
        (250pt, 250.0)
        """
        if self.parent is None:
            return False
        self.y = self.parent.h/2
        return True

    def bottom2Middle(self):
        """Move margin bottom of the element to the padding middle of the parent.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import TOP, MIDDLE, BOTTOM
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.bottom2Middle() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.bottom2Middle()
        >>> e2.y, 80 + (500 - 30 - 80)/2 + 120, e1.pb + (e1.h - e1.pb - e1.pt)/2 + e2.h
        (395pt, 395.0, 395pt)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.bottom2Middle()
        >>> e2.y, 80 + (500 - 30 - 80)/2 + 120/2, e1.pb + (e1.h - e1.pb - e1.pt)/2 + e2.h/2
        (335pt, 335.0, 335pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.bottom2Middle()
        >>> e2.y, 80 + (500 - 30 - 80)/2, e1.pb + (e1.h - e1.pb - e1.pt)/2
        (275pt, 275.0, 275pt)
        """

        """
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.bottom2Middle() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.bottom2Middle()
        >>> e2.y, 30 + (500 - 30 - 80)/2 - 120
        (105pt, 105.0)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.bottom2Middle()
        >>> e2.y, 30 + (500 - 30 - 80)/2 - 120/2
        (165pt, 165.0)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.bottom2Middle()
        >>> e2.y, 30 + (500 - 30 - 80)/2
        (225pt, 225.0)
        """

        if self.parent is None:
            return False
        self.mBottom = self.parent.pb + self.parent.ph/2
        return True

    def bottom2MiddleSides(self):
        """Move margin bottom of the element to the sides middle of the parent.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import TOP, MIDDLE, BOTTOM
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.bottom2MiddleSides() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.bottom2MiddleSides()
        >>> e2.y, 500/2 + 120, e1.h/2 + e2.h
        (370pt, 370.0, 370pt)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.bottom2MiddleSides()
        >>> e2.y, 500/2 + 120/2, e1.h/2 + e2.h/2
        (310pt, 310.0, 310pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.bottom2MiddleSides()
        >>> e2.y, 500/2, e1.h/2
        (250pt, 250.0, 250pt)
        """

        """
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.bottom2MiddleSides() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.bottom2MiddleSides()
        >>> e2.y, 500/2 - 120
        (130pt, 130.0)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.bottom2MiddleSides()
        >>> e2.y, 500/2 - 120/2
        (190pt, 190.0)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.bottom2MiddleSides()
        >>> e2.y, 500/2
        (250pt, 250.0)
        """

        if self.parent is None:
            return False
        self.mBottom = self.parent.h/2
        return True

    def top2Bottom(self):
        """Move margin top of the element to the padding bottom of the parent.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import BOTTOM, TOP, MIDDLE
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.top2Bottom() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.top2Bottom()
        >>> e2.y, 80, e1.pb
        (80pt, 80, 80pt)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.top2Bottom()
        >>> e2.y, 80 - 120/2, e1.pb - e2.h/2
        (20pt, 20.0, 20pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.top2Bottom()
        >>> e2.y, 80 - 120, e1.pb - e2.h
        (-40pt, -40, -40pt)
        """

        """
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.top2Bottom() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.top2Bottom()
        >>> e2.y, 500 - 80
        (420pt, 420)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.top2Bottom()
        >>> e2.y, 500 - 80 + 120/2
        (480pt, 480.0)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.top2Bottom()
        >>> e2.y, 500 - 80 + 120
        (540pt, 540)
        """

        if self.parent is None:
            return False
        self.mTop = self.parent.pb
        return True

    def top2Top(self):
        """Move margin top of the element to the padding top of the parent.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import BOTTOM, TOP, MIDDLE
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.top2Top() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.top2Top()
        >>> e2.y, 500 - 30, e1.h - e1.pt
        (470pt, 470, 470pt)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.top2Top()
        >>> e2.y, 500 - 30 - 120/2, e1.h - e1.pt - e2.h/2
        (410pt, 410.0, 410pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.top2Top()
        >>> e2.y, 500 - 30 - 120, e1.h - e1.pt - e2.h
        (350pt, 350, 350pt)
        """

        """
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.top2Top() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.top2Top()
        >>> e2.y, 30
        (30pt, 30)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.top2Top()
        >>> e2.y, 30 + 120/2
        (90pt, 90.0)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.top2Top()
        >>> e2.y, 30 + 120
        (150pt, 150)
        """

        if self.parent is None:
            return False
        self.mTop = self.parent.h - self.parent.pt
        return True

    def top2SideTop(self):
        """Move margin top of the element to the top side of the parent.

        >>> from pagebot.elements.element import Element
        >>> from pagebot.constants import BOTTOM, TOP, MIDDLE
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.top2SideTop() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.top2SideTop()
        >>> e2.y, 500, e1.h
        (500pt, 500, 500pt)
        >>> e2.yAlign = MIDDLE
        >>> success = e2.top2SideTop()
        >>> e2.y, 500 - 120/2, e1.h - e2.h/2
        (440pt, 440.0, 440pt)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.top2SideTop()
        >>> e2.y, 500 - 120, e1.h - e2.h
        (380pt, 380, 380pt)
        """
        """
        >>> e1 = Element(h=500, pt=30, pb=80)
        >>> e1.top2SideTop() # Element without parent answers False
        False
        >>> e2 = Element(h=120, parent=e1, yAlign=TOP)
        >>> success = e2.top2SideTop()
        >>> e2.y
        0pt
        >>> e2.yAlign = MIDDLE
        >>> success = e2.top2SideTop()
        >>> e2.y, 120/2
        (60pt, 60.0)
        >>> e2.yAlign = BOTTOM
        >>> success = e2.top2SideTop()
        >>> e2.y, 120
        (120pt, 120)
        """

        if self.parent is None:
            return False
        self.mTop = self.parent.h
        return True

    def top2BleedTop(self):
        """Move margin top of the element to the top side of the parent, overshooting
        by bleed."""
        if self.parent is None:
            return False
        self.mTop = self.parent.h + self.bleedTop
        return True

    # Floating parent padding

    def float2Top(self):
        """Float the element upward, until top hits the parent top padding or
        "hooks" into another element at the same z-layer position. Include
        margin to decide if it fits."""
        self.mTop = min(self.getFloatSideTop(), self.parent.h - self.parent.pt)
        return True

    def float2Bottom(self):
        self.mBottom = min(self.getFloatSideBottom(), self.parent.pb)
        return True

    def float2Left(self):
        self.mLeft = max(self.getFloatSideLeft(), self.parent.pl) # padding left
        return True

    def float2Right(self):
        self.mRight = min(self.getFloatSideRight(), self.parent.w - self.parent.pr)
        return True

    # Floating to parent sides, go as far as there are no other elements in the
    # same z-layer

    def float2SideTop(self):
        self.mTop = self.getFloatSideTop()
        return True

    def float2SideBottom(self):
        """Float margin bottom to bottom side."""
        self.mBottom = self.getFloatSideBottom()
        return True

    def float2SideLeft(self):
        """Float margin left to left side."""
        self.mLeft = self.getFloatSideLeft()
        return True

    def float2SideRight(self):
        """Float margin right to right side."""
        self.mRight = self.getFloatSideRight()
        return True

    # With fitting (and shrinking) we need to change the actual size of the
    # element. This can have implications on it's content, and we need to take
    # the min/max sizes into conderantion: setting the self.w and self.h to a
    # value, does not mean that the size really got that value, if exceeding a
    # min/max limit.

    def fit2Bottom(self):
        self.h = self.mTop - self.parent.pb
        self.mBottom = self.parent.pb
        return True

    def fit2SideBottom(self):
        top = self.mTop
        self.mBottom = 0
        self.h = top
        return True

    def fit2BleedBottom(self):
        top = self.mTop
        self.mBottom = -self.bleedBottom
        self.h = top + self.bleedBottom
        return True

    def fit2Left(self):
        """Fit to left, inlcuding margin left and margin right."""
        right = self.mRight
        self.mLeft = self.parent.pl # Padding left
        self.w += right - self.mRight
        return True

    def fit2SideLeft(self):
        """Fit to left, including margin left and margin right."""
        right = self.mRight
        self.mLeft = 0
        self.w += right - self.mRight
        return True

    def fit2Right(self):
        """Make the right side of self fit the right padding of the parent,
        without moving the left position. Text implements it's own method
        to make the text fit by adjusting the size.

        >>> from pagebot.elements.element import Element
        >>> e1 = Element(x=100, y=20, w=100, h=50)
        >>> e2 = Element(w=300, h=300, elements=[e1], padding=10)
        >>> e1.x, e1.y, e1.w, e1.h # Default position and size
        (100pt, 20pt, 100pt, 50pt)
        >>> success = e1.fit2Right()
        >>> e1.x, e1.y, e1.w, e1.h # Position and size, solved by position, fitting parent on padding
        (100pt, 20pt, 190pt, 50pt)
        >>>
        """
        self.w = self.parent.w - self.parent.pr - self.x
        return True

    def scale2Right(self):
        """Make the right side of self fit the right padding of the parent,
        without moving the left position. The scale the height according to the
        original ratio.

        >>> from pagebot.elements.element import Element
        >>> e1 = Element(x=100, y=20, w=100, h=50)
        >>> e2 = Element(w=300, h=300, elements=[e1], padding=10)
        >>> e1.x, e1.y, e1.w, e1.h # Default position and size
        (100pt, 20pt, 100pt, 50pt)
        >>> success = e1.scale2Right()
        >>> e1.x, e1.y, e1.w, e1.h # Position and size, solved by position, fitting parent on padding
        (100pt, 20pt, 190pt, 95pt)
        >>>
        """
        orgW = self.w
        if orgW:
            self.w = self.parent.w - self.parent.pr - self.x
            self.h = self.h * self.w.pt / orgW.pt
            return True
        return False # No original width, cannot calculate due to zero division.

    def fit2SideRight(self):
        """Make the right side of self fit the right side of the parent,
        without moving the left position.

        >>> from pagebot.elements.element import Element
        >>> e1 = Element(x=100, y=20, w=100, h=50)
        >>> e2 = Element(w=300, h=300, elements=[e1], padding=10)
        >>> e1.x, e1.y, e1.w, e1.h # Default position and size
        (100pt, 20pt, 100pt, 50pt)
        >>> success = e1.fit2SideRight()
        >>> e1.x, e1.y, e1.w, e1.h # Position and size, solved by position, fitting parent on padding
        (100pt, 20pt, 200pt, 50pt)
        >>>
        """
        self.w = self.parent.w - self.x
        return True

    def fit2BleedRight(self):
        """Make the right side of self fit the right bleed side of the parent,
        without moving the left position."""
        self.w = self.parent.w - self.x + self.bleedRight
        return True

    def fit2Top(self):
        """Make the top side of self fit the top padding of the parent, without
        moving the bottom position.

        >>> from pagebot.elements.element import Element
        >>> e1 = Element(x=100, y=20, w=100, h=50)
        >>> e2 = Element(w=300, h=300, elements=[e1], padding=10)
        >>> e1.x, e1.y, e1.w, e1.h # Default position and size
        (100pt, 20pt, 100pt, 50pt)
        >>> success = e1.fit2Top()
        >>> e1.x, e1.y, e1.w, e1.h # Position and size, solved by position, fitting parent on padding
        (100pt, 20pt, 100pt, 270pt)
        """
        self.h += self.parent.h - self.parent.pt - self.mTop
        return True

    def fit2SideTop(self):
        self.h += self.parent.h - self.mTop
        return True

    def fit2BleedTop(self):
        self.h += self.parent.h - self.mTop + self.bleedTop
        return True

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
