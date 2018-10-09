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
#     stems.py
#
from pagebot.toolbox.mathematics import distance
from pagebot.fonttoolbox.analyzers.apoint import APoint
from pagebot.fonttoolbox.analyzers.apointcontext import APointContext

class Stem:
    """
    The <code>Stem</code> class instant takes the CVT related to this stem, and the  left and point <code>Vertical
    </code> instance that stem binds.
    """

    def __init__(self, parent, point, glyphName=None, offset=None, name=None):
        """Parent and point can be point or point context, depending on available data and usage."""
        assert parent is None or isinstance(parent, (tuple, list, APointContext))
        assert point is None or isinstance(point, (tuple, list, APointContext))
        self.parent = parent
        self.point = point
        self.offset = offset or (0,0) # Optional offset (dx, dy) tuple, e.g. used for stems derived from component references.
        self.glyphName = glyphName
        self.name = name

    def __repr__(self):
        if self.offset in (None, (0,0)):
             return '[%s.%s: %s --> %s]' % (self.glyphName, self.name or self.__class__.__name__, self.parent, self.point)
        return '[%s.%s: %s+%s --> %s+%d]' % (self.glyphName, self.name or self.__class__.__name__, self.parent, self.point, self.offset[0], self.offset[1])

    def copy(self):
        return self.__class__(self.parent, self.point, self.glyphName, self.offset)

    def addOffset(self, offset):
        """In case of multiple chained component reference, analyzer will add incremental offset this way."""
        self.offset = self.offset[0] + offset[0], self.offset[1] + offset[1]

    # self.size
    def _get_size(self):
        """Note that size can be negative, to indicate the direction of the arrow, as in the top blueBar."""
        return self.point[0] - self.parent[0] 
    size = property(_get_size)

    # self.xSpan    # Answers the span tuple of both x value, shifted by x-offset 
    def _get_xSpan(self):
        dx = self.offset[0]
        return self.parent[0] + dx, self.point[0] + dx
    xSpan = property(_get_xSpan)
    
    # self.x    Answers parent.x, shifted by x-offset   
    def _get_x(self):
        dx = self.offset[0]
        return self.parent[0] + dx
    x = property(_get_x)
    
    # self.ys    Answers the span tuple of both y values, shifted by y-offset   
    def _get_ySpan(self):
        dy = self.offset[1]
        return self.parent[1] + dy, self.point[1] + dy
    ySpan = property(_get_ySpan)
    
    # self.y    Answers parent.y, shifted by y-offset   
    def _get_y(self):
        dy = self.offset[1]
        return self.parent[1] + dy
    y = property(_get_y)

    def isWhite(self):
        return False

    # self.nearestPoint   
    def _get_nearestPoint(self):
        """
        The <code>getNearestPoint</code> method gets the nearest point in the <code>self.point</code> point context
        to <code>self.parent</code>.
        """
        nearp = self.point.p
        d = abs(self.parent.y - nearp.y)
        if self.isOnCurve(self.point.p1):
            d1 = abs(self.parent.p.y - self.point.p1.y)
            if d1 < d:
                nearp = self.point.p1
                d = d1
        if self.isOnCurve(self.point.p_1):
            d1 = abs(self.parent.p.y - self.point.p_1.y)
            if d1 < d:
                nearp = self.point.p_1
        return nearp
    nearestPoint = property(_get_nearestPoint)
    
    def isTerminal(self):
        """The stem is also a terminal, if the end of the parallel lines also are connected point contexts."""
        return False

class Counter(Stem):

    def __init__(self, parent, point, value, offset=None):
        Stem.__init__(self, parent, point, value, offset=offset)

    def isWhite(self):
        return True

class Width(Stem):

    def __init__(self, pc, value=None, offset=None):
        Stem.__init__(self, None, pc, offset=offset)
        self.value = value
    
    # self.size
    
    def _get_size(self):
        if self.value is not None:
            return self.value
        return self.point.p.x
    size = property(_get_size)
    
class Height(Width):

    # self.size
    
    def _get_size(self):
        if self.value is not None:
            return self.value
        return self.point.p.y
    size = property(_get_size)
    
class Bar(Stem):

    # self.size
    
    def _get_size(self):
        return abs(self.parent[1] - self.point[1])
    size = property(_get_size)
    
    def _get_nearestPoint(self):
        """
        The <code>getNearestPoint</code> method gets the nearest point in the <code>self.point</code> point context
        to <code>self.parent</code>.
        """
        nearp = self.point.p
        d = abs(self.parent.p.x - nearp.x)
        if self.isOnCurve(self.point.p1):
            d1 = abs(self.parent.p.x - self.point.p1.x)
            if d1 < d:
                nearp = self.point.p1
                d = d1
        if self.isOnCurve(self.point.p_1):
            d1 = abs(self.parent.p.x - self.point.p_1.x)
            if d1 < d:
                nearp = self.point.p_1
        return nearp

    nearestPoint = property(_get_nearestPoint)

class BlueBar(Bar):
    pass

class VerticalCounter(Bar):

    def __init__(self, parent, point, value, offset=None):
        Bar.__init__(self, parent, point, value, offset=offset)

    def isWhite(self):
        return True

class DiagonalStem(Stem):
    
    # self.run answers the horizontal run of the diagonal.

    # self.nearestPoint
    
    def _get_nearestPoint(self):
        """The <code>getNearestPoint</code> method gets the nearest point in the <code>self.point</code> point context
        to <code>self.parent</code>. Default for a diagonal is always to answer <code>self.point.p</code>.
        """
        return self.point.p

    nearestPoint = property(_get_nearestPoint)
    
    # self.size    Average distance between the diagonal projected line segments.
    
    def _get_size(self):
        d = 0
        projectionLines = self.projectionLines
        for p, projectedP in projectionLines: # p is PointContext instance, projectP is Point instance.
            d += distance([p.x, p.y], [projectedP.x, projectedP.y])
        return int(round(d/len(projectionLines)))
        
    size = property(_get_size)

    """A diagonal is a special kind of <b>Stem</b>, as it also is able to calculate 
    the projected window points."""
    
    # self.projectionLines    Answer the list of valid projection lines (tuple of point + projected point) 
    
    def _get_projectionLines(self):
        projectionLines = []
        for projectionLine in self.point.getProjectedWindowLines(self.parent):
            if not None in projectionLine:
                projectionLines.append(projectionLine)
        return projectionLines
    
    projectionLines = property(_get_projectionLines)
    
    # self.perpendicularMiddleLine     Answer the line that is average perpendicular and in the middle of the projected window
    
    def _get_perpendicularMiddleLine(self):
        # Calculate the average middle from the projections
        mx = my = 0
        projectionLines = self.projectionLines
        count = len(projectionLines)*2 # Avoid double division of average
        for p, projectedP in projectionLines:
            mx += p.x + projectedP.x
            my += p.y + projectedP.y

        #FIXME: I'm not sure if APoint (from apoint.py) is the correct object to use here:
        m = APoint(mx/count, my/count)

        # Now project this window middle points on the two lines again. 
        pp0 = self.point.getProjectedPoint(m)
        pp1 = self.parent.getProjectedPoint(m)
        return pp0, pp1
    
    perpendicularMiddleLine = property(_get_perpendicularMiddleLine)

    # self.perpendicularLines   Answer the relevant perpendicular lines (start, middle, end) of the projectionLines.

    def _get_perpendicularLines(self):
        projectionLines = self.projectionLines
        if len(projectionLines) == 2:
            return projectionLines[0], self.perpendicularMiddleLine, self.projectionLines[1]
        return [self.perpendicularMiddleLine]

    perpendicularLines = property(_get_perpendicularLines)

class Serif(Stem):
    """
    The <code>Serif</code> class holds the two point contexts (<code>self.parent</code> and <code>self.point</code>)
    that span a continuous set of point contexts defining a serif.
    """

    def _get_boundingBox(self):
        # TODO: get this to work
        #bb = BoundingBox()
        #bb.extendByPointContext(self.parent)
        #bb.extendByPointContext(self.point)
        #return bb
        return 0, 0, 0, 0
    boundingBox = property(_get_boundingBox)
    
class Overshoot:

    def __init__(self, pc, reference):
        self.pc = pc
        self.reference = reference

    def _get_size(self):
        return self.pc.p.y - self.reference.y

    size = property(_get_size)

