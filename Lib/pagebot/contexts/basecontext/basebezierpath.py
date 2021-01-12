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
#     basebezierpath.py
#

import math
import booleanOperations
from fontTools.pens.basePen import BasePen
from fontTools.pens.pointPen import PointToSegmentPen
from fontTools.pens.boundsPen import BoundsPen
from pagebot.errors import PageBotError
from pagebot.contexts.basecontext.basebeziercontour import BaseBezierContour
from pagebot.contexts.basecontext.basebezierpoint import BaseBezierPoint
from pagebot.contexts.basecontext.basebeziersegment import BaseBezierSegment
from pagebot.constants import MOVETO, CLOSEPATH

_FALLBACKFONT = "LucidaGrande"

class BaseBezierPath(BasePen):
    """Base class with same interface as DrawBot Bézier path."""

    contourClass = BaseBezierContour

    def __init__(self, path=None, glyphSet=None):
        """

        >>> path = BaseBezierPath()
        >>> path
        <BaseBezierPath>
        """
        self._contours = []
        #super().__init__(glyphSet)
        BasePen.__init__(self, glyphSet)

    def __repr__(self):
        return "<BaseBezierPath>"

    def _points(self, onCurve=True, offCurve=True):
        """Internal points representation, corresponding to the DrawBot Bézier
        path."""
        points = []

        if not onCurve and not offCurve:
            return points

        for contour in self._contours:
            for segment in contour:
                pts = segment.points

                if not onCurve:
                    pts = pts[:-1]
                elif not offCurve:
                    pts = pts[-1:]
                points.extend([(p.x, p.y) for p in pts])

        return tuple(points)

    def _get_points(self):
        return self._points()

    points = property(_get_points, doc="Return a list of all points.")

    def _get_onCurvePoints(self):
        return self._points(offCurve=False)

    onCurvePoints = property(_get_onCurvePoints, doc="Return a list of all on curve points.")

    def _get_offCurvePoints(self):
        return self._points(onCurve=False)

    offCurvePoints = property(_get_offCurvePoints, doc="Return a list of all off curve points.")

    def _get_contours(self):
        """Internal contour representation, corresponding to the DrawBot Bézier path."""
        contours = []
        for contour in self._contours:
            for segment in contour:
                if segment.instruction == MOVETO:
                    contours.append(BaseBezierContour())
                if segment.instruction == CLOSEPATH:
                    contours[-1].open = False
                if segment.points:
                    contours[-1].append([(p.x, p.y) for p in segment.points])

        if len(contours) >= 2 and len(contours[-1]) == 1 and contours[-1][0] == contours[-2][0]:
            contours.pop()

        return tuple(contours)

    contours = property(_get_contours, doc="Return a list of contours with all point coordinates sorted in segments. A contour object has an `open` attribute.")

    def __len__(self):
        return len(self.contours)

    def __getitem__(self, index):
        return self.contours[index]

    def __iter__(self):
        contours = self.contours
        count = len(contours)
        index = 0
        while index < count:
            contour = contours[index]
            yield contour
            index += 1

    def addSegment(self, instruction, points):
        """Adds a new segment to the current contour."""
        segment = BaseBezierSegment(instruction, points)
        contour = self.getContour()
        contour.append(segment)

    def getContour(self):
        """Gets the current contour if it exists, else make one."""
        if len(self._contours) == 0:
            contour = self.contourClass()
            self._contours.append(contour)
        else:
            contour = self._contours[-1]

        return contour

    def getPoint(self, p, onCurve=True):
        x, y = p
        point = BaseBezierPoint(x, y, onCurve=onCurve)
        return point

    # FontTools PointToSegmentPen routines.

    def beginPath(self, identifier=None):
        """Begin using the path as a point pen and start a new subpath."""
        self._pointToSegmentPen = PointToSegmentPen(self)
        self._pointToSegmentPen.beginPath()

    def addPoint(self, point, segmentType=None, smooth=False, name=None,
            identifier=None, **kwargs):
        """Use the path as a point pen and add a point to the current subpath.
        `beginPath` must have been called prior to adding points with
        `addPoint` calls."""
        if not hasattr(self, "_pointToSegmentPen"):
            msg = "path.beginPath() must be called before the path can be used as a point pen."
            raise PageBotError(msg)
        self._pointToSegmentPen.addPoint(
            point,
            segmentType=segmentType,
            smooth=smooth,
            name=name,
            identifier=identifier,
            **kwargs
        )

    def endPath(self):
        """Ends the current subpath. Calling this method has two distinct
        meanings depending on the context:

        When the Bézier path is used as a segment pen (using `moveTo`,
        `lineTo`, etc.), the current subpath will be finished as an open
        contour.

        When the Bézier path is used as a point pen (using `beginPath`,
        `addPoint` and `endPath`), the path will process all the points added
        with `addPoint`, finishing the current subpath."""
        if hasattr(self, "_pointToSegmentPen"):
            pointToSegmentPen = self._pointToSegmentPen
            del self._pointToSegmentPen
            pointToSegmentPen.endPath()
        else:
            msg = "path.beginPath() must be called before the path can be used as a point pen."
            raise PageBotError(msg)

    def draw(self, pen):
        """Draws the contours with **pen**."""
        pointPen = PointToSegmentPen(pen)
        self.drawToPointPen(pointPen)

    def bounds(self):
        """Returns the bounding box of the path."""
        pen = BoundsPen(self)
        self.draw(pen)
        return pen.bounds

    def drawToPointPen(self, pointPen):
        """Draws the Bézier path into a point pen."""
        contours = self.contours

        for contour in contours:
            contour.drawToPointPen(pointPen)

    def drawToPen(self, pen):
        """Draws the Bézier path into a pen."""
        contours = self.contours

        for contour in contours:
            contour.drawToPen(pen)

    # Drawing.

    def addComponent(self, glyphName, transformation):
        """
        Adds a sub glyph. The 'transformation' argument must be a 6-tuple
        containing an affine transformation, or a Transform object from the
        fontTools.misc.transform module. More precisely: it should be a
        sequence containing 6 numbers.

        A `glyphSet` is required during initialization of the BezierPath
        object.
        """
        raise NotImplementedError

    # Shapes.

    def rect(self, x, y, w, h):
        """Adds a rectangle at position `x`, `y` with a size of `w`, `h`."""
        x1 = x + w
        y1 = y + h
        p0 = (x, y)
        p1 = (x1, y)
        p2 = (x1, y1)
        p3 = (x, y1)
        self.moveTo(p0)
        self.lineTo(p1)
        self.lineTo(p2)
        self.lineTo(p3)
        self.closePath()

    def oval(self, x, y, w, h):
        """Adds an oval at position `x`, `y` with a size of `w`, `h`"""
        # Control point offsets.
        kappa = .5522848
        offsetX = (w / 2) * kappa
        offsetY = (h / 2) * kappa

        # Middle and other extreme points.
        x0 = x + (w / 2)
        y0 = y + (h / 2)
        x1 = x + w
        y1 = y + h

        self.moveTo((x0, y0))

        cp1 = (x, y0 - offsetY)
        cp2 = (x0 - offsetX, y)
        p = (x1, y0)
        self.curveTo(cp1, cp2, p)

        cp1 = (x0 + offsetX, y)
        cp2 = (x1, y0 - offsetY)
        p = (x1, y0)
        self.curveTo(cp1, cp2, p)

        cp1 = (x1, y0 + offsetY)
        cp2 = (x0 + offsetX, y1)
        p = (x0, y1)
        self.curveTo(cp1, cp2, p)

        cp1 = (x0 - offsetX, y1)
        cp2 = (x, y0 + offsetY)
        p = (x, y0)
        self.curveTo(cp1, cp2, p)

    def line(self, point1, point2):
        """Adds a line between two given points."""
        self.moveTo(point1)
        self.lineTo(point2)

    def polygon(self, *points, **kwargs):
        """Draws a polygon with `n` points. Optionally a `close` argument can
        be provided to open or close the path. By default a `polygon` is a
        closed path."""
        self.moveTo(points[0])

        for point in points[1:]:
            self.lineTo(point)

        # TODO: optionally close.

    def arc(self, center, radius, startAngle, endAngle, clockwise):
        """Arc with `center` and a given `radius`, from `startAngle` to
        `endAngle`, going clockwise if `clockwise` is True and counter
        clockwise if `clockwise` is False."""
        raise NotImplementedError

    def arcTo(self, point1, point2, radius):
        """Arc defined by a circle inscribed inside the angle specified by
        three points: the current point, `point1`, and `point2`. The arc is
        drawn between the two points of the circle that are tangent to the two
        legs of the angle."""
        raise NotImplementedError

    # Text.

    def text(self, txt, offset=None, font=_FALLBACKFONT, fontSize=10,
            align=None):
        """Draws a `txt` with a `font` and `fontSize` at an `offset` in the
        Bézier path. If a font path is given the font will be installed and
        used directly.

        * Optionally an alignment can be set. Possible `align` values are:
          `"left"`, `"center"` and `"right"`.
        * The default alignment is `left`.
        * Optionally `txt` can be a `FormattedString`.

        """
        raise NotImplementedError

    def textBox(self, txt, box, font=None, fontSize=10, align=None,
            hyphenation=None):
        """
        Draws a `txt` with a `font` and `fontSize` in a `box` in the Bézier path.
        If a font path is given the font will be installed and used directly.

        Optionally an alignment can be set.

        * Possible `align` values are: `"left"`, `"center"` and `"right"`.
        * The default alignment is `left`.
        * Optionally `hyphenation` can be provided.
        * Optionally `txt` can be a `FormattedString`.
        * Optionally `box` can be a `BezierPath`.

        """
        raise NotImplementedError

    # Path operations.
    # These are specific for a DrawBot path, dropping from interface.

    #def getNSBezierPath(self):
    def getBezierPath(self):
        """Returns the equivalent of an NSBezierPath."""

    #def setNSBezierPath(self, path):
    def setBezierPath(self, path):
        """Sets the equivalent of an NSBezierPath."""

    def traceImage(self, path, threshold=.2, blur=None, invert=False, turd=2,
            tolerance=0.2, offset=None):
        """Converts a given image to a vector outline. Optionally some tracing
        options can be provided:

        * `threshold`: the threshold used to bitmap an image
        * `blur`: the image can be blurred
        * `invert`: invert to the image
        * `turd`: the size of small turd that can be ignored
        * `tolerance`: the precision tolerance of the vector outline
        * `offset`: add the traced vector outline with an offset to the BezierPath
        """
        # TODO: use potrace, see drawBot.context.tools.TraceImage.

    def pointInside(self, xy):
        """Checks if a point `x`, `y` is inside a path."""
        raise NotImplementedError

    def bounds(self):
        """Returns the bounding box of the path."""
        raise NotImplementedError

    def controlPointBounds(self):
        """Returns the bounding box of the path including the offcurve
        points."""
        raise NotImplementedError

    def optimizePath(self):
        raise NotImplementedError

    def copy(self):
        """Copy the Bézier path."""
        raise NotImplementedError

    def reverse(self):
        """Reverse the path direction."""
        raise NotImplementedError

    def appendPath(self, otherPath):
        """Append a path."""
        raise NotImplementedError

    # transformations
    # NOTE: currently handled within context.

    def translate(self, x=0, y=0):
        """Translates the path with a given offset."""
        self.transform((1, 0, 0, 1, x, y))

    def rotate(self, angle, center=(0, 0)):
        """Rotates the path around the `center` point (which is the origin by
        default) with a given angle in degrees."""
        angle = math.radians(angle)
        c = math.cos(angle)
        s = math.sin(angle)
        self.transform((c, s, -s, c, 0, 0), center)

    def scale(self, x=1, y=None, center=(0, 0)):
        """Scales the path with a given `x` (horizontal scale) and `y`
        (vertical scale).

        If only 1 argument is provided a proportional scale is applied.

        The center of scaling can optionally be set via the `center` keyword
        argument. By default this is the origin."""
        if y is None:
            y = x
        self.transform((x, 0, 0, y, 0, 0), center)

    def skew(self, angle1, angle2=0, center=(0, 0)):
        """Skews the path with given `angle1` and `angle2`. If only one argument
        is provided a proportional skew is applied. The center of skewing can
        optionally be set via the `center` keyword argument. By default this is
        the origin."""
        angle1 = math.radians(angle1)
        angle2 = math.radians(angle2)
        self.transform((1, math.tan(angle2), math.tan(angle1), 1, 0, 0), center)

    def transform(self, transformMatrix, center=(0, 0)):
        """Transforms a path with a transform matrix (xy, xx, yy, yx, x, y)."""

    # Boolean operations.

    def _contoursForBooleanOperations(self):
        # contours are temporary objects
        # redirect drawToPointPen to drawPoints
        contours = self.contours
        for contour in contours:
            contour.drawPoints = contour.drawToPointPen
            if contour.open:
                raise PageBotError("open contours are not supported during boolean operations")
        return contours


    def union(self, other):
        """Returns the union between two Bézier paths."""
        assert isinstance(other, self.__class__)
        contours = self._contoursForBooleanOperations() + other._contoursForBooleanOperations()
        result = self.__class__()
        booleanOperations.union(contours, result)
        return result

    def removeOverlap(self):
        """Remove all overlaps in a Bézier path."""
        contours = self._contoursForBooleanOperations()
        result = self.__class__()
        booleanOperations.union(contours, result)
        # TODO:
        #self.setNSBezierPath(result.getNSBezierPath())
        #self.setBezierPath(result.getBezierPath())
        return self

    def difference(self, other):
        """Returns the difference between two Bézier paths.
        """
        subjectContours = self._contoursForBooleanOperations()
        clipContours = other._contoursForBooleanOperations()
        result = self.__class__()
        booleanOperations.difference(subjectContours, clipContours, result)
        return result

    def intersection(self, other):
        """Returns the intersection between two Bézier paths."""
        assert isinstance(other, self.__class__)
        subjectContours = self._contoursForBooleanOperations()
        clipContours = other._contoursForBooleanOperations()
        result = self.__class__()
        booleanOperations.intersection(subjectContours, clipContours, result)
        return result

    def xor(self, other):
        """Returns the xor between two Bézier paths."""
        assert isinstance(other, self.__class__)
        subjectContours = self._contoursForBooleanOperations()
        clipContours = other._contoursForBooleanOperations()
        result = self.__class__()
        booleanOperations.xor(subjectContours, clipContours, result)
        return result

    def intersectionPoints(self, other=None):
        """
        Returns a list of intersection points as `x`, `y` tuples. Optionaly
        provides another path object to find intersection points.
        """
        contours = self._contoursForBooleanOperations()
        if other is not None:
            assert isinstance(other, self.__class__)
            contours += other._contoursForBooleanOperations()
        return booleanOperations.getIntersections(contours)

    def expandStroke(self, width, lineCap="round", lineJoin="round",
            miterLimit=10):
        """Returns a new Bézier path with an expanded stroke around the original path,
        with a given `width`. Note: the new path will not contain the original path.

        The following optional arguments are available with respect to line caps and joins:
        * `lineCap`: Possible values are `"butt"`, `"square"` or `"round"`
        * `lineJoin`: Possible values are `"bevel"`, `"miter"` or `"round"`
        * `miterLimit`: The miter limit to use for `"miter"` lineJoin option
        """
        # TODO: find cross-platform alternative to Quartz.CGPathCreateCopyByStrokingPath.

    #

    def __add__(self, otherPath):
        #new = self.copy()
        #new.appendPath(otherPath)
        #return new
        pass

    def __iadd__(self, other):
        self.appendPath(other)
        return self

    def __mod__(self, other):
        return self.difference(other)

    __rmod__ = __mod__

    def __imod__(self, other):
        #result = self.difference(other)
        #self.setBezierPath(result.getBezierPath())
        #return self
        pass

    def __or__(self, other):
        return self.union(other)

    __ror__ = __or__

    def __ior__(self, other):
        #result = self.union(other)
        #self.setBezierPath(result.getBezierPath())
        #return self
        pass

    def __and__(self, other):
        return self.intersection(other)

    __rand__ = __and__

    def __iand__(self, other):
        #result = self.intersection(other)
        #self.setBezierPath(result.getBezierPath())
        #return self
        pass

    def __xor__(self, other):
        return self.xor(other)

    __rxor__ = __xor__

    def __ixor__(self, other):
        #result = self.xor(other)
        #self.setBezierPath(result.getBezierPath())
        #return self
        pass

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
