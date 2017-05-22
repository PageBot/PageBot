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
#     glyph.py
#
#     Implements a PageBot font classes to get info from a TTFont.
#
import weakref
from AppKit import NSFont
from fontTools.ttLib import TTFont, TTLibError
from drawBot import BezierPath
from fontinfo import FontInfo
from pagebot.fonttoolbox.analyzers.glyphanalyzer import GlyphAnalyzer
from pagebot.toolbox.transformer import point2D

C = 0.5
F = 2.0 / 3.0

class Point(object):
    def __init__(self, x, y, onCurve):
        self.x = x
        self.y = y
        self.onCurve = bool(onCurve)

    def __repr__(self):
        return 'Pt(%s,%s,%s)' % (self.x, self.y,{True:'On', False:'Off'}[self.onCurve])

class Segment(object):
    def __init__(self, points=None):
        if points is None:
            points = []
        self.points = points

    def __len__(self):
        return len(self.points)

    def __repr__(self):
        return 'Sg(%s)' % self.points

    def append(self, p):
        self.points.append(p)

class Glyph(object):
    u"""This Glyph class is a wrapper around the glyph structure of a ttFont.
    It is supposed to copy the functions of the RoboFont raw glyph, for all
    needed functions in PageBot. It is not complete, will be added to when
    needed."""

    ANALYZER_CLASS = GlyphAnalyzer

    def __init__(self, font, name):
        self.name = name
        self.parent = font # Stored as weakref
        self._points = None
        self._pointContexts = None
        self._contours = None
        self._segments = None
        self._components = None
        self._path = None
        self._analyzer = None # Initialized upon property self.analyzer usage.

    def __eq__(self, g):
        return self.parent is g.parent and self.name == g.name

    def __ne__(self, g):
        return not self.parent is g.parent or self.name != g.name

    def __repr__(self):
        return '<PageBot Glyph %s Pts:%d/Cnt:%d/Cmp:%d>' % (self.name,
            len(self.coordinates), len(self.endPtsOfContours), len(self.components))

    def _initialize(self):
        u"""Initialize the cached data, such as self.points, self.contour, self.components and self.path."""
        self._points = []
        self._contours = []
        self._components = []
        self._segments = []

        coordinates = self.coordinates
        components = self.components
        flags = self.flags
        endPtsOfContours = set(self.endPtsOfContours)
        openContour = False
        openSegment = None
        currentOnCurve = None
        p0 = None

        if coordinates or components:
            self._path = path = BezierPath() # There must be points and/or components, start path

        for index, (x, y) in enumerate(coordinates):
            #if index > 6:
            #    break
            p = Point(x, y, flags[index])
            self._points.append(p)

            if not openContour:
                path.moveTo((x, y))
                p0 = p
                currentOnCurve = p
                openContour = []
                self._contours.append(openContour)

            openContour.append(p)

            if not openSegment:
                openSegment = Segment()
                self._segments.append(openSegment)

            openSegment.append(p)

            #start = index - 1 in self.endPtsOfContours
            # If there is an open segment, it may contain multiple
            # quadratics. Split into cubics.

            if index in endPtsOfContours and openContour:
                # End of contour.
                if openSegment:
                    openSegment.append(p0)
                    currentOnCurve = self._drawSegment(currentOnCurve, openSegment, path)

                path.closePath()
                openContour = None
                openSegment = None
                print 'new seg, new contour'

            elif p.onCurve:
                # Inside contour.
                currentOnCurve = self._drawSegment(currentOnCurve, openSegment, path)
                #currentOnCurve = p
                openSegment = None
                print 'new seg'


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
            print 'third option', segment.points

            # handle implied on-curve points.
            for n in range(len(segment)-1):
                p0 = cp # Previous oncurve.
                p1 = segment.points[n] # next offcurve.
                p2 = segment.points[n+1] # offcurve or last point.

                if n < len(segment) - 2:
                    # Implied point.
                    m = Point(p1.x + (p2.x - p1.x) / 2, p1.y + (p2.y - p1.y) / 2, True)
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
        return self.parent.ttFont['glyf'][self.name]
    ttGlyph = property(_get_ttGlyph)

    def _set_parent(self, font):
        self._parent = weakref.ref(font)
    def _get_parent(self):
        if self._parent is not None:
            return self._parent()
        return None
    parent = property(_get_parent, _set_parent)

    def _get_width(self):
        return self.parent.ttFont['hmtx'][self.name][0]
    def _set_width(self, width):
        hmtx = list(self.parent.ttFont['hmtx'][self.name]) # Keep vertical value
        hmtx[0] = width
        self.parent.ttFont['hmtx'][self.name] = hmtx
    width = property(_get_width, _set_width)

    # Direct TTFont cooridinates compatibility

    def _get_coordinates(self):
        u"""Answer the ttFont.coordinates, if it exists. Otherwise answer None. Note that this is the
        “raw” list of (x, y) positions, without information on contour index or if the point is on/off curve.
        This information is stored in ttFont.endPtsOfContours and ttFont.flags. This property is only for low-level
        access of the coordinates. For regular use, self.points and self.contours are available.
        Also notice that writing the list is at “own risk”, e.g hinting and related tables are not automatically
        updated."""
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

    def _get_points(self): # Read only for now.
        if self._points is None:
            self._initialize()
        return self._points

    points = property(_get_points)

    def _get_pointContexts(self):
        if self._pointContexts is None:
            self._pointContexts = []
            for cIndex, contour in enumerate(self.contours):
                openPointContext = {} # Tuples of points -3, -2, -1, 0, 1, 2, 3 contour index
                self._pointContexts.append(openPointContext)
                numPoints = len(contour)
                contour3 = contour+contour+contour
                for n in range(numPoints):
                    openPointContext[n] = contour3[n+numPoints-3:n+numPoints+4]
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
            self._analyzer = self.ANALYZER_CLASS(self)
        return self._analyzer
    analyzer = property(_get_analyzer)

    def onBlack(self, p):
        u"""Answers the boolean flag is the single point (x, y) is on black."""
        p = point2D(p)
        return self.path._path.containsPoint_(p)

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
