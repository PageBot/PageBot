# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     glyphanalyzer.py
#
import time
import traceback
import weakref
from AppKit import NSPoint
from math import sqrt

from defcon.objects.glyph import Glyph as DefconGlyph
from tnbits.objects.component import Component
from tnbits.constants import Constants
from tnbits.constantsparts.smartsets import SS_ACCENTSCMB, ANCHOR_TOP
from tnbits.toolbox.transformer import TX
from tnbits.floqmodel.objects.glyph import getComponents, getPoints
from tnbits.analyzers.elements.pointanalyzer import PointAnalyzer
from tnbits.analyzers.elements.pointcontextlist import Vertical, Horizontal
from tnbits.analyzers.elements.stems import Stem, Bar, Counter, VerticalCounter, Width, DiagonalStem
from tnbits.analyzers.elements.boundingbox import BoundingBox
from tnbits.analyzers.elements.pointcontext import PointContext
from tnbits.analyzers.elements.nakedwrapper import NakedWrapper
from tnbits.analyzers.memes.location import Location

DEBUG = False

UP = 1
UNDEFINED = 0
DOWN = -1

SPANSTEP = 4

class GlyphAnalyzer(PointAnalyzer):
    u"""The GlyphAnalyzer analyzes the defcon glyph and find key measures
    about its outline or components."""
    C = Constants

    VERTICALCLASS = Vertical # Allow inheriting classes to change this
    HORIZONTALCLASS = Horizontal
    STEMCLASS = Stem
    BARCLASS = Bar
    COUNTERCLASS = Counter
    VCOUNTERCLASS = VerticalCounter
    DIAGONALSTEMCLASS = DiagonalStem
    WIDTHCLASS = Width
    BOUNDINGBOXCLASS = BoundingBox
    POINTCONTEXTCLASS = PointContext

    # See also SmartSets SS_ACCENTSCMD. TODO: Combine as import to make
    # additions more consistent?
    # from tnbits.constantparts.smartsets import SS_ACCENTSCMD
    DIACRITICS = set()
    TOPDIACRITICS = set()
    for anchorName, (_, anchorY) in SS_ACCENTSCMB.items():
        if anchorName.endswith('cmb'):
            anchorName = anchorName[:-3]
        DIACRITICS.add(anchorName)
        if anchorY == ANCHOR_TOP: # Name of anchor in accent glyph.
            TOPDIACRITICS.add(anchorName)

    def __init__(self, parent, name, fuzz=None):
        self.fuzz = fuzz or self.initializeFuzz()
        self.resetGlyph(parent, name)

    # A T T R I B U T E S

    def get(self, attribute):
        u"""
        Dispatches the attribute name from hook method.
        """
        if hasattr(self, attribute):
            return getattr(self, attribute)()
        return None

    def __repr__(self):
        glyph = self.glyph
        return '[%s of "%s"]' % (self.__class__.__name__, glyph.name)

    def resetGlyph(self, parent, name):
        u"""Initializes the GlyphAnalyzer from the no-overlap layer. We have
        to decide what happens if it exists but we don't know if it is up to
        date. How slow would it be always to generate a new no-overlap?"""
        self.parent = parent
        self.name = name
        self.reset()

    def reset(self):
        self._decomposedName = None # Decompose the name into baseName, diacritics and extensions
        self._components = None
        self._contourDirections = None
        self._pointContexts = None
        self._overlappingPoints = None
        self._boundingBox = None
        self._boundings = None # Holds the cache of self.boundings, 4-tuple of (x1, y1, x2, y2)
        self._italicBoundings = None # Holds cache of the self.italicBounding, where x values are projected on x-axis.
        self._sideBearings = None
        #self._scanlineProfiles = None # Cache profile of scan lines for sides/types
        self._gaussProfiles = None # Cache profile from Gaussian photon counts.
        self._diagonals = None # Recognized diagonals, not filtered by FloqMemes
        self._inflections = None
        self._heights = None

        self._verticals = None
        self._stems = None # Recognized stems, so not filtered by FloqMemes
        self._roundStems = None # Recognized round stems, not filtered by FloqMemes
        self._allHorizontalCounters = None # Collection of counters of all neighboring stems.
        self._allStems = None
        self._allStemsCounters = None # Collection of all types of stems and all their in-between counters.
        self._allStemsCountersComponents = None # Collection of _allStemsCounters and collection of all component dimensions.
        self._straightRoundStems = None # Stems from round extreme on one side and straight on the other side.

        self._horizontals = None
        self._bars = None # Recognized bars, so not filtered by FloqMemes
        self._roundBars = None # Recognized round bars, so not filtered by FloqMemes
        self._allVerticalCounters = None
        self._allBars = None
        self._allBarsCounters = None # Collection of all types of bars and all their in-between counters.
        self._allBarsCountersComponents = None # Collection of _allBarsCounters and collection of all component dimensions.
        self._straightRoundBars = None
        self._roundOvershoots = None # Storage of round extreme overshoots.

        self._leftBeamMargin = None
        self._rightBeamMargin = None

        self._serifs = None
        self._terminals = None
        self._hints = None

        '''
        Unfortunately we have to clear the glyphPath here, as the glyph outline
        may have changed (resulting in the reset request). Is there a way of
        testing if if really changed? And is that worth checking, as normally
        generating the glyph path is a very fast operation by Cocoa.
        self._glyphPath is initialized again upon request for self.glyphPath.
        The glyph path is stored for fast response if a point is inside the
        black on the contour or not.
        '''
        self._glyphPath = None

    def initialize(self):
        u"""Whoever gets called first, this will do the initializing of the
        cached values."""
        self._boundingBox = self.BOUNDINGBOXCLASS() # Will be filled upon initialization of the next.
        self._components = []
        self.initializeComponents()
        self._pointContexts = []
        self.initializePointContexts()
        self._contourDirections = []

    def initializeFuzz(self):
        u"""The @initializeFuzz@ method answers the @FUZZ@ value: the amount
        that values can be off and still be treated as the same."""
        return self.FUZZ

    def intersectWithLine(self, glyph, line, canHaveComponent=False):
        # TODO: test if we can make canHaveComponent default True
        # TODO: Make the analyzers independent from RoboFont code.
        from mojo.tools import IntersectGlyphWithLine
        return IntersectGlyphWithLine(glyph, line, canHaveComponent=canHaveComponent)

    def validate(self):
        u"""Run several tests on the glyph and answer a list with report
        lines."""
        errors = []
        style = self.glyph.getParent()

        for component in getComponents(self.glyph):
            if not component.baseGlyph in style:
                errors.append('Glyph "%s" component base "%s" missing.' % (self.glyph.name, component.baseGlyph))

        return errors

    def _get_glyphPath(self):
        u"""Cache the path for fast point inside/outside query."""
        if self._glyphPath is None: # Not yet initialized?
            self._glyphPath = self.glyph.getRepresentation("defconAppKit.NSBezierPath")

        return self._glyphPath

    glyphPath = property(_get_glyphPath)

    def isEqualShape(self, glyph):
        u"""Answers the boolean flag if glyph is the same as the glyph of
        self, ignoring the sidebearings and correcting the position of the
        bounding box on the left side bearing."""
        # Test equality of the components.
        lsb1 = glyph.leftMargin
        lsb2 = self.leftMargin

        if None in (lsb1, lsb2):
            return lsb1 == lsb2 # True if both are None

        components1 = getComponents(glyph)
        components2 = getComponents(self.glyph)

        if not None in (components1, components2):
            if len(components1) != len(components2):
                return False # Quick check
            for index, component1 in enumerate(components1):
                component2 = components2[index]
                if component1.baseGlyph != component2.baseGlyph or\
                   component1.transformation[-2]-lsb1 != component2.transformation[-2]-lsb2 or\
                   component1.transformation[-1] != component2.transformation[-1]:
                    return False

        # Test equality of the points.
        points1 = getPoints(glyph)
        points2 = getPoints(self.glyph)

        if not None in (points1, points2):
            if len(points1) != len(points2):
                return False # Quick check
            for index, point1 in enumerate(points1):
                point2 = points2[index]
                if point1.x-lsb1 != point2.x-lsb2 or\
                   point1.y != point2.y:
                     return False
        return True

    def __eq__(self, glyph):
        u"""Answers the boolean flag if glyph is the same as the glyph of
        self."""
        return self.isEqualShape(glyph)

    def getAnalyzer(self, name):
        u"""Answers the analyzer of the another glyph, through the parent,
        inside the font of self."""
        # TODO: Needs to extended later to get the analyzer of a layer.
        return self.parent.get(name)

    # self.decomposedName

    def _getDecomposedBaseName(self, name, result=None):
        u"""Deconstructs the name, starting from the right side, recognizing
        chunks that are diacritics names. Recursively adds as many as possible.
        Once there is no match, the remaining left part must be the base name
        of the glyph. Recursively answers the baseName and the list of found
        diacritics. In the "altBaseName" result attribute. The caller gets
        translated "i" and "j" into "dotlessi" and "dotlessj" info for lc only.
        For capitals and smallcaps the main base name is used."""
        if result is None:
            result = []

        for index in range(1, len(name)):
            diacritics = name[-index:]
            if diacritics in self.DIACRITICS:
                result = [diacritics] + result
                return self._getDecomposedBaseName(name[:-index], result)
        return name, result

    def _get_decomposedName(self):
        u"""Decomposes the glyph name into a dict, holding name, baseName, a
        list of diacritics and a list of extensions, by splitting on
        glyph/accent name patterns. Exceptions to this method are ('Thorn' and
        'thorn')."""
        if self._decomposedName is None:
            if self.name in ('Thorn', 'thorn') or self.name.startswith('.'):
                self._decomposedName = dict(name=self.name, baseName=self.name, altBaseName=self.name,
                    coreName=self.name, diacritics=[], srcName=self.name, extensions=[])
            else:
                parts = self.name.split('.') # Agrave.sc --> ['Agrave', 'sc']
                extensions = parts[1:]
                baseName, diacritics = self._getDecomposedBaseName(parts[0])
                srcName = self.name.split('.')[0] # Hbar.sc --> Hbar

                # If the baseName is "i" or "j" make altBaseName into
                # "dotlessi" or "dotlessj" of it is combined with a top accent.
                # Otherwise altBaseName is equal to baseName. And also ignore if this is a smallcap.
                if not 'sc' in extensions and baseName in ('i', 'j') and self.TOPDIACRITICS.intersection(set(diacritics)):
                    altBaseName = 'dotless'+baseName # Make alternative baseName
                elif 'sc' in extensions:
                    altBaseName = baseName + '.sc'
                elif 'dnom' in extensions:
                    altBaseName = baseName + '.dnom'
                elif 'sups' in extensions:
                    altBaseName = baseName + '.sups'
                elif 'sinf' in extensions:
                    altBaseName = baseName + '.sinf'
                elif 'uc' in extensions:
                    altBaseName = baseName + '.uc'
                elif 'lc' in extensions:
                    altBaseName = baseName + '.lc'
                else:
                    altBaseName = baseName
                coreName = baseName
                if extensions: # Put them back on the base name
                    baseName += '.' + '.'.join(extensions)
                self._decomposedName = dict(name=self.name, baseName=baseName, srcName=srcName,
                    altBaseName=altBaseName, coreName=coreName, diacritics=diacritics, extensions=extensions)
        return self._decomposedName
    decomposedName = property(_get_decomposedName)

    # self.style   Answers the weakref style through the parent.style instance.

    def _get_style(self):
        return self.parent.style
    style = property(_get_style)

    # self.parent    Weakref to the parent (style) analyzer

    def _get_parent(self):
        return self._parent()
    def _set_parent(self, analyzer):
        # Set the weakref to the parent (style) analyzer
        self._parent = weakref.ref(analyzer)
    parent = property(_get_parent, _set_parent)

    def inFuzzRange(self, value, reference, factor=1):
        return (reference - factor * self.fuzz) <= value <= (reference + factor * self.fuzz)

    # self.glyph

    def getGlyph(self, glyphName):
        u"""Answers the glyph with this name. Answers None if it does not
        exist."""
        style = self.style
        if style is not None and glyphName in style:
            return self.style[glyphName]
        return None
    def _get_glyph(self, name=None):
        # Called by self.glyph property. Answers None of the glyph does not exist.
        return self.getGlyph(name or self.name)
    glyph = property(_get_glyph)

    # self.contours    Answers the list of contours (can be empty).

    def hasContours(self):
        u"""Answers the boolean flag if the glyph has contours."""
        return len(self.contours) > 0

    def _get_contours(self):
        if self.glyph is not None:
            if isinstance(self.glyph, DefconGlyph):
                contours = []
                for contour in self.glyph:
                    contours.append(contour)
                return contours
            else:
                # In RoboFont, DoodleGlyph sets contours in autoContourOrder().
                return self.glyph._contours # self.glyph is defcon glyph
        return []

    contours = property(_get_contours)

    # ---------------------------------------------------------------------------------------------------------
    #   G L Y P H  T Y P E S

    def isCapital(self):
        u"""
        http://www.fileformat.info/info/unicode/category/index.htm
        http://code.typesupply.com/browser/packages/defcon/trunk/Lib/defcon/objects/uniData.py
        """
        return self.style.unicodeData.categoryForGlyphName(self.glyph.name) == 'Lu'

    def isSmallCap(self):
        return self.glyph.name.endswith('.sc')

    def isXHeight(self):
        name = self.style.unicodeData.decompositionBaseForGlyphName(self.glyph.name, True)
        return name == name.lower() and not self.isAscender()

    def isAscender(self):
        return self.glyph.name in ('b','d','f','h','i','j','k','l','t') # TODO Needs more general approach

    def isDescender(self):
        return self.glyph.name in ('g','j','J','p','q','y') # TODO Needs more general approach.

    # ---------------------------------------------------------------------------------------------------------
    #    A X I S

    # self.verticals

    def _get_verticals(self):
        if self._verticals is None:
            self.findVerticals()
        return self._verticals
    verticals = property(_get_verticals)

    # self.horizontals

    def _get_horizontals(self):
        if self._horizontals is None:
            self.findHorizontals()
        return self._horizontals
    horizontals = property(_get_horizontals)

    # self.diagonals

    def _get_diagonals(self):
        if self._diagonals is None:
            self.findDiagonals()
        return self._diagonals
    diagonals = property(_get_diagonals)

    # self.relevantHeight

    def _get_relevantHeight(self):
        u"""Answers the height of the group that fits best on the basename glyph of self."""
        if self.name.endswith('.sc'):
            return self.parent.scapHeight
        if self.name[0] == self.name[0].upper(): # Must be capital kind of glyph
            return self.parent.capHeight
        # Otherwise try to see if the baseName is closest to xHeight or ascender.
        decomposedName = self.decomposedName # Decompose into glyph name parts
        baseName = decomposedName['baseName'] # Try to get the analyzer of the base glyph.
        if baseName in self.parent:
            sa = self.parent[baseName]
        else:
            sa = self
        if baseName in ('i', 'j'): # Treat as xHeight, taken care of by dotlessi and dotlessj
            return self.parent.xHeight
        my = sa.maxY
        # Calculate differences if possible (only if the base glyph exists)
        if my is not None and abs(self.parent.xHeight - my) > abs(self.parent.ascender - my):
            return self.parent.ascender
        return self.parent.xHeight
    relevantHeight = property(_get_relevantHeight)

    # self.boundingBox

    def _get_boundingBox(self):
        u"""Answers the BoundingBox instance, made from Vertical and Horizontal
        instances. The BoundingBox just looks at outlines of the current glyph
        and not to components. The reason is that the BoundingBox keeps
        Vertical/Horizontal/PointContext instances, they should not be passed
        between glyphs. Use the 4-tuple of self.boundings to get the (x1, y1,
        x2, y2) as expanded rect of all nested components."""
        if self._boundingBox is None:
            self.initialize()
        return self._boundingBox
    boundingBox = property(_get_boundingBox)

    # self.boundings

    def _get_boundings(self):
        u"""Answers the tuple bounding box for self, including the component
        proportions. The boundings is a 4-tuple of real values. Initially
        derived from the self.boundingBox (which is make from
        Vertical/Horizontal/PointContext instances) the self.boundings is more
        flexible, because it allows alteration. self.boundings is read-only.
        Expand the boundings by the boundings and offset of all components."""
        if self._boundings is None:
            bb = self.boundingBox.asList() # Or None if the bounding box is undefined.
            for component in self.components:
                baseGlyph = self.getGlyph(component.baseName)
                if baseGlyph is not None:
                    px, py = component.position # Offset of the component.
                    '''
                    Takes the bounding of the base glyphs and adjusts the
                    bounding box by these positions, creating new Vertical and
                    Horizontal instances, filled with the point contexts of the
                    base glyph. To keep track of where these point contexts
                    came from, they will be marked with the name of the base
                    glyph.
                    '''
                    analyzer = self.getAnalyzer(baseGlyph.name)
                    basebb = analyzer.boundings # Boundings of base defcon glyph
                    if not None in basebb:
                        bx1, by1, bx2, by2 = basebb
                        if None in bb:
                            bb = bx1+px, by1+py, bx2+px, by2+py
                        else:
                            x1, y1, x2, y2 = bb
                            bb = min(x1, bx1+px), min(y1, by1+py), max(x2, bx2+px), max(y2, by2+py)
            self._boundings = bb
        return self._boundings
    boundings = property(_get_boundings)

    # self.boundingsOrNone   Answers the list of bounding values. Answers None if one of them is None

    def _get_boundingsOrNone(self):
        return self.boundingBox.asListOrNone()
    boundingsOrNone = property(_get_boundingsOrNone)

    # self.angledBoundings  Answers the list of bounding values, projected by italic angle on the x-axis."""

    def _get_angledBoundings(self):
        if self._italicBoundings is None:
            self._italicBoundings = list(self.boundings)
            aLeft = self.angledLeftMargin # "Angled" only is relevant if there actual are margins.
            aRight = self.angledRightMargin
            if not None in (aLeft, aRight, self._italicBoundings):
                self._italicBoundings[0] = aLeft # Angled left margin exists
                self._italicBoundings[2] = self.width - aRight # Angled right margin
        return self._italicBoundings
    angledBoundings = property(_get_angledBoundings)

    # self.vacuumeBox

    def _get_vacuumeBox(self, minX=-10000000, minY=-10000000, maxX=10000000, maxY=10000000):
        u"""The @getVacuumeBox@ answers the vacuumed box around all points
        that are located in the rectangle @(minX, minY, maxX, maxY)@. This way
        it is possible to get the vacuume box for all points, but also from a
        selection of points inside the given area, including the transformed
        component references. The tricky thing is what to do with letters like
        "V". We we'll also cut across the letter on x-height and takes these
        points into the comparison as well."""
        bMinX = maxX
        bMaxX = minX
        bMinY = maxY
        bMaxY = minY
        style = self.glyph.getParent()
        for p in getPoints(self.glyph):
            # First scan through all point that fit within the
            if minX <= p.x <= maxX and minY <= p.y <= maxY:
                bMinX = min(bMinX, p.x)
                bMaxX = max(bMaxX, p.x)
                bMinY = min(bMinY, p.y)
                bMaxY = max(bMaxY, p.y)
        # We'll cut through with the horizontal line on minY and maxY
        for x, _ in self.intersectLine((minX, minY), (maxX, minY), canHaveComponent=True):
            bMinX = min(bMinX, x)
            bMaxX = max(bMaxX, x)
        for x, _ in self.intersectLine((minX, maxY), (maxX, maxY), canHaveComponent=True):
            bMinX = min(bMinX, x)
            bMaxX = max(bMaxX, x)
        # Finally compare with the recursive vacuumed boxes of all components.
        for component in getComponents(self.glyph):
            if component.baseGlyph in style:
                # TODO: Make other transformations work here too
                dx = component.transformation[-2]
                dy = component.transformation[-1]
                cMinX, cMinY, cMaxX, cMaxY = self.parent[component.baseGlyph].getVacuumeBox(minX-dx, minY-dy, maxX-dx, maxY-dy)
                bMinX = min(bMinX, cMinX+dx)
                bMaxX = max(bMaxX, cMaxX+dx)
                bMinY = min(bMinY, cMinY+dy)
                bMaxY = max(bMaxY, cMaxY+dy)
        return int(bMinX), int(bMinY), int(bMaxX), int(bMaxY)

    getVacuumeBox = _get_vacuumeBox
    vacuumeBox = property(_get_vacuumeBox)

    def getPointContext(self, index):
        u"""Answers the point context indicated by <i>index</i>. If the index
        is out of range, then answer <b>None</b>."""
        pointContexts = self.pointContexts # Force initialize if not already done
        if 0 <= index < len(pointContexts):
            return pointContexts[index]
        return None

    def getPointContextByID(self, cid):
        for pc in self.pointContexts:
            if pc.uniqueID == cid: # uniqueID comes from the RoboFont pointWrapper instance
                return pc
        return None

    # self.pointContexts

    def _get_pointContexts(self):
        if self._pointContexts is None:
            self.initialize()
        return self._pointContexts
    pointContexts = property(_get_pointContexts)

    # self.overlappingPoints

    def _get_overlappingPoints(self):
        if self._overlappingPoints is None:
            self._overlappingPoints = []
            for pc in self.pointContexts:
                if (pc.x == pc.p1.x and pc.y == pc.p1.y) or (pc.x == pc.p_1.x and pc.y == pc.p_1.y):
                    self._overlappingPoints.append(pc)
        return self._overlappingPoints

    overlappingPoints = property(_get_overlappingPoints)

    # self.components

    def _get_components(self):
        u"""The @self.components@ method find all components of the glyph. If
        the cache @self._components @ already exists, then answer that."""
        if self._components is None:
            self.initialize() # Initializing all of boundingBox, side bearings, components and points
        return self._components
    components = composites = property(_get_components)

    def hasComponents(self):
        return len(self.components) > 0

    hasComposites = hasComponents # Naming compatibility

    def findComponents(self):
        u"""The @findComponents@ method answers a list of @Component@ instances
        of the current glyph."""
        components = []
        if self.glyph is not None:
            for c in self.glyph.components: # MS calls them composites, RoboFont calls them components.
                xScale, xyScale, yxScale, yScale, x, y = c.transformation
                components.append(Component(c.baseGlyph, x, y, xScale, xyScale, yxScale, yScale))
        return components

    findComposites = findComponents # Naming compatibility

    def initializeComponents(self):
        for component in self.findComponents():
            self._components.append(component)
    initializeComposites = initializeComponents # Naming compatibility

    # self.sideBearings

    def _get_sideBearings(self):
        if self._sideBearings is None:
            self.findSideBearings()
        return self._sideBearings
    sideBearings = property(_get_sideBearings)

    #   S T E M S

    # self.stems
    def _get_stems(self):
        if self._stems is None:
            self.findStems()
        return self._stems
    stems = property(_get_stems)

    # self.averageStemSize
    def _get_averageStemSize(self):
        u"""Answers the average float value of all stems found in the glyph.
        """
        total = 0
        stems = self.stems

        if not stems:
            return 0
        for stem in stems.keys():
            total += stem

        return float(total) / float(len(stems))
    averageStemSize = property(_get_averageStemSize)

    # self.straightRoundStems
    def _get_straightRoundStems(self):
        u"""Stems that are round extreme on one side and straight on the other
        side."""
        if self._straightRoundStems is None:
            self.findStems()
        return self._straightRoundStems
    straightRoundStems = property(_get_straightRoundStems)

    # self.straightRoundBars
    def _get_straightRoundBars(self):
        u"""Bars that are round extreme on one side and straight on the other
        side."""
        if self._straightRoundBars is None:
            self.findBars()
        return self._straightRoundBars
    straightRoundBars = property(_get_straightRoundBars)

    # self.minStem
    def _get_minStem(self):
        u"""Answers the minimal stem of all stems found in the glyph.
        """
        stems = self.stems.keys()
        if stems:
            return min(stems)
        return None
    minStem = property(_get_minStem)

    # self.maxStem

    def _get_maxStem(self):
        u"""Answers the maximal stem of all stems found in the glyph."""
        stems = self.stems.keys()
        if stems:
            return max(stems)
        return None
    maxStem = property(_get_maxStem)

    def _get_roundStems(self):
        if self._roundStems is None:
            self.findStems() # Finds both stems and round stems.
        return self._roundStems
    roundStems = property(_get_roundStems)

    # self.minRoundStem

    def _get_minRoundStem(self):
        u"""Answers the minimal round stem of all round stems found in the glyph.
        """
        roundStems = self.roundStems.keys()
        if roundStems:
            return min(roundStems)
        return None
    minRoundStem = property(_get_minRoundStem)

    # self.maxRoundStem

    def _get_maxRoundStem(self):
        u"""Answers the maximal round stem of all round stems found in the glyph."""
        roundStems = self.roundStems.keys()
        if roundStems:
            return max(roundStems)
        return None
    maxRoundStem = property(_get_maxRoundStem)

    # self.terminals

    def _get_terminals(self):
        u"""Terminals are recognizes stem and bar endings where the point contexts are connected."""
        if self._terminals is None:
            self._terminals = []
            for stems in self.stems.values():
                for stem in stems:
                    if stem.isTerminal():
                        self._terminals.append(stem)
            for roundStems in self.roundStems.values():
                for roundStem in roundStems:
                    if roundStem.isTerminal():
                        self._terminals.append(roundStem)
            for bars in self.bars.values():
                for bar in bars:
                    if bar.isTerminal():
                        self._terminals.append(bar)
            for roundBars in self.roundBars.values():
                for roundBar in roundBars:
                    if roundBar.isTerminal():
                        self._terminals.append(roundBar)
        return self._terminals
    terminals = property(_get_terminals)

    def initializePointContexts(self):
        bb = self.boundingBox
        pointContexts = self._pointContexts
        # Overall point index in the glyph.
        pointIndex = 0

        for contourIndex, contour in enumerate(self.contours):
            clockwise = contour.clockwise

            for index, point in enumerate(contour):
                if self.isOffCurve(point):
                    continue
                prev1 = index - 1 # Automatic running over to -1 index
                prev2 = index - 2 # Automatic running over to -2 index
                prev3 = index - 3 # Automatic running over to -3 index
                next1 = index + 1
                if next1 >= len(contour):
                    next1 = 0
                next2 = next1 + 1
                if next2 >= len(contour):
                    next2 = 0
                next3 = next2 + 1
                if next3 >= len(contour):
                    next3 = 0
                pc = self.POINTCONTEXTCLASS(contour[prev3], contour[prev2], contour[prev1], point, contour[next1], contour[next2],
                                  contour[next3], pointIndex, contourIndex, clockwise)
                pointContexts.append(pc)
                # Adjusts the glyph bounding box for this point context.
                bb.extendByPointContext(pc)
                pointIndex += 1

    # self.inflectionPoints

    def _get_inflectionPoints(self):
        # Answers the point contexts that have an inflection in the curve
        inflectionPoints = []
        for pc in self.pointContexts:
            if self.isInflection(pc):
                inflectionPoints.append(pc)
        return inflectionPoints
    inflectionPoints = property(_get_inflectionPoints)

    # ---------------------------------------------------------------------------------------------------------
    #    X  P A R T S

    def findSideBearings(self):
        u"""Initialize the <b>self._boundingBox</b> and answer it for
        convenience of the caller."""
        bb = self.boundingBox
        self._sideBearings = bb.left, bb.right
        return self._sideBearings

    def findVerticals(self):
        u"""The @findVerticals@ method answers a list of verticals.
        """
        self._verticals = verticals = {}

        for pc in self.pointContexts:
            if pc.isVertical():
                if not pc.x in verticals:
                    verticals[pc.x] = self.VERTICALCLASS()
                verticals[pc.x].append(pc)

    def isLandscape(self, pc0, pc1):
        u"""Bars are supposed to be landscape within the FUZZ range. May not
        work in all extremely wide or narrow glyphs."""
        if pc0.isVerticalExtreme() or pc1.isVerticalExtreme():
            return True
        return abs(pc0.p.x - pc1.p.x) - abs(pc0.p.y - pc1.p.y) > self.fuzz

    def isPortrait(self, pc0, pc1):
        u"""Stems are supposed to be portrait  within the FUZZ range. May not
        work in all extremely wide or narrow glyphs. For round stems, always
        answer True."""
        if pc0.isHorizontalExtreme() or pc1.isHorizontalExtreme():
            return True
        return abs(pc0.p.y - pc1.p.y) - abs(pc0.p.x - pc1.p.x) > self.fuzz

    def intersectLine(self, p1, p2, canHaveComponent=False):
        u"""The @intersectLine@ method answers the intersection points of the
        glyph with the line @ (p1, p2)@."""
        return self.intersectWithLine(NakedWrapper(self.glyph), (p1, p2), canHaveComponent=False)

    def intersect(self, pc0, pc1, nextP=False):
        u"""The @intersect@ method test if the line from @pc0.p@ to @pc1.p@ is
        intersecting with other lines of the glyph. The amount of intersection
        is answered. Since the line also intersects with it’s own points, no
        intersection answers a set of two elements. If optional attribute
        <i>next<i> is @True@ (default is @False@ then test on the next point of
        the point contexts."""
        # We cannot simply check for stems on "same contour", because stems made from counters
        # take 2 contours to define.
        if nextP:
            line = ((pc0.p1.x, pc0.p1.y), (pc1.p1.x, pc1.p1.y))
        else:
            line = ((pc0.p.x, pc0.p.y), (pc1.p.x, pc1.p.y))
        return set(self.intersectWithLine(NakedWrapper(self.glyph), line))

    def noIntersect(self, pc0, pc1, nextP=False):
        return len(self.intersect(pc0, pc1, nextP)) in (1, 2)

    def spanRoundsOnBlack(self, pc0, pc1):
        u"""Answers the boolean flag if the line between <i>pc0</i> and
        <i>pc1</i> just spans black area."""
        return self.lineOnBlack(pc0, pc1)

    def onBlack(self, x, y):
        u"""Answers the boolean flag is the single point <b>(x, y)</b> is on
        black."""
        return self.glyphPath.containsPoint_((x, y))

    def coveredInBlack(self, x, y):
        u"""The fast glyphPath test always answers <b>True</b> if the point is
        exact on the contour.  So we'll test the "+" shape (not a square) that
        is one unit around the point. All must be black to decide if the point
        <b>(x, y)</b> is black."""
        return self.onBlack(x, y) and self.onBlack(x-1, y) and self.onBlack(x+1, y) and\
            self.onBlack(x, y-1) and self.onBlack(x, y+1)

    def pointOnBlack(self, p):
        return self.onBlack(p.x, p.y)

    def pointCoveredInBlack(self, p):
        return self.coveredInBlack(p.x, p.y)

    def spanBlack(self, x1, y1, x2, y2, step=SPANSTEP):
        u"""The <b>spanBlack</b> method answers the boolean flag if the number
        of recursive steps between <i>pc0</i> and <i>pc1</i> are on black area
        of the glyph. If step is smaller than the distance between the points,
        then just check in the middle of the line.  The method does not check
        on the end points of the segment, allowing to test these separate
        through <b>self.onBlack</b> or <b>self.coveredInBlack</b>."""
        dx = x2 - x1
        dy = y2 - y1
        distance = dx*dx + dy*dy # Save sqrt time, compare with square of step
        mx = x1 + dx/2
        my = y1 + dy/2
        result = self.onBlack(mx, my) # Check the middle of the vector distance.
        if distance > step*step: # Check for the range of steps if the middle point of the line is still on black
            result = result and self.spanBlack(x1, y1, mx, my, step) and self.spanBlack(mx, my, x2, y2, step)
        # Check if distance is still larger than step, otherwise just check in the middle
        return result

    def lineOnBlack(self, pc0, pc1=None, step=SPANSTEP):
        u"""Answers the boolean flag if the line betweep <i>pc0</i> and
        <i>pc1</i> is entirely running on black, except for the end point. To
        test if the line is entirely on black, use <b>self.lineInBlack()</b>.
        If <i>pc1</i> is omitted, then test the line between <i>pc0</i> and the
        next point on the contour."""
        if pc1 is None:
            pc1 = pc0.p1
        return self.spanBlack(pc0.x, pc0.y, pc1.x, pc1.y, step)

    def middleLineOnBlack(self, pc0, pc1, step=SPANSTEP):
        m0 = pc0.middle()
        m1 = pc1.middle()
        return self.spanBlack(m0.x, m0.y, m1.x, m1.y, step)

    def overlappingLinesInWindowOnBlack(self, pc0, pc1, step=SPANSTEP):
        u"""Answers the boolean flag if the vertical span between <i>pc0</i>
        and <i>pc1</i> just spans black area, by stepping from a point on one
        line to a point on the other line. The trick is to fine the right
        points. If the line it too angled (e.g. under certain circumstances the
        line between the middle points is almost parallel to the line, then our
        trick with testing on the blackness the 4 one-unit points around a
        point fails, when the segments is tested close to one of the main
        points. So we need to test on from the middle of the overlapping window
        perpendicular to the other line."""
        pp0, pp1 = pc0.getProjectedWindowLine(pc1)
        return not None in (pp0, pp1) and self.lineOnBlack(pp0, pp1, step)

    def overlappingLinesInWindowOnWhite(self, pc0, pc1, step=SPANSTEP):
        u"""See <b>self.overlappingLinesInWindowOnBlack</b>."""
        pp0, pp1 = pc0.getProjectedWindowLine(pc1)
        return not None in (pp0, pp1) and self.lineOnWhite(pp0, pp1, step)

    def lineInBlack(self, pc0, pc1=None, step=SPANSTEP):
        u"""Answers the boolean flag if the line (including the points) is
        totally covered in black."""
        if pc1 is None:
            pc1 = pc0.p1
        return self.pointCoveredInBlack(pc0) and self.pointCoverdInBlack(pc1) and self.lineOnBlack(pc0, pc1, step)

    def onWhite(self, x, y):
        u"""Answers the boolean flag if the single point <b>(x, y)</b> is on
        white."""
        return not self.onBlack(x, y)

    def coveredInWhite(self, x, y):
        u"""The fast glyphPath test always answers <b>True</b> if the point is
        exact on the contour.  So we'll test the "+" shape (not square) that is
        one unit around the point. All of the 5 points must be black to decide
        if the point <b>(x, y)</b> is covered in black. Note that this gives a
        difference result than <b>not self.onBlack(x, y)</b>."""
        return self.onWhite(x, y) and self.onWhite(x-1, y) and self.onWhite(x+1, y) and\
            self.onWhite(x, y-1) and self.onWhite(x, y+1)

    def pointOnWhite(self, p):
        return self.onWhite(p.x, p.y)

    def pointCoveredInWhite(self, p):
        return self.coveredInWhite(p.x, p.y)

    def spanWhite(self, x1, y1, x2, y2, step=SPANSTEP):
        u"""The <b>spanWhite</b> method answers the boolean flag if the number
        of recursive steps between <i>pc0</i> and <i>pc1</i> are all on white
        area of the glyph. If step is smaller than the distance between the
        points, then just check in the middle of the line.  """
        dx = x2 - x1
        dy = y2 - y1
        distance = dx*dx + dy*dy # Save sqrt time, compare with square of step
        mx = x1 + dx/2
        my = y1 + dy/2
        result = self.onWhite(mx, my) # Just take the middle of this small distance.
        if distance > step*step: # Check for the range of steps if that point of the line is still on black
            result = result and self.spanWhite(x1, y1, mx, my, step) and self.spanWhite(mx, my, x2, y2, step)
        # Check if distance is still larger than step, otherwise just check in the middle
        return result

    def lineOnWhite(self, pc0, pc1=None, step=SPANSTEP):
        u"""Answers the boolean flag if the line is just spanning white area."""
        if pc1 is None:
            pc1 = pc0.p1
        return self.spanWhite(pc0.x, pc0.y, pc1.x, pc1.y, step)

    def lineInWhite(self, pc0, pc1=None, step=SPANSTEP):
        u"""Answers the boolean flag if the line (including the points) is
        totally covered in white."""
        if pc1 is None:
            pc1 = pc0.p1
        return self.pointCoveredInWhite(pc0) and self.pointCoveredInWhite(pc1) and self.lineOnWhite(pc0, pc1, step)

    def XXXspanGray(self, x1, y1, x2, y2, step):
        u"""Spanning gray is neither full spanning white or spanning black"""
        return not self.overlappingLinesInWindowOnBlack(x1, y1, x2, y2, step) and not self.overlappingLinesInWindowOnWhite(x1, y1, x2, y2, step)

    def isSameHorizontalRoundExtreme(self, pc0, pc1):
        u""" The @isSameHorizontalRoundExtreme@ method answers @True@ if
        <i>pc0</i> and <i>px2</i> are both left or both right round extremes.
        """
        return (pc0.isLeftRoundExtreme() and pc1.isLeftRoundExtreme())\
            or (pc0.isRightRoundExtreme() and pc1.isRightRoundExtreme())

    def isSameVerticalRoundExtreme(self, pc0, pc1):
        u"""The <b>isSameVerticalRoundExtreme</b> method answers @True@ if
        <i>pc0</i> and <i>px2</i> are both top or both bottom round extremes.
        """
        return (pc0.isTopRoundExtreme() and pc1.isTopRoundExtreme())\
            or (pc0.isBottomRoundExtreme() and pc1.isBottomRoundExtreme())

    def matchStem(self, p0, p1):
        u"""Find the matching stem that is located on the x positions of p0 and
        p1. Answers <b>None</b> if not matching stem can be found."""
        for stems in self.stems.values():
            for stem in stems:
                x01 = stem.x
                if p0.x in x01 and p1.x in x01: # Test for swapped values too, assume p0.x != p1.x
                    return stem
        return None

    def isStem(self, pc0, pc1):
        u"""The <b>isStem</b> method takes the point contexts <i>pc0</i> and
        <i>pc1</i> to compare if the can be defined as a “stem”: if they are
        not round extremes, if the two point contexts have overlap in the
        vertical directions (being part of the same window) that runs on black
        and if both lines are not entirely covered in black.
        """
        return not pc0.isHorizontalRoundExtreme() \
            and not pc1.isHorizontalRoundExtreme()\
            and pc0.isVertical() and pc1.isVertical()\
            and pc0.inHorizontalWindow(pc1)\
            and self.middleLineOnBlack(pc0, pc1)\
            and self.overlappingLinesInWindowOnBlack(pc0, pc1)
            #and not (self.pointCoveredInBlack(pc0) or self.pointCoveredInBlack(pc1))

    def matchRoundStem(self, p0, p1):
        u"""Find the matching round stem that is located on the x positions of
        p0 and p1. Answers <b>None</b> if not matching stem can be found."""
        for roundStems in self.roundStems.values():
            for roundStem in roundStems:
                x01 = roundStem.x
                if p0.x in x01 and p1.x in x01: # Test for swapped values too, assume p0.x != p1.x
                    return roundStem
        return None

    def isRoundStem(self, pc0, pc1):
        u"""The <b>isRoundStem</b> method answers the boolean flag if the
        <i>pc0</i> and <i>pc1</i> define a round stem. This is @True@ if one of
        both of point contexts are extremes and if both, they must “bend” in
        the same direction.<br/> Also there should be overlap in horizontal
        direction and the point context should span black only.  """
        return pc0.isHorizontalRoundExtreme()\
            and pc1.isHorizontalRoundExtreme()\
            and self.spanRoundsOnBlack(pc0, pc1)

    def isStraightRoundStem(self, pc0, pc1):
        u"""Answers the boolean flag if one of (pc0, pc1) is a straight extreme
        and the other is a curve extreme.  The stem is only valid if the y of
        the curve extreme is between the y of the 2 vertical on-curves."""
        if not self.spanRoundsOnBlack(pc0, pc1):
            return False # Must be only black between the curve extreme and one of the oncurves.
        pc0Ext = pc0.isHorizontalRoundExtreme()
        pc1Ext = pc1.isHorizontalRoundExtreme()
        if pc0Ext == pc1Ext: # Extremes need to be different type.
            return False
        # Seems to be right, finalize by testing the vertical window overlap.
        p0y = pc0.p.y, pc0.p1.y
        p1y = pc1.p.y, pc1.p1.y
        return (not pc0Ext and min(p0y) <= pc1.p.y and pc1.p.y <= max(p0y))\
            or (not pc1Ext and min(p1y) <= pc0.p.y and pc0.p.y <= max(p1y))

    def isStraightRoundBar(self, pc0, pc1):
        u"""Answers the boolean flag if one of (pc0, pc1) is a straight extreme
        and the other is a curve extreme.  The stem is only valid if the y of
        the curve extreme is between the y of the 2 vertical on-curves."""
        if not self.spanRoundsOnBlack(pc0, pc1):
            return False # Must be only black between the curve extreme and one of the oncurves.
        pc0Ext = pc0.isVerticalRoundExtreme()
        pc1Ext = pc1.isVerticalRoundExtreme()
        if pc0Ext == pc1Ext: # Extremes need to be different type.
            return False
        # Seems to be right, finalize by testing the vertical window overlap.
        p0x = pc0.p.x, pc0.p1.x
        p1x = pc1.p.x, pc1.p1.x
        return (not pc0Ext and min(p0x) <= pc1.p.x and pc1.p.x <= max(p0x))\
            or (not pc1Ext and min(p1x) <= pc0.p.x and pc0.p.x <= max(p1x))

    def isHorizontalCounter(self, pc0, pc1):
        u"""Answers the boolean flag is the connection between pc0.x and pc1.x
        is running entirely over white, and they both are some sort of
        horizontal extreme. The connection is a “white stem”."""
        if not (pc0.isHorizontalRoundExtreme() or pc0.isVertical()):
            return False
        if not (pc1.isHorizontalRoundExtreme() or pc1.isVertical()):
            return False
        if not pc0.inHorizontalWindow(pc1):
            return False
        # Don't use plain self.lineOnWhite(pc0, px1) here, as corner-->roundExtreme (as in the counter of "P"
        # will be too close to the horizontal stroke, so it's recognized as black. Instead we take bigger steps
        # from the corner point, so the iterations of the line are always white.
        return self.lineOnWhite(pc0, pc1, 50) or self.lineOnWhite(pc1, pc0, 50)

    def isVerticalCounter(self, pc0, pc1):
        u"""Answers the boolean flag is the connection between pc0.y and pc1.y
        is running entirely over white, and they both are some sort of
        horizontal extreme. The connection is a “white bar”."""
        if not (pc0.isVerticalRoundExtreme() or pc0.isHorizontal()):
            return False
        if not (pc1.isVerticalRoundExtreme() or pc1.isHorizontal()):
            return False
        if not pc0.inVerticalWindow(pc1):
            return False
        # Don't use plain self.lineOnWhite(pc0, px1) here, as corner-->roundExtreme (as in the counter of "P"
        # will be too close to the horizontal stroke, so it's recognized as black. Instead we take bigger steps
        # from the corner point, so the iterations of the line are always white.
        return self.lineOnWhite(pc0, pc1, 50) or self.lineOnWhite(pc1, pc0, 50)

    def matchBar(self, p0, p1):
        u"""Find the matching bar that is located on the y positions of p0 and
        p1.  Answers <b>None</b> if not matching stem can be found."""
        for bars in self.bars.values():
            for bar in bars:
                y01 = bar.y
                if p0.y in y01 and p1.y in y01: # Test for swapped values too, assume p0.y != p1.y
                    return bar
        return None

    def isBar(self, pc0, pc1):
        u"""
        The <b>isBar</b> method takes the point contexts <i>pc0</i> and
        <i>pc1</i> to compare if the can be defined as a “bar”: if two point
        contexts have overlap in the horizontal directions if the line between
        them is entirely on black, and if the lines are not entirely covered in
        black.
        """
        return not pc0.isVerticalRoundExtreme()\
            and not pc1.isVerticalRoundExtreme()\
            and pc0.isHorizontal() and pc1.isHorizontal()\
            and pc0.inVerticalWindow(pc1)\
            and self.middleLineOnBlack(pc0, pc1)\
            and self.overlappingLinesInWindowOnBlack(pc0, pc1)
            #and (not self.pointCoveredInBlack(pc0) or not self.pointCoveredInBlack(pc1))

    def matchRoundBar(self, p0, p1):
        u"""Find the matching round bar that is located on the y positions of
        p0 and p1. Answers <b>None</b> if not matching stem can be found."""
        for roundBars in self.roundBars.values():
            for roundBar in roundBars:
                y01 = roundBar.y
                if p0.y in y01 and p1.y in y01: # Test for swapped values too, assume p0.y != p1.y
                    return roundBar
        return None

    def isRoundBar(self, pc0, pc1):
        # self.isSameVerticalRoundExtreme(pc0, pc1) and\
        return pc0.isVerticalRoundExtreme()\
            and pc1.isVerticalRoundExtreme()\
            and self.spanRoundsOnBlack(pc0, pc1)

    def isDiagonalStem(self, pc0, pc1):
        u"""Test on more or less parallel."""
        return pc0.isParallel(pc1) and self.overlappingLinesInWindowOnBlack(pc0, pc1)

    def findStems(self):
        u"""
        The @findStems@ method finds the stems in the current glyph and assigns
        them as dictionary to @self._stems@. Since we cannot use the CVT of the
        glyph (the analyzer is used to find these values, not to use them),
        we'll make an assumption about the pattern of vertices found. It is up
        to the caller to make sure that the current glyph is relevant in the
        kind of vertices that we are looking for.<br/>

        NOTE: An alternative approach could be to make a Fourier analysis of all
        stem distances of the font, and so find out which are likely to have a
        stem distance.

        Additionally the stems are found by manual hints in the glyph, as
        generated by the Hint Editor. Since these stem definitions not
        necessarily run from point to point (instead an interpolated location
        on a curve or straight line can be used), a special kind of
        PointContext is added there.
        """
        self._stems = stems = {}
        self._roundStems = roundStems = {}
        self._straightRoundStems = straightRoundStems = {}
        self._allHorizontalCounters = horizontalCounters = {} # Space between all neighboring stems, running over white only.

        hints = self.hints
        if hints:
            for hint in hints:
                if self.C.FLOQMEME_STEM in hint['types']: # Is this is hint defining a stem?
                    stem = self.STEMCLASS(hint['pc0'], hint['pc1'], self.glyph.name)
                    size = stem.size
                    if not size in stems:
                        stems[size] = []
                    stems[size].append(stem)
        if not stems: # No "manual" hints defined, try to analyze from the found Vertical instances.
            verticals = self.verticals
            checked = set() # Store what we checked, to avoid doubles in the loops

            for _, vertical1 in sorted(verticals.items()): # x1, vertical1
                for _, vertical2 in sorted(verticals.items()): # x2, vertical2
                    if vertical1 is vertical2:
                        continue
                    # We need to loop through the points of the vertical
                    # separate, to find e.g. the horizontal separate round stems
                    # of the points of a column. Otherwise they will be seen as one vertical.
                    for pc0 in vertical1:
                        for pc1 in vertical2:
                            # Skip if identical, they cannot be a stem.
                            if pc0 is pc1:
                                continue
                            # Skip if we already examined this one.
                            if (pc0.index, pc1.index) in checked:
                                continue
                            checked.add((pc0.index, pc1.index))
                            checked.add((pc1.index, pc0.index))
                            # Test if the y values are in range so this can be seen as stem pair
                            # and test if this pair is spanning a black space and the lines are
                            # not entirely covered in black.
                            if self.isStem(pc0, pc1):
                                # Add this stem to the result.
                                stem = self.STEMCLASS(pc0, pc1, self.glyph.name)
                                size = TX.asInt(stem.size) # Make sure not to get floats as key
                                if not size in stems:
                                    stems[size] = []
                                stems[size].append(stem)

                            elif self.isRoundStem(pc0, pc1):
                                # If either of the point context is a curve extreme
                                # then count this stem as round stem
                                stem = self.STEMCLASS(pc0, pc1, self.glyph.name)
                                size = TX.asInt(stem.size) # Make sure not to get floats as key
                                if not size in roundStems:
                                    roundStems[size] = []
                                roundStems[size].append(stem)

                            elif self.isStraightRoundStem(pc0, pc1):
                                # If one side is straight and the other side is round extreme
                                # then count this stem as straight round stem.
                                stem = self.STEMCLASS(pc0, pc1, self.glyph.name)
                                size = TX.asInt(stem.size) # Make sure not to get floats as key
                                if not size in straightRoundStems:
                                    straightRoundStems[size] = []
                                straightRoundStems[size].append(stem)

                            elif self.isHorizontalCounter(pc0, pc1):
                                # If there is just whitspace between the points and they are some kind of extreme,
                                # then assume this is a counter.
                                counter = self.COUNTERCLASS(pc0, pc1, self.glyph.name)
                                size = TX.asInt(counter.size)
                                if not size in horizontalCounters:
                                    horizontalCounters[size] = []
                                horizontalCounters[size].append(counter)

        return self._stems

    def findHints(self):
        u"""
        The @findHints@ method finds the hints (previously floqMemes) in the
        current glyph and assigns them as dictionary to @self._hints@."""
        hints = []
        for hint in self.glyph.lib.get(self.C.LIB_FLOQMEMESLIST, []):
            if not 'types' in hint:
                continue
            loc0 = Location.fromDict(self.glyph, hint['loc0'])
            loc1 = Location.fromDict(self.glyph, hint['loc1'])
            # Make "fake" point contexts, where the next and prev point are the two neighboring interpolation points
            # of the locations. pc0 and pc1 are then the intermediate points of the interpolation
            pc0 = loc0.pointContext
            pc1 = loc1.pointContext
            # Depending on the defined flags in hint['types'] this points can be used as stem, bar, diagonal, etc.
            hints.append(dict(pc0=pc0, pc1=pc1, loc0=loc0, loc1=loc1, types=hint['types']))
        if hints:
            self._hints = hints # Only initialize if something was created.

    # ---------------------------------------------------------------------------------------------------------
    #    Y  P A R T S

    def findHorizontals(self):
        u"""
        The @findHorizontals@ method answers a list of horizontals where the
        main point is on curve.
        """
        self._horizontals = horizontals = {}

        for pc in self.pointContexts:
            if pc.isHorizontal():
                if not pc.y in horizontals:
                    horizontals[pc.y] = self.HORIZONTALCLASS()
                horizontals[pc.y].append(pc)

    def findBars(self):
        u"""The @findBars@ method finds the bars in the current glyph and
        assigns them as dictionary to @self._bars@. Since we cannot use the CVT
        of the glyph (the analyzer is user to find these values, not to use
        them), we'll make an assumption about the pattern of vertices found. It
        is up to the caller to make sure that the current glyph is relevant in
        the kind of vertices that we are looking for."""
        horizontals = self.horizontals
        self._bars = bars = {}
        self._roundBars = roundBars = {}
        self._straightRoundBars = straightRoundBars = {}
        self._allVerticalCounters = verticalCounters = {} # Space between neighboring bars

        checked = set() # Store what we checked, to avoid doubles in the loops
        hints = self.hints
        if hints:
            for hint in hints:
                if self.C.FLOQMEME_BAR in hint['types']: # Is this this hint defining a stem?
                    bar = self.BARCLASS(hint['pc0'], hint['pc1'], self.glyph.name)
                    size = bar.size
                    if not size in bars:
                        bars[size] = []
                    bars[size].append(bar)
        if not bars: # No "manual" hints defined, try to analyze from the found Vertical instances.
            for _, horizontal1 in sorted(horizontals.items()): # y1, horizontal1
                for _, horizontal2 in sorted(horizontals.items()): # y2, horizontal2
                    if horizontal1 is horizontal2:
                        continue
                    # We need to loop through the points of the horizontal
                    # separate, to find e.g. the vertical separate round bars
                    # of the points of a ellipsis. Otherwise they will seen as one horizontal.
                    for pc0 in horizontal1:
                        for pc1 in horizontal2:
                            # Skip if identical, they cannot be a stem.
                            if pc0 is pc1:
                                continue
                            # Skip if we already examined this one.
                            if (pc0.index, pc1.index) in checked:
                                continue
                            checked.add((pc0.index, pc1.index))
                            checked.add((pc1.index, pc0.index))
                            # Test if the y values are in range so this can be seen as stem pair
                            # and test if this pair is spanning a black space and not covered in black.
                            if self.isBar(pc0, pc1):
                                # Add this bar to the result.
                                bar = self.BARCLASS(pc0, pc1, self.glyph.name)
                                size = TX.asInt(bar.size) # Make sure not to get floats as keys
                                if not size in bars:
                                    bars[size] = []
                                bars[size].append(bar)

                            elif self.isRoundBar(pc0, pc1):
                                # If either of the point context is a curve extreme
                                # then count this bar as round bar
                                bar = self.BARCLASS(pc0, pc1, self.glyph.name)
                                size = TX.asInt(bar.size) # Make sure not to get floats as keys
                                if not size in roundBars:
                                    roundBars[size] = []
                                roundBars[size].append(bar)

                            elif self.isStraightRoundBar(pc0, pc1):
                                # If one side is straight and the other side is round extreme
                                # then count this stem as straight round bar.
                                bar = self.BARCLASS(pc0, pc1, self.glyph.name)
                                size = TX.asInt(bar.size) # Make sure not to get floats as key
                                if not size in straightRoundBars:
                                    straightRoundBars[size] = []
                                straightRoundBars[size].append(bar)

                            elif self.isVerticalCounter(pc0, pc1):
                                # If there is just whitespace between the points and they are some kind of extreme,
                                # then assume this is a counter.
                                counter = self.VCOUNTERCLASS(pc0, pc1, self.glyph.name)
                                size = TX.asInt(counter.size)
                                if not size in verticalCounters:
                                    verticalCounters[size] = []
                                verticalCounters[size].append(counter)

        return self._bars

    # ---------------------------------------------------------------------------------------------------------
    #    D I A G O N A L S

    def findDiagonals(self):
        u"""Find the dictionary of all point contexts, where the key is the
        normalized integer rounded angle.  Definition of a diagonal is that it
        cannot be a vertical or horizontal."""
        self._diagonals = diagonals = {} # Angle (different from 0, 90) is the key
        for pc in self.pointContexts:
            if pc.isDiagonal():
                angle = int(round(pc.normalizedAngle))
                if not angle in diagonals:
                    diagonals[angle] = []
                diagonals[angle].append(pc)
        return self._diagonals

    # self.diagonalStems

    def _get_diagonalStems(self):

        diagonals = self.diagonals
        found = set()
        self._diagonalstems = diagonalStems = {}

        hints = self.hints
        if hints:
            for hint in hints:
                if self.C.FLOQMEME_DIAGONAL in hint['types']: # Is this this hint defining a stem?
                    diagonalStem = self.DIAGONALSTEMCLASS(hint['pc0'], hint['pc1'], self.glyph.name)
                    distance = diagonalStem.size
                    if not distance in diagonalStems:
                        diagonalStems[distance] = []
                    diagonalStems[distance].append(diagonalStem)
        if not diagonalStems: # No "manual" hints defined, try to get them comparing the direction of segments..
            for _, diagonals1 in diagonals.items(): # Angles are normalized, angle0, diagonals1
                for diagonal0 in diagonals1:
                    for _, diagonals2 in diagonals.items(): # angle1, diagonals2
                        for diagonal1 in diagonals2:
                            if diagonal0 is diagonal1 or not diagonal0.isParallel(diagonal1): # Default tolerance of pc
                                continue
                            if (diagonal0.index, diagonal1.index) in found:
                                continue
                            # Test if the y values are in range so this can be seen as stem pair
                            # and test if this pair is spanning a black space
                            if not self.isDiagonalStem(diagonal0, diagonal1):
                                continue
                            found.add((diagonal0.index, diagonal1.index))
                            found.add((diagonal1.index, diagonal0.index))

                            diagonalStem = self.DIAGONALSTEMCLASS(diagonal0, diagonal1, self.glyph.name)
                            distance = diagonalStem.size # Average length of the diagonal projected lines
                            if not distance in diagonalStems:
                                diagonalStems[distance] = []
                            diagonalStems[distance].append(diagonalStem)
        return diagonalStems
    diagonalStems = property(_get_diagonalStems)

    # ---------------------------------------------------------------------------------------------------------
    #    I N F L E C T I O N S

    # self.inflections

    def _get_inflections(self):
        if self._inflections is None:
            self.findInflections()
        return self._inflections
    inflections = property(_get_inflections)

    def findInflections(self):
        self._inflections = inflections = []

        for pc in self.pointContexts:
            if pc.isInflection():
                inflections.append(pc)
        return self._inflections

    # ---------------------------------------------------------------------------------------------------------
    #    S E R I F S

    def _get_serifs(self):
        # Not implemented yet
        if self._serifs is None:
            self.findSerifs()
        return self._serifs
    serifs = property(_get_serifs)

    def findSerifs(self):
        u"""
        The @findSerifs@ method finds serif structures in the glyph. A serif
        structure is defined as a continuous set of points (running from one
        point context to another point context), where the end points have one
        of the following characteristics:

        <ul>
        <li>Start and end with a stem or bar</li>
        <li>Start with a stem or bar and end with a (local) extreme</li>
        <li>Start with a (local) extreme and end with a stem or bar</li>
        </ul>
        """
        # if the left point of the left stem does not match the x-position of
        # the left boundingBox, then we assume there mus be serifs there.
        self._serifs = {}
        items = []
        for stems in self.stems.values():
            for stem in stems:
                items.append(stem)
        for bars in self.bars.values():
            for bar in bars:
                items.append(bar)
        for diagonals in self.diagonalStems.values():
            for diagonal in diagonals:
                items.append(diagonal)
        # @@@ Needs to be extended

    # ---------------------------------------------------------------------------------------------------------
    #    H I N T S

    def _get_hints(self):
        if self._hints is None:
            self.findHints()
        return self._hints
    hints = property(_get_hints)

    # ---------------------------------------------------------------------------------------------------------
    #    A P I

    # self.maxYPoint    Answers the contour PointContext of with max Y. (Independent of components).

    def _get_maxYPoint(self):
        return self.boundingBox.top.minXPoint
    maxYPoint = property(_get_maxYPoint)

    # self.maxY         Answers the max Y of self.boundings. (Including components).

    def _get_maxY(self):
        bb = self.boundings
        if None in bb:
            return None
        _, y1, _, y2 = self.boundings
        return max(y1, y2)
    maxY = property(_get_maxY)

    # self.minYPoint     Answers the contour PointContext of with min Y. (Independent of components).

    def _get_minYPoint(self):
        return self.boundingBox.bottom.minXPoint
    minYPoint = property(_get_minYPoint)

    # self.minY          Answers the min Y of self.boundings. (Including components).

    def _get_minY(self):
        bb = self.boundings
        if None in bb:
            return None
        _, y1, _, y2 = self.boundings
        return min(y1, y2)
    minY = property(_get_minY)

    # self.maxXPoint    Answers the contour PointContext of with max X. (Independent of components).

    def _get_maxXPoint(self):
        return self.boundingBox.right.minYPoint
    maxXPoint = property(_get_maxXPoint)

    # self.maxX         Answers the min X of self.boundings. (Including components).

    def _get_maxX(self):
        bb = self.boundings
        if None in bb:
            return None
        x1, _, x2, _ = self.boundings
        return max(x1, x2)
    maxX = property(_get_maxX)

    # self.minXPoint    Answers the contour PointContext of with min X. (Independent of components).

    def _get_minXPoint(self):
        return self.boundingBox.left.minYPoint
    minXPoint = property(_get_minXPoint)

    # self.minX         Answers the min X of self.boundings. (Including components).

    def _get_minX(self):
        bb = self.boundings
        if None in bb:
            return None
        x1, _, x2, _ = self.boundings
        return min(x1, x2)
    minX = property(_get_minX)

    # self.stem

    def _get_stem(self):
        u"""Answers the left most stem as <b>Stem</b> instance."""
        stem = None
        stems = self.stems
        if stems:
            xkey = sorted(stems.keys())[0]
            stem = stems[xkey][0]
        return stem
    stem = property(_get_stem)

    # self.allStems      Answers the combination dict of stems and round stems
    def _get_allStems(self):
        if self._allStems is None:
            self._allStems = {}
            for value, stems in self.stems.items():
                self._allStems[value] = stems[:] # Make copy, as we'll be appnding to it.
            for value, roundStems in self.roundStems.items():
                if not value in self._allStems:
                    self._allStems[value] = []
                for roundStem in roundStems:
                    self._allStems[value].append(roundStem)
            for value, straightRoundStems in self.straightRoundStems.items():
                if not value in self._allStems:
                    self._allStems[value] = []
                for straightRoundStem in straightRoundStems:
                    self._allStems[value].append(straightRoundStem)

        return self._allStems
    allStems = property(_get_allStems)

    # self.allStemsCounters
    def _get_allStemsCounters(self):
        if self._allStemsCounters is None:
            self._allStemsCounters = {}
            for value, stems in self.allStems.items():
                self._allStemsCounters[value] = stems
            for value, counters in self.allHorizontalCounters.items():
                if not value in self._allStemsCounters:
                    self._allStemsCounters[value] = []
                for counter in counters:
                    self._allStemsCounters[value].append(counter)
        return self._allStemsCounters
    allStemsCounters = property(_get_allStemsCounters)

    # self.allStemsCountersComponents
    def _get_allStemsCountersComponents(self):
        if self._allStemsCountersComponents is None:
            self._allStemsCountersComponents = {}
            for value, stems in self.allStemsCounters.items():
                self._allStemsCountersComponents[value] = stems[:] # Make copy, as we'll appending to it.
            # Now recursively repeat for all components in the glyph. We don't do the counters of the components.
            for component in getComponents(self.glyph):
                if component.baseGlyph in self.style:
                    offset = component.transformation[-2:]
                    cga = self.parent[component.baseGlyph]
                    for size, stems in cga.allStems.items():
                        if not size in self._allStems:
                            self._allStems[size] = []
                        for stem in stems:
                            stem = stem.copy() # Add offset to copy. Use as (x1, x2) = stem.x to calc position + offset.
                            stem.addOffset(offset) # Incremental if multiple chained component reference.
                            self._allStems[size].append(stem)
        return self._allStemsCountersComponents
    allStemsCountersComponents = property(_get_allStemsCountersComponents)

    # self.allHorizontalCounters  Answers the combination dict of all types of horizontal counters.
    def _get_allHorizontalCounters(self):
        if self._allHorizontalCounters is None:
            self.findStems() # Also finds all horizontal counters.
        return self._allHorizontalCounters
    allHorizontalCounters = property(_get_allHorizontalCounters)

    # self.allVerticalCounters  Answers the combination dict of all types of vertical counters.
    def _get_allVerticalCounters(self):
        if self._allVerticalCounters is None:
            self.findBars() # Also finds all vertical counters.
        return self._allVerticalCounters
    allVerticalCounters = property(_get_allVerticalCounters)

    # self.roundStem
    def _get_roundStem(self):
        u"""Use the left round stem, if there are multiple in the glyph."""
        rstem = None
        rstems = self.roundStems
        if rstems:
            xkey = sorted(rstems.keys())[0]
            rstem = rstems[xkey][0]
        return rstem
    roundStem = property(_get_roundStem)

    # self.bar
    def _get_bar(self):
        u"""Answers the left most bar as <b>Stem</b> instance."""
        bar = None
        bars = self.bars
        if bars:
            ykey = sorted(bars.keys())[0]
            bar = bars[ykey][0]
        return bar
    bar = property(_get_bar)

    # self.bars
    def _get_bars(self):
        if self._bars is None:
            self.findBars()
        return self._bars
    bars = property(_get_bars)

    # self.allBars      Answers the combination dict of bars and round bars
    def _get_allBars(self):
        if self._allBars is None:
            self._allBars = {}
            for value, bars in self.bars.items():
                self._allBars[value] = bars
            for value, roundBars in self.roundBars.items():
                if not value in self._allBars:
                    self._allBars[value] = []
                for roundBar in roundBars:
                    self._allBars[value].append(roundBar)
            for value, straightRoundBars in self.straightRoundBars.items():
                if not value in self._allBars:
                    self._allBars[value] = []
                for straightRoundBar in straightRoundBars:
                    self._allBars[value].append(straightRoundBar)

        return self._allBars
    allBars = property(_get_allBars)

    # self.allBarsCounters
    def _get_allBarsCounters(self):
        if self._allBarsCounters is None:
            self._allBarsCounters = {}
            for value, bars in self.allBars.items():
                self._allBarsCounters[value] = bars
            for value, counters in self.allVerticalCounters.items():
                if not value in self._allBarsCounters:
                    self._allBarsCounters[value] = []
                for counter in counters:
                    self._allBarsCounters[value].append(counter)
        return self._allBarsCounters
    allBarsCounters = property(_get_allBarsCounters)

    # self.allBarsCountersComponents
    def _get_allBarsCountersComponents(self):
        if self._allBarsCountersComponents is None:
            self._allBarsCountersComponents = {}
            for value, bars in self.allBarsCounters.items():
                self._allBarsCountersComponents[value] = bars[:] # Make copy, as we'll appending to it.
            # Now add bars from the component glyphs. We don't do the counters of the components.
            for component in getComponents(self.glyph):
                if component.baseGlyph in self.style:
                    offset = component.transformation[-2:] # We may need to transform the found stems.
                    cga = self.parent[component.baseGlyph]
                    for size, bars in cga.allBars.items():
                        if not size in self._allBars:
                            self._allBars[size] = []
                        for bar in bars:
                            bar = bar.copy() # Add offset to copy. Use as (y1, y2) = bar.y to calc position + offset.
                            bar.addOffset(offset) # Incremental if multiple chained component reference.
                            self._allBars[size].append(bar)
        return self._allBarsCountersComponents
    allBarsCountersComponents = property(_get_allBarsCountersComponents)

    # self.minBar

    def _get_minBar(self):
        u"""Answers the minimal bar of all bars found in the glyph."""
        bars = self.bars.keys()
        if bars:
            return min(bars)
        return None
    minBar = property(_get_minBar)

    # self.maxBar

    def _get_maxBar(self):
        u"""Answers the maximal bar of all bars found in the glyph."""
        bars = self.bars.keys()
        if bars:
            return max(bars)
        return None
    maxBar = property(_get_maxBar)

    # self.roundBar

    def _get_roundBar(self):
        u"""Use the left round bar, if there are multiple in the glyph."""
        rbar = None
        rbars = self.roundBars
        if rbars:
            ykey = sorted(rbars.keys())[0]
            rbar = rbars[ykey][0]
        return rbar
    roundBar = property(_get_roundBar)

    # self.roundBars

    def _get_roundBars(self):
        if self._roundBars is None:
            self.findBars() # Cache finds of both bars and round bars
        return self._roundBars
    roundBars = property(_get_roundBars)

    # self.minRoundBar

    def _get_minRoundBar(self):
        u"""Answers the minimum round bar of all round bars found in the
        glyph."""
        roundBars = self.roundBars.keys()
        if roundBars:
            return min(roundBars)
        return None
    minRoundBar = property(_get_minRoundBar)

    # self.maxRoundBar

    def _get_maxRoundBar(self):
        u"""Answers the maximum round bar of all round bars found in the
        glyph."""
        roundBars = self.roundBars.keys()
        if roundBars:
            return max(roundBars)
        return None
    maxRoundBar = property(_get_maxRoundBar)

    def _get_width(self):
        return self.glyph.width
    def _set_width(self, width):
        self.glyph.width = width
    width = property(_get_width, _set_width)

    # self.rightMargin

    def _get_rightMargin(self):
        u"""Answers the rightMargin value. Use <b>self.boundingBox.maxX</b> to
        get the <b>Vertical</b> instance that defines the right margin. This
        way the point contexts involved can be queried. If there are no
        outlines (<b>self.boundingBox is None</b>, then answer 0 by definition
        (compatible with RoboFont)). Answers default 0 if glyph does not exist
        in the style.
        """
        #return self.width - self.boundingBox.right.x # Calculate or get from glyph?
        glyph = self.glyph
        if glyph is None:
            return 0 # Default is glyph does not exist in the style
        return glyph.rightMargin
    def _set_rightMargin(self, margin):
        glyph = self.glyph
        if glyph is not None: # Ignore if glyph does not exist.
            self.glyph.rightMargin = margin
    rightMargin = property(_get_rightMargin, _set_rightMargin)

    # self.leftMargin

    def _get_leftMargin(self):
        u"""Answers the leftMargin value. Use <b>self.boundingBox.minX</b> to
        get the <b>Vertical</b> instance that defines the left margin. This way
        the point contexts involved can be queried. If there are no outlines
        (<b>self.boundingBox is None</b>, then answer 0 by definition
        (compatible with RoboFont)). Answers default 0 if glyph does not exist
        in the style."""
        #return self.boundingBox.left.x # Calculate or get from glyph?
        glyph = self.glyph
        if glyph is None:
            return 0 # Default if glyph does not exist in the style.
        return glyph.leftMargin
    def _set_leftMargin(self, margin):
        glyph = self.glyph
        if glyph is not None: # Ignore if glyph does not exist.
            glyph.leftMargin = margin
    leftMargin = property(_get_leftMargin, _set_leftMargin)

    # self.angledLeftMargin

    def _get_angledLeftMargin(self):
        glyph = self.glyph
        if glyph is None:
            return 0 # Default value if glyph does not exist in the style.
        return glyph.angledLeftMargin
    def _set_angledLeftMargin(self, margin):
        glyph = self.glyph
        if glyph is not None: # Ignore if glyph does not exist in the style.
            glyph.angledLeftMargin = margin
    angledLeftMargin = property(_get_angledLeftMargin, _set_angledLeftMargin)

    # self.angledRightMargin

    def _get_angledRightMargin(self):
        glyph = self.glyph
        if glyph is None:
            return 0 # Default value if glyph does not exist in the style
        return glyph.angledRightMargin
    def _set_angledRightMargin(self, margin):
        glyph = self.glyph
        if glyph is not None: # Ignore if glyph does not exist in the style.
            glyph.angledRightMargin = margin
    angledRightMargin = property(_get_angledRightMargin, _set_angledRightMargin)

    # self.leftBeamMargin       Answers the left margin, as measured by a beam on xHeight/2
    # self.rightBeamMargin      Answers the right margin, as measured by a beam on xHeight/2

    def _get_leftBeamMargin(self):
        glyph = self.glyph
        if glyph is not None and self._leftBeamMargin is None: # Answers undefined 0 if glyph does not exist.
            y = self.parent.style.info.xHeight/2
            line = ((-10000, y), (10000, y))
            for x, _ in self.intersectWithLine(NakedWrapper(glyph), line):
                self._leftBeamMargin = int(round(min(self._leftBeamMargin or 10000, x)))
        return self._leftBeamMargin or 0
    def _set_leftBeamMargin(self, margin):
        self.leftMargin += int(round(margin - self.leftBeamMargin))
        self._leftBeamMargin = None
    leftBeamMargin = property(_get_leftBeamMargin, _set_leftBeamMargin)

    def _get_rightBeamMargin(self):
        glyph = self.glyph
        if glyph is not None and self._rightBeamMargin is None: # Answers undefined 0 if glyph does not exist.
            y = self.parent.style.info.xHeight/2
            line = ((-10000, y), (10000, y))
            for x, _ in self.intersectWithLine(NakedWrapper(glyph), line):
                self._rightBeamMargin = int(round(max(self._rightBeamMargin or -10000, x)))
        return self._rightBeamMargin or 0
    def _set_rightBeamMargin(self, margin):
        self.rightMargin += int(round(margin - self.rightBeamMargin))
        self._rightBeamMargin = None
    rightBeamMargin = property(_get_rightBeamMargin, _set_rightBeamMargin)

    def findNearestBlack(self, x, y, radius=2):
        u"""Make a horizontal beam, and measure the distances to the nearest black, if (x, y) is not black
        from itself."""
        glyph = self.glyph
        if glyph is not None:
            if self.onBlack(x, y):
                return x
            newX = x
            line =((-10000, y), (10000, y))
            for ix, _ in self.intersectWithLine(NakedWrapper(glyph), line):
                if abs(newX - ix) <= abs(x - ix):
                    if self.onBlack(ix+radius, y):
                        newX = ix+radius
                    elif self.onBlack(ix-radius, y):
                        newX = ix-radius
                    else: # Excepational cases, if the area < radius.
                        newX = ix
            return newX
        return None

    # self.leftBaseMargin

    def _get_leftBaseMargin(self):
        u"""Answers the left angled margin of the base glyph (referred to by
        the component that has the same base name as self. If there is a
        "dotless"+self.name in the style, then take that as base for accent
        glyphs. This method assumes that the "dotless" right margin and width
        are synced with self. Use the global function syncDotless(glyph) to be
        sure."""
        baseName = self.decomposedName['altBaseName'] # In altBaseName, "i" and "j" are translated in "dotlessi" and "dotlessj"
        for component in getComponents(self.glyph):
            if component.baseGlyph == baseName: # Answers transformed left margin of this glyph
                if baseName in self.parent:
                    leftMargin = self.parent[baseName].angledLeftMargin
                    if leftMargin is not None:
                        return self.parent[baseName].angledLeftMargin + component.transformation[4]
        return self.angledLeftMargin
    def _set_leftBaseMargin(self, margin):
        self.angledLeftMargin = 0
        baseName = self.decomposedName['altBaseName']
        for component in getComponents(self.glyph):
            if component.baseGlyph == baseName: # Answers transformed left margin of this glyph
                if baseName in self.parent:
                    leftMargin = self.parent[baseName].angledLeftMargin
                    if leftMargin is not None:
                        self.angledLeftMargin = margin - self.parent[baseName].angledLeftMargin - component.transformation[4]
                    else:
                        self.angledLeftMargin = margin
                return
        self.angledLeftMargin = margin
    leftBaseMargin = property(_get_leftBaseMargin, _set_leftBaseMargin)

    def _get_rightBaseMargin(self):
        u"""Answers the right angled margin of the base glyph (referred to by
        the component that has the same base name as self. If there is a
        "dotless"+self.name in the style, then take that as base for accent
        glyphs. This method assumed that the "dotless" left margin and width
        are synced with self. Use the global function syncDotless(glyph) to be
        sure."""
        baseName = self.decomposedName['altBaseName']
        for component in getComponents(self.glyph) or []:
            if component.baseGlyph == baseName: # Answers transformed left margin of this glyph
                if baseName in self.parent:
                    rightMargin = self.parent[baseName].angledRightMargin
                    if rightMargin is not None:
                        return self.width - self.parent[baseName].width - component.transformation[4] + rightMargin
        return self.angledRightMargin
    def _set_rightBaseMargin(self, margin):
        self.angledRightMargin = 0 # Reset, so easier to calculate.
        baseName = self.decomposedName['altBaseName']
        components = getComponents(self.glyph)
        for component in components:
            if component.baseGlyph == baseName: # Answers transformed left margin of this glyph
                if baseName in self.parent:
                    baseGlyph = self.parent[baseName]
                    rightMargin = baseGlyph.angledRightMargin
                    if rightMargin is not None:
                        self.glyph.width = baseGlyph.width + component.transformation[4] - rightMargin + margin
                    else:
                        self.angledRightMargin = margin
                return
        self.angledRightMargin = margin
    rightBaseMargin = property(_get_rightBaseMargin, _set_rightBaseMargin)

    # self.width

    def _get_width(self):
        u"""Answers the glyph width. This method is for compatibility reason,
        there is no <b>PointContext</b> involved."""
        glyph = self.glyph
        if glyph is None:
            return 0 # Default value if glyph does not exist in the style.
        return glyph.width
    def _set_width(self, width):
        glyph = self.glyph
        if glyph is not None: # Ignore if glyph does exist in the style.
            self.glyph.width = width
    width = property(_get_width, _set_width)

    # self.unitsPerEm

    def _get_unitsPerEm(self):
        u"""Answers the units per em for this font. Identical to
        <b>self.style.info.unitsPerEm</b>."""
        return self.style.info.unitsPerEm
    unitsPerEm = property(_get_unitsPerEm)

    # self.diagonalRun

    def _get_diagonalRun(self):
        #diagonalRun = None
        diagonals = self.diagonalStems
        if diagonals:
            pass
        # @@@@@@@@@@
        return self.WIDTHCLASS(None, 100)
    diagonalRun = property(_get_diagonalRun)

    # self.diagonal

    def _get_diagonal(self):
        return self.WIDTHCLASS(None, 200)
    diagonal = property(_get_diagonal)

    # self.roundOvershoots

    def _get_roundOvershoots(self):
        if self._roundOvershoots is None:
            self._roundOvershoots = []
            for _, horizontal in self.horizontals.items(): # value, horizontal
                pcy = horizontal[0]
                if pcy.isTopRoundExtreme() or pcy.isBottomRoundExtreme():
                    self._roundOvershoots.append(pcy)
        return self._roundOvershoots
    roundOvershoots = property(_get_roundOvershoots)

    # ---------------------------------------------------------------------------------------------------------
    #    A N C H O R S

    def guessAnchorPosition(self, position):
        u"""
        Answers the guessed position (x, y) of the anchor for the glyph of this
        analyzer. There are several options, depending on the content of the
        position attribute. If the position is close to xheight or baseline,
        then answer that y position of the glyph. Otherwise the position is
        answered relative to what x-height would have been. This way the
        accents are assumed to be positioned on x-height and the other vertical
        positions are moving relative to that.

        The <i>position</i> attriibute is one of <b>(C.ANCHORTOP, C.ANCHOR_TOP,
        C.ANCHORBOTTOM, C.ANCHOR_BOTTOM, C.ANCHORCENTER, C.ANCHOR_CENTER)</b>.
        The “_” in the name indicates the position of an accent, which is on
        the opposite side of the glyph anchor.  For the horizontal position the
        context of the point is examined. Since we cannot count on the amount
        of points (a serif with many points would add more value to the
        average, where the shape itself may not be very different.  So the
        measure is done by counting the length and position of horizontal
        "scanlines" and their position to the target point.
        """
        # Test if there are any contours at all.
        if not self.hasContours():
            return None, None

        if position == self.C.ANCHORTOP:
            # Get the x position on top of the glyph, averaged by the y position of the point.
            # The more vertical distance there is, relative to the top point, the less this
            # x position will add to the total.
            # First find the bou
            maxY = self.maxY
            if maxY is None:
                x = y = 0
            else:
                x = self.getAverageXByWeightedScanlineYDistance(maxY)
                y = maxY

        elif position == self.C.ANCHOR_BOTTOM:
            # This is requesting the position of an accent, use the width as bounding box now and
            x = self.width / 2
            y = 0 # Top of bottom accents is defined to be on the baseline

        elif position in (self.C.ANCHOR_CENTER, self.C.ANCHORCENTER):
            minX = self.minX
            maxX = self.maxX
            minY = self.minY
            maxY = self.maxY
            if minX is None or maxX is None or minY is None or maxY is None:
                x = y = 0
            else:
                x = TX.asRoundedInt((minX + maxX) / 2)
                y = TX.asRoundedInt((minY + maxY) / 2)

        elif position == self.C.ANCHORBOTTOM:
            # Get the bounding box of the bottom half of the glyph, where the
            # top line is slightly under the middle, in order to include the
            # points that are more ore less on half y. Take value a little
            # higher (em/20) to add round extremes
            minY = self.minY
            if minY is None:
                x = y = 0
            else:
                x = self.getAverageXByWeightedScanlineYDistance(minY)
                y = minY

        else: # position == C.ANCHOR_TOP:
            # This is requesting the position of an accent, use the width as
            # bounding box now and Get xheight from a set of glyphs in the
            # font, not from this glyph and not from the font info. Guess it
            # from the real data.  y values. By definition take to smallest.
            x = self.width / 2
            y = self.parent.xHeight

        return int(round(x)), int(round(y))

    # ---------------------------------------------------------------------------------------------------------
    #    S C A N N I N G

    def getAverageXByWeightedScanlineYDistance(self, py):
        u"""
        Answers the averaged x value by measuring against black parts of a set
        of scan lines. This way we can calculate the average middle point of
        all scan lines, but weighted against the distance to the target py
        value. The more distance between the target and a scan line, the less
        the black of that line will contribute to the overall average. To
        optimize for speed, the distance to the next scan line is incremented
        getting further away from the starting value py. We calculate upwards
        to the yMax and downwards to the yMin. The contribution of black is
        reducing reciprocal quadratic by the vertical distance, so in practice
        the bottom bar of an L has (almost) no influence on the horizontal
        position of an anchor at the top of the stem. The exception to all
        this, is that is there is a single extreme point with an y that is
        equal to py, then this point is answered. We want o void, e.g. that the
        serifs of C, will answer the x value of that point.
        """
        glyph = self.glyph
        #em = self.unitsPerEm
        minX, minY, maxX, maxY = self.boundings
        # Sum average the x values of scanlines
        totalLines = 0
        # Loop through the set of scanlines that intersect with the glyph
        countLines = 0
        step = 2 # Incrementing step to the next scan line
        dy = 0 # Current relative offset to py
        topY = maxY - py # The y top area for scan lines
        botY = py - minY # The y bottom area for scan lines
        limitY = max(topY, botY) # We run the dy of scan lines in this range
        while dy <= limitY:
            weight = 100.0 / max(dy, 1) # Relevance of scanline decreases 1/dy by distance from py
            # Note that if py is equal to one of the vertical extremes, one of the two calls won't have effect.
            if dy < topY: # Do incremental scanline above the py
                xSum, xCount = self._getScanLineSumCount(py, edges)
                if xCount: # If there were any black pixels, add the to the average.
                    totalLines += weight * xSum
                    countLines += weight * xCount
                    # if step < 2:
                    #    print 'top', py, dy, step, weight, topY, botY, py + dy, edges, xSum, xCount
            if dy < botY: # Do incremental scanline below the py
                line = ((minX - 20, py - dy), (maxX + 20, py - dy)) # Take safe x range for the scan line, it may try to hit a curve without extreme.
                edges = self.intersectWithLine(NakedWrapper(glyph), line)
                xSum, xCount = self._getScanLineSumCount(py, edges)
                if xCount: # If there were any black pixels, add them to the average.
                    totalLines += weight * xSum
                    countLines += weight * xCount # Count the averaging total
                    # if step < 2:
                    #    print 'bottom', py, dy, step, weight, topY, botY, py - dy, edges, xSum, xCount
            step *= 1.01
            dy += int(step)
        # Position could be determined, set anchor on y-axis by default.
        if countLines == 0:
            return 0
        # Answers the calculated average
        return totalLines / countLines

    def _getScanLineSumCount(self, py, edges):
        u"""Better not to use a for loop, since the step is changing."""
        xList = []
        for i in range(0, len(edges), 2): # Take white-black and black-white together
            if len(edges) == 1: # Scan line hits e.g. round top or bottom
                averageX = edges[0][0] # Must be an extreme or horizontal inflection. Take single value as average
                xList.append(averageX)
            elif i + 1 < len(edges): # Must be hitting black area, average to the edge with white area
                x1 = int(edges[i][0])
                x2 = int(edges[i + 1][0])
                xList += range(min(x1, x2), max(x1, x2))
            else: # At the end of the list, this must be a local extreme single point.
                averageX = edges[i][0]
                xList.append(averageX)
        return sum(xList), len(xList)

    def getLeftWhiteScanLines(self, step):
        u"""Answers the list of left white scan lines from <i>py1</i> to
        <i>py2</i> by <i>step</i>."""
        lines = []
        left, bottom, right, top = self.boundings
        for y in range(bottom, top, step):
            line = ((left, y), (right, y)) # Take safe x range for the scan line, it may try to hit a curve without extreme.
            lines.append(self.intersectWithLine(NakedWrapper(self.glyph), line))
        return lines

    # ---------------------------------------------------------------------------------------------------------
    #    V A L U E  B Y  N A M E

    def getPointByNamedValue(self, name):
        u"""
        Answers the value (as point, where x or y depend on the type of value)
        as indicated by name.
        """
        hook = '_getPointByNamedValue_' + name
        if not hasattr(self, hook):
            return None
        return getattr(self, hook)()

    def _getPointByNamedValue_leftMargin(self):
        return NSPoint(self.leftMargin, 0)

    def _getPointByNamedValue_rightMargin(self):
        return NSPoint(self.rightMargin, 0)

    def show(self):
        if DEBUG: t = time.time()
        s = []
        s.append('\n=== Glyph Data %s' % self.glyph.name)
        s.append('\n\n...FUZZ %s' % self.fuzz)

        components = self.components
        if components:
            s.append('\n\n...COMPONENTS')
            for component in components:
                s.append('\nComponent %s' % component.baseGlyph)

        bb = self.boundingBox
        s.append('\n\n...BOUNDING BOX')
        s.append('\nX LEFT')
        for pc in bb.left:
            s.append(' %s' % pc.index)
            if pc.glyphName is not None:
                s.append(' (%s)' % pc.glyphName)
        s.append('\nX RIGHT')
        for pc in bb.right:
            s.append(' %s' % pc.index)
            if pc.glyphName is not None:
                s.append(' (%s)' % pc.glyphName)
        s.append('\nY BOTTOM')
        for pc in bb.bottom:
            s.append(' %s' % pc.index)
            if pc.glyphName is not None:
                s.append(' (%s)' % pc.glyphName)
        s.append('\nY TOP')
        for pc in bb.top:
            s.append(' %s' % pc.index)
            if pc.glyphName is not None:
                s.append(' (%s)' % pc.glyphName)

        sidebearings = self.sideBearings
        if sidebearings:
            s.append('\n\n...SIDE BEARINGS')
            for sidebearing in sidebearings:
                s.append('\n%s' % sidebearing)

        verticals = self.verticals # Get dictionary of verticals
        if verticals:
            s.append('\n\n...VERTICALS')
            for x, pcs in sorted(verticals.items()):
                s.append('\n %s %s' % (x, pcs))

        stems = self.stems
        if stems:
            s.append('\n\n...STEMS')
            for size, sizedstems in sorted(stems.items()):
                for stem in sizedstems:
                    s.append('\n%s %s' % (size, stem))

        stems = self.roundStems
        if stems:
            s.append('\n\n...ROUND STEMS')
            for size, roundedsizedstems in sorted(stems.items()):
                for stem in roundedsizedstems:
                    s.append('\n%s %s' % (size, stem))

        horizontals = self.horizontals # Get dictionary of horizontals
        if horizontals:
            s.append('\n\n...HORIZONTALS')
            for y, pcs in sorted(horizontals.items()):
                s.append('\n%s %s' % (y, pcs))

        bars = self.bars
        if bars:
            s.append('\n\n...BARS')
            for size, sizedBars in sorted(bars.items()):
                for bar in sizedBars:
                    s.append('\n%s %s' % (size, bar))

        bars = self.roundBars
        if bars:
            s.append('\n\n...ROUND BARS')
            for size, roundedsizedbar in sorted(bars.items()):
                for bar in roundedsizedbar:
                    s.append('\n%s %s' % (size, bar))

        diagonals = self.diagonalStems
        if diagonals:
            s.append('\n\n...DIAGONALS')
            for size, sizedDiagonals in sorted(diagonals.items()):
                for diagonal in sizedDiagonals:
                    s.append('\n%s %s' % (size, diagonal))

        inflections = self.inflections
        if inflections:
            s.append('\n\n...INFLECTIONS')
            for inflection in inflections:
                s.append('\n%s' % inflection)
        """
        heights = self.heights
        s.append('\n\n...HEIGHTS')
        for height in sorted(heights.items()):
            s.append('\n%s' % height)
        """
        serifs = self.serifs
        if serifs:
            s.append('\n\n...SERIFS')
            for sid, serif in serifs.items():
                s.append('\n%s' % (sid, serif))

        roundOvershoots = self.roundOvershoots
        if roundOvershoots:
            s.append('\n\n...ROUND OVERSHOOTS')
            for rid, roundOvershoot in roundOvershoots.items():
                s.append('\n%s' % (rid, roundOvershoot))

        terminals = self.terminals
        if terminals:
            s.append('\n\n...TERMINALS')
            for tid, terminal in terminals.items():
                s.append('\n%s' % (tid, terminal))

        if DEBUG: print '### GlyphAnalyzer: %0.2d' % (t - time.time())
        return ''.join(s)


if __name__ == "__main__":
    from lib.fontObjects.robofabWrapper import FBfabWrapperFont
    from lib.fontObjects.factories import registerAllDoodleFactories

    registerAllDoodleFactories()
    glyphName = 'H'
    font = FBfabWrapperFont(path='/FontDevelopment/TypeNetworkMasters/trunk/TypeNetwork/TruthFB/TruthFB-Regular.ufo', showUI=False)
    glyph = font[glyphName]
    g = glyph.naked()
    """
    print FontQuery.isQuadraticFont(font)
    print bool(glyph.preferedSegmentType == C.POINTTYPE_QUADRATIC)
    print g.hasSplinesCurves
    print FontQuery.isBezierFont(font)
    print bool(glyph.preferedSegmentType == C.POINTTYPE_BEZIER)
    print g.hasBezierCurves
    """
    for contour in g:
        print 'Clockwise', contour.clockwise

    ga = GlyphAnalyzer(font, glyphName)
    print ga.show()
    g = glyph
    # g = glyph.getLayer('noverlap')
    i = 0
    """
    for contour in g:
        prev = None
        for p in contour.points:
            print i, p, p.labels,
            if prev is None:
                print
            else:
                print ga.isRightBlack(prev, p, contour.clockwise)
            i += 1
            prev = p
    """
