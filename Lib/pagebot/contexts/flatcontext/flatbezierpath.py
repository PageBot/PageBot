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
#     flatbezierpath.py
#

from fontTools.pens.pointPen import PointToSegmentPen
from pagebot.errors import PageBotError
from pagebot.contexts.basecontext.basebezierpath import BaseBezierPath
from pagebot.constants import MOVETO, LINETO, CURVETO, CLOSEPATH

class FlatBezierPath(BaseBezierPath):
    """Bézier path that implements commands like Flat, but with the same API
    as DrawBot.BezierPath.

    >>> import flat
    >>> path = FlatBezierPath(flat)
    >>> path
    <FlatBezierPath>
    >>> path.moveTo((0, 0))
    >>> path
    <FlatBezierPath>
    >>> path.lineTo((0, 100))
    >>> path.lineTo((100, 100))
    >>> path.lineTo((100, 0))
    >>> path.lineTo((0, 0))
    >>> path.closePath()
    >>> len(path.contours[-1])
    5
    """

    def __init__(self, b, path=None, glyphSet=None):
        self.b = b
        self.commands = []
        super().__init__(path=path, glyphSet=glyphSet)

    def __repr__(self):
        return '<FlatBezierPath>'

    # FontTools PointToSegmentPen routines..

    def beginPath(self, identifier=None):
        """Begin using the path as a so called point pen and start a new subpath."""
        self._pointToSegmentPen = PointToSegmentPen(self)
        self._pointToSegmentPen.beginPath()

    def addPoint(self, point, segmentType=None, smooth=False, name=None, identifier=None, **kwargs):
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
        """Ends the current subpath. Calling this method has two distinct
        meanings depending on the context:

        When the Bézier path is used as a segment pen (using `moveTo`,
        `lineTo`, etc.), the current subpath will be finished as an open
        contour.

        When the Bézier path is used as a point pen (using `beginPath`,
        `addPoint` and `endPath`), the path will process all the points added
        with `addPoint`, finishing the current subpath."""
        if hasattr(self, "_pointToSegmentPen"):
            # its been uses in a point pen world
            pointToSegmentPen = self._pointToSegmentPen
            del self._pointToSegmentPen
            pointToSegmentPen.endPath()
        else:
            raise PageBotError("path.beginPath() must be called before the path can be used as a point pen")

    def drawToPen(self, pen):
        """Draws the Bézier path into a pen."""
        contours = self.contours

        for contour in contours:
            contour.drawToPen(pen)

    def drawToPointPen(self, pointPen):
        """Draws the Bézier path into a point pen."""
        contours = self.contours

        for contour in contours:
            contour.drawToPointPen(pointPen)

    # Curve.

    def _moveTo(self, p):
        self.commands.append(self.b.moveto(p[0], p[1]))
        point = self.getPoint(p)
        self.addSegment(MOVETO, [point])

    def _lineTo(self, p):
        self.commands.append(self.b.lineto(p[0], p[1]))
        point = self.getPoint(p)
        self.addSegment(LINETO, [point])

    def _curveToOne(self, cp1, cp2, p):
        """
        * cp1: control point 1, off curve.
        * cp2: control point 2, off curve.
        * p: on curve point.
        """
        self.commands.append(self.b.curveto(cp1[0], cp1[1], cp2[0], cp2[1],
            p[0], p[1]))
        cpoint1 = self.getPoint(cp1, onCurve=False)
        cpoint2 = self.getPoint(cp2, onCurve=False)
        point = self.getPoint(p)
        points = [cpoint1, cpoint2, point]
        self.addSegment(CURVETO, points)

    def closePath(self):
        """Closes the path, add the first point to the end of the points
        list."""
        contour = self.contours[-1]
        p0 = contour[0][0]
        point = self.getPoint(p0)
        self.addSegment(CLOSEPATH, [])
        self.addSegment(MOVETO, [point])
        self.commands.append(self.b.closepath)

    def appendPath(self, path):
        """Joins another path with this one.

        TODO: also parse each command and add its points.
        """
        # for command in path.commands:
        # ...
        self.commands += path.commands

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

    def text(self, txt, offset=None, font=None, fontSize=10, align=None):
        """Draws a `txt` with a `font` and `fontSize` at an `offset` in the
        Bézier path. If a font path is given the font will be installed and
        used directly.

        - Optionally an alignment can be set.
        - Possible `align` values are: `"left"`, `"center"` and `"right"`.
        - The default alignment is `left`.
        - Optionally `txt` can be a `FormattedString`.
        """

    def textBox(self, txt, box, font=None, fontSize=10, align=None,
            hyphenation=None):
        """Draws a `txt` with a `font` and `fontSize` in a `box` in the Bézier
        path. If a font path is given the font will be installed and used
        directly.

        - Optionally an alignment can be set.
        - Possible `align` values are: `"left"`, `"center"` and `"right"`.
        - The default alignment is `left`.
        - Optionally `hyphenation` can be provided.
        - Optionally `txt` can be a `FormattedString`.
        - Optionally `box` can be a `BezierPath`.
        """

    # Path operations.

    def getBezierPath(self):
        """Returns the BezierPath."""

    def setBezierPath(self, path):
        """Sets a BezierPath."""

    def pointInside(self, xy):
        """Checks if a point `x`, `y` is inside a path."""

    def bounds(self):
        """Returns the bounding box of the path."""

    def controlPointBounds(self):
        """Returns the bounding box of the path including the offcurve
        points."""

    def optimizePath(self):
        pass

    def copy(self):
        """Copy the Bézier path."""
        return None

    def reverse(self):
        """Reverse the path direction."""

    def appendPath(self, otherPath):
        """Append a path."""
        return None

    # TODO

    def addComponent(self, glyphName, transformation):
        pass

    def arc(self, center, radius, startAngle, endAngle, clockwise):
        pass

    def arcTo(self, point1, point2, radius):
        pass

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
