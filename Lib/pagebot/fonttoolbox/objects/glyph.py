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
#     glyph.py
#
#     Implements a PageBot font classes to get info from a TTFont.
#
import sys
import weakref

from pagebot.constants import XXXL
from pagebot.fonttoolbox.analyzers import GlyphAnalyzer, APointContext
from pagebot.fonttoolbox.analyzers.apoint import APoint
from pagebot.fonttoolbox.analyzers.asegment import ASegment
from pagebot.fonttoolbox.analyzers.acomponent import AComponent

F = 2.0 / 3.0
C = 0.5

class AxisDeltas:
    """Hold the list of axis parts with their minValue, defaultValue, maxValue and list of deltas."""
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

class Glyph:
    """The Glyph class wraps the glyph structure of a TrueType Font and
    extracts data from the raw glyph such as point sequence and type.

    >>> from pagebot.fonttoolbox.objects.font import findFont
    >>> f = findFont('RobotoDelta-VF') # Keep font alive to glyph.font weakref
    >>> g = f['a']
    >>> g.name
    'a'
    """

    """
    >>> len(g.points)
    46
    >>> g.points[-1].onCurve
    False
    >>> contours = g.contours
    >>> len(contours)
    2
    >>> g = f['agrave']
    >>> g.components
    [Cmp(a, 0, 0), Cmp(grave, 51, 0)]
    >>> g.getComponentNames()
    ['a', 'grave']

    """
    GLYPHANALYZER_CLASS = GlyphAnalyzer
    AXIS_DELTAS_CLASS = AxisDeltas

    def __init__(self, font, name):

        self.name = name
        self.font = font # Stored as weakref
        self.dirty = True # Mark that we need initialization or something changed in the points.

        self._analyzer = None # Installed upon request
        self._points = None # Same as self.points property with added 4 spacing points in TTF style.
        self._points4 = None
        self._pointContexts = None
        self._contours = None
        self._segments = None
        self._components = None
        self._cubic = None
        self._analyzer = None # Initialized upon property self.analyzer usage.
        self._axisDeltas = None # Caching for AxisDeltas instances.
        self._boundingBox = None # Initialized on property call.
        self._box = None

    def __eq__(self, g):
        return self.font is g.font and self.name == g.name

    def __ne__(self, g):
        return not self.font is g.font or self.name != g.name

    def __repr__(self):
        return '<PageBot Glyph %s Pts:%d/Cnt:%d/Cmp:%d>' % (self.name,
            len(self.coordinates), len(self.endPtsOfContours), len(self.components))

    def __getitem__(self, contourIndex):
        if self._contours is None:
            self._initialize()
        return self._contours[contourIndex]

    def _initialize(self):
        """Initializes the cached data, such as points, contours, components,
        segments and bounding box. """
        self._points = []

        # Same as self.points property with added 4 spacing points in TTF
        # style.
        self._points4 = []
        self._contours = []
        self._segments = []
        self._cubic = []
        self._boundingBox = None

        components = self.components
        coordinates = self.coordinates

        if coordinates or components:
            minX = minY = XXXL # Store bounding box as we process the coordinate.
            maxX = maxY = -XXXL
        else:
            minX = minY = maxX = maxY = 0

        for component in components:
            componentName = component.baseGlyph
            if componentName in self.font.keys():
                componentGlyph = self.font[componentName]
                self._cubic.append(('component', ((component.x, component.y), componentGlyph)))

                # Expand bounding box.
                cMinX, cMinY, cMaxX, cMaxY = componentGlyph.boundingBox
                minX = min(cMinX+component.x, minX)
                minY = min(cMinY+component.y, minY)
                maxX = max(cMaxX+component.x, maxX)
                maxY = max(cMaxY+component.y, maxY)

        flags = self.flags
        openContour = False
        openSegment = None
        currentOnCurve = None
        endPtsOfContours = set(self.endPtsOfContours)
        p0 = None

        for index, (x, y) in enumerate(coordinates):
            # Expand bounding box.
            minX = min(x, minX)
            maxX = max(x, maxX)
            minY = min(y, minY)
            maxY = max(y, maxY)

            # Create APoint, to store weakref to self and index for altering
            # the coordinate and onCurve.
            p = APoint((x, y), flags[index], self, index)
            self._points.append(p)

            if not openContour:
                # Also store as cubic command.
                self._cubic.append(('moveTo', (x, y)))
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

                    currentOnCurve = self.expandSegment(currentOnCurve, openSegment)
                self._cubic.append(('closePath', None))
                openContour = None
                openSegment = None

            elif p.onCurve:
                # Inside contour.
                currentOnCurve = self.expandSegment(currentOnCurve, openSegment)
                openSegment = None

        # Add 4 spacing points, as default in TTF. No index, as they cannot be
        # written back. Instead, for writing, use self.leftMargin,
        # self.rightMargin and self.width.
        self._points4 = self._points[:] + [
            APoint((minX, 0), glyph=self),
            APoint((0, minY), glyph=self),
            APoint((maxX, 0), glyph=self),
            APoint((0, maxY), glyph=self)
        ]

        self._boundingBox = (minX, minY, maxX, maxY)
        self.dirty = False # All cleaned up.

    def update(self):
        """Update the font if it became dirty by changing cooridinates.
        Otherwise ignore. Note that in case the caller cache points, contours,
        components, etc. these are no longer valid."""
        if self.dirty:
            self._initialize()

    def getAxisDeltas(self):
        """Answers dictionary of axis-delta relations. Key is axis name, value
        is an *AxisDeltas* instance. The instance containse (minValue,
        defaultValue, maxValue) keys, holding the sets of deltas for the glyph
        points."""
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

    def expandSegment(self, cp, segment):
        """Expands the Segment instance. It may contain multiple quadratics.
        Split into cubics and lines."""

        if len(segment) == 1:
            # Straight line.
            p1 = segment.points[-1]
            self._cubic.append(('lineTo', (p1.x, p1.y)))
            cp = p1

        elif len(segment) == 2:
            # Converts quadratic curve to cubic.
            p1, p2 = segment.points
            self.expandQuadratic2Cubic(cp.x, cp.y, p1.x, p1.y, p2.x, p2.y)
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

                self.expandQuadratic2Cubic(cp.x, cp.y, p1.x, p1.y, m.x, m.y)
                cp = m

        return cp

    def expandQuadratic2Cubic(self, p0x, p0y, p1x, p1y, p2x, p2y):
        """Converts a quadtratic control point into a cubic curve-to segment.

        p0 = onCurve0
        p1 = offCurve
        p2 = onCurve1
        """

        # First cubic offcurve control points.
        pp0x = p0x + (p1x - p0x) * F
        pp0y = p0y + (p1y - p0y) * F

        # Second cubic offcurve control points.
        pp1x = p2x + (p1x - p2x) * F
        pp1y = p2y + (p1y - p2y) * F

        # i.e. curve-to (offCurve0, offCurve1, onCurve1)
        self._cubic.append(('curveTo', ((pp0x, pp0y), (pp1x, pp1y), (p2x, p2y))))

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
        """TODO: Does not seem to work. How about saving the font?"""
        hmtx = list(self.font.ttFont['hmtx'][self.name]) # Keep vertical value
        hmtx[0] = width
        self.font.ttFont['hmtx'][self.name] = hmtx
    width = property(_get_width, _set_width)

    def _get_leftMargin(self):
        return self.minX
    leftMargin = property(_get_leftMargin)

    def _get_rightMargin(self):
        return self.width - self.maxX
    rightMargin = property(_get_rightMargin)

    def isClockwise(self, contour):
        """Answers Contour direction. Simple and fast.

        http://stackoverflow.com/questions/1165647/how-to-determine-if-a-list-of-polygon-points-are-in-clockwise-order
        """
        total = 0
        for index, point in enumerate(contour):
            p = contour[index-1] # Takes last point of list if index == 0 :)
            total += (point.x - p.x) * (point.y + p.y)
        return total > 0

    # Direct TTFont coordinates compatibility

    def _get_coordinates(self):
        """Answers the ttFont.coordinates, if it exists, as GlyphCoordinates
        instance. Otherwise answer None. Note that this is the “raw” list of
        (x, y) positions, without information on contour index or if the point
        is on/off curve. This information is stored in ttFont.endPtsOfContours
        and ttFont.flags. This property is only for low-level access of the
        coordinates. For regular use, self.points and self.contours are
        available. Also notice that writing the list is at “own risk”, e.g
        hinting and related tables are not automatically updated."""
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

    def __len__(self):
        return len(self.contours)

    def _get_points(self):
        """Answers the list of APoint instances, representing the outline of
        the glyph, not including the standard 4 spacing points at the end of
        the list in TTF style.  Read only for now. Although APoints are
        constructed from the self.ttFont coordinates, they keep a weakref to
        the glyph and their index. This way point positions in the self.ttFont
        can be modified."""
        if self._points is None or self.dirty:
            self._initialize()
        return self._points
    points = property(_get_points)

    def _get_points4(self):
        """Answers the list of APoints instances, representing the outline of
        the glyph, including the standard 4 spacing points at the end of the
        list in TTF style.  Read only for now. Although APoints are constructed
        from the self.ttFont coordinates, they keep a weakref to the glyph and
        their index. This way point positions in the self.ttFont can be
        modified."""
        if self._points4 is None or self.dirty:
            self._initialize()
        return self._points4
    points4 = property(_get_points4)

    def _get_pointContexts(self):
        if self._pointContexts is None or self.dirty:
            self._pointContexts = []
            for cIndex, contour in enumerate(self.contours):
                #openPointContext = PointContext # Instance as tuple of points -3, -2, -1, 0, 1, 2, 3 contour index
                #def __init__(self, points, index, contourIndex, clockwise, glyphName=None):
                #self._pointContexts.append(openPointContext)
                numPoints = len(contour)
                contour3 = contour+contour+contour
                for pIndex in range(numPoints):
                    points = contour3[pIndex+numPoints-3:pIndex+numPoints+4]
                    if not points:
                        break # Nothing here, back out.
                    # Make sure number of points is 7, otherwise extend by
                    # doubling on both ends.
                    while len(points) < 7:
                        # Alternate left-right, until we reach exact 7 point
                        # contexts.
                        points = [points[0]] + points
                        if len(points) < 7:
                            points = points + [points[-1]]
                    pc = APointContext(points, pIndex, cIndex )
                    self._pointContexts.append(pc)
        return self._pointContexts
    pointContexts = property(_get_pointContexts)

    def _get_contours(self): # Read only for now. List of Point instance lists.
        if self._contours is None or self.dirty:
            self._initialize()
        return self._contours
    contours = property(_get_contours)

    def _get_segments(self): # Read only for now. List of Segment instance lists.
        if self._segments is None or self.dirty:
            self._initialize()
        return self._segments

    segments = property(_get_segments)

    def _get_cubic(self):
        if self._cubic is None or self.dirty:
            self._initialize()
        return self._cubic

    cubic = property(_get_cubic)

    def _get_components(self): # Read only for now. List Contour instances.
        if self._components is None or self.dirty:
            self._components = []
            self.ttGlyph.expand(self.font.ttFont['glyf'])
            # Initialize the AComponent wrappers
            if hasattr(self.ttGlyph, 'components'):
                for ttComponent in self.ttGlyph.components:
                    self._components.append(AComponent(ttComponent))

        return self._components
    components = property(_get_components)

    def getComponentNames(self):
        componentNames = []
        for component in self.components:
            componentNames.append(component.baseGlyph)
        return componentNames

    def _get_variables(self):
        """Answers the axis-deltas for this glyph. Answer an None if there are
        no deltas for this glyph or if the parent is not a Var-font.

        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> from pagebot.fonttoolbox.objects.font import getFont
        >>> fontPath = getTestFontsPath()
        >>> path = fontPath + '/fontbureau/Amstelvar-Roman-VF.ttf'
        >>> font = getFont(path) # Keep font alive to glyph.font weakref
        >>> glyph = font['H']
        """

        """
        TODO: Get more docTests to work
        >>> variables = glyph.variables
        >>> sorted(glyph.variables.keys())
        ['GRAD', 'XOPQ', 'XTRA', 'YOPQ', 'YTRA', 'YTSE', 'YTUC', 'opsz', 'wdth', 'wght']
        >>> axis, deltas = variables['GRAD']
        >>> axis
        {'GRAD': (0.0, 1.0, 1.0)}
        >>> deltas[:6]
        [(0, 0), None, (52, 0), None, None, (89, 0)]
        """
        return self.font.variables.get(self.name) # Answer None if variations for this glyph don't exist.
    variables = property(_get_variables)

    def _get_analyzer(self):
        if self._analyzer is None:
            self._analyzer = self.GLYPHANALYZER_CLASS(self)
        return self._analyzer
    analyzer = property(_get_analyzer) # Read only for now.

    def _get_box(self):
        u"""Answers the bounding box as defined by self.ttGlyph boundaries.
        """
        if self._box is None:
            self._box = (self.ttGlyph.xMin, self.ttGlyph.yMin, self.ttGlyph.xMax, self.ttGlyph.yMax)
        return self._box
    box = property(_get_box) # Read only for now.

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
        if self._boundingBox is None or self.dirty:
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

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
