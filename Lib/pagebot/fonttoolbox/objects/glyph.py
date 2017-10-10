# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#     
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     glyph.py
#
#     Implements a PageBot font classes to get info from a TTFont.
#
import sys
import weakref
from AppKit import NSFont
from fontTools.ttLib import TTFont, TTLibError

# TODO: Needs DrawBot/Flex context.
from drawBot import BezierPath

from fontinfo import FontInfo
from pagebot.fonttoolbox.analyzers import GlyphAnalyzer, APointContext
from pagebot.toolbox.transformer import point2D
from pagebot.fonttoolbox.analyzers.apoint import APoint
from pagebot.fonttoolbox.analyzers.asegment import ASegment

C = 0.5
F = 2.0 / 3.0

class AxisDeltas(object):
    u"""Hold the list of axis parts with their minValue, defaultValue, maxValue and list of deltas."""
    def __init__(self, name):
        self.name = name
        self.deltas = {}

    def __repr__(self):
        return '[AxisDeltas:%s]' % self.name

    def __setitem__(self, key, value):
        assert isinstance(key, tuple) and len(key) == 3 and isinstance(value, (tuple, list))
        self.deltas[key] = value

    def __getitem__(self, key):
        return self.deltas[key]

class Glyph(object):
    u"""The Glyph class wraps the glyph structure of a TrueType Font and
    extracts data from the raw glyph such as point sequence and type.
    >>> import pagebot
    >>> from pagebot.toolbox.transformer import getFontPath
    >>> p = getFontPath('AmstelvarAlpha-VF')
    >>> from pagebot.fonttoolbox.objects.font import Font
    >>> f = Font(p, install=False)
    >>> g = f['a']
    >>> g.name
    'a'
    >>> len(g.points)
    40
    >>> g.points[-1].onCurve
    False
    >>> contours = g.contours
    >>> len(contours)
    2
    >>> path = g.path
    >>> print path
    <BezierPath>
    >>> nspath = path.getNSBezierPath()
    >>> bounds = nspath.bounds()
    >>> print bounds
    <NSRect origin=<NSPoint x=38.0 y=-15.0> size=<NSSize width=948.0 height=1037.0>>
    >>> len(bounds)
    2
    >>> len(bounds[0])
    2
    >>> len(bounds[1])
    2
    >>> print bounds[0]
    <NSPoint x=38.0 y=-15.0>
    >>> bounds[0][0]
    38.0
    """

    GLYPHANALYZER_CLASS = GlyphAnalyzer
    AXIS_DELTAS_CLASS = AxisDeltas

    def __init__(self, font, name):
        self.name = name
        self.font = font # Stored as weakref
        self._analyzer = None # Installed upon request
        self._points = None # Same as self.points property with added 4 spacing points in TTF style.
        self._points4 = None
        self._pointContexts = None
        self._contours = None
        self._segments = None
        self._components = None
        self._path = None # "Expensive", create self.path property value on initialize.
        self._flattenedPath = None # "More expensive", create property value upon request.
        self._flattenedPathPoints = None # "More expensive", create property value upon request.
        self._analyzer = None # Initialized upon property self.analyzer usage.
        self._axisDeltas = None # Caching for AxisDeltas instances.
        self._boundingBox = None # Initialized on property call.

    def __eq__(self, g):
        return self.font is g.font and self.name == g.name

    def __ne__(self, g):
        return not self.font is g.font or self.name != g.name

    def __repr__(self):
        return '<PageBot Glyph %s Pts:%d/Cnt:%d/Cmp:%d>' % (self.name,
            len(self.coordinates), len(self.endPtsOfContours), len(self.components))

    def _initialize(self):
        u"""Initializes the cached data, such as self.points, self.contour,
        self.components and self.path."""
        self._points = []
        self._points4 = [] # Same as self.points property with added 4 spacing points in TTF style.
        self._contours = []
        self._components = []
        self._segments = []
        self._boundingBox = None

        coordinates = self.coordinates
        components = self.components
        flags = self.flags
        endPtsOfContours = set(self.endPtsOfContours)
        openContour = False
        openSegment = None
        currentOnCurve = None
        p0 = None

        minX = minY = sys.maxint # Store bounding box as we process the coordinate.
        maxX = maxY = -sys.maxint

        if coordinates or components:
            # TODO: Needs context for DrawBot/Flex usage
            self._path = path = BezierPath()

        for index, (x, y) in enumerate(coordinates):
            minX = min(x, minX)
            maxX = max(x, maxX)
            minY = min(y, minY)
            maxY = max(y, maxY)

            p = APoint((x, y), flags[index])
            self._points.append(p)

            if not openContour:
                path.moveTo((x, y))
                p0 = p
                currentOnCurve = p
                openContour = []
                self._contours.append(openContour)

            openContour.append(p)

            if not openSegment:
                openSegment = ASegment()
                self._segments.append(openSegment)

            openSegment.append(p)

            # If there is an open segment, it may contain multiple
            # quadratics. Split into cubics.

            if index in endPtsOfContours and openContour:
                # End of contour.
                if openSegment:
                    if not p.onCurve:
                        openSegment.append(p0)

                    currentOnCurve = self._drawSegment(currentOnCurve, openSegment, path)

                path.closePath()
                openContour = None
                openSegment = None

            elif p.onCurve:
                # Inside contour.
                currentOnCurve = self._drawSegment(currentOnCurve, openSegment, path)
                openSegment = None

        self._points4 = self._points[:] + [APoint((minX, 0)), APoint((0, minY)), APoint((maxX, 0)), APoint((0, maxY))]
        self._boundingBox = (minX, minY, maxX, maxY)

    def _get_flattenedPath(self):
        u"""Answer the flattened NSBezier path. 
        TODO: Needs to get DrawBotContext reference, and Flex equivalent."""
        if self._flattenedPath is None:
            self._flattenedPath = self.path.getNSBezierPath().bezierPathByFlatteningPath()
        return self._flattenedPath
    flattenedPath = property(_get_flattenedPath)

    def _get_flattenedPathPoints(self):
        u"""Answer the flattened NSBezier path As contour list [contour, contour, ...] where
        contours are lists of point2D() points.
        TODO: Needs to get DrawBotContext reference, and Flex equivalent."""
        if self._flattenedPathPoints is None:
            contour = []
            self._flattenedPathPoints = [contour]
            flatPath = self.flattenedPath
            for index in range(flatPath.elementCount()): # Typical NSBezierPath size + index call. 
                p = flatPath.elementAtIndex_associatedPoints_(index)[1]
                if p:
                    contour.append((p[0].x, p[0].y)) # Make point2D() tuples.
                else:
                    contour = []
                    self._flattenedPathPoints.append(contour)
        return self._flattenedPathPoints
    flattenedPathPoints = property(_get_flattenedPathPoints)

    #def _get_drawPath(self):
    #    u"""Answer the cached Cocoa drawing path. If it does not yet exist, create it first and cache it."""
    #    if self._drawPath is None:
    #        pen = CocoaPen(None)
            
    def getAxisDeltas(self):
        u"""Answer dictionary of axis-delta relations. Key is axis name, value is an *AxisDeltas* instance.
        The instance containse (minValue, defaultValue, maxValue) keys, holding the sets of deltas for the
        glyph points."""
        if self._axisDeltas is None:
            font = self.font
            self._axisDeltas = {}
            if font is not None:
                axisName = None
                for rawDelta in font.rawDeltas[self.name]:
                    axes = rawDelta.axes
                    assert len(axes) == 1 # Can there be others here?
                    axisName = axes.keys()[0]
                    if not axisName in self._axisDeltas:
                        self._axisDeltas[axisName] = self.AXIS_DELTAS_CLASS(axisName)
                    self._axisDeltas[axisName][tuple(axes[axisName])] = rawDelta.coordinates
        return self._axisDeltas

    def _drawSegment(self, cp, segment, path):
        u"""Draws the Segment instance into the path. It may contain multiple
        quadratics. Split into cubics and lines."""

        if len(segment) == 1:
            # Straight line.
            p1 = segment.points[-1]
            path.lineTo((p1.x, p1.y))
            cp = p1

        elif len(segment) == 2:
            # Converts quadratic curve to cubic.
            p1, p2 = segment.points
            self._drawQuadratic2Cubic(cp.x, cp.y, p1.x, p1.y, p2.x, p2.y, path)
            cp = p2

        else:
            # Handles implied on-curve points.
            for n in range(len(segment)-1):
                p0 = cp # Previous oncurve.
                p1 = segment.points[n] # next offcurve.
                p2 = segment.points[n+1] # offcurve or last point.

                if n < len(segment) - 2:
                    # Implied point.
                    m = APoint((p1.x + (p2.x - p1.x) / 2, p1.y + (p2.y - p1.y) / 2), True)
                else:
                    # Last (oncurve) point.
                    m = p2

                self._drawQuadratic2Cubic(cp.x, cp.y, p1.x, p1.y, m.x, m.y, path)
                cp = m

        return cp

    def _drawQuadratic2Cubic(self, p0x, p0y, p1x, p1y, p2x, p2y, path):
        u"""Converts a quatratic control point into a cubic.

        p0 = onCurve0
        p1 = offCurve
        p2 = onCurve1
        """

        # Cubic control points.
        pp0x = p0x + (p1x - p0x) * F
        pp0y = p0y + (p1y - p0y) * F
        pp1x = p2x + (p1x - p2x) * F
        pp1y = p2y + (p1y - p2y) * F
        path.curveTo((pp0x, pp0y), (pp1x, pp1y), (p2x, p2y))

    def _get_ttGlyph(self):
        return self.font.ttFont['glyf'][self.name]
    ttGlyph = property(_get_ttGlyph)

    def _set_font(self, font):
        self._font = weakref.ref(font)
    def _get_font(self):
        if self._font is not None:
            return self._font()
        return None
    font = property(_get_font, _set_font)

    def _get_width(self):
        try:
            return self.font.ttFont['hmtx'][self.name][0]
        except KeyError:
            return None # Glyph is undefined in hmtx table.
    def _set_width(self, width):
        hmtx = list(self.font.ttFont['hmtx'][self.name]) # Keep vertical value
        hmtx[0] = width
        self.font.ttFont['hmtx'][self.name] = hmtx
    width = property(_get_width, _set_width)

    # Direct TTFont cooridinates compatibility

    def _get_coordinates(self):
        u"""Answers the ttFont.coordinates, if it exists. Otherwise answer None.
        Note that this is the “raw” list of (x, y) positions, without
        information on contour index or if the point is on/off curve. This
        information is stored in ttFont.endPtsOfContours and ttFont.flags.
        This property is only for low-level access of the coordinates. For
        regular use, self.points and self.contours are available. Also notice
        that writing the list is at “own risk”, e.g hinting and related tables
        are not automatically updated."""
        if hasattr(self.ttGlyph, 'coordinates'):
            return self.ttGlyph.coordinates
        return [] # No coordinates in the TTGlyph
    def _set_coordinates(self, coordinates):
        self.ttGlyph.coordinates = coordinates
    coordinates = property(_get_coordinates, _set_coordinates)

    def _get_endPtsOfContours(self):
        if hasattr(self.ttGlyph, 'endPtsOfContours'):
            return self.ttGlyph.endPtsOfContours
        return [] # No endPtsOfContours in the TTGlyph
    def _set_endPtsOfContours(self, endPtsOfContours):
        self.ttGlyph.endPtsOfContours = endPtsOfContours
    endPtsOfContours = property(_get_endPtsOfContours, _set_endPtsOfContours)

    def _get_flags(self):
        if hasattr(self.ttGlyph, 'flags'):
            return self.ttGlyph.flags
        return [] # No flags in the TTGlyph
    def _set_flags(self, flags):
        self.ttGlyph.flags = flags
    flags = property(_get_flags, _set_flags)

    # Kind of RoboFont glyph compatibility

    def _get_points(self): 
        u"""Answer the list of Point instances, representing the outline of the glyph,
        not including the standard 4 spacing points at the end of the list in TTF style.
        Read only for now."""
        if self._points is None:
            self._initialize()
        return self._points
    points = property(_get_points)

    def _get_points4(self):
        u"""Answer the list of Points instances, representing the outline of the glyph,
        including the standard 4 spacing points at the end of the list in TTF style.
        Read only for now."""
        if self._points4 is None:
            self._initialize()
        return self._points4
    points4 = property(_get_points4)

    def _get_pointContexts(self):
        if self._pointContexts is None:
            self._pointContexts = []
            for cIndex, contour in enumerate(self.contours):
                #openPointContext = PointContext # Instance as tuple of points -3, -2, -1, 0, 1, 2, 3 contour index
                #def __init__(self, points, index, contourIndex, clockwise, glyphName=None):
                #self._pointContexts.append(openPointContext)
                numPoints = len(contour)
                contour3 = contour+contour+contour
                for pIndex in range(numPoints):
                    points = contour3[pIndex+numPoints-3:pIndex+numPoints+4]
                    pc = APointContext(points, pIndex, cIndex )
                    self._pointContexts.append(pc)
        return self._pointContexts
    pointContexts = property(_get_pointContexts)

    def _get_contours(self): # Read only for now. List of Point instance lists.
        if self._contours is None:
            self._initialize()
        return self._contours
    contours = property(_get_contours)

    def _get_segments(self): # Read only for now. List of Segment instance lists.
        if self._segments is None:
            self._initialize()
        return self._contours
    segments = property(_get_contours)

    def _get_components(self): # Read only for now. List Contour instances.
        if self._components is None:
            self._initialize()
        return self._components
    components = property(_get_components)

    def _get_path(self): # Read only for now.
        if self._path is None:
            self._initialize()
        return self._path
    path = property(_get_path)

    def _get_analyzer(self): # Read only for now.
        if self._analyzer is None:
            self._analyzer = self.GLYPHANALYZER_CLASS(self)
        return self._analyzer
    analyzer = property(_get_analyzer)

    def onBlack(self, p):
        u"""Answers the boolean flag is the single point (x, y) is on black."""
        p = point2D(p)
        return self.path._path.containsPoint_(p)

    def _get_minX(self):
        return self.boundingBox[0]
    minX = property(_get_minX)
    
    def _get_minY(self):
        return self.boundingBox[1]
    minY = property(_get_minY)
    
    def _get_maxX(self):
        return self.boundingBox[2]
    maxX = property(_get_maxX)
    
    def _get_maxY(self):
        return self.boundingBox[3]
    maxY = property(_get_maxY)
    
    def _get_boundingBox(self):
        if self._boundingBox is None:
            self._initialize()
        return self._boundingBox
    boundingBox = property(_get_boundingBox)

    """
    TTGlyph Functions to implement

 |  Methods defined here:
 |
 |  __getitem__(self, componentIndex)
 |
 |  __init__(self, data='')
 |
  |
 |  compact(self, glyfTable, recalcBBoxes=True)
 |
 |  compile(self, glyfTable, recalcBBoxes=True)
 |
 |  compileComponents(self, glyfTable)
 |
 |  compileCoordinates(self)
 |
 |  compileDeltasGreedy(self, flags, deltas)
 |
 |  compileDeltasOptimal(self, flags, deltas)
 |
 |  decompileComponents(self, data, glyfTable)
 |
 |  decompileCoordinates(self, data)
 |
 |  decompileCoordinatesRaw(self, nCoordinates, data)
 |
 |  draw(self, pen, glyfTable, offset=0)
 |
 |  expand(self, glyfTable)
 |
 |  fromXML(self, name, attrs, content, ttFont)
 |
 |  getComponentNames(self, glyfTable)
 |
 |  getCompositeMaxpValues(self, glyfTable, maxComponentDepth=1)
 |
 |  getCoordinates(self, glyfTable)
 |
 |  getMaxpValues(self)
 |
 |  isComposite(self)
 |      Can be called on compact or expanded glyph.
 |
 |  recalcBounds(self, glyfTable)
 |
 |  removeHinting(self)
 |
 |  toXML(self, writer, ttFont)
 |
 |  trim(self, remove_hinting=False)
 |      Remove padding and, if requested, hinting, from a glyph.
 |      This works on both expanded and compacted glyphs, without
 |      expanding it.
    """
