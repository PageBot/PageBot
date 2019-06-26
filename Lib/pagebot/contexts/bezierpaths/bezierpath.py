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
#     bezierpath.py
#
import math
import AppKit
import Quartz
import CoreText
from pagebot.contexts.basecontext import BaseContext
from pagebot.contexts.bezierpaths.beziercontour import BezierContour
from fontTools.pens.basePen import BasePen
from pagebot.errors import PageBotError

_FALLBACKFONT = "LucidaGrande"

from fontTools.misc.transform import Transform

def transformationAtCenter(matrix, centerPoint):
    """Helper function for rotate(), scale() and skew() to apply a transformation
    with a specified center point.

        >>> transformationAtCenter((2, 0, 0, 2, 0, 0), (0, 0))
        (2, 0, 0, 2, 0, 0)
        >>> transformationAtCenter((2, 0, 0, 2, 0, 0), (100, 200))
        (2, 0, 0, 2, -100, -200)
        >>> transformationAtCenter((-2, 0, 0, 2, 0, 0), (100, 200))
        (-2, 0, 0, 2, 300, -200)
        >>> t = Transform(*transformationAtCenter((0, 1, 1, 0, 0, 0), (100, 200)))
        >>> t.transformPoint((100, 200))
        (100, 200)
        >>> t.transformPoint((0, 0))
        (-100, 100)
    """
    if centerPoint == (0, 0):
        return matrix
    t = Transform()
    cx, cy = centerPoint
    t = t.translate(cx, cy)
    t = t.transform(matrix)
    t = t.translate(-cx, -cy)
    return tuple(t)



class BezierPath(BasePen):
    """A Bézier path object, if you want to draw the same over and over
    again."""

    contourClass = BezierContour

    _textAlignMap = dict(
        center=AppKit.NSCenterTextAlignment,
        left=AppKit.NSLeftTextAlignment,
        right=AppKit.NSRightTextAlignment,
        justified=AppKit.NSJustifiedTextAlignment,
    )

    _instructionSegmentTypeMap = {
        AppKit.NSMoveToBezierPathElement: "move",
        AppKit.NSLineToBezierPathElement: "line",
        AppKit.NSCurveToBezierPathElement: "curve"
    }

    def __init__(self, path=None, glyphSet=None):
        if path is None:
            self._path = AppKit.NSBezierPath.alloc().init()
        else:
            self._path = path
        BasePen.__init__(self, glyphSet)

    def __repr__(self):
        return "<BezierPath>"

    # pen support

    '''
    def moveTo(self, point):
        """
        Move to a point `x`, `y`.
        """
        super(BezierPath, self).moveTo(point)
    '''

    def _moveTo(self, pt):
        self._path.moveToPoint_(pt)

    '''
    def lineTo(self, point):
        """
        Line to a point `x`, `y`.
        """
        super(BezierPath, self).lineTo(point)
    '''

    def _lineTo(self, pt):
        self._path.lineToPoint_(pt)

    '''
    def curveTo(self, *points):
        """
        Draw a cubic bezier with an arbitrary number of control points.

        The last point specified is on-curve, all others are off-curve
        (control) points.
        """
        super(BezierPath, self).curveTo(*points)

    def qCurveTo(self, *points):
        """
        Draw a whole string of quadratic curve segments.

        The last point specified is on-curve, all others are off-curve
        (control) points.
        """
        super(BezierPath, self).qCurveTo(*points)
    '''

    def _curveToOne(self, pt1, pt2, pt3):
        """Curve to a point `x3`, `y3`. With given bezier handles `x1`, `y1`
        and `x2`, `y2`."""
        self._path.curveToPoint_controlPoint1_controlPoint2_(pt3, pt1, pt2)

    def closePath(self):
        """Close the path."""
        self._path.closePath()

    def beginPath(self, identifier=None):
        """Begin using the path as a so called point pen and start a new
        subpath."""
        from fontTools.pens.pointPen import PointToSegmentPen
        self._pointToSegmentPen = PointToSegmentPen(self)
        self._pointToSegmentPen.beginPath()

    def addPoint(self, point, segmentType=None, smooth=False, name=None,
            identifier=None, **kwargs):
        """Use the path as a point pen and add a point to the current subpath.
        `beginPath` must have been called prior to adding points with
        `addPoint` calls."""
        if not hasattr(self, "_pointToSegmentPen"):
            raise PageBotError("path.beginPath() must be called before the path can be used as a point pen")
        self._pointToSegmentPen.addPoint(
            point,
            segmentType=segmentType,
            smooth=smooth,
            name=name,
            identifier=identifier,
            **kwargs
        )

    def endPath(self):
        """End the current subpath. Calling this method has two distinct
        meanings depending on the context:

        When the bezier path is used as a segment pen (using `moveTo`,
        `lineTo`, etc.), the current subpath will be finished as an open
        contour.

        When the bezier path is used as a point pen (using `beginPath`,
        `addPoint` and `endPath`), the path will process all the points added
        with `addPoint`, finishing the current subpath."""
        if hasattr(self, "_pointToSegmentPen"):
            # its been uses in a point pen world
            pointToSegmentPen = self._pointToSegmentPen
            del self._pointToSegmentPen
            pointToSegmentPen.endPath()
        else:
            # with NSBezierPath, nothing special needs to be done for an open subpath.
            pass

    '''
    def addComponent(self, glyphName, transformation):
        """
        Add a sub glyph. The 'transformation' argument must be a 6-tuple
        containing an affine transformation, or a Transform object from the
        fontTools.misc.transform module. More precisely: it should be a
        sequence containing 6 numbers.

        A `glyphSet` is required during initialization of the BezierPath object.
        """
        super(BezierPath, self).addComponent(glyphName, transformation)
    '''
    def drawToPen(self, pen):
        """
        Draw the bezier path into a pen
        """
        contours = self.contours
        for contour in contours:
            contour.drawToPen(pen)

    def drawToPointPen(self, pointPen):
        """Draw the bezier path into a point pen."""
        contours = self.contours
        for contour in contours:
            contour.drawToPointPen(pointPen)

    def arc(self, center, radius, startAngle, endAngle, clockwise):
        """Arc with `center` and a given `radius`, from `startAngle` to
        `endAngle`, going clockwise if `clockwise` is True and counter
        clockwise if `clockwise` is False."""
        self._path.appendBezierPathWithArcWithCenter_radius_startAngle_endAngle_clockwise_(
            center, radius, startAngle, endAngle, clockwise)

    def arcTo(self, point1, point2, radius):
        """Arc defined by a circle inscribed inside the angle specified by
        three points: the current point, `point1`, and `point2`. The arc is
        drawn between the two points of the circle that are tangent to the two
        legs of the angle. """
        self._path.appendBezierPathWithArcFromPoint_toPoint_radius_(point1, point2, radius)

    def rect(self, x, y, w, h):
        """Add a rectangle at possition `x`, `y` with a size of `w`, `h`."""
        self._path.appendBezierPathWithRect_(((x, y), (w, h)))

    def oval(self, x, y, w, h):
        """Add a oval at possition `x`, `y` with a size of `w`, `h`."""
        self._path.appendBezierPathWithOvalInRect_(((x, y), (w, h)))
        self.closePath()

    def text(self, txt, offset=None, font=_FALLBACKFONT, fontSize=10, align=None):
        """Draws a `txt` with a `font` and `fontSize` at an `offset` in the
        bezier path.  If a font path is given the font will be installed and
        used directly.

        - Optionally an alignment can be set.
        - Possible `align` values are: `"left"`, `"center"` and `"right"`.
        - The default alignment is `left`.
        - Optionally `txt` can be a `FormattedString`.
        """
        context = BaseContext()
        if align and align not in self._textAlignMap.keys():
            raise PageBotError("align must be %s" % (", ".join(self._textAlignMap.keys())))
        context.font(font, fontSize)

        attributedString = context.attributedString(txt, align)
        w, h = attributedString.size()
        w *= 2
        if offset:
            x, y = offset
        else:
            x = y = 0
        if align == "right":
            x -= w
        elif align == "center":
            x -= w * .5
        setter = CoreText.CTFramesetterCreateWithAttributedString(attributedString)
        path = Quartz.CGPathCreateMutable()
        Quartz.CGPathAddRect(path, None, Quartz.CGRectMake(x, y, w, h * 2))
        frame = CoreText.CTFramesetterCreateFrame(setter, (0, 0), path, None)
        ctLines = CoreText.CTFrameGetLines(frame)
        origins = CoreText.CTFrameGetLineOrigins(frame, (0, len(ctLines)), None)
        if origins:
            y -= origins[0][1]
        self.textBox(txt, box=(x, y, w, h * 2), font=font, fontSize=fontSize, align=align)

    def textBox(self, txt, box, font=_FALLBACKFONT, fontSize=10, align=None,
            hyphenation=None):
        """Draws a `txt` with a `font` and `fontSize` in a `box` in the bezier
        path. If a font path is given the font will be installed and used
        directly.

        - Optionally an alignment can be set.
        - Possible `align` values are: `"left"`, `"center"` and `"right"`.
        - The default alignment is `left`.
        - Optionally `hyphenation` can be provided.
        - Optionally `txt` can be a `FormattedString`.
        - Optionally `box` can be a `BezierPath`.
        """
        if align and align not in self._textAlignMap.keys():
            raise PageBotError("align must be %s" % (", ".join(self._textAlignMap.keys())))
        context = BaseContext()
        context.font(font, fontSize)
        context.hyphenation(hyphenation)
        path, (x, y) = context._getPathForFrameSetter(box)
        attributedString = context.attributedString(txt, align)

        setter = CoreText.CTFramesetterCreateWithAttributedString(attributedString)
        frame = CoreText.CTFramesetterCreateFrame(setter, (0, 0), path, None)
        ctLines = CoreText.CTFrameGetLines(frame)
        origins = CoreText.CTFrameGetLineOrigins(frame, (0, len(ctLines)), None)

        for i, (originX, originY) in enumerate(origins):
            ctLine = ctLines[i]
            ctRuns = CoreText.CTLineGetGlyphRuns(ctLine)
            for ctRun in ctRuns:
                attributes = CoreText.CTRunGetAttributes(ctRun)
                font = attributes.get(AppKit.NSFontAttributeName)
                baselineShift = attributes.get(AppKit.NSBaselineOffsetAttributeName, 0)
                glyphCount = CoreText.CTRunGetGlyphCount(ctRun)
                for i in range(glyphCount):
                    glyph = CoreText.CTRunGetGlyphs(ctRun, (i, 1), None)[0]
                    ax, ay = CoreText.CTRunGetPositions(ctRun, (i, 1), None)[0]
                    if glyph:
                        self._path.moveToPoint_((x + originX + ax, y + originY + ay + baselineShift))
                        self._path.appendBezierPathWithGlyph_inFont_(glyph, font)
        self.optimizePath()
        return context.clippedText(txt, box, align)

    def traceImage(self, path, threshold=.2, blur=None, invert=False, turd=2, tolerance=0.2, offset=None):
        """
        Convert a given image to a vector outline.

        Optionally some tracing options can be provide:

        * `threshold`: the threshold used to bitmap an image
        * `blur`: the image can be blurred
        * `invert`: invert to the image
        * `turd`: the size of small turd that can be ignored
        * `tolerance`: the precision tolerance of the vector outline
        * `offset`: add the traced vector outline with an offset to the BezierPath
        """
        from .tools import traceImage
        traceImage.TraceImage(path, self, threshold, blur, invert, turd, tolerance, offset)

    def getNSBezierPath(self):
        """
        Return the nsBezierPath.
        """
        return self._path

    def _getCGPath(self):
        path = Quartz.CGPathCreateMutable()
        count = self._path.elementCount()
        for i in range(count):
            instruction, points = self._path.elementAtIndex_associatedPoints_(i)
            if instruction == AppKit.NSMoveToBezierPathElement:
                Quartz.CGPathMoveToPoint(path, None, points[0].x, points[0].y)
            elif instruction == AppKit.NSLineToBezierPathElement:
                Quartz.CGPathAddLineToPoint(path, None, points[0].x, points[0].y)
            elif instruction == AppKit.NSCurveToBezierPathElement:
                Quartz.CGPathAddCurveToPoint(
                    path, None,
                    points[0].x, points[0].y,
                    points[1].x, points[1].y,
                    points[2].x, points[2].y
                )
            elif instruction == AppKit.NSClosePathBezierPathElement:
                Quartz.CGPathCloseSubpath(path)
        # hacking to get a proper close path at the end of the path
        x, y, _, _ = self.bounds()
        Quartz.CGPathMoveToPoint(path, None, x, y)
        Quartz.CGPathAddLineToPoint(path, None, x, y)
        Quartz.CGPathAddLineToPoint(path, None, x, y)
        Quartz.CGPathAddLineToPoint(path, None, x, y)
        Quartz.CGPathCloseSubpath(path)
        return path

    def setNSBezierPath(self, path):
        """
        Set a nsBezierPath.
        """
        self._path = path

    def pointInside(self, xy):
        """
        Check if a point `x`, `y` is inside a path.
        """
        x, y = xy
        return self._path.containsPoint_((x, y))

    def bounds(self):
        """
        Return the bounding box of the path.
        """
        if self._path.isEmpty():
            return None
        (x, y), (w, h) = self._path.bounds()
        return x, y, x + w, y + h

    def controlPointBounds(self):
        """
        Return the bounding box of the path including the offcurve points.
        """
        (x, y), (w, h) = self._path.controlPointBounds()
        return x, y, x + w, y + h

    def optimizePath(self):
        count = self._path.elementCount()
        if self._path.elementAtIndex_(count - 1) == AppKit.NSMoveToBezierPathElement:
            optimizedPath = AppKit.NSBezierPath.alloc().init()
            for i in range(count - 1):
                instruction, points = self._path.elementAtIndex_associatedPoints_(i)
                if instruction == AppKit.NSMoveToBezierPathElement:
                    optimizedPath.moveToPoint_(*points)
                elif instruction == AppKit.NSLineToBezierPathElement:
                    optimizedPath.lineToPoint_(*points)
                elif instruction == AppKit.NSCurveToBezierPathElement:
                    p1, p2, p3 = points
                    optimizedPath.curveToPoint_controlPoint1_controlPoint2_(p3, p1, p2)
                elif instruction == AppKit.NSClosePathBezierPathElement:
                    optimizedPath.closePath()
            self._path = optimizedPath

    def copy(self):
        """
        Copy the bezier path.
        """
        new = self.__class__()
        new._path = self._path.copy()
        return new

    def reverse(self):
        """
        Reverse the path direction
        """
        self._path = self._path.bezierPathByReversingPath()

    def appendPath(self, otherPath):
        """
        Append a path.
        """
        self._path.appendBezierPath_(otherPath.getNSBezierPath())

    def __add__(self, otherPath):
        new = self.copy()
        new.appendPath(otherPath)
        return new

    def __iadd__(self, other):
        self.appendPath(other)
        return self

    # transformations

    def translate(self, x=0, y=0):
        """
        Translate the path with a given offset.
        """
        self.transform((1, 0, 0, 1, x, y))

    def rotate(self, angle, center=(0, 0)):
        """
        Rotate the path around the `center` point (which is the origin by default) with a given angle in degrees.
        """
        angle = math.radians(angle)
        c = math.cos(angle)
        s = math.sin(angle)
        self.transform((c, s, -s, c, 0, 0), center)

    def scale(self, x=1, y=None, center=(0, 0)):
        """
        Scale the path with a given `x` (horizontal scale) and `y` (vertical scale).

        If only 1 argument is provided a proportional scale is applied.

        The center of scaling can optionally be set via the `center` keyword argument. By default this is the origin.
        """
        if y is None:
            y = x
        self.transform((x, 0, 0, y, 0, 0), center)

    def skew(self, angle1, angle2=0, center=(0, 0)):
        """
        Skew the path with given `angle1` and `angle2`.

        If only one argument is provided a proportional skew is applied.

        The center of skewing can optionally be set via the `center` keyword argument. By default this is the origin.
        """
        angle1 = math.radians(angle1)
        angle2 = math.radians(angle2)
        self.transform((1, math.tan(angle2), math.tan(angle1), 1, 0, 0), center)

    def transform(self, transformMatrix, center=(0, 0)):
        """
        Transform a path with a transform matrix (xy, xx, yy, yx, x, y).
        """
        if center != (0, 0):
            transformMatrix = transformationAtCenter(transformMatrix, center)
        aT = AppKit.NSAffineTransform.alloc().init()
        aT.setTransformStruct_(transformMatrix[:])
        self._path.transformUsingAffineTransform_(aT)

    # boolean operations

    def _contoursForBooleanOperations(self):
        # contours are very temporaly objects
        # redirect drawToPointPen to drawPoints
        contours = self.contours
        for contour in contours:
            contour.drawPoints = contour.drawToPointPen
            if contour.open:
                raise PageBotError("open contours are not supported during boolean operations")
        return contours

    def union(self, other):
        """
        Return the union between two bezier paths.
        """
        assert isinstance(other, self.__class__)
        import booleanOperations
        contours = self._contoursForBooleanOperations() + other._contoursForBooleanOperations()
        result = self.__class__()
        booleanOperations.union(contours, result)
        return result

    def removeOverlap(self):
        """
        Remove all overlaps in a bezier path.
        """
        import booleanOperations
        contours = self._contoursForBooleanOperations()
        result = self.__class__()
        booleanOperations.union(contours, result)
        self.setNSBezierPath(result.getNSBezierPath())
        return self

    def difference(self, other):
        """Return the difference between two bezier paths."""
        assert isinstance(other, self.__class__)
        import booleanOperations
        subjectContours = self._contoursForBooleanOperations()
        clipContours = other._contoursForBooleanOperations()
        result = self.__class__()
        booleanOperations.difference(subjectContours, clipContours, result)
        return result

    def intersection(self, other):
        """Return the intersection between two bezier paths."""
        assert isinstance(other, self.__class__)
        import booleanOperations
        subjectContours = self._contoursForBooleanOperations()
        clipContours = other._contoursForBooleanOperations()
        result = self.__class__()
        booleanOperations.intersection(subjectContours, clipContours, result)
        return result

    def xor(self, other):
        """
        Return the xor between two bezier paths.
        """
        assert isinstance(other, self.__class__)
        import booleanOperations
        subjectContours = self._contoursForBooleanOperations()
        clipContours = other._contoursForBooleanOperations()
        result = self.__class__()
        booleanOperations.xor(subjectContours, clipContours, result)
        return result

    def intersectionPoints(self, other=None):
        """
        Return a list of intersection points as `x`, `y` tuples.

        Optionaly provide an other path object to find intersection points.
        """
        import booleanOperations
        contours = self._contoursForBooleanOperations()
        if other is not None:
            assert isinstance(other, self.__class__)
            contours += other._contoursForBooleanOperations()
        return booleanOperations.getIntersections(contours)

    def __mod__(self, other):
        return self.difference(other)

    __rmod__ = __mod__

    def __imod__(self, other):
        result = self.difference(other)
        self.setNSBezierPath(result.getNSBezierPath())
        return self

    def __or__(self, other):
        return self.union(other)

    __ror__ = __or__

    def __ior__(self, other):
        result = self.union(other)
        self.setNSBezierPath(result.getNSBezierPath())
        return self

    def __and__(self, other):
        return self.intersection(other)

    __rand__ = __and__

    def __iand__(self, other):
        result = self.intersection(other)
        self.setNSBezierPath(result.getNSBezierPath())
        return self

    def __xor__(self, other):
        return self.xor(other)

    __rxor__ = __xor__

    def __ixor__(self, other):
        result = self.xor(other)
        self.setNSBezierPath(result.getNSBezierPath())
        return self

    def _points(self, onCurve=True, offCurve=True):
        points = []
        if not onCurve and not offCurve:
            return points
        for index in range(self._path.elementCount()):
            instruction, pts = self._path.elementAtIndex_associatedPoints_(index)
            if not onCurve:
                pts = pts[:-1]
            elif not offCurve:
                pts = pts[-1:]
            points.extend([(p.x, p.y) for p in pts])
        return points

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
        contours = []
        for index in range(self._path.elementCount()):
            instruction, pts = self._path.elementAtIndex_associatedPoints_(index)
            if instruction == AppKit.NSMoveToBezierPathElement:
                contours.append(self.contourClass())
            if instruction == AppKit.NSClosePathBezierPathElement:
                contours[-1].open = False
            if pts:
                contours[-1].append([(p.x, p.y) for p in pts])
        if len(contours) >= 2 and len(contours[-1]) == 1 and contours[-1][0] == contours[-2][0]:
            contours.pop()
        return contours

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


