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
#     glyphanalyzer.py
#
#     Implements a PageBot font classes to get info from a TTFont.
#
import sys
import weakref

# TODO: Import needs to be done inside DrawBotContext
#from AppKit import NSBezierPath

from pagebot.toolbox.transformer import asInt
from pagebot.fonttoolbox.analyzers.apointcontextlist import Vertical, Horizontal
from pagebot.fonttoolbox.analyzers.stems import Stem, Bar, Counter, VerticalCounter
from pagebot.fonttoolbox.analyzers.apointcontext import APointContext

SPANSTEP = 4

class GlyphAnalyzer:

    FUZZ = 4 # Default amount that a value can be off while treated the same.

    VERTICAL_CLASS = Vertical # Allow inheriting classes to change this
    HORIZONTAL_CLASS = Horizontal
    STEM_CLASS = Stem
    BAR_CLASS = Bar
    COUNTER_CLASS = Counter
    VERTICAL_COUNTER_CLASS = VerticalCounter

    def __init__(self, glyph):
        self.glyph = glyph # Set weakref to glyph
        self.reset()

    def reset(self):
        """Clear all cached value to force recalculation."""
        # Get cache initialize on first access by any property.
        self._horizontals = None
        self._stems = None # Recognized stems, so not filtered by FloqMemes
        self._stem = None # Holds cache of the left most stem found
        self._roundStems = None # Recognized round stems, not filtered by FloqMemes
        self._straightRoundStems = None
        self._allStems = None
        self._allHorizontalCounters = None

        self._verticals = None
        self._bars = None # Recognized bars, so not filtered by FloqMemes
        self._roundBars = None # Recognized round bars.
        self._straightRoundBars = None # Bars with round on one side and straight on the other size.
        self._allBars = None # Collection of all types of bars
        self._allVerticalCounters = None

        self._blueBars = None # Collect bloeBars from H on property call.
        self._bottomBlueBar = None
        self._baselineBlueBar = None
        self._topBlueBar = None

        # User defined dimensions, overruling automatic analyzer dimensions (UFO only)
        self._dimensions = None

    def _get_name(self):
        return self.glyph.name
    name = property(_get_name)

    # self.glyph    Weakref to the glyph
    def _get_glyph(self):
        return self._glyph() # Can be None, in case of broken weakref.
    def _set_glyph(self, glyph):
        # Set the weakref to the glyph
        self._glyph = weakref.ref(glyph)
    glyph = property(_get_glyph, _set_glyph)

    def _get_font(self):
        glyph = self.glyph
        if glyph is not None:
            return self.glyph.font
        return None # Could not find glyph, maybe broken weakref.
    font = property(_get_font)

    def _get_parent(self):
        """Answers the analyzer of the parent font."""
        font = self.font
        if font is not None:
            return font.analyzer
        return None # Could not find font, maybe broken weakref.
    parent = property(_get_parent)

    def __repr__(self):
        return '<Analyzer of %s[%s]>' % (self.font.info.fullName, self.name)

    #   M E T R I C S

    def _get_width(self):
        return self.glyph.width
    width = property(_get_width)

    def _get_leftMargin(self):
        return self.glyph.minX
    leftMargin = property(_get_leftMargin)

    def _get_rightMargin(self):
        return self.glyph.width - self.glyph.maxX
    rightMargin = property(_get_rightMargin)

    def _get_dimensions(self):
        if self._dimensions is None:
            # TODO: Needs to be written
            self._dimensions = [] # User defined dimension references, overruling analyzer findings (UFO only)
        return self._dimensions
    dimensions = property(_get_dimensions)

    #   V E R T I C A L S

    # self.verticals
    def _get_verticals(self):
        if self._verticals is None:
            self.findVerticals()
        return self._verticals
    verticals = property(_get_verticals)

    def findVerticals(self):
        """The findVerticals method answers a list of verticals."""
        self._verticals = verticals = {}

        for pc in self.glyph.pointContexts:
            if pc.isVertical():
                if not pc.x in verticals:
                    verticals[pc.x] = self.VERTICAL_CLASS()
                verticals[pc.x].append(pc)

    #   H O R I Z O N T A L S

    # self.horizontals
    def _get_horizontals(self):
        if self._horizontals is None:
            self.findHorizontals()
        return self._horizontals
    horizontals = property(_get_horizontals)

    def findHorizontals(self):
        """The findHorizontals method answers a list of horizontals where the
        main point is on curve."""
        self._horizontals = horizontals = {}

        for pc in self.glyph.pointContexts:
            if pc.isHorizontal():
                if not pc.y in horizontals:
                    horizontals[pc.y] = self.HORIZONTAL_CLASS()
                horizontals[pc.y].append(pc)

    #   B L A C K

    def spanRoundsOnBlack(self, pc0, pc1):
        """Answers if the line between *pc0* and
        *pc1* just spans black area."""
        return self.lineOnBlack(pc0, pc1)

    def middleLineOnBlack(self, pc0, pc1, step=SPANSTEP):
        m0 = pc0.middle()
        m1 = pc1.middle()
        return self.spanBlack(m0, m1, step)

    def lineOnBlack(self, p0, p1, step=SPANSTEP):
        """Answers if the line between point p0 and p1
        is entirely running on black, except for the end point. To
        test if the line is entirely on black, use **self.lineInBlack()"""
        return self.spanBlack(p0, p1, step)

    def onBlack(self, p):
        """Answers is the single point (x, y) is on black."""
        # TODO: We need to make a method to have the context available here.
        from pagebot import getContext
        context = getContext()
        glyphPath = context.getGlyphPath(self.glyph)
        return context.onBlack(p, glyphPath)

    def spanBlack(self, p0, p1, step=SPANSTEP):
        """The spanBlack method answers if the number
        of recursive steps between p1 and p2 are on black area
        of the glyph. If step is smaller than the distance between the points,
        then just check in the middle of the line.  The method does not check
        on the end points of the segment, allowing to test these separate
        through self.onBlack or self.coveredInBlack."""
        dx = p1[0] - p0[0]
        dy = p1[1] - p0[1]
        distance = dx*dx + dy*dy # Save sqrt time, compare with square of step
        m = p0[0] + dx/2, p0[1] + dy/2
        result = self.onBlack(m) # Check the middle of the vector distance.
        if distance > step*step: # Check for the range of steps if the middle point of the line is still on black
            result = result and self.spanBlack(p0, m, step) and self.spanBlack(m, p1, step)
        # Check if distance is still larger than step, otherwise just check in the middle
        return result

    #   W H I T E

    def spanWhite(self, p0, p1, step=SPANSTEP):
        """The **spanWhite** method answers if the number
        of recursive steps between *pc0* and *pc1* are all on white
        area of the glyph. If step is smaller than the distance between the
        points, then just check in the middle of the line.  """
        dx = p1[0] - p0[0]
        dy = p1[1] - p1[1]
        distance = dx*dx + dy*dy # Save sqrt time, compare with square of step
        m = p0[0] + dx/2, p0[1] + dy/2
        result = self.onWhite(m) # Just take the middle of this small distance.
        if distance > step*step: # Check for the range of steps if that point of the line is still on black
            result = result and self.spanWhite(p0, m, step) and self.spanWhite(m, p1, step)
        # Check if distance is still larger than step, otherwise just check in the middle
        return result

    def lineOnWhite(self, pc0, pc1, step=SPANSTEP):
        """Answers if the line is just spanning white area."""
        return self.spanWhite(pc0, pc1, step)

    def onWhite(self, p):
        """Answers if the single point **(x, y)** is on
        white."""
        return not self.onBlack(p)

    def overlappingLinesInWindowOnBlack(self, pc0, pc1, step=SPANSTEP):
        """Answers if the vertical span between *pc0*
        and *pc1* just spans black area, by stepping from a point on one
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
        """See **self.overlappingLinesInWindowOnBlack**."""
        pp0, pp1 = pc0.getProjectedWindowLine(pc1)
        return not None in (pp0, pp1) and self.lineOnWhite(pp0, pp1, step)

    #   S T E M S

    # self.stems
    def _get_stems(self):
        if self._stems is None:
            self.findStems()
        return self._stems
    stems = property(_get_stems)

    def findStems(self):
        """The @findStems@ method finds the stems in the current glyph and
        assigns them as dictionary to @self._stems@. Since we cannot use the
        CVT of the glyph (the analyzer is used to find these values, not to use
        them), we'll make an assumption about the pattern of vertices found. It
        is up to the caller to make sure that the current glyph is relevant in
        the kind of vertices that we are looking for.

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
                            stem = self.STEM_CLASS(pc0, pc1, self.glyph.name)
                            size = asInt(stem.size) # Make sure not to get floats as key
                            if not size in stems:
                                stems[size] = []
                            stems[size].append(stem)

                        elif self.isRoundStem(pc0, pc1):
                            # If either of the point context is a curve extreme
                            # then count this stem as round stem
                            stem = self.STEM_CLASS(pc0, pc1, self.glyph.name)
                            size = asInt(stem.size) # Make sure not to get floats as key
                            if not size in roundStems:
                                roundStems[size] = []
                            roundStems[size].append(stem)

                        elif self.isStraightRoundStem(pc0, pc1):
                            # If one side is straight and the other side is round extreme
                            # then count this stem as straight round stem.
                            stem = self.STEM_CLASS(pc0, pc1, self.glyph.name)
                            size = asInt(stem.size) # Make sure not to get floats as key
                            if not size in straightRoundStems:
                                straightRoundStems[size] = []
                            straightRoundStems[size].append(stem)

                        elif self.isHorizontalCounter(pc0, pc1):
                            # If there is just whitspace between the points and they are some kind of extreme,
                            # then assume this is a counter.
                            counter = self.COUNTER_CLASS(pc0, pc1, self.glyph.name)
                            size = asInt(counter.size)
                            if not size in horizontalCounters:
                                horizontalCounters[size] = []
                            horizontalCounters[size].append(counter)

        return self._stems

    def isStem(self, pc0, pc1, tolerance=0):
        """The isStem method takes the point contexts pc0 and pc1 to compare if
        the can be defined as a “stem”: if they are not round extremes, if the
        two point contexts have overlap in the vertical directions (being part
        of the same window) that runs on black and if both lines are not
        entirely covered in black."""
        return not pc0.isHorizontalRoundExtreme(tolerance) \
            and not pc1.isHorizontalRoundExtreme(tolerance)\
            and pc0.isVertical(tolerance) and pc1.isVertical(tolerance)\
            and pc0.inHorizontalWindow(pc1)\
            and self.middleLineOnBlack(pc0, pc1)\
            and self.overlappingLinesInWindowOnBlack(pc0, pc1)
            #and not (self.pointCoveredInBlack(pc0) or self.pointCoveredInBlack(pc1))

    # self.roundStems
    def _get_roundStems(self):
        if self._roundStems is None:
            self.findStems() # Cache finds of both stems and round stems
        return self._roundStems
    roundStems = property(_get_roundStems)

    # self.straightRoundStems
    def _get_straightRoundStems(self):
        if self._straightRoundStems is None:
            self.findStems() # Cache finds of both stems and round stems
        return self._straightRoundStems
    straightRoundStems = property(_get_straightRoundStems)

    def getBeamStemCounters(self, context, y=None):
        """Calculate the stems and counters by a horizontal beam through the middle of the bounding box.
        This works best with the capital I. The value is uncached and should only be used if
        normal stem detection fails. Or in case of italic."""
        beamStems = {}
        beamCounters = {}
        if y is None:
            y = (self.maxY - self.minY)/2
        line = ((-sys.maxsize, y), (sys.maxsize, y))
        # Get intersections with this line. We can assume they are sorted set by x value
        intersections = self.intersectWithLine(line, context)
        # If could not make path or flattened path or no intersections or just one, give up.
        if intersections is None or len(intersections) < 2:
            return None
        # Now make Stem instance from these values, as if they we Verticals positions.
        # The difference is that we only have points, not point contexts here,
        # but for limited use that should not make a difference for entry in a Stem
        p0 = ap0 = None
        for n in range(0, len(intersections)):
            # Add this stem or counter to the result. Create point contexts, simulating vertical
            # We cannot just check on odd/even, as a line may pass exactly on the top/bottom of a curve.
            p = intersections[n]
            pUp = p[0], p[1]+10
            pDown = p[0], p[1]-10
            ap = APointContext((pUp, pUp, pUp, p, pDown, pDown, pDown)) # Simulate vertical context.

            if p0 is None:
                p0 = p
                ap0 = ap
                continue

            p1 = p0
            ap1 = ap0
            p0 = p
            ap0 = ap

            # If middle of the point is on black, then it is a stem. Otherwise it is a counter.
            mp = (p0[0]+p1[0])/2, (p0[1]+p1[1])/2
            if self.onBlack(mp):
                stem = self.STEM_CLASS(ap1, ap0, self.glyph.name)
                size = asInt(stem.size) # Make sure not to get floats as key
                if not size in beamStems:
                    beamStems[size] = []
                beamStems[size].append(stem)
            else: # Otherwise, middle point between intersections is on white, it must be a counter
                counter = self.COUNTER_CLASS(ap1, ap0, self.glyph.name)
                size = asInt(counter.size) # Make sure to get floats as key
                if not size in beamCounters:
                    beamCounters[size] = []
                beamCounters[size].append(counter)
        return beamStems, beamCounters

    def isPortrait(self, pc0, pc1):
        """Stems are supposed to be portrait within the FUZZ range. May not
        work in all extremely wide or narrow glyphs."""
        return not self.isLandscape(pc0, pc1)

    def isRoundStem(self, pc0, pc1):
        """The **isRoundStem** method answers if the
        *pc0* and *pc1* define a round stem. This is @True@ if one of
        both of point contexts are extremes and if both, they must “bend” in
        the same direction.

        Also there should be overlap in horizontal direction and the point
        context should span black only.  """
        return pc0.isHorizontalRoundExtreme()\
            and pc1.isHorizontalRoundExtreme()\
            and self.spanRoundsOnBlack(pc0, pc1)

    def isStraightRoundStem(self, pc0, pc1):
        """Answers if one of (pc0, pc1) is a straight extreme
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

    # self.allStems      Answers the combination dict of stems and round stems
    def _get_allStems(self):
        """Collect all stems in the dictionary with their value as key."""
        if self._allStems is None:
            self.findStems()
            self._allStems = {}
            for value, stems in self.stems.items():
                self._allStems[value] = stems
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

    def _get_stem(self):
        """Answers left stem. Answer None if no stems can be found."""
        if self._stem is None:
            self.findStems()
            for stems in self.allStems.values():
                for stem in stems:
                    if self._stem is None or stem.parent[0] < self._stem.parent[0]:
                        self._stem = stem
        return self._stem
    sortedStems = property(_get_stem)

    #   H O R I Z O N T A L  C O U N T E R

    def isHorizontalCounter(self, pc0, pc1, tolerance=0):
        """Answers is the connection between pc0.x and pc1.x
        is running entirely over white, and they both are some sort of
        horizontal extreme. The connection is a “white stem”."""
        #print('pc0', pc0, pc0.isHorizontalRoundExtreme(tolerance), pc0.isVertical(tolerance))
        #print('pc1', pc1, pc1.isHorizontalRoundExtreme(tolerance), pc1.isVertical(tolerance))
        #print('===', pc0.inHorizontalWindow(pc1))
        #print('---', self.lineOnWhite(pc0, pc1, 50), self.lineOnWhite(pc1, pc0, 50))
        if not (pc0.isHorizontalRoundExtreme(tolerance) or pc0.isVertical(tolerance)):
            return False
        if not (pc1.isHorizontalRoundExtreme(tolerance) or pc1.isVertical(tolerance)):
            return False
        if not pc0.inHorizontalWindow(pc1):
            return False
        # Don't use plain self.lineOnWhite(pc0, px1) here, as corner-->roundExtreme (as in the counter of "P"
        # will be too close to the horizontal stroke, so it's recognized as black. Instead we take bigger steps
        # from the corner point, so the iterations of the line are always white.
        return self.lineOnWhite(pc0, pc1, 50) or self.lineOnWhite(pc1, pc0, 50)

    def _get_horizontalCounters(self):
        if self._allHorizontalCounters is None:
            self.findStems()
        return self._allHorizontalCounters
    horizontalCounters = property(_get_horizontalCounters)

    def _get_hotizontalCounter(self):
        """Answers single horizontal counter value, which by definintion is the smallest straight counter found.
        Answer None if no counters can be found."""
        counters = self.horizontalCounters.keys()
        if counters:
            return min(counters)
        return None
    horizontalCounter = property(_get_hotizontalCounter)

    #   V E R T I C A L  C O U N T E R

    def isVerticalCounter(self, pc0, pc1, tolerance=0):
        """Answers is the connection between pc0.y and pc1.y
        is running entirely over white, and they both are some sort of
        horizontal extreme. The connection is a “white bar”."""
        if not (pc0.isVerticalRoundExtreme(tolerance) or pc0.isHorizontal(tolerance)):
            return False
        if not (pc1.isVerticalRoundExtreme(tolerance) or pc1.isHorizontal(tolerance)):
            return False
        if not pc0.inVerticalWindow(pc1):
            return False
        # Don't use plain self.lineOnWhite(pc0, px1) here, as corner-->roundExtreme (as in the counter of "P"
        # will be too close to the horizontal stroke, so it's recognized as black. Instead we take bigger steps
        # from the corner point, so the iterations of the line are always white.
        return self.lineOnWhite(pc0, pc1, 50) or self.lineOnWhite(pc1, pc0, 50)

    def _get_verticalCounters(self):
        if self._allVerticalCounters is None:
            self.findBars()
        return self._allVerticalCounters
    verticalCounters = property(_get_verticalCounters)

    #   B A R S

    # self.bars
    def _get_bars(self):
        if self._bars is None:
            self.findBars()
        return self._bars
    bars = property(_get_bars)

    def findBars(self):
        """The @findBars@ method finds the bars in the current glyph and
        assigns them as dictionary to @self._bars@. Since we cannot use the CVT
        of the glyph (the analyzer is user to find these values, not to use
        them), we'll make an assumption about the pattern of vertices found. It
        is up to the caller to make sure that the current glyph is relevant in
        the kind of vertices that we are looking for."""
        horizontals = self.horizontals
        self._bars = bars = {}
        # BlueBars by separate property call
        self._roundBars = roundBars = {}
        self._straightRoundBars = straightRoundBars = {}
        self._verticalCounters = verticalCounters = {}
        self._verticalRoundCounters = verticalRoundCounters = {}
        self._verticalMixedCounters = verticalMixedCounters = {}
        self._allVerticalCounters = allVerticalCounters = {} # Space between all neighboring stems, running over white only.


        checked = set() # Store what we checked, to avoid doubles in the loops
        dimensions = self.dimensions
        if dimensions:
            for dimension in dimensions: # UFO only, needs to be written.
                if self.FLOQMEME_BAR in dimensions['types']: # Is this this dimension defining a stem?
                    bar = self.BAR_CLASS(dimensions['pc0'], dimensions['pc1'], self.glyph.name)
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
                                bar = self.BAR_CLASS(pc0, pc1, self.glyph.name)
                                size = asInt(bar.size) # Make sure not to get floats as keys
                                if not size in bars:
                                    bars[size] = []
                                bars[size].append(bar)

                            elif self.isRoundBar(pc0, pc1):
                                # If either of the point context is a curve extreme
                                # then count this bar as round bar
                                bar = self.BAR_CLASS(pc0, pc1, self.glyph.name)
                                size = asInt(bar.size) # Make sure not to get floats as keys
                                if not size in roundBars:
                                    roundBars[size] = []
                                roundBars[size].append(bar)

                            elif self.isStraightRoundBar(pc0, pc1):
                                # If one side is straight and the other side is round extreme
                                # then count this stem as straight round bar.
                                bar = self.BAR_CLASS(pc0, pc1, self.glyph.name)
                                size = asInt(bar.size) # Make sure not to get floats as key
                                if not size in straightRoundBars:
                                    straightRoundBars[size] = []
                                straightRoundBars[size].append(bar)

                            elif self.isVerticalCounter(pc0, pc1):
                                # If there is just white space between the points and they are some kind of extreme,
                                # then assume this is a counter.
                                counter = self.VERTICAL_COUNTER_CLASS(pc0, pc1, self.glyph.name)
                                size = asInt(counter.size)

                                if pc0.isHorizontalExtreme() and pc1.isHorizontalExtreme():
                                    if not size in verticalCounters:
                                        verticalCounters[size] = []
                                    verticalCounters[size].append(counter)
                                elif pc0.isHorizontalRoundExtreme() and pc1.isHorizontalRoundExtreme():
                                    if not size in verticalRoundCounters:
                                        verticalRoundCounters[size] = []
                                    verticalRoundCounters[size].append(counter)
                                else:
                                    if not size in verticalMixedCounters:
                                        verticalMixedCounters[size] = []
                                    verticalMixedCounters[size].append(counter)

                                if not size in allVerticalCounters:
                                    allVerticalCounters[size] = []
                                allVerticalCounters[size].append(counter)

        return self._bars

    def isBar(self, pc0, pc1):
        """The **isBar** method takes the point contexts *pc0* and *pc1* to
        compare if the can be defined as a “bar”: if two point contexts have
        overlap in the horizontal directions if the line between them is
        entirely on black, and if the lines are not entirely covered in
        black."""
        return not pc0.isVerticalRoundExtreme()\
            and not pc1.isVerticalRoundExtreme()\
            and pc0.isHorizontal() and pc1.isHorizontal()\
            and self.isVerticalSpanInRange(pc0, pc1, self.font.info.capHeight/2)\
            and self.middleLineOnBlack(pc0, pc1)\
            and self.overlappingLinesInWindowOnBlack(pc0, pc1)
            #and (not self.pointCoveredInBlack(pc0) or not self.pointCoveredInBlack(pc1))

    # self.roundBars
    def _get_roundBars(self):
        if self._roundBars is None:
            self.findBars() # Cache finds of both bars and round bars
        return self._roundBars
    roundBars = property(_get_roundBars)

    # self.straightRoundBars
    def _get_straightRoundBars(self):
        if self._straightRoundBars is None:
            self.findBars() # Cache finds of both bars and round bars
        return self._straightRoundBars
    straightRoundBars = property(_get_straightRoundBars)

    def isVerticalSpanInRange(self, pc0, pc1, dy):
        """Check for vertical spans to be within dy range."""
        return abs(pc0.p.y - pc1.p.y) < dy

    def isLandscape(self, pc0, pc1):
        """Bars are supposed to be landscape within the FUZZ range. May not
        work in all extremely wide or narrow glyphs."""
        if pc0.isVerticalExtreme() or pc1.isVerticalExtreme():
            return True
        return abs(pc0.p.x - pc1.p.x) - abs(pc0.p.y - pc1.p.y) > self.FUZZ

    def isRoundBar(self, pc0, pc1):
        # self.isSameVerticalRoundExtreme(pc0, pc1) and\
        return pc0.isVerticalRoundExtreme()\
            and pc1.isVerticalRoundExtreme()\
            and self.spanRoundsOnBlack(pc0, pc1)

    def isStraightRoundBar(self, pc0, pc1):
        """Answers if one of (pc0, pc1) is a straight extreme
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

    # self.allBars      Answers the combination dict of bars and round bars
    def _get_allBars(self):
        """Collect all bars in the dictionary with their value as key.
        BlueBars are not added to self._allBars, to be addressed separately from self.blueBars """
        if self._allBars is None:
            self.findBars()
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

    #   B L U E B A R S

    def _get_blueBars(self):
        """If not self._blueBars defined, make the 3: minY->up, baseline->up and maxY->down."""
        if self._blueBars is None:
            gaH = self['H'] # Seperate from blueBars property, so no recursion problem.
            if gaH.bars: # Check if there were any bars found for 'H'
                bar = min(sorted(gaH.bars.keys()))
            else: # Otherwise take an arbitrary number for now.
                bar = self.font.info.unitsPerEm/20
            self._bottomBlueBar = self.BLUEBAR_CLASS((0, self.minY), (0, self.minY+bar), self.name, name='bottom')
            self._baselineBlueBar = self.BLUEBAR_CLASS((0, 0), (0, bar), self.name, name='baseline')
            self._topBlueBar = self.BLUEBAR_CLASS((0, self.maxY), (0, self.maxY-bar), self.name, name='top')
            self._blueBars = {self.minY: self._topBlueBar, 0: self._baselineBlueBar, self.maxY: self._topBlueBar}
        return self._blueBars
    blueBars = property(_get_blueBars)

    def _get_bottomBlueBar(self):
        self._get_blueBars() # Make sure they are initialized.
        return self._bottomBlueBar
    bottomBlueBar = property(_get_bottomBlueBar)

    def _get_baselineBlueBar(self):
        self._get_blueBars() # Make sure they are initialized.
        return self._baselineBlueBar
    baselineBlueBar = property(_get_baselineBlueBar)

    def _get_topBlueBar(self):
        self._get_blueBars() # Make sure they are initialized.
        return self._topBlueBar
    topBlueBar = property(_get_topBlueBar)

    #   P O I N T S

    def _get_boundingBox(self):
        return self.glyph.boundingBox
    boundingBox = property(_get_boundingBox)

    # self.maxY         Answers the max Y of self.boundings. (Including components).
    def _get_maxY(self):
        return self.glyph.maxY
    maxY = property(_get_maxY)

    def _get_minY(self):
        return self.glyph.minY
    minY = property(_get_minY)

    def _get_maxX(self):
        return self.glyph.maxX
    maxX = property(_get_maxX)

    # self.minX         Answers the min X of self.boundings. (Including components).
    def _get_minX(self):
        return self.glyph.minX
    minX = property(_get_minX)


