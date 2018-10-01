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
#     pointcontext.py
#
#     Naming of "context" here has not relation with DrawBotContext/FlexContext.
#     It is glyph contour pints with its +3 and -3 neighbors, combined into one point.
#     This way users can easily see the progression of lines through a points and
#     test on vertical/horizontal directions.
#     The 7 contained points can be of type point2D (x,y)-tuple, or APoint instances.
#
import math
from pagebot.toolbox.mathematics import *
from pagebot.fonttoolbox.analyzers.apoint import APoint

def calculateAngle(p1, p2, inDegrees=True):
    """Calculate the angle between points p1 and p2. Points can be either 2D or 3D
    point tuples or Point instances. In the case of Point3D, only the 2D projection
    in (x, y) plane is calculated."""
    xDiff = p2[0] - p1[0]
    yDiff = p2[1] - p1[1]
    angle = math.atan2(yDiff, xDiff)
    if inDegrees:
        angle = math.degrees(angle)
    return angle

def angleOfLines(p1, p2, q1, q2, inDegrees=True):
    """Answers the angle difference (radials or default degrees) between p1-->p2 and q1-->q2.
    Points can be either 2D or 3D point tuples or Point instances.
    In the case of Point3D, only the 2D projection in (x, y) plane is calculated."""
    angle1 = calculateAngle(p1, p2, inDegrees)
    angle2 = calculateAngle(q1, q2, inDegrees)
    angle = angle2 - angle1
    if angle < -180: angle += 360
    elif angle > 180: angle -= 360
    return angle

class APointContext:
    """The PointContext instance is a Point wrapper, that also takes the 3 points previous
    and next 3 points on the contour. The instance behaves like a normal point p, but
    additional information is available as interpreted from the point context in relation
    to the neighbor points. The total of 7 points is derived
    from the average construction of a serif, so it is possible to hold (and interpret) an
    entire serif sequence inside one point context.
    """
    PARALLEL_TOLERANCE = 2 # Difference tolerance angle in degrees to take point contexts as parallel

    def __init__(self, points, index=None, contourIndex=None, clockwise=None, glyphName=None):
        """Points list is supposed to contain Point instances, not point lists.
        We need the extra storage, e.g. for point type that Point holds."""
        assert len(points) == 7
        self.p_3, self.p_2, self.p_1, self.p, self.p1, self.p2, self.p3 = points
        self.contourIndex = contourIndex
        self.index = index
        #self.clockwise = clockwise # TODO: Add clockwise attribute from caller.
        self.glyphName = glyphName
        self._direction = None  # Cache direction once calculated.
        self._angle = None  # Cache axis once calculated.

    def __getitem__(self, index):
        return self.p[index]

    def __lt__(self, p):
        u"""Compare the points.

        >>> o = APoint((0, 0))
        >>> pc1 = APointContext((o, o, o, APoint((100, 200)), o, o, o))
        >>> pc2 = APointContext((o, o, o, APoint((200, 200)), o, o, o))
        >>> pc3 = APointContext((o, o, o, APoint((200, 200)), o, o, o))
        >>> pc1 < pc2
        True
        >>> pc2 < pc3
        False
        """
        return self.p < p.p

    def __le__(self, p):
        u"""Compare the points.

        >>> o = APoint((0, 0))
        >>> pc1 = APointContext((o, o, o, APoint((100, 200)), o, o, o))
        >>> pc2 = APointContext((o, o, o, APoint((200, 200)), o, o, o))
        >>> pc3 = APointContext((o, o, o, APoint((200, 199)), o, o, o))
        >>> pc1 < pc2
        True
        >>> pc2 <= pc3
        False
        """
        return self.p <= p.p

    def __gt__(self, p):
        u"""Compare the points.

        >>> o = APoint((0, 0))
        >>> pc1 = APointContext((o, o, o, APoint((100, 200)), o, o, o))
        >>> pc2 = APointContext((o, o, o, APoint((200, 200)), o, o, o))
        >>> pc3 = APointContext((o, o, o, APoint((200, 199)), o, o, o))
        >>> pc1 > pc2
        False
        >>> pc2 > pc3
        True
        """
        return self.p > p.p

    def __ge__(self, p):
        u"""Compare the points.

        >>> o = APoint((0, 0))
        >>> pc1 = APointContext((o, o, o, APoint((100, 200)), o, o, o))
        >>> pc2 = APointContext((o, o, o, APoint((200, 200)), o, o, o))
        >>> pc3 = APointContext((o, o, o, APoint((200, 199)), o, o, o))
        >>> pc1 >= pc2
        False
        >>> pc2 >= pc3
        True
        """
        return self.p >= p.p

    def __sub__(self, p):
        u"""Subtract the points. Result is a point3D tuple.

        >>> APoint((200, 500)) - APoint((100, 300))
        (100, 200, 0)
        >>> APoint((200, 500, 10)) - APoint((100, 300))
        (100, 200, 10)
        >>> APoint((200, 500, 10)) - APoint((-100, -300, -100))
        (300, 800, 110)
        """
        return self.p[0] - p[0], self.p[1] - p[1], self.p[2] - p[2]

    def __add__(self, p):
        u"""Add the points. Result is a point3D tuple.

        >>> APoint((200, 500)) + APoint((100, 300))
        (300, 800, 0)
        >>> APoint((200, 500, 10)) + APoint((100, 300))
        (300, 800, 10)
        >>> APoint((200, 500, 10)) + APoint((-100, -300, -100))
        (100, 200, -90)
        """
        return self.p[0] + p[0], self.p[1] + p[1], self.p[2] + p[2]

    def __mul__(self, v):
        u"""Multiple the point with a scalar. Result is a point3D tuple.

        >>> APoint((200, 500)) * 2
        (400, 1000, 0)
        >>> APoint((200, 500, 10)) * 2
        (400, 1000, 20)
        """
        assert isinstance(v, (int, float))
        return self.p[0] * v, self.p[1] * v, self.p[2] * v

    def __div__(self, v):
        u"""Divide the point by a scalar. Result is a point3D tuple.

        >>> APoint((200, 500)) / 2
        (100, 250, 0)
        >>> APoint((200, 500, 10)) / 2
        (100, 250, 5)
        """
        assert isinstance(v, (int, float))
        return self.p[0] / v, self.p[1] / v, self.p[2] / v


    def _get_x(self):
        return self.p.x
    x = property(_get_x)

    def _get_y(self):
        return self.p.y
    y = property(_get_y)

    def _get_rx(self):
        # Get rounded value.
        return int(round(self.x))
    rx = property(_get_x)

    def _get_ry(self):
        # Get rounded value
        return int(round(self.y))
    ry = property(_get_ry)

    # self.angle    Answer angle of the point context
    def _get_angle(self):
        if self._angle is None:
            xDiff = self.p1[0] - self.p[0]
            yDiff = self.p1[1] - self.p[1]
            self._angle = round(math.atan2(yDiff, xDiff) * 180 / math.pi, 3)
        return self._angle
    angle = property(_get_angle)

    # self.normalizedAngle    Answer the normalized angle of self, -90 <= angle <= 90
    def _get_normalizedAngle(self):
        angle = self.angle
        while angle < 0:
            angle += 180
        while angle > 360:
            angle -= 180
        return angle
    normalizedAngle = property(_get_normalizedAngle)

    def __repr__(self):
        s = 'pc'
        if self.index is not None:
            s += '[index:%s]' % self.index
        s += '(%s,%s)' % (self.p[0], self.p[1])
        if self.isNextVertical():
            s += ' vertical'
        elif self.isNextHorizontal():
            s += ' horizontal'
        if self.isRoundStemExtreme():
            s += ' roundstem'
        elif self.isRoundBarExtreme():
            s += ' roundbar'
        if self.isTerminal():
            s += ' terminal'
        # TODO: Add clocksize info at initialization
        #if self.clockwise:
        #    s += ' c%d CW' % self.contourIndex
        #else:
        #    s += ' c%s CCW' % self.contourIndex
        if self.glyphName is not None:
            s += ' (%s)' % self.glyphName
        return s

    def isOffCurve(self, p=None):
        if p is None:
            p = self.p
        if isinstance(p, APoint):
            return not p.onCurve
        return False # Point2D type is always on-curve by definition.

    def isOnCurve(self, p=None):
        if p is None:
            p = self.p
        if isinstance(p, APoint):
            return p.onCurve
        return True # Point2D type is always on-curve by definition.

    def isUp(self):
        return self.p[1] < self.p1[1]

    def isDown(self):
        return self.p[1] > self.p1[1]

    def isLeft(self):
        return self.p[0] < self.p1[0]

    def isRight(self):
        return self.p[0] > self.p1[0]

    def isHorizontalExtreme(self, tolerance=0):
        """
        The <code>isHorizontalExtreme</code> method answers if the point context is an extreme
        (such as the side of an O).
        """
        # Is the point context a vertical and extreme in x-direction?
        # @@@ Also test on non-inflection point.
        return self.isNextVertical(tolerance)\
            and self.isPrevVertical(tolerance)\
            and self.isOffCurve(self.p1)\
            and self.isOffCurve(self.p_1)

    def isLeftRoundExtreme(self, tolerance=0):
        """Answers if the point context is a left round extreme.
        x/y selection by index, as these can be APoint or point2D tuple instances."""
        nextP = self.nextOnCurvePoint
        prevP = self.prevOnCurvePoint
        return nextP is not None and prevP is not None\
            and self.p[0] < (nextP[0] - tolerance)\
            and self.p[0] < (prevP[0] - tolerance)

    def isRightRoundExtreme(self, tolerance=0):
        """Answers if the point context is a right round extreme.
        x/y selection by index, as these can be APoint or point2D tuple instances."""
        nextP = self.nextOnCurvePoint
        prevP = self.prevOnCurvePoint
        return nextP is not None and prevP is not None\
            and self.p[0] > (nextP[0] + tolerance)\
            and self.p[0] > (prevP[0] + tolerance)

    def isTopRoundExtreme(self, tolerance=0):
        """Answers if the point context is a top round extreme.
        x/y selection by index, as these can be APoint or point2D tuple instances."""
        nextP = self.nextOnCurvePoint
        prevP = self.prevOnCurvePoint
        return nextP is not None and prevP is not None\
            and self.p[1] > (nextP[1] + tolerance)\
            and self.p[1] > (prevP[1] + tolerance)

    def isBottomRoundExtreme(self, tolerance=0):
        """Answers if the point context is a bottom round extreme.
        x/y selection by index, as these can be APoint or point2D tuple instances."""
        nextP = self.nextOnCurvePoint
        prevP = self.prevOnCurvePoint
        return nextP is not None and prevP is not None\
            and self.p[1] < (nextP[1] - tolerance)\
            and self.p[1] < (prevP[1] - tolerance)

    def isVerticalRoundExtreme(self, tolerance=0):
        """Answers if the point context is a vertical round extreme.
        x/y selection by index, as these can be APoint or point2D tuple instances."""
        return self.isTopRoundExtreme(tolerance) or self.isBottomRoundExtreme(tolerance)

    def isHorizontalRoundExtreme(self, tolerance=0):
        """Answers if the point context is a horizontal round extreme.
        x/y selection by index, as these can be APoint or point2D tuple instances."""
        return self.isLeftRoundExtreme(tolerance) or self.isRightRoundExtreme(tolerance)

    def isNextVertical(self, tolerance=0):
        """Answers if the point context next point is vertical.
        x/y selection by index, as these can be APoint or point2D tuple instances."""
        return abs(self.p[0] - self.p1[0]) <= tolerance

    isVertical = isNextVertical

    def isPrevVertical(self, tolerance=0):
        """Answers if the point context prev point is vertical.
        x/y selection by index, as these can be APoint or point2D tuple instances."""
        return abs(self.p[0] - self.p_1[0]) <= tolerance

    def isVerticalExtreme(self, tolerance=0):
        """Is the point context a horizontal and extreme in y-direction?"""
        return self.isNextHorizontal(tolerance)\
            and self.isPrevHorizontal(tolerance)\
            and self.isOffCurve(self.p1)\
            and self.isOffCurve(self.p_1)

    def isNextHorizontal(self, tolerance=0):
        """Answers if the point context prev point is horizontal.
        x/y selection by index, as these can be APoint or point2D tuple instances."""
        return abs(self.p[1] - self.p1[1]) <= tolerance

    isHorizontal = isNextHorizontal

    def isPrevHorizontal(self, tolerance=0):
        """Answers if the point context prev point is horizontal.
        x/y selection by index, as these can be APoint or point2D tuple instances."""
        return abs(self.p[1] - self.p_1[1]) <= tolerance

    def isInflection(self):
        valid = self.isOnCurve(self.p) and self.isOffCurve(self.p_1) and self.isOffCurve(self.p1)
        nextP = self.nextOnCurvePoint
        prevP = self.prevOnCurvePoint
        if valid and nextP is not None and prevP is not None:
            a1 = angleOfLines(self.p, self.p1, self.p, nextP)
            a2 = angleOfLines(self.p, self.p_1, self.p, prevP)
            if a1 * a2 > 0:
                return True
        return False

    def isDiagonal(self):
        return not (self.isVertical() or self.isHorizontal())

    def isParallel(self, pc, tolerance=None):
        """Answers if self is parallel to pc point context.
        Optional attribute tolerance
        is the margin to interpret point context lines to be parallel. Default is self.PARALLEL_TOLERANCE."""
        if tolerance is None:
            tolerance = self.PARALLEL_TOLERANCE
        return abs(self.normalizedAngle - pc.normalizedAngle) <= tolerance

    def isRoundStemExtreme(self, tolerance=0):
        return self.isHorizontalExtreme(tolerance)\
            and (self.isLeftRoundExtreme(tolerance) or self.isRightRoundExtreme(tolerance))\
            and self.isOffCurve(self.p1)\
            and self.isOffCurve(self.p_1)

    def isRoundBarExtreme(self, tolerance=0):
        return self.isVerticalExtreme(tolerance)\
            and (self.isTopRoundExtreme(tolerance) or self.isBottomRoundExtreme(tolerance))\
            and self.isOffCurve(self.p1)\
            and self.isOffCurve(self.p_1)

    def isTerminal(self):
        return False

    def isRoundStem(self, pc0, pc1, tolerance=0):
        """The isRoundStem method answers if the pc0 and pc1 define a
        round stem. This is True if one of both of point contexts are extremes and if both, they must
        “bend” in the same direction.
        Also there should be overlap in horizontal direction and the point context should span black only.
        """
        return pc0.isHorizontalRoundExtreme(tolerance)\
            and pc1.isHorizontalRoundExtreme(tolerance)\
            and self.spanRoundsOnBlack(pc0, pc1)

    def inVerticalWindow(self, pc):
        """
        The <code>inVerticalWindow</code> method checks if there is any overlap in X-direction to make
        the vertical comparison optically define as a "bar".

        True    self.minx-------------self.maxx
                            p.minx----------------p.maxx

        True               self.minx----------------------p.maxx
                p.minx---------------p.maxx

        True               self.minx------------self.maxx
                p.minx-------------------------------p.maxx

        False                               self.minx----------self.maxx
                p.minx--------p.maxx

        False   self.minx--------self.maxx
                                                 p.minx------------------------p.maxx
        """
        return pc.minx() < self.maxx() and self.minx() < pc.maxx()

    def inHorizontalWindow(self, pc):
        """
        The <code>inHorizontalWindow</code> method checks if there is any overlap in X-direction to make
        the vertical comparison optically define as a "stem".

        True    self.miny-------------self.maxy
                            p.miny----------------p.maxy

        True               self.miny----------------------p.maxy
                p.miny---------------p.maxy

        True               self.miny------------self.maxy
                p.miny-------------------------------p.maxy

        False                               self.miny----------self.maxy
                p.miny--------p.maxy

        False   self.miny--------self.maxy
                                                 p.miny------------------------p.maxy
        """
        return pc.miny() < self.maxy() and self.miny() < pc.maxy()

    def inDiagonalWindow(self, pc):
        """Answers if pc fits in the diagonal window of self."""
        return not None in self.getProjectedWindowLine(pc)

    def getProjectedPoint(self, p):
        """Answers the perpendicular projection of point p in the line segment of self.
        If the projection in not within the range of the line segment, then answer None.
        """
        pp = self.projectedOnLine(p)
        if self.inBoundingBox(pp): # Is the projected point in inside the line segment
            return pp
        return None # Projection not within the line segment window.

    def getProjectedWindowLines(self, pc):
        """Answers all 4 projected window lines. Note that some of them can be None
        is the projects falls outside the window (the overlapping area of a perpendicular line that
        intersects with both line segments). This method is different from self.getProjectedWindowLine
        as that one only answers one of the projected points that is not None. For efficiency
        reasons only one of the projections is made there. For almost parallel lines all projects are
        more or less identical."""
        return (
            (pc.p, self.getProjectedPoint(pc.p)),
            (pc.p1, self.getProjectedPoint(pc.p1)),
            (self.p, pc.getProjectedPoint(self.p)),
            (self.p1, pc.getProjectedPoint(self.p1))
        )

    def getProjectedWindowLine(self, pc):
        """Answers a tuple of one of the 4 points of (self.p, self.p1, pc.p, pc.p1)
        that has a projection on the other line and its projection point.
        If no projection exists in the window of the two line segments, then answer
        (None, None)."""
        pp = self.getProjectedPoint(pc.p)
        if pp is not None:
            return pc.p, pp
        pp = self.getProjectedPoint(pc.p1)
        if pp is not None:
            return pc.p1, pp
        pp = pc.getProjectedPoint(self.p)
        if pp is not None:
            return self.p, pp
        pp = pc.getProjectedPoint(self.p1)
        if pp is not None:
            return self.p1, pp
        return None, None

    def inBoundingBox(self, p):
        """Answers is p is inside the bounding box of the glyph.
        p can be a point-typles or a Point instance."""
        return (self.p[0] <= p[0] <= self.p1[0] or self.p1[0] <= p[0] <= self.p[0]) and \
               (self.p[1] <= p[1] <= self.p1[1] or self.p1[1] <= p[1] <= self.p[1])

    def minx(self):
        """Answers the minimum x, compared with the two neighbor points.
        x/y selection by index, as these can be APoint or point2D tuple instances."""
        return min(self.p_1[0], self.p[0], self.p1[0])

    def maxx(self):
        """Answers the maximum x, compared with the two neighbor points.
        x/y selection by index, as these can be APoint or point2D tuple instances."""
        return max(self.p_1[0], self.p[0], self.p1[0])

    def miny(self):
        """Answers the minimum y, compared with the two neighbor points.
        x/y selection by index, as these can be APoint or point2D tuple instances."""
        return min(self.p_1[1], self.p[1], self.p1[1])

    def maxy(self):
        """Answers the maximum y, compared with the two neighbor points.
        x/y selection by index, as these can be APoint or point2D tuple instances."""
        return max(self.p_1[1], self.p[1], self.p1[1])

    def middle(self, p1=None):
        """Answers the Point instance of the middle between the optional attribute points p0 and p1.
        If the points are omitted, then use respectively self.p and self.p1.
        x/y selection by index, as these can be APoint or point2D tuple instances."""
        if p1 is None:
            p1 = self.p1
        return int(round((self.p[0] + p1[0])/2)), int(round((self.p[1] + p1[1])/2))

    def distanceTo(self, p):
        """Answers the distance of point p to the line of self."""
        return point2Line(self.p, self.p1, p)

    def projectedOnLine(self, p):
        """Answers the point context pc projects on the line of self."""
        xy = pointProjectedOnLine(self.p.p, self.p1.p, p.p)
        return APoint(xy)

    # self.nextOnCurvePoint

    def _get_nextOnCurvePoint(self):
        if self.isOnCurve(self.p1):
            return self.p1
        if self.isOnCurve(self.p2):
            return self.p2
        if self.isOnCurve(self.p3):
            return self.p3
        return None

    nextOnCurvePoint = property(_get_nextOnCurvePoint)

    # self.prevOnCurvePoint

    def _get_prevOnCurvePoint(self):
        if self.isOnCurve(self.p_1):
            return self.p_1
        if self.isOnCurve(self.p_2):
            return self.p_2
        if self.isOnCurve(self.p_3):
            return self.p_3
        return None

    prevOnCurvePoint = property(_get_prevOnCurvePoint)



if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])


