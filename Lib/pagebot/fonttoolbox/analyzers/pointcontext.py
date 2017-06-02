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
#     pointcontext.py
#
import math
from pagebot.toolbox.mathematics import *
from point import Point

def calculateAngle(p1, p2, inDegrees=True):
    u"""Calculate the angle between points p1 and p2. Points can be either 2D or 3D 
    point tuples or Point instances."""
    xDiff = p2[0] - p1[0]
    yDiff = p2[1] - p1[1]
    angle = math.atan2(yDiff, xDiff)
    if inDegrees:
        angle = math.degrees(angle)
    return angle

def angleOfLines(p1, p2, q1, q2, inDegrees=True):
    u"""Answer the angle difference (radials or default degrees) between p1-->p2 and q1-->q2."""
    angle1 = calculateAngle(p1, p2, inDegrees)
    angle2 = calculateAngle(q1, q2, inDegrees)
    angle = angle2 - angle1
    if angle < -180: angle += 360
    elif angle > 180: angle -= 360
    return angle

class PointContext(object):
    u"""The PointContext instance is a Point wrapper, that also takes the 3 points previous
    and next 3 points on the contour. The instance behaves like a normal point p, but
    additional information is available as interpreted from the point context in relation 
    to the neighbor points. The total of 6 points is derived
    from the average construction of a serif, so it is possible to hold (and interpret) an 
    entire serif sequence inside one point context.
    """
    PARALLEL_TOLERANCE = 2 # Difference tolerance angle in degrees to take point contexts as parallel
    
    def __init__(self, points, index, contourIndex, clockwise, glyphName=None):
        u"""Points list is supposed to contain Point instances, not point lists.
        We need the extra storage, e.g. for point type that Point holds."""
        self.p_3, self.p_2, self.p_1, self.p, self.p1, self.p2, self.p3 = points
        self.contourIndex = contourIndex
        self.index = index
        self.clockwise = clockwise
        self.glyphName = glyphName
        self._direction = None  # Cache direction once calculated.
        self._angle = None  # Cache axis once calculated.
        
    def _get_x(self):
        return self.p[0]
    x = property(_get_x)

    def _get_y(self):
        return self.p[1]
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
            xDiff = self.p1.x - self.p.x
            yDiff = self.p1.y - self.p.y
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
        s = 'pc[%s] (%s,%s)' % (self.index, self.p.x, self.p.y)
        if self.isNextVertical():
            s += ' vertical'
        if self.isNextHorizontal():
            s += ' horizontal'
        if self.isRoundStemExtreme():
            s += ' roundstem'
        if self.isRoundBarExtreme():
            s += ' roundbar'
        if self.isTerminal():
            s += ' terminal'
        if self.clockwise:
            s += ' c%d CW' % self.contourIndex
        else:
            s += ' c%s CCW' % self.contourIndex
        if self.glyphName is not None:
            s += ' (%s)' % self.glyphName
        return s

    def isOffCurve(self, p=None):
        if p is None:
            p = self.p
        if isinstance(p, Point):
            return not p.onCurve
        return False # Point2D type is always on-curve.

    def isOnCurve(self, p=None):
        if p is None:
            p = self.p
        if isinstance(p, Point):
            return p.onCurve
        return True # Point2D type is always on-curve.

    def isUp(self):
        return self.p.y < self.p1.y

    def isDown(self):
        return self.p.y > self.p1.y

    def isLeft(self):
        return self.p.x < self.p1.x

    def isRight(self):
        return self.p.y > self.p1.y

    def isHorizontalExtreme(self):
        u"""
        <doc>The <code>isHorizontalExtreme</code> method answers the boolean flag if the point context is an extreme
        (such as the side of an O).</doc>
        """
        # Is the point context a vertical and extreme in x-direction?
        # @@@ Also test on non-inflection point.
        return self.isNextVertical()\
            and self.isPrevVertical()\
            and self.isOffCurve(self.p1)\
            and self.isOffCurve(self.p_1)

    def isLeftRoundExtreme(self):
        nextP = self.nextOnCurvePoint
        prevP = self.prevOnCurvePoint
        return nextP is not None and prevP is not None\
            and self.p.x < nextP.x\
            and self.p.x < prevP.x

    def isRightRoundExtreme(self):
        nextP = self.nextOnCurvePoint
        prevP = self.prevOnCurvePoint
        return nextP is not None and prevP is not None\
            and self.p.x > nextP.x\
            and self.p.x > prevP.x

    def isTopRoundExtreme(self):
        nextP = self.nextOnCurvePoint
        prevP = self.prevOnCurvePoint
        return nextP is not None and prevP is not None\
            and self.p.y > nextP.y\
            and self.p.y > prevP.y

    def isBottomRoundExtreme(self):
        nextP = self.nextOnCurvePoint
        prevP = self.prevOnCurvePoint
        return nextP is not None and prevP is not None\
            and self.p.y < nextP.y\
            and self.p.y < prevP.y

    def isVerticalRoundExtreme(self):
        return self.isTopRoundExtreme() or self.isBottomRoundExtreme()

    def isHorizontalRoundExtreme(self):
        return self.isLeftRoundExtreme() or self.isRightRoundExtreme()

    def isNextVertical(self):
        return self.p.x == self.p1.x

    isVertical = isNextVertical

    def isPrevVertical(self):
        return self.p.x == self.p_1.x

    def isVerticalExtreme(self):
        u"""Is the point context a horizontal and extreme in y-direction?"""
        return self.isNextHorizontal()\
            and self.isPrevHorizontal()\
            and self.isOffCurve(self.p1)\
            and self.isOffCurve(self.p_1)

    def isNextHorizontal(self):
        return self.p.y == self.p1.y

    isHorizontal = isNextHorizontal

    def isPrevHorizontal(self):
        return self.p.y == self.p_1.y

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
        u"""Answer the boolean flag if self is parallel to pc point context. 
        Optional attribute tolerance
        is the margin to interpret point context lines to be parallel. Default is self.PARALLEL_TOLERANCE."""
        if tolerance is None:
            tolerance = self.PARALLEL_TOLERANCE
        return abs(self.normalizedAngle - pc.normalizedAngle) <= tolerance
            
    def isRoundStemExtreme(self):
        return self.isHorizontalExtreme()\
            and (self.isLeftRoundExtreme() or self.isRightRoundExtreme())\
            and self.isOffCurve(self.p1)\
            and self.isOffCurve(self.p_1)

    def isRoundBarExtreme(self):
        return self.isVerticalExtreme()\
            and (self.isTopRoundExtreme() or self.isBottomRoundExtreme())\
            and self.isOffCurve(self.p1)\
            and self.isOffCurve(self.p_1)

    def isTerminal(self):
        return False

    def isRoundStem(self, pc0, pc1):
        u"""The isRoundStem method answers the boolean flag if the pc0 and pc1 define a
        round stem. This is True if one of both of point contexts are extremes and if both, they must
        “bend” in the same direction.
        Also there should be overlap in horizontal direction and the point context should span black only.
        """
        return pc0.isHorizontalRoundExtreme()\
            and pc1.isHorizontalRoundExtreme()\
            and self.spanRoundsOnBlack(pc0, pc1)

    def inVerticalWindow(self, pc):
        u"""
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
        u"""
        <doc>The <code>inHorizontalWindow</code> method checks if there is any overlap in X-direction to make
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
        u"""Answer the boolean flag if pc fits in the diagonal window of self."""
        return not None in self.getProjectedWindowLine(pc)
    
    def getProjectedPoint(self, p):
        u"""Answer the perpendicular projection of point p in the line segment of self.
        If the projection in not within the range of the line segment, then answer None.
        """
        pp = self.projectedOnLine(p)
        if self.inBoundingBox(pp): # Is the projected point in inside the line segment
            return pp
        return None # Projection not within the line segment window.
    
    def getProjectedWindowLines(self, pc):
        u"""Answer all 4 projected window lines. Note that some of them can be None
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
        u"""Answer a tuple of one of the 4 points of (self.p, self.p1, pc.p, pc.p1)
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
        u"""Answer the boolean flag is p is inside the bounding box of the glyph.
        p can be a point-typles or a Point instance."""
        return (self.p.x <= p[0] <= self.p1.x or self.p1.x <= p[0] <= self.p.x) and \
               (self.p.y <= p[1] <= self.p1.y or self.p1.y <= p[1] <= self.p.y)
        
    def minx(self):
        return min(self.p_1.x, self.p.x, self.p1.x)
    
    def maxx(self):
        return max(self.p_1.x, self.p.x, self.p1.x)
    
    def miny(self):
        return min(self.p_1.y, self.p.y, self.p1.y)
    
    def maxy(self):
        return max(self.p_1.y, self.p.y, self.p1.y)
    
    def middle(self, p1=None):
        u"""Answer the Point instance of the middle between the optional attribute points p0 and p1.
        If the points are omitted, then use respectively self.p and self.p1."""
        if p1 is None:
            p1 = self.p1
        return int(round((self.p[0] + p1[0])/2)), int(round((self.p[1] + p1[1])/2))
     
    def distanceTo(self, p):
        u"""Answer the distance of point p to the line of self."""
        return point2Line(self.p, self.p1, p)
    
    def projectedOnLine(self, p):
        u"""Answer the point context pc projects on the line of self."""
        xy = pointProjectedOnLine(self.p, self.p1, p)
        return Point(xy)
    
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
