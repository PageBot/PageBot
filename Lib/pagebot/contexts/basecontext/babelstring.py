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
#     babelstring.py
#
#     BabelString is a generic string format, that stores a string or
#     text as a list of BabelRun instances. Those runs can be manipulated
#     without the setting of a context, as long as the methods don't need
#     rendering of the rest flow.
#     A number of operation requires a context to return a rendered native
#     format, such as size, line positions and overflow.
#     For efficiency that rendered string and meta information (such as
#     position of lines) are calculate upon request and stored in the
#     BabelString for later use. Changes to the runs will reset this cache.
#
from copy import copy, deepcopy
import weakref

from pagebot.constants import (DEFAULT_LANGUAGE, DEFAULT_FONT_SIZE, DEFAULT_FONT,
    DEFAULT_LEADING, TOP, LEFT)
from pagebot.fonttoolbox.objects.font import findFont, Font
from pagebot.toolbox.units import units, pt
from pagebot.toolbox.color import color

class BabelRun:
    def __init__(self, s, style=None):
        """Answer the storage for string + style in BabelString.
        Note that the style values of sequential runs are *not* cascading.
        This is similar to the behavior of the DrawBot FormattedString attributes.

        >>> from pagebot.elements import *
        >>> BabelRun('ABCD', dict(font='PageBot-Regular'))
        <BabelRun "ABCD">
        >>> BabelRun('ABCD'*10) # Abbreviated for string > 10 characters.
        <BabelRun "ABCDABCDAB...">
        >>> len(BabelRun('ABCD'*10))
        40
        """
        assert isinstance(s, str)
        self.s = s
        if style is None:
            style = {}
        self.style = style

    def __len__(self):
        return len(self.s)

    def __eq__(self, pbr):
        """
        >>> from pagebot.toolbox.units import pt
        >>> br1 = BabelRun('ABCD')
        >>> br2 = BabelRun('ABCD')
        >>> br1 == br2, br1 is br2
        (True, False)
        >>> br2.style['fontSize'] = pt(12)
        >>> br1 == br2
        False
        """
        if not isinstance(pbr, self.__class__):
            return False
        return self.s == pbr.s and self.style == pbr.style

    def __repr__(self):
        r = '<%s' % self.__class__.__name__
        if self.s:
            s = self.s[:10]
            if s != self.s:
                s += '...'
            r += ' "%s"' % s.replace('\n',' ')
        return r + '>'


class BabelLineInfo:
    def __init__(self, x, y, cLine, context):
        self.x = units(x)
        self.y = units(y)
        self.runs = []
        self.cLine = cLine # Native context line (e.g. CTLine instance.
        self.context = context # Just in case it is needed.

    def __repr__(self):
        return '<%s x=%s y=%s runs=%d>' % (self.__class__.__name__, self.x, self.y, len(self.runs))

class BabelRunInfo:
    def __init__(self, s, style):
        assert isinstance(s, str)
        self.s = s
        self.style = style

    def __repr__(self):
        return '<%s "%s">' % (self.__class__.__name__, self.s)

class BabelString:
    """BabelString is a generic string format, that stores a string or
    text as a list of BabelRun instances.
    Note that the styles values of sequential runs are *not* cascading.
    This is similar to the behavior of the DrawBot FormattedString attributes.
    Plain numbers are by default converted to points.
    Attribute properties refer to the style of the last run.

    >>> from pagebot.toolbox.units import pt, mm
    >>> bs = BabelString('ABCD', style=dict(fontSize=12))
    >>> bs.fontSize
    12pt
    >>>
    >>> bs.fontSize = mm(24)
    >>> bs.fontSize, bs.runs[0].style['fontSize']
    (24mm, 24mm)
    >>> bs.runs # Without context a BabelString can do all that does not need rendering.
    [<BabelRun "ABCD">]

    """
    def __init__(self, s=None, style=None, w=None, h=None, context=None):
        """Constructor of BabelString. @s is a plain string, style is a
        dictionary compatible with the document root style keys to add one
        PageBotRun as default. Otherwise self.runs is created as empty list.
        @s should be a plain string, but gets cast by str(s) otherwise.
        Optional @w and @h make the difference if this BabelString behaves
        as a plain string (answering it's own size) or a text (answering
        the defined size and overflow).
        Some methods only work if context is defined (e.g. self.textSize,
        self.lines and self.overflow)

        >>> bs = BabelString()
        >>> len(bs.runs)
        0
        >>> bs.add('ABCD')
        >>> len(bs), len(bs.runs)
        (4, 1)
        >>> bs.add('EFGH') # Without style, adding to the last run
        >>> len(bs), len(bs.runs)
        (8, 1)
        >>> from pagebot.contexts import getContext
        >>> context = getContext('DrawBot') 
        >>> bs = context.newString('ABCD') 
        >>> # Equivalent do BabelString('ABCD', context=context)
        >>> bs.context
        <DrawBotContext>
        """
        # Context instance @context is used for text size rendering methods.
        self.runs = [] # List of BabelRun instances.
        if s is not None or style is not None:
            self.runs.append(BabelRun(s, style))
        self.context = context # Store optional as weakref property. Clears cache.
        self._w = units(w) # Set source value of the properties, not need clear cache again.
        self._h = units(h) # Set to points, if not already a Unit instance.
        # Cache is initialize by the self.context-->self.reset() property call.
        # In case there is overflow for a given width and height, the overflow indiced
        # store the slice in self.lines for the current everflow render by the context. 
        # _overflowStart Line index where overflow starts.
        # _overflowEnd Line (non-inclusive) 
        # _cs  Cache of native context string (e.g. FormattedString)
        # _lines Cache of calculated meta info after line wrapping.
        # _twh Cache of calculated text width (self.tw, self.th)
        # _pwh Cache of calculated pixel width (self.pw, self.ph)
        
    def _get_context(self):
        """Answer the weakref context if it is defined.

        >>> from pagebot.contexts import getContext
        >>> context = getContext('DrawBot')
        >>> bs = BabelString('ABCD', context=context)
        >>> bs.context
        <DrawBotContext>
        >>> context = None # Delete context reference
        >>> bs.context # But weakref to global context remains
        <DrawBotContext>
        """
        context = None
        if self._context is not None:
            context = self._context()
        return context
    def _set_context(self, context):
        if context is not None:
            context = weakref.ref(context)
        self._context = context
        self.reset() # Clear context cache
    context = property(_get_context, _set_context)

    def reset(self):
        """Clear the context cache, in case the string source changed,
        to force new calculation of context dependent wrapping.

        >>> from pagebot.contexts import getContext
        >>> context = getContext('DrawBot')
        >>> bs = BabelString('ABCD', dict(fontSize=24), context=context)
        >>> bs.cs is not None # Trigger rendering of the FormattedString
        True
        >>> bs.reset() # Reset the caching
        >>> bs._cs is None
        True
        """
        self._cs = None # Cache of native context string (e.g. FormattedString)
        self._lines = None # Cache of calculated meta info after line wrapping.
        self._twh = None # Cache of calculated text width (self.tw, self.th)
        self._pwh = None # Cache of calculated pixel width (self.pw, self.ph)
        self._overflowStart = None # Line index where overflow starts.
        self._overflowEnd = None # Line (non-inclusive) 

    def _get_w(self):
        """Answer the width of this string. If the value if self._w
        is not defined, then answer the self.tw width of the rendered 
        context string.

        >>> from pagebot.toolbox.units import pt
        >>> from pagebot.contexts import getContext
        >>> context = getContext('DrawBot')
        >>> bs = BabelString('ABCD', dict(fontSize=pt(100)), w=pt(1000), context=context)
        >>> bs.w
        1000pt
        >>> bs.tw
        250.9pt
        """
        return self._w or self.tw
    def _set_w(self, w):
        self._w = units(w)
        self.reset() # Force context wrapping to be recalculated.
    w = property(_get_w, _set_w)

    def _get_h(self):
        """Answer the optional height of this string. If the value if self._h
        is not defined, then answer the height of the rendered context string.
        """
        return self._h or self.th
    def _set_h(self, h):
        self._h = units(h)
        self.reset() # Force context wrapping to be recalculated.
    h = property(_get_h, _set_h)

    def _get_hasWidth(self):
        """Answer the boolean flag if self has a width defined (True) or gets
        its width from the rendered self.tw text width.

        >>> bs = BabelString('ABCD')
        >>> bs.hasWidth
        False
        >>> bs.w = pt(500)
        >>> bs.hasWidth
        True
        """
        return self._w is not None
    hasWidth = property(_get_hasWidth)
    
    def _get_hasHeight(self):
        """Answer the boolean flag if self has a height defined (True) or gets
        its height from the rendered self.th text height.

        >>> bs = BabelString('ABCD')
        >>> bs.hasHeight
        False
        >>> bs.h = pt(500)
        >>> bs.hasHeight
        True
        """
        return self._h is not None
    hasHeight = property(_get_hasHeight)
    
    def _get_tw(self):
        """Answer the cached calculated context width

        >>> from pagebot.toolbox.units import em
        >>> from pagebot.contexts import getContext
        >>> bs = BabelString('ABCD') # No context, cannot render.
        >>> bs.th is None
        True
        >>> context = getContext('DrawBot')
        >>> style = dict(font='PageBot-Regular', fontSize=pt(100), leading=em(1))
        >>> bs = context.newString('ABCD', style, h=500)
        >>> bs.w, bs.tw, bs.h, bs.th
        (500pt, 250.9pt, 100pt, 100pt)
        """
        if self.context is None: # Required context to be defined.
            return None
        if self._twh is None:
            self._twh = self.context.textSize(self.cs, w=self._w, h=self._h)
        return self._twh[0]
    tw = property(_get_tw)

    def _get_th(self):
        """Answer the cached calculated context height.

        >>> from pagebot.toolbox.units import em
        >>> from pagebot.contexts import getContext
        >>> bs = BabelString('ABCD') # No context, cannot render.
        >>> bs.th is None
        True
        >>> context = getContext('DrawBot')
        >>> style = dict(font='PageBot-Regular', fontSize=pt(100), leading=em(1))
        >>> bs = context.newString('ABCD', style, h=500)
        >>> bs.w, bs.tw, bs.h, bs.th # Not width defined, comes from bs.tw
        (250.9pt, 250.9pt, 500pt, 100pt)
        >>> from pagebot.toolbox.loremipsum import loremipsum
        >>> style = dict(font='PageBot-Regular', fontSize=pt(10), leading=em(1))
        >>> bs = context.newString(loremipsum(), style, w=500)
        >>> bs.w, bs.tw, bs.h, bs.th
        (500pt, 250.9pt, 100pt, 100pt)
        """
        if self.context is None: # Required context to be defined
            return None
        if self._twh is None:
            self._twh = self.context.textSize(self.cs, w=self._w, h=self._h)
        return self._twh[1]
    th = property(_get_th)

    def _get_cs(self):
        """Answer the native formatted string of the context. If it does
        not exist, then ask the context to render it before answering.
        Cache the result in self._cs.

        >>> from pagebot.contexts import getContext
        >>> context = getContext('DrawBot')
        >>> bs = BabelString('ABCD', dict(fontSize=24), context=context)
        >>> bs.cs, bs.cs.__class__.__name__ # Answer cached rendered FormattedString.
        (ABCD, 'FormattedString')
        """
        if self._cs is None:
            self._cs = self.context.fromBabelString(self)
        return self._cs
    cs = property(_get_cs)

    def _get_lines(self):
        """Answer the list of BabelLine instances, with meta information about
        the line wrapping done by the context. If it does not exist, then ask
        the context to render it before answersing.
        Cache the result in self._lines.

        >>> from pagebot.toolbox.loremipsum import loremipsum
        >>> from pagebot.toolbox.units import pt
        >>> from pagebot.contexts import getContext
        >>> context = getContext('DrawBot')
        >>> style = dict(font='PageBot-Regular', fontSize=pt(24))
        >>> bs = BabelString(loremipsum(), style, w=pt(500), context=context)
        >>> lines = bs.lines
        >>> len(lines)
        113
        """
        if self._lines is None:
            self._lines = self.context.textLines(self.cs, w=self.w, h=self.h)
        return self._lines
    lines = property(_get_lines)

    def _get_topLineAscender(self):
        """Answer the largest ascender height in the first line.

        >>> from pagebot.toolbox.units import em
        >>> from pagebot.contexts import getContext
        >>> context = getContext('DrawBot')
        >>> style = dict(font='PageBot-Regular', fontSize=pt(100), leading=em(1))
        >>> bs = BabelString('ABCD', style, context=context)
        >>> bs.topLineAscender
        74.8pt
        >>> bs.add('EFGH\\n', dict(font='PageBot-Regular', fontSize=200))
        >>> bs.runs
        [<BabelRun "ABCD">, <BabelRun "EFGH ">]
        >>> bs.lines[0].runs
        [<BabelRunInfo "ABCD">, <BabelRunInfo "EFGH">]
        >>> bs.topLineAscender # First line ascender height increased
        149.6pt
        >>> bs.add('IJKL', dict(fontSize=300)) # Second line does not change
        >>> bs.topLineAscender # First line ascender height increased
        149.6pt
        """
        topLineAscender = 0
        if self.lines:
            for run in self.lines[0].runs:
                font = findFont(run.style.get('font', DEFAULT_FONT))
                fontSize = units(run.style.get('fontSize', DEFAULT_FONT_SIZE))
                topLineAscender = max(topLineAscender, fontSize * font.info.typoAscender / font.info.unitsPerEm)
        return topLineAscender
    topLineAscender = property(_get_topLineAscender)

    def _get_topLineAscender_h(self):
        """Answer the largest ascender height for /h in the first line.

        >>> from pagebot.toolbox.units import em
        >>> from pagebot.contexts import getContext
        >>> context = getContext('DrawBot')
        >>> style = dict(font='PageBot-Regular', fontSize=pt(100), leading=em(1))
        >>> bs = BabelString('ABCD', style, context=context)
        >>> bs.topLineAscender_h
        72pt
        >>> bs.add('EFGH\\n', dict(font='PageBot-Regular', fontSize=200))
        >>> bs.runs
        [<BabelRun "ABCD">, <BabelRun "EFGH ">]
        >>> bs.lines[0].runs
        [<BabelRunInfo "ABCD">, <BabelRunInfo "EFGH">]
        >>> bs.topLineAscender_h # First line ascender height increased
        144pt
        >>> bs.add('IJKL', dict(fontSize=300)) # Second line does not change
        >>> bs.topLineAscender_h # First line ascender height increased
        144pt
        """
        topLineAscender_h = 0
        if self.lines:
            for run in self.lines[0].runs:
                font = findFont(run.style.get('font', DEFAULT_FONT))
                ascender_h = font['h'].maxY
                fontSize = units(run.style.get('fontSize', DEFAULT_FONT_SIZE))
                topLineAscender_h = max(topLineAscender_h, fontSize * ascender_h / font.info.unitsPerEm)
        return topLineAscender_h
    topLineAscender_h = property(_get_topLineAscender_h)

    def _get_topLineCapHeight(self):
        """Answer the largest capHeight in the first line. The height is
        derived from the fonts, independent if there are actually capitals
        in the first line.

        >>> from pagebot.contexts import getContext
        >>> context = getContext('DrawBot')
        >>> bs = BabelString('ABCD', dict(fontSize=100), context=context)
        >>> bs.topLineCapHeight
        65.8pt
        >>> bs.add('EFGH\\n', dict(fontSize=200))
        >>> bs.topLineCapHeight # First line capheight increased
        131.6pt
        >>> bs.add('IJKL', dict(fontSize=300)) # Second line does not change
        >>> bs.topLineCapHeight # First line capHeight increased
        131.6pt
        """
        topLineCapHeight = 0
        if self.lines:
            for run in self.lines[0].runs:
                font = findFont(run.style.get('font', DEFAULT_FONT))
                fontSize = units(run.style.get('fontSize', DEFAULT_FONT_SIZE))
                topLineCapHeight = max(topLineCapHeight, fontSize * font.info.capHeight / font.info.unitsPerEm)
        return topLineCapHeight
    topLineCapHeight = property(_get_topLineCapHeight)

    def _get_topLineXHeight(self):
        """Answer the largest xHeight in the first line. The height is
        derived from the fonts, independent if there are actually lower case
        in the first line.

        >>> from pagebot.contexts import getContext
        >>> context = getContext('DrawBot')
        >>> bs = BabelString('ABCD', dict(fontSize=100), context=context)
        >>> bs.topLineXHeight
        46.6pt
        >>> bs.add('EFGH\\n', dict(fontSize=200))
        >>> bs.topLineXHeight # First line xHeight increased
        93.2pt
        >>> bs.add('IJKL', dict(fontSize=300)) # Second line does not change
        >>> bs.topLineXHeight # First line xHeight increased
        93.2pt
        """
        topLineXHeight = 0
        if self.lines:
            for run in self.lines[0].runs:
                font = findFont(run.style.get('font', DEFAULT_FONT))
                fontSize = units(run.style.get('fontSize', DEFAULT_FONT_SIZE))
                topLineXHeight = max(topLineXHeight, fontSize * font.info.xHeight / font.info.unitsPerEm)
        return topLineXHeight
    topLineXHeight = property(_get_topLineXHeight)

    def _get_bottomLineDescender(self):
        """Answer the largest abs(descender) in the bottom line. The height is
        derived from the fonts, independent if there are actually lower case
        in the first line. The value answered is a position (negative number),
        not a distance, relative to the baseline of the last line.

        >>> from pagebot.contexts import getContext
        >>> context = getContext('DrawBot')
        >>> bs = BabelString('ABCD', dict(fontSize=100), context=context)
        >>> bs.bottomLineDescender
        -25.2pt
        >>> bs.add('EFGH', dict(fontSize=1000))
        >>> bs.bottomLineDescender # Last line descender increased
        -252pt
        >>> bs.add('IJ\\nKL', dict(fontSize=50)) # New last line with small descender
        >>> bs.bottomLineDescender # Last line descender increased
        -12.6pt
        >>> bs.lines[1]
        <BabelLineInfo x=0pt y=135pt runs=1>
        """
        bottomLineDescender = 0
        if self.lines:
            for run in self.lines[-1].runs:
                font = findFont(run.style.get('font', DEFAULT_FONT))
                fontSize = units(run.style.get('fontSize', DEFAULT_FONT_SIZE))
                bottomLineDescender = min(bottomLineDescender, fontSize * font.info.typoDescender / font.info.unitsPerEm)
        return bottomLineDescender
    bottomLineDescender = property(_get_bottomLineDescender)

    def _get_bottomLineDescender_p(self):
        """Answer the largest abs(descender) for /p in the bottom line. The height is
        derived from the fonts, independent if there are actually lower case
        in the first line. The value answered is a position (negative number),
        not a distance, relative to the baseline of the last line.

        >>> from pagebot.contexts import getContext
        >>> context = getContext('DrawBot')
        >>> bs = BabelString('ABCD', dict(fontSize=100), context=context)
        >>> bs.bottomLineDescender_p
        -21.2pt
        >>> bs.add('EFGH', dict(fontSize=1000))
        >>> bs.bottomLineDescender_p # Last line descender increased
        -212pt
        >>> bs.add('IJ\\nKL', dict(fontSize=50)) # New last line with small descender
        >>> bs.bottomLineDescender_p # Last line descender decreased
        -10.6pt
        """
        bottomLineDescender_p = 0
        if self.lines:
            for run in self.lines[-1].runs:
                font = findFont(run.style.get('font', DEFAULT_FONT))
                descender_p = font['p'].minY
                fontSize = units(run.style.get('fontSize', DEFAULT_FONT_SIZE))
                bottomLineDescender_p = min(bottomLineDescender_p, fontSize * descender_p / font.info.unitsPerEm)
        return bottomLineDescender_p
    bottomLineDescender_p = property(_get_bottomLineDescender_p)


    def addMarker(self, markerId, arg):
        """Add a marker as a new run. Code can run through the
        self.runs to mark a run with additional information.
        A marker is a tiny piece of string in transparant color,
        that can its positions traced back in a rendered BabelText
        instance.

        >>> from pagebot.contexts import getContext
        >>> context = getContext('DrawBot')
        >>> style = dict(font='PageBot-Regular', fontSize=20)
        >>> bs = context.newString('ABCD', style)
        >>> bs.addMarker('M1', 'abcd')
        >>> bs.getMarkerRuns('M1')
        [<BabelRun "[[M1::abcd...">]
        >>> bs.addMarker('M2', 'abcd')
        >>> bs.addMarker('M2', 'efgh')
        >>> bs.getMarkerRuns('M2')
        [<BabelRun "[[M2::abcd...">, <BabelRun "[[M2::efgh...">]
        >>> bs.getMarkerRuns('M1')
        [<BabelRun "[[M1::abcd...">]
        """
        # Transparant white extremely small string added in the output.
        style = dict(fontSize=pt(0.0000001), textFill=color(1, 1, 1, 0))
        self.runs.append(BabelRun('[[%s::%s]]' % (markerId, arg), style))

    def getMarkerRuns(self, markerId):
        """Answer the list of filtered runs that contain the marker.
        In general this query is applied on rendered BabelText instances.
        """
        marker = '[[%s::' % markerId
        runs = []
        for run in self.runs:
            if marker in run.s:
                runs.append(run)
        return runs


    def _get_textSize(self):
        """Answer the text size of self, rendered by the defined context.
        Raise an error if the context is not defined.

        >>> from pagebot.toolbox.units import pt, em
        >>> from pagebot.contexts import getContext
        >>> context = getContext('DrawBot')
        >>> style = dict(font='PageBot-Regular', fontSize=pt(100), leading=em(1))
        >>> bs = context.newString('ABCD', style)
        >>> bs.textSize
        (250.9pt, 100pt)
        """
        return self.tw, self.th
    textSize = property(_get_textSize)

    def __getitem__(self, given):
        """Answers a copy of self with a sliced string or with a single indexed
        character. We can't just slice the concatenated string, as there may be
        overlapping runs and styles.
        Note that the styles are copied within slice range. No cascading
        style values are taken from previous runs.

        >>> from pagebot.contexts import getContext
        >>> from pagebot.toolbox.units import pt
        >>> context = getContext('DrawBot')
        >>> style1 = dict(fontSize=pt(12))
        >>> style2 = dict(fontSize=pt(18))
        >>> style3 = dict(fontSize=pt(24))
        >>> bs = context.newString('ABCD', style1)
        >>> bs += context.newString('EFGH', style2) # Adding needs context
        >>> bs += context.newString('IJKL', style3)
        >>> bs # Show concatinated string, spanning the 2 styles
        $ABCDEFGHIJ...$
        >>> bs[3], bs[3].runs # Take indexed character from the first run
        ($D$, [<BabelRun "D">])
        >>> bs[7], bs[7].runs # Spanning into the second run
        ($H$, [<BabelRun "H">])
        >>> bs[2:], bs[2:].runs
        ($CDEFGHIJKL$, [<BabelRun "CD">, <BabelRun "EFGH">, <BabelRun "IJKL">])
        >>> bs[:5], bs[:5].runs
        ($ABCDE$, [<BabelRun "ABCD">, <BabelRun "E">])
        >>> bs[2:9], bs[2:9].runs
        ($CDEFGHI$, [<BabelRun "CD">, <BabelRun "EFGH">, <BabelRun "I">])
        >>> bs[2:-5], bs[2:-5].runs
        ($CDEFG$, [<BabelRun "CD">, <BabelRun "EFG">])
        >>> bs[-6:-2], bs[-6:-2].runs
        ($GHIJ$, [<BabelRun "GH">, <BabelRun "IJ">])
        """
        if isinstance(given, slice):
            start = given.start or 0
            if start < 0:
                start += len(self)
            stop = given.stop or len(self)+1
            if stop < 0:
                stop += len(self)
            slicedBs = self.__class__(context=self.context) # Context can be None
            i = 0
            for run in self.runs:
                style = copy(run.style)
                l = len(run)
                if i + l < start:
                    i += len(run)
                    continue # Not yet there
                if i < start:
                    if i+l < stop:
                        slicedBs.add(run.s[start-i:], style)
                        i += len(run)
                        continue
                    slicedBs.add(run.s[start-i:stop-i], style)
                    i += len(run)
                    continue
                if i+l <= stop:
                    slicedBs.add(run.s, style)
                    i += len(run)
                    continue
                if i < stop:
                    slicedBs.add(run.s[:stop-i], style)
                    i += len(run)

            return slicedBs

        # Untouched.
        if isinstance(given, (list, tuple)):
            return self

        # Single index.
        i = 0
        for run in self.runs:
            l = len(run)
            if i+l < given:
                i += l
                continue
            return BabelString(run.s[given-i], copy(run.style), context=self.context)
        return None

    def __repr__(self):
        """Answer the identifier string with format $ABCD$, to show the
        difference with the actual string. Abbreviate with ... if the
        concatenated string is longer than 10 characers.

        >>> BabelString('ABCD')
        $ABCD$
        >>> BabelString('ANCDEFGHIJKLM')
        $ANCDEFGHIJ...$
        """
        s = self.s[:10]
        if s != self.s:
            s += '...'
        return '$%s$' % s.replace('\n',' ')

    def add(self, s, style=None):
        """Create a new PabeBotRun instance and add it to self.runs.

        >>> from pagebot.toolbox.units import pt
        >>> style0 = dict(fontSize=pt(12))
        >>> style1 = dict(fontSize=pt(12))
        >>> style2 = dict(fontSize=pt(18))
        >>> bs = BabelString('AB', style0)
        >>> bs.style
        {'fontSize': 12pt}
        >>> bs.add('CD') # No style, adds to the last run
        >>> bs
        $ABCD$
        >>> bs.runs
        [<BabelRun "ABCD">]
        >>> bs.add('EF', style=style0) # Identical style, adds to the last run
        >>> bs.runs
        [<BabelRun "ABCDEF">]
        >>> bs.add('GH', style=style1) # Similar style, adds to the last run
        >>> bs.runs
        [<BabelRun "ABCDEFGH">]
        >>> bs.add('XYZ', style2) # Different style creates a new run
        >>> bs.runs
        [<BabelRun "ABCDEFGH">, <BabelRun "XYZ">]
        >>> len(bs), len(bs.runs) # Total number of characters and number of runs
        (11, 2)
        """
        if s:
            if self.runs and (style is None or self.style == style):
                # If styles are matching, then just add.
                self.runs[-1].s += str(s)
            else: # With incompatible styles, make a new run.
                self.runs.append(BabelRun(s, style))
            self.reset() # As we changed the content, cache needs to recalculate.

    def __len__(self):
        """Answer total string length.

        >>> from pagebot.toolbox.units import pt
        >>> bs = BabelString('ABCD')
        >>> len(bs), len(bs.runs)
        (4, 1)
        >>> bs.add('EFGH') # Without style, add to the last run
        >>> len(bs), len(bs.runs)
        (8, 1)
        >>> bs.add('XYZ', style=dict(fontSize=pt(12)))
        >>> len(bs), len(bs.runs) # Added to the total chars and new run
        (11, 2)
        """
        return len(self.s)

    def __add__(self, bs):
        """If pbs is a plain string, then just add it to the last run.
        Otherwise create a new BabelString and copy all runs there.

        >>> from pagebot.contexts import getContext
        >>> from pagebot.toolbox.units import pt
        >>> context = getContext('DrawBot')
        >>> bs1 = context.newString('ABCD', dict(fontSize=pt(18)))
        >>> bs2 = context.newString('EFGH', dict(fontSize=pt(24)))
        >>> bs3 = bs1 + bs2 # Create new instance, concatenated from both
        >>> bs1 is not bs2 and bs1 is not bs3 and bs2 is not bs3
        True
        >>> bs3.runs
        [<BabelRun "ABCD">, <BabelRun "EFGH">]
        """
        bsResult = BabelString(context=self.context) # Context can be None
        for run in self.runs:
            bsResult.runs.append(deepcopy(run))
        if isinstance(bs, str):
            bsResult.add(bs) # Add to last run or create new PageBotRun
        elif isinstance(bs, BabelString):
            for run in bs.runs:
                bsResult.runs.append(deepcopy(run))
            bsResult.w = bs.w
            bsResult.h = bs.h
        else:
            raise ValueError("@bs must be string or other %s" % self.__class__.__name__)
        bsResult.reset()
        return bsResult

    def __eq__(self, bs):
        """Compare @bs with self.

        >>> from pagebot.toolbox.units import pt
        >>> bs1 = BabelString('ABCD', style=dict(font='Verdana', fontSize=pt(18)))
        >>> bs2 = BabelString('ABCD', style=dict(font='Verdana', fontSize=pt(18)))
        >>> bs3 = BabelString('ABCD', style=dict(font='Verdana', fontSize=pt(20)))
        >>> bs1 == bs2 # Compares True, even for identical, but not the same styles.
        True
        >>> bs1 is bs2 # Although equal, they are not the same instance.
        False
        >>> bs2 == bs3 # Not equal, due to difference in style.
        False
        """
        if not isinstance(bs, self.__class__):
            return False
        if len(self.runs) != len(bs.runs):
            return False
        for rIndex, run in enumerate(self.runs):
            if run != bs.runs[rIndex]:
                return False
        return True

    def __ne__(self, bs):
        return not self == bs

    def _get_s(self):
        """Set/get the of the last run.

        >>> bs = BabelString('ABCD')
        >>> bs, bs.runs[0].s
        ($ABCD$, 'ABCD')
        >>> bs.s = 'XYZ'
        >>> bs, bs.runs[0].s
        ($XYZ$, 'XYZ')
        """
        s = []
        for run in self.runs:
            s.append(run.s)
        return ''.join(s)

    def _set_s(self, s):
        if self.runs:
            style = self.runs[-1].style # Keep last style if it exists
        else:
            style = None
        self.runs = [BabelRun(s, style)]

    s = property(_get_s, _set_s)

    #  Attributes, based on current style (not cascading)
    #  If the current style does not include the attributes,
    #  then answer the default for that value.

    def _get_style(self):
        if self.runs:
            return self.runs[-1].style
        return {}
    def _set_style(self, style):
        if self.runs:
            self.runs[-1].style = style
        else: # No runs, create a new one, with style and empty string.
            self.runs.append(BabelRun(style=style))
    style = property(_get_style, _set_style)

    def _get_language(self):
        """Answer the langauge value of the current style.

        >>> from pagebot.constants import LANGUAGE_NL
        >>> bs = BabelString('ABCD', dict(font='Roboto'))
        >>> bs.language == DEFAULT_LANGUAGE
        True
        >>> bs.language = LANGUAGE_NL
        >>> bs.language
        'nl'
        """
        return self.style.get('language', DEFAULT_LANGUAGE)

    def _set_language(self, language):
        self.style['language'] = language # Set in current style
    language = property(_get_language, _set_language)

    def _get_hyphenation(self):
        """Answer the hyphenation value of the current style.

        >>> bs = BabelString('ABCD', dict(font='Roboto'))
        >>> bs.hyphenation
        False
        >>> bs.hyphenation = DEFAULT_LANGUAGE
        >>> bs.hyphenation
        'en'
        """
        return (self.style or {}).get('hyphenation', False)

    def _set_hyphenation(self, hyphenation):
        (self.style or {})['hyphenation'] = hyphenation

    hyphenation = property(_get_hyphenation, _set_hyphenation)

    def _get_font(self):
        """Answer the font that is defined in the current style.
        If the font is just a string, then find the font and answer it.
        Answer the default font, if the font name cannot be found.

        >>> bs = BabelString('ABCD', dict(font='PageBot-Regular'))
        >>> bs.font
        <Font PageBot-Regular>
        >>> bs.font = 'Roboto-Regular'
        >>> bs.font # Answer the new defined Font instance
        <Font Roboto-Regular>
        >>> bs = BabelString('ABCD')
        >>> bs.font, isinstance(bs.font, Font) # Default font instance
        (<Font PageBot-Regular>, True)
        """
        return findFont(self.style.get('font', DEFAULT_FONT))
    def _set_font(self, font):
        assert isinstance(font, (str, Font))
        self.style['font'] = font # Set the font in the current style
        self.reset() # Make sure context cache recalculates.
    font = property(_get_font, _set_font)

    def _get_fontSize(self):
        """Answer the fontSize that is defined in the current style.

        >>> from pagebot.toolbox.units import mm
        >>> bs = BabelString('ABCD', dict(fontSize=12))
        >>> bs.fontSize # Converts to units
        12pt
        >>> bs.fontSize = mm(24)
        >>> bs.fontSize
        24mm
        >>> bs = BabelString()
        >>> bs.fontSize # Answer default font size
        12pt
        """
        return units(self.style.get('fontSize', DEFAULT_FONT_SIZE))
    def _set_fontSize(self, fontSize):
        # Set the fontSize in the current style
        self.style['fontSize'] = units(fontSize)
        self.reset() # Make sure context cache recalculates.
    fontSize = property(_get_fontSize, _set_fontSize)

    def _get_leading(self):
        """Answer the leading that is defined in the current style.
        Render relative leading units with self.fontSize as base.
        Note that this only refers to the leading of the last run.

        >>> from pagebot.toolbox.units import pt, em
        >>> bs = BabelString('ABCD', dict(leading=em(1), fontSize=pt(100)))
        >>> bs.leading, pt(bs.leading) # Render relative unit with fontSize as base.
        (1em, 100pt)
        >>> bs.leading = em(1.2)
        >>> bs.leading, pt(bs.leading)
        (1.2em, 120pt)
        >>> bs.leading = pt(30)
        >>> bs.leading
        30pt
        """
        return units(self.style.get('leading', DEFAULT_LEADING), base=self.fontSize)
    def _set_leading(self, leading):
        # Set the leading in the current style
        self.style['leading'] = units(leading, base=self.fontSize)
        self.reset() # Make sure context cache recalculates.
    leading = property(_get_leading, _set_leading)

    def _get_tracking(self):
        """Answer the tracking that is defined in the current style.
        Render relative tracking units with self.fontSize as base.
        Note that this only refers to the tracking of the last run.

        >>> from pagebot.toolbox.units import pt, em
        >>> bs = BabelString('ABCD', dict(tracking=em(0.1), fontSize=pt(100)))
        >>> bs.tracking, pt(bs.tracking) # Render relative unit with fontSize as base.
        (0.1em, 10pt)
        >>> bs.tracking = em(0.2)
        >>> bs.tracking, pt(bs.tracking)
        (0.2em, 20pt)
        >>> bs.tracking = pt(30)
        >>> bs.tracking
        30pt
        """
        return units(self.style.get('tracking', 0), base=self.fontSize)
    def _set_tracking(self, tracking):
        # Set the tracking in the current style
        self.style['tracking'] = units(tracking, base=self.fontSize)
        self.reset() # Make sure context cache recalculates.
    tracking = property(_get_tracking, _set_tracking)

    def _get_xTextAlign(self):
        """Answer the xTextAlign attribute, as defined in the current style.
        Note that this only refers to the alignments of the last run.

        >>> from pagebot.constants import CENTER, RIGHT
        >>> bs = BabelString('ABCD', dict(xTextAlign=CENTER))
        >>> bs.xTextAlign
        'center'
        >>> bs.xTextAlign = RIGHT
        >>> bs.xTextAlign
        'right'
        """
        return self.style.get('xTextAlign', LEFT)
    def _set_xTextAlign(self, xTextAlign):
        self.style['xTextAlign'] = xTextAlign
        self.reset() # Make sure context cache recalculates.
    xTextAlign = property(_get_xTextAlign, _set_xTextAlign)

    def _get_yTextAlign(self):
        """Answer the yTextAlign attribute, as defined in the current style.
        Note that this only refers to the alignments of the last run.

        >>> from pagebot.constants import CENTER, RIGHT
        >>> bs = BabelString('ABCD', dict(yTextAlign=CENTER))
        >>> bs.yTextAlign
        'center'
        >>> bs.yTextAlign = RIGHT
        >>> bs.yTextAlign
        'right'
        """
        return self.style.get('yTextAlign', TOP)
    def _set_yTextAlign(self, yTextAlign):
        self.style['yTextAlign'] = yTextAlign
        self.reset() # Make sure context cache recalculates.
    yTextAlign = property(_get_yTextAlign, _set_yTextAlign)

    def _get_baselineShift(self):
        """Answer the baselineShift attribute, as defined in the current style.
        Note that this only refers to the baselineShift of the last run.

        >>> from pagebot.toolbox.units import em, pt
        >>> bs = BabelString('ABCD', dict(baselineShift=em(0.2), fontSize=pt(100)))
        >>> bs.baselineShift, pt(bs.baselineShift)
        (0.2em, 20pt)
        >>> bs.baselineShift = em(0.3)
        >>> bs.baselineShift, pt(bs.baselineShift)
        (0.3em, 30pt)
        >>> bs.baselineShift == bs.runs[0].style['baselineShift']
        True
        """
        return units(self.style.get('baselineShift', 0), base=self.fontSize)
    def _set_baselineShift(self, baselineShift):
        self.style['baselineShift'] = units(baselineShift, base=self.fontSize)
        self.reset() # Make sure context cache recalculates.
    baselineShift = property(_get_baselineShift, _set_baselineShift)

    def _get_openTypeFeatures(self):
        """Answer the openTypeFeatures attribute, as defined in the current style.
        Note that this only refers to the openTypeFeatures of the last run.

        >>> bs = BabelString('ABCD', dict(openTypeFeatures=dict(smcp=True)))
        >>> bs.openTypeFeatures
        {'smcp': True}
        >>> bs.openTypeFeatures = dict(onum=True)
        >>> bs.openTypeFeatures
        {'onum': True}
        >>> bs.openTypeFeatures is bs.runs[0].style['openTypeFeatures']
        True
        """
        return self.style.get('openTypeFeatures', {})
    def _set_openTypeFeatures(self, openTypeFeatures):
        self.style['openTypeFeatures'] = openTypeFeatures
        self.reset() # Make sure context cache recalculates.
    openTypeFeatures = property(_get_openTypeFeatures, _set_openTypeFeatures)

    def _get_underline(self):
        """Answer the underline attribute, as defined in the current style.
        Note that this only refers to the underline of the last run.

        >>> bs = BabelString('ABCD', dict(underline=True))
        >>> bs.underline
        True
        >>> bs.underline = False
        >>> bs.underline
        False
        """
        return self.style.get('underline', False)
    def _set_underline(self, underline):
        self.style['underline'] = underline
        self.reset() # Make sure context cache recalculates.
    underline = property(_get_underline, _set_underline)

    def _get_indent(self):
        """Answer the indent attribute, as defined in the current style.
        Note that this only refers to the indent of the last run.

        >>> from pagebot.toolbox.units import em, pt
        >>> bs = BabelString('ABCD', dict(indent=em(0.2), fontSize=pt(100)))
        >>> bs.indent, pt(bs.indent)
        (0.2em, 20pt)
        >>> bs.indent = em(0.3)
        >>> bs.indent, pt(bs.indent)
        (0.3em, 30pt)
        >>> bs.indent == bs.runs[0].style['indent']
        True
        """
        return units(self.style.get('indent', 0), base=self.fontSize)
    def _set_indent(self, indent):
        self.style['indent'] = units(indent, base=self.fontSize)
        self.reset() # Make sure context cache recalculates.
    indent = property(_get_indent, _set_indent)

    def _get_tailIndent(self):
        """Answer the tailIndent attribute, as defined in the current style.
        Note that this only refers to the tailIndent of the last run.

        >>> from pagebot.toolbox.units import em, pt
        >>> bs = BabelString('ABCD', dict(tailIndent=em(0.2), fontSize=pt(100)))
        >>> bs.tailIndent, pt(bs.tailIndent)
        (0.2em, 20pt)
        >>> bs.tailIndent = em(0.3)
        >>> bs.tailIndent, pt(bs.tailIndent)
        (0.3em, 30pt)
        >>> bs.tailIndent == bs.runs[0].style['tailIndent']
        True
        """
        return units(self.style.get('tailIndent', 0), base=self.fontSize)
    def _set_tailIndent(self, tailIndent):
        self.style['tailIndent'] = units(tailIndent, base=self.fontSize)
        self.reset() # Make sure context cache recalculates.
    tailIndent = property(_get_tailIndent, _set_tailIndent)

    def _get_firstLineIndent(self):
        """Answer the tailIndent attribute, as defined in the current style.
        Note that this only refers to the tailIndent of the last run.

        >>> from pagebot.toolbox.units import em, pt
        >>> bs = BabelString('ABCD', dict(firstLineIndent=em(0.2), fontSize=pt(100)))
        >>> bs.firstLineIndent, pt(bs.firstLineIndent)
        (0.2em, 20pt)
        >>> bs.firstLineIndent = em(0.3)
        >>> bs.firstLineIndent, pt(bs.firstLineIndent)
        (0.3em, 30pt)
        >>> bs.firstLineIndent == bs.runs[0].style['firstLineIndent']
        True
        """
        return units(self.style.get('firstLineIndent', 0), base=self.fontSize)
    def _set_firstLineIndent(self, firstLineIndent):
        self.style['firstLineIndent'] = units(firstLineIndent, base=self.fontSize)
        self.reset() # Make sure context cache recalculates.
    firstLineIndent = property(_get_firstLineIndent, _set_firstLineIndent)

    def _get_textFill(self):
        """Answer the textFill as defined in the current style.

        >>> from pagebot.toolbox.units import mm
        >>> bs = BabelString('ABCD', dict(textFill=color(1, 0, 0)))
        >>> bs.textFill
        Color(r=1, g=0, b=0)
        >>> bs.textFill = color(0, 0.5, 0) # Set the current style color
        >>> bs.textFill
        Color(r=0, g=0.5, b=0)
        >>> bs.textFill = 0.25 # Converts from single value
        >>> bs.textFill
        Color(r=0.25, g=0.25, b=0.25)
        """
        return color(self.style.get('textFill', 0))
    def _set_textFill(self, textFill):
        self.style['textFill'] = color(textFill)
    textFill = property(_get_textFill, _set_textFill)

    def _get_textStroke(self):
        """Answer the textStroke as defined in the current style.

        >>> from pagebot.toolbox.units import mm
        >>> bs = BabelString('ABCD', dict(textStroke=color(1, 0, 0)))
        >>> bs.textStroke
        Color(r=1, g=0, b=0)
        >>> bs.textStroke = color(0, 0.5, 0) # Set the current style color
        >>> bs.textStroke
        Color(r=0, g=0.5, b=0)
        >>> bs.textStroke = 0.25 # Converts from single value
        >>> bs.textStroke
        Color(r=0.25, g=0.25, b=0.25)
        """
        return color(self.style.get('textStroke', 0))
    def _set_textStroke(self, textStroke):
        self.style['textStroke'] = color(textStroke)
    textStroke = property(_get_textStroke, _set_textStroke)

    def _get_textStrokeWidth(self):
        """Answer the textStrokeWidth as defined in the current style.

        >>> from pagebot.toolbox.units import mm
        >>> bs = BabelString('ABCD', dict(textStrokeWidth=2))
        >>> bs.runs[0].style
        {'textStrokeWidth': 2}
        >>> bs.textStrokeWidth
        2pt
        >>> bs.textStrokeWidth = 0.5
        >>> bs.textStrokeWidth
        0.5pt
        """
        return units(self.style.get('textStrokeWidth', 0))
    def _set_textStrokeWidth(self, textStrokeWidth):
        self.style['textStrokeWidth'] = units(textStrokeWidth)
    textStrokeWidth = property(_get_textStrokeWidth, _set_textStrokeWidth)

    def _get_capHeight(self):
        """Answer the font capHeight as defined in the current style,
        in absolute measures, by calculating self.font.info.unisPerEm
        and self.fontSize ratio.

        >>> from pagebot.toolbox.units import mm
        >>> style = dict(font='PageBot-Regular', fontSize=12)
        >>> bs = BabelString('ABCD', style=style)
        >>> bs.capHeight # Converts to absolute units
        7.9pt
        >>> bs.fontSize = 100
        >>> bs.capHeight
        65.8pt
        >>> bs.fontSize = mm(50)
        >>> bs.capHeight # Capheight converts to absolute mm.
        32.9mm
        """
        font = self.font
        return self.fontSize * font.info.capHeight / font.info.unitsPerEm
    capHeight = property(_get_capHeight)

    def _get_xHeight(self):
        """Answer the font capHeight as defined in the current style,
        in absolute measures, by calculating self.font.info.unisPerEm
        and self.fontSize ratio.

        >>> from pagebot.toolbox.units import mm
        >>> style = dict(font='PageBot-Regular', fontSize=12)
        >>> bs = BabelString('ABCD', style=style)
        >>> bs.xHeight # Converts to absolute units
        5.59pt
        >>> bs.fontSize = 100
        >>> bs.xHeight
        46.6pt
        >>> bs.fontSize = mm(50)
        >>> bs.xHeight # xheight converts to absolute mm.
        23.3mm
        """
        font = self.font
        return self.fontSize * font.info.xHeight / font.info.unitsPerEm
    xHeight = property(_get_xHeight)

    def _get_ascender(self):
        """Answer the font ascender as defined in the current style,
        in absolute measures, by calculating self.font.info.unisPerEm
        and self.fontSize ratio.
        Use the self.info.typoAscender (from the [OS/2] table) instead of
        the self.info.ascender (which some from the [hhea] table.)

        >>> from pagebot.toolbox.units import mm
        >>> style = dict(font='PageBot-Regular', fontSize=1000)
        >>> bs = BabelString('ABCD', style=style)
        >>> bs.ascender # Converts to absolute units
        748pt
        >>> bs.fontSize = 100
        >>> bs.ascender
        74.8pt
        >>> bs.fontSize = mm(50)
        >>> bs.ascender # xheight converts to absolute mm.
        37.4mm
        """
        font = self.font
        return self.fontSize * font.info.typoAscender / font.info.unitsPerEm
    ascender = property(_get_ascender)

    def _get_descender(self):
        """Answer the font descender as defined in the current style,
        in absolute measures, by calculating self.font.info.unisPerEm
        and self.fontSize ratio.
        Use the self.info.typoDescender (from the [OS/2] table) instead of
        the self.info.ascender (which some from the [hhea] table.)
        Note that the descender is a position, not a distance, so it is
        a negative value.

        >>> from pagebot.toolbox.units import mm
        >>> style = dict(font='PageBot-Regular', fontSize=1000)
        >>> bs = BabelString('ABCD', style=style)
        >>> bs.descender # Converts to absolute units
        -252pt
        >>> bs.fontSize = 100
        >>> bs.descender
        -25.2pt
        >>> bs.fontSize = mm(50)
        >>> bs.descender # xheight converts to absolute mm.
        -12.6mm
        """
        font = self.font
        return self.fontSize * font.info.typoDescender / font.info.unitsPerEm
    descender = property(_get_descender)

    def getStyleAtIndex(self, index):
        """Answer the style at character index. If a run style is None,
        then answer the latest defined style.

        >>> from pagebot.toolbox.units import pt
        >>> style1 = dict(font='Verdana', fontSize=pt(12))
        >>> style2 = dict(font='Georgia', fontSize=pt(18))
        >>> style3 = dict(font='Verdana', fontSize=pt(10))
        >>> bs = BabelString('ABCD', style1)
        >>> bs.add('EFGH', style2)
        >>> bs.add('IJKL') # Will find style2
        >>> bs.add('XYZ', style3)
        >>> bs.getStyleAtIndex(2) == style1, bs.s[2]
        (True, 'C')
        >>> bs.getStyleAtIndex(6) == style2, bs.s[6]
        (True, 'G')
        >>> bs.getStyleAtIndex(9) == style2, bs.s[9] # Inheriting from previous run
        (True, 'J')
        >>> bs.getStyleAtIndex(-1) == style3, bs.s[-1] # Works as list index
        (True, 'Z')
        """
        cIndex = 0
        style = None
        for run in self.runs:
            l = len(run)
            if style is None or run.style is not None:
                style = run.style
            if cIndex < index < cIndex + l:
                return style
            cIndex += l
        return style

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
