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
#     glyphanalyzer.py
#
#     Implements a PageBot font classes to get info from a TTFont.
#
import weakref

from pagebot.toolbox.transformer import point2D, asInt
from apointcontextlist import Vertical, Horizontal
from stems import Stem, Bar, Counter, VerticalCounter

SPANSTEP = 4

class GlyphAnalyzer(object):

    VERTICAL_CLASS = Vertical # Allow inheriting classes to change this
    HORIZONTAL_CLASS = Horizontal
    STEM_CLASS = Stem
    BAR_CLASS = Bar
    COUNTER_CLASS = Counter
    VERTICAL_COUNTER_CLASS = VerticalCounter

    def __init__(self, style, name):
        self._style = style
        self.name = name

        # Get cache initialize on first access by any property.
        self._horizontals = None
        self._stems = None # Recognized stems, so not filtered by FloqMemes
        self._roundStems = None # Recognized round stems, not filtered by FloqMemes

        self._verticals = None
        self._bars = None # Recognized bars, so not filtered by FloqMemes
        self._roundBars = None # Recognized round bars, so not filtered by FloqMemes
        self._blueBars = None # Tuple of 3 bars for minY->up, baseline->up, maxY->down.

    def _get_glyph(self):
        return self._style[self.name]
    glyph = property(_get_glyph)

    def __repr__(self):
        return '<Analyzer of %s[%s]>' % (self.style.info.fullName, self.name)

    #   M E T R I C S

    def _get_width(self):
        return self.glyph.width
    width = property(_get_width)
    
    #   V E R T I C A L S

    # self.verticals
    def _get_verticals(self):
        if self._verticals is None:
            self.findVerticals()
        return self._verticals
    verticals = property(_get_verticals)

    def findVerticals(self):
        u"""The findVerticals method answers a list of verticals."""
        self._verticals = verticals = {}

        for pc in sorted(self.glyph.pointContexts):
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
        u"""
        The findHorizontals method answers a list of horizontals where the
        main point is on curve."""
        self._horizontals = horizontals = {}

        for pc in sorted(self.glyph.pointContexts):
            if pc.isHorizontal():
                if not pc.y in horizontals:
                    horizontals[pc.y] = self.HORIZONTAL_CLASS()
                horizontals[pc.y].append(pc)

    #   B L A C K

    def spanRoundsOnBlack(self, pc0, pc1):
        u"""Answers the boolean flag if the line between <i>pc0</i> and
        <i>pc1</i> just spans black area."""
        return self.lineOnBlack(pc0, pc1)

    def middleLineOnBlack(self, pc0, pc1, step=SPANSTEP):
        m0 = pc0.middle()
        m1 = pc1.middle()
        return self.spanBlack(m0, m1, step)

    def lineOnBlack(self, p0, p1, step=SPANSTEP):
        u"""Answers the boolean flag if the line between point p0 and p1
        is entirely running on black, except for the end point. To
        test if the line is entirely on black, use <b>self.lineInBlack()"""
        return self.spanBlack(p0, p1, step)

    def onBlack(self, p):
        u"""Answers the boolean flag is the single point (x, y) is on black."""
        return self.glyph.onBlack(p)

    def spanBlack(self, p0, p1, step=SPANSTEP):
        u"""The spanBlack method answers the boolean flag if the number
        of recursive steps between p1 and p2 are on black area
        of the glyph. If step is smaller than the distance between the points,
        then just check in the middle of the line.  The method does not check
        on the end points of the segment, allowing to test these separate
        through self.onBlack or self.coveredInBlack."""
        dx = p1[0] - p0[0]
        dy = p1[1] - p0[1]
        distance = dx*dx + dy*dy # Save sqrt time, compare with square of step
        m = p0[0] + dx/2, p1[1] + dy/2
        result = self.onBlack(m) # Check the middle of the vector distance.
        if distance > step*step: # Check for the range of steps if the middle point of the line is still on black
            result = result and self.spanBlack(p0, m, step) and self.spanBlack(m, p1, step)
        # Check if distance is still larger than step, otherwise just check in the middle
        return result

    #   W H I T E

    def spanWhite(self, p0, p1, step=SPANSTEP):
        u"""The <b>spanWhite</b> method answers the boolean flag if the number
        of recursive steps between <i>pc0</i> and <i>pc1</i> are all on white
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
        u"""Answers the boolean flag if the line is just spanning white area."""
        return self.spanWhite(pc0, pc1, step)

    def onWhite(self, p):
        u"""Answers the boolean flag if the single point <b>(x, y)</b> is on
        white."""
        return not self.onBlack(p)

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

    #   S T E M S

    # self.stems
    def _get_stems(self):
        if self._stems is None:
            self.findStems()
        return self._stems
    stems = property(_get_stems)

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
                            size = TX.asInt(stem.size) # Make sure not to get floats as key
                            if not size in stems:
                                stems[size] = []
                            stems[size].append(stem)

                        elif self.isRoundStem(pc0, pc1):
                            # If either of the point context is a curve extreme
                            # then count this stem as round stem
                            stem = self.STEM_CLASS(pc0, pc1, self.glyph.name)
                            size = TX.asInt(stem.size) # Make sure not to get floats as key
                            if not size in roundStems:
                                roundStems[size] = []
                            roundStems[size].append(stem)

                        elif self.isStraightRoundStem(pc0, pc1):
                            # If one side is straight and the other side is round extreme
                            # then count this stem as straight round stem.
                            stem = self.STEM_CLASS(pc0, pc1, self.glyph.name)
                            size = TX.asInt(stem.size) # Make sure not to get floats as key
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

    def isStem(self, pc0, pc1):
        u"""The isStem method takes the point contexts pc0 and
        pc1 to compare if the can be defined as a “stem”: if they are
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

    #   C O U N T E R

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

    #   B A R S

    # self.bars
    def _get_bars(self):
        if self._bars is None:
            self.findBars()
        return self._bars
    bars = property(_get_bars)

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

 
