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
#     BabelString is a generic string format that stores a string or text as a
#     list of BabelRun instances. runs can be manipulated independent of the
#     context as long as rendering of the rest flow isn't required.
#
#     A number of operations require a context to return a rendered native
#     format, such as size, line positions and overflow. For efficiency that
#     rendered string and meta information (such as position of lines) are
#     calculate upon request and stored in the BabelString for later use.
#     Changes to the runs will reset this cache.
#

from copy import copy, deepcopy
import weakref

from pagebot.constants import (DEFAULT_LANGUAGE, DEFAULT_FONT_SIZE, DEFAULT_FONT,
    DEFAULT_LEADING, LEFT, BASELINE) # , CENTER, RIGHT
from pagebot.contexts.basecontext.babelrun import *
from pagebot.fonttoolbox.objects.font import findFont, Font
from pagebot.toolbox.units import units, pt, em, upt
from pagebot.toolbox.color import color

class BabelString:
    """BabelString is a generic string format, that stores a string or text as
    a list of BabelRun instances. String behaviour can differ between various
    output contexts and platforms.

    A BabelString should not know anything about contexts, except that it can
    execute the text, textBox, textSize and textLines fuctions. Styles in runs
    are not cascading.

    ?? self.leading returns the value of the last run, because
    that is the attribute value if plain text gets appended.

    For platform-specific doctests, see
    doctests/strings-*.txt in the repository root.

    NOTE:
    - The styles values of sequential runs are *not* cascading. This is
      similar to the behavior of the DrawBot FormattedString attributes.
    - Plain numbers are by default converted to points.
    - Attribute properties refer to the style of the last run.

    >>> from pagebot.toolbox.units import pt, mm
    >>> from pagebot.contexts import getContext
    >>> context = getContext()
    >>> bs = BabelString('ABCD', style=dict(fontSize=12), context=context)
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
        """Constructor of BabelString. `s` is a plain string, style is a
        dictionary compatible with the document root style keys to add one
        PageBotRun as default. Otherwise self.runs is created as empty list.
        @s should be a plain string, but gets cast by `str(s)` otherwise.
        Optional `w` and `h` make the difference if this BabelString behaves as
        a plain string (answering it's own size) or a text (answering the
        defined size and overflow).

        Some methods only work if context is defined (e.g. self.textSize,
        self.lines and self.overflow)

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs = BabelString(context=context)
        >>> len(bs.runs)
        0
        >>> bs.add('ABCD')
        >>> len(bs), len(bs.runs)
        (4, 1)
        >>> bs.add('EFGH') # Without style, adding to the last run
        >>> len(bs), len(bs.runs)
        (8, 1)
        >>> bs = context.newString('ABCD')
        >>> bs
        $ABCD$
        """
        # Context instance @context is used for text size rendering methods.
        self.runs = [] # List of BabelRun instances.
        if s is not None or style is not None:
            self.runs.append(BabelRun(s, style))
        self.context = context # Store optional as weakref property. Clears cache.
        assert self.context
        self._w = units(w) # Set source value of the properties, not need clear cache again.
        self._h = units(h) # Set to points, if not already a Unit instance.

        # Cache is initialize by the self.context-->self.reset() property call.
        # In case of overflow for a given width and height, the overflow indices
        # store the slice in self.lines for the current overflow render by the context.
        # _overflowStart Line index where overflow starts.
        # _overflowEnd Line (non-inclusive)
        # _cs Cache of native context string (e.g. DrawBot.FormattedString or FlatStringData)
        # _lines Cache of calculated meta info after line wrapping BabelLine
        # _twh Cached tuple of calculated text width (self.tw, self.th)
        # _pwh Cached tuple of calculated pixel width (self.pw, self.ph)
        #self.reset() # Clear cache of previous context

    def _get_context(self):
        """Answers the weakref context if it is defined.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs = BabelString('ABCD', context=context)
        >>> bs.cs # Context put FormattedString cache data there
        ABCD
        """
        context = None
        if self._context is not None:
            context = self._context()
        return context

    def _set_context(self, context):
        if context is not None:
            context = weakref.ref(context)
        self._context = context
        self.reset() # Clear cache of previous context
        for run in self.runs: # Reset the run context too.
            run.context = context

    context = property(_get_context, _set_context)

    def reset(self):
        """Clears the context cache, in case the string source changed, to
        force new calculation of context dependent wrapping.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs = BabelString('ABCD', dict(fontSize=24), context=context)
        >>> # Triggers rendering of the FormattedString.
        >>> bs.cs is not None
        True
        >>> bs.reset() # Reset the caching.
        >>> bs._cs is None
        True
        """
        # Storage of native context string (e.g. Drawbot.FormattedString or
        # FlatStringData, containing Strike/Paragraph/Text instances).
        self._cs = None
        self._lines = None # Cache of calculated meta info after line wrapping.
        self._twh = None # Cache of calculated text width (self.tw, self.th)
        self._pwh = None # Cache of calculated pixel width (self.pw, self.ph)
        self._overflowStart = None # Line index where overflow starts.
        self._overflowEnd = None # Line (non-inclusive)

    def _get_w(self):
        """Answers the request width of this string. If None, no width is
        defined, therefore no wrapping is done and `self.tw` will just answer
        the original width of the string.

        >>> from pagebot.toolbox.units import pt
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs = BabelString('ABCD', dict(fontSize=pt(100)), w=pt(1000), context=context)
        >>> bs.w
        1000pt
        >>> bs.tw
        250.9pt
        >>> bs.context = getContext() # Will reset the cache
        >>> bs.w
        1000pt
        >>> bs.tw
        250.9pt
        """
        return self._w # Can be None

    def _set_w(self, w):
        """Answers the requested width of this string. If None, no width is
        defined, therefore no wrapping is done and `self.tw` will just answer
        the original width of the string."""
        self._w = units(w)
        self.reset() # Force context wrapping for self.tw to be recalculated.

    w = property(_get_w, _set_w)

    def _get_h(self):
        """Answers the requested height of this string. If None, no height is
        defined, so not overlap checking is done and `self.th` will just answer
        the original height of the string."""
        return self._h

    def _set_h(self, h):
        self._h = units(h)
        self.reset() # Force context wrapping to be recalculated.

    h = property(_get_h, _set_h)

    def _get_hasWidth(self):
        """Answers if self has a defined width (True) or gets its width from the
        rendered self.tw text width.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs = BabelString('ABCD', context=context)
        >>> bs.hasWidth
        False
        >>> bs.w = pt(500)
        >>> bs.hasWidth
        True
        """
        return self.w is not None
    hasWidth = property(_get_hasWidth)

    def _get_hasHeight(self):
        """Answers if self has a defined height (True) or gets its height from
        the rendered self.th text height.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs = BabelString('ABCD', context=context)
        >>> bs.hasHeight
        False
        >>> bs.h = pt(500)
        >>> bs.hasHeight
        True
        """
        return self.h is not None
    hasHeight = property(_get_hasHeight)

    def _get_tw(self):
        """Answers the cached calculated width within a certain context.

        >>> from pagebot.toolbox.units import em
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> style = dict(font='PageBot-Regular', fontSize=pt(100), leading=em(1))
        >>> bs = context.newString('ABCD', style, h=500)
        >>> bs.w, bs.tw, bs.h, bs.th # Difference between given height and text height.
        (None, 250.9pt, 500pt, 100pt)
        >>> context = getContext()
        >>> style = dict(font='PageBot-Regular', fontSize=pt(100), leading=em(1))
        >>> bs = context.newString('ABCD', style, h=500)
        >>> bs.w, bs.tw, bs.h, bs.th # Difference between given height and text height.
        (None, 250.9pt, 500pt, 100pt)
        """
        if self._twh is None:
            self._twh = self.getTextSize() # Same as self.textSize

        if self._twh is not None:
            return self._twh[0]

        return None
    tw = property(_get_tw)

    def _get_th(self):
        """Answers the cached calculated string height within a certain
        context.

        >>> from pagebot.toolbox.units import em
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> style = dict(font='PageBot-Regular', fontSize=pt(100), leading=em(1))
        >>> bs = context.newString('ABCD', style, h=500)
        >>> bs.w, bs.tw, bs.h, bs.th # No width defined, comes from bs.tw
        (None, 250.9pt, 500pt, 100pt)
        >>> bs.w = 1000
        >>> bs.w, bs.tw, bs.h, bs.th # Width defined, real with by bs.tw
        (1000pt, 250.9pt, 500pt, 100pt)
        """
        if self._twh is None:
            self._twh = self.getTextSize() # Same as self.textSize

        if self._twh is not None:
            return self._twh[1]

        return None
    th = property(_get_th)

    def _get_xTextAlign(self):
        """Answer the horizontal alignment of the first run style in self.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> from pagebot.constants import CENTER
        >>> bs = context.newString('ABCD', dict(font='PageBot-Regular', fontSize=24, xTextAlign=CENTER))
        >>> bs.xTextAlign
        'center'
        """
        if self.runs:
            return self.runs[0].style.get('xTextAlign')
        return LEFT

    xTextAlign = property(_get_xTextAlign)

    def _get_yTextAlign(self):
        """Answer the vertical alignment of the first run style in self.

        >>> from pagebot.contexts import getContext
        >>> from pagebot.constants import CENTER
        >>> context = getContext()
        >>> bs = context.newString('ABCD', dict(font='PageBot-Regular', fontSize=24, yTextAlign=CENTER))
        >>> bs.yTextAlign
        'center'
        """
        if self.runs:
            return self.runs[0].style.get('yTextAlign')
        return BASELINE
    yTextAlign = property(_get_yTextAlign)

    #   C O N T E X T  C A C H I N G

    def _get_cs(self):
        """Answers the native formatted string of the context. If it does not
        exist, then ask the context to render it before answering. Caches the
        result in self._cs.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs = BabelString('ABCD', dict(fontSize=24), context=context)
        >>> bs.cs
        ABCD
        """
        # FIXME: caches FlatBabelData in DrawBotContext.
        if self._cs is None:
            if self.context is not None:
                self._cs = self.context.fromBabelString(self)
        return self._cs
    cs = property(_get_cs)

    def _get_lines(self):
        """Answers the list of BabelLineInfo instances, with meta information
        about the line wrapping done by the context. If it does not exist, then
        ask the context to render it before answering. Caches the result in
        self._lines.

        >>> from pagebot.toolbox.loremipsum import loremIpsum
        >>> from pagebot.toolbox.units import pt
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> style = dict(font='PageBot-Regular', fontSize=pt(24))
        >>> bs = BabelString(loremIpsum(), style, w=pt(500), context=context)
        >>> lines = bs.lines
        >>> len(lines)
        113
        >>> lines[0].__class__.__name__
        'BabelLineInfo'
        """
        return self.getTextLines(self.w, self.h)

    lines = property(_get_lines)

    def getTextLines(self, w=None, h=None):
        """
        Also see doctests/string-*.txt.
        """
        #if w == self.w and h == self.h:
        if self._lines is None:
            self._lines = self.context.getTextLines(self, w=w, h=h)
        return self._lines
        #return self.context.getTextLines(self, w=w, h=h)

    def _get_topLineAscender(self):
        """Answers the largest ascender height in the first line.

        >>> from pagebot.toolbox.units import em
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> style = dict(font='PageBot-Regular', fontSize=pt(100), leading=em(1))
        >>> bs = BabelString('ABCD', style, context=context)
        >>> bs.topLineAscender
        74.8pt
        >>> bs.add('EFGH\\n', dict(font='PageBot-Regular', fontSize=200))
        """
        """
        >>> bs.runs
        [<BabelRun "ABCD">, <BabelRun "EFGH ">] >>> bs.lines

        >>> bs.lines[0].runs
        [<BabelRunInfo "ABCD">, <BabelRunInfo "EFGH">]
        >>> bs.topLineAscender # First line ascender height increased.
        149.6pt
        >>> bs.add('IJKL', dict(fontSize=300)) # Second line does not change.
        >>> bs.topLineAscender # First line ascender height increased.
        149.6pt
        """
        topLineAscender = 0
        if self.lines:
            for run in self.lines[0].runs:
                font = self.getFont(run.style)
                fontSize = units(run.style.get('fontSize', DEFAULT_FONT_SIZE))
                topLineAscender = max(topLineAscender, fontSize * font.info.typoAscender / font.info.unitsPerEm)
        return topLineAscender
    topLineAscender = property(_get_topLineAscender)

    def _get_topLineAscender_h(self):
        """Answers the largest ascender height for /h in the first line.

        >>> from pagebot.toolbox.units import em
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> style = dict(font='PageBot-Regular', fontSize=pt(100), leading=em(1))
        >>> bs = BabelString('ABCD', style, context=context)
        >>> bs.topLineAscender_h
        72pt
        >>> bs.add('EFGH\\n', dict(font='PageBot-Regular', fontSize=200))
        """
        """
        >>> bs.runs
        [<BabelRun "ABCD">, <BabelRun "EFGH ">]
        >>> bs.lines[0].runs
        [<BabelRunInfo "ABCD">, <BabelRunInfo "EFGH">]
        >>> bs.topLineAscender_h # First line ascender height increased
        144pt
        >>> bs.add('IJKL', dict(fontSize=300)) # Second line does not change
        """
        """
        >>> bs.topLineAscender_h # First line ascender height increased
        144pt
        """
        topLineAscender_h = 0
        if self.lines:
            for run in self.lines[0].runs:
                font = self.getFont(run.style)
                ascender_h = font['h'].maxY
                fontSize = units(run.style.get('fontSize', DEFAULT_FONT_SIZE))
                topLineAscender_h = max(topLineAscender_h, fontSize * ascender_h / font.info.unitsPerEm)
        return topLineAscender_h
    topLineAscender_h = property(_get_topLineAscender_h)

    def _get_topLineDescender(self):
        """Answers the largest descender height in the first line.

        >>> from pagebot.toolbox.units import em
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> style = dict(font='PageBot-Regular', fontSize=pt(100), leading=em(1))
        >>> bs = BabelString('ABCD', style, context=context)
        >>> bs.topLineDescender
        -25.2pt
        >>> bs.add('EFGH\\n', dict(font='PageBot-Regular', fontSize=200))
        >>> bs.runs
        [<BabelRun "ABCD">, <BabelRun "EFGH ">]
        """
        """
        >>> bs.lines[0].runs
        [<BabelRunInfo "ABCD">, <BabelRunInfo "EFGH">]
        >>> bs.topLineDescender # First line descender height increased
        -50.4pt
        >>> bs.add('IJKL', dict(fontSize=300)) # Second line does not change
        >>> bs.topLineDescender # First line descender height increased
        -75.6pt
        """
        topLineDescender = 0
        if self.lines:
            for run in self.lines[0].runs:
                font = self.getFont(run.style)
                fontSize = units(run.style.get('fontSize', DEFAULT_FONT_SIZE))
                topLineDescender = min(topLineDescender, fontSize * font.info.typoDescender / font.info.unitsPerEm)
        return topLineDescender
    topLineDescender = property(_get_topLineDescender)


    def _get_topLineCapHeight(self):
        """Answers the largest capHeight in the first line. The height is
        derived from the fonts, independent of if there are actually capitals
        in the first line."""
        topLineCapHeight = 0

        if self.lines:
            for run in self.lines[0].runs:
                font = self.getFont(run.style)
                fontSize = units(run.style.get('fontSize', DEFAULT_FONT_SIZE))
                topLineCapHeight = max(topLineCapHeight, fontSize * font.info.capHeight / font.info.unitsPerEm)
        return topLineCapHeight
    topLineCapHeight = property(_get_topLineCapHeight)

    def _get_topLineXHeight(self):
        """Answers the largest xHeight in the first line. The height is derived
        from the fonts, independent of if there are actually lower case in the
        first line."""
        topLineXHeight = 0
        if self.lines:
            for run in self.lines[0].runs:
                font = self.getFont(run.style)
                fontSize = units(run.style.get('fontSize', DEFAULT_FONT_SIZE))
                topLineXHeight = max(topLineXHeight, fontSize * font.info.xHeight / font.info.unitsPerEm)
        return topLineXHeight
    topLineXHeight = property(_get_topLineXHeight)

    def _get_bottomLineDescender(self):
        """Answers the largest abs(descender) in the bottom line. The height is
        derived from the fonts, independent of if there are actually lower case
        in the first line. The value answered is a position (negative number),
        not a distance, relative to the baseline of the last line."""
        bottomLineDescender = 0
        if self.lines:
            for run in self.lines[-1].runs:
                font = self.getFont(run.style)
                fontSize = units(run.style.get('fontSize', DEFAULT_FONT_SIZE))
                bottomLineDescender = min(bottomLineDescender, fontSize * font.info.typoDescender / font.info.unitsPerEm)
        return bottomLineDescender
    bottomLineDescender = property(_get_bottomLineDescender)

    def _get_bottomLineDescender_p(self):
        """Answers the largest abs(descender) for /p in the bottom line. The
        height is derived from the fonts, independent of if there are actually
        lower case in the first line. The value answered is a position
        (negative number), not a distance, relative to the baseline of the last
        line."""
        bottomLineDescender_p = 0
        if self.lines:
            for run in self.lines[-1].runs:
                font = self.getFont(run.style)
                descender_p = font['p'].minY
                fontSize = units(run.style.get('fontSize', DEFAULT_FONT_SIZE))
                bottomLineDescender_p = min(bottomLineDescender_p, fontSize * descender_p / font.info.unitsPerEm)
        return bottomLineDescender_p
    bottomLineDescender_p = property(_get_bottomLineDescender_p)


    def addMarker(self, markerId, arg):
        """Adds a marker as a new run. Code can run through the self.runs to
        mark a run with additional information. A marker is a tiny piece of
        string in transparent color, that can its positions traced back in a
        rendered BabelString instance.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
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
        """Answers the list of filtered runs that contain the marker. In
        general this query is applied on rendered BabelString instances."""
        marker = '[[%s::' % markerId
        runs = []
        for run in self.runs:
            if marker in run.s:
                runs.append(run)
        return runs

    def _getTextSizeFromLines(self, lines):
        tw = th = 0
        for lineInfo in lines:
            tw = max(tw, lineInfo.w)
            th += lineInfo.h
        return tw, th

    def getTextSize(self, w=None, h=None):
        """Answers the width and height of the formatted string with an
        optional given w or h.

        >>> from pagebot.document import Document
        >>> from pagebot.toolbox.units import pt
        >>> from pagebot.contexts import getContext
        >>> from pagebot.elements import *
        >>> context = getContext()
        >>> # Make the string, we can adapt the document/page size to it.
        >>> style = dict(font='PageBot-Regular', leading=em(1), fontSize=pt(100))
        >>> bs = context.newString('Hkpx', style)
        >>> tw, th = context.textSize(bs) # Same as bs.textSize, Show size of the text box, with baseline.
        >>> (tw, th) == bs.textSize
        True
        >>> m = 50
        >>> doc = Document(w=tw+2*m, h=th+m, context=context)
        >>> page = doc[1]
        >>> tw, th, bs.fontSize, bs.ascender, bs.descender
        (209.7pt, 100pt, 100pt, 74.8pt, -25.2pt)
        >>> e = newText(bs, x=m, y=m, parent=page)
        >>> e = newRect(x=m, y=m+bs.descender, w=tw, h=th, fill=None, stroke=(0, 0, 1), strokeWidth=0.5, parent=page)
        >>> e = newLine(x=m, y=m, w=tw, h=0, fill=None, stroke=(0, 0, 1), strokeWidth=0.5, parent=page)
        >>> e = newLine(x=m, y=m+bs.xHeight, w=tw, h=0, fill=None, stroke=(0, 0, 1), strokeWidth=0.5, parent=page)
        >>> e = newLine(x=m, y=m+bs.capHeight, w=tw, h=0, fill=None, stroke=(0, 0, 1), strokeWidth=0.5, parent=page)
        >>> doc.export('_export/DrawBotContext-textSize.pdf')

        >>> bs = context.newString('Hkpx', style)
        >>> tw, th = bs.textSize # Answering point units. Same as context.textSize(bs)
        >>> tw.rounded, th.rounded
        (210pt, 100pt)
        >>> bs.fontSize *= 0.5 # Same as bs.runs[0].style['fontSize'] *= 0.5 to scale by 50%
        >>> tw, th = bs.textSize # Render to FormattedString for new size.
        >>> tw.rounded, th.rounded
        (105pt, 50pt)
        >>>
        """
        if w is not None or h is not None:
            # Want something different than defined requested bs.w or bs.h.
            if w != self.w or h != self.h:
                # Different indeed? Reflow in temporary lines.
                #return self.context.textSize(self, w=w, h=h, ascDesc=False) <-- Not here
                return self.context.textSize(self, w=w, h=h)

        # FIXME: probably needs a w, h.
        #self._twh = twh = self.context.textSize(self, ascDesc=False)
        self._twh = twh = self.context.textSize(self)
        return twh

    def _get_textSize(self):
        """Answers the text size of self, rendered by the defined context.
        Raise an error if the context is not defined.
        >>> from pagebot.toolbox.units import pt, em
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> style = dict(font='PageBot-Regular', fontSize=pt(100), leading=em(1))
        >>> bs = context.newString('ABCD', style)
        >>> bs.textSize
        (250.9pt, 100pt)
        >>> bs.context = getContext() # Reset to new context
        >>> bs.textSize
        (250.9pt, 100pt)
        """
        return self.getTextSize() # Use default (self.w, self.h) parameters
    textSize = property(_get_textSize)

    def __getitem__(self, given):
        """Answers a copy of self with a sliced string or with a single indexed
        character. We can't just slice the concatenated string, as there may be
        overlapping runs and styles.
        Note that the styles are copied within slice range. No cascading
        style values are taken from previous runs.

        >>> from pagebot.contexts import getContext
        >>> from pagebot.toolbox.units import pt
        >>> context = getContext()
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
        >>> bs.context = getContext() # Reset to other context
        >>> bs[3], bs[3].runs
        ($D$, [<BabelRun "D">])
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
        """Answers the identifier string with format $ABCD$, to show the
        difference with the actual string. Abbreviate with ... if the
        concatenated string is longer than 10 characers.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> BabelString('ABCD', context=context)
        $ABCD$
        >>> BabelString('ANCDEFGHIJKLM', context=context)
        $ANCDEFGHIJ...$
        """
        s = self.s[:10]
        if s != self.s:
            s += '...'
        return '$%s$' % s.replace('\n',' ')

    def add(self, s, style=None):
        """Creates a new PabeBotRun instance and add it to self.runs.

        >>> from pagebot.toolbox.units import pt
        >>> style0 = dict(fontSize=pt(12))
        >>> style1 = dict(fontSize=pt(12))
        >>> style2 = dict(fontSize=pt(18))
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs = BabelString('AB', style0, context=context)
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
        """Answers total string length.

        >>> from pagebot.toolbox.units import pt
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs = BabelString('ABCD', context=context)
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
        """If pbs is a plain string, just adds it to the last run. Otherwise
        creates a new BabelString and copy all runs there.

        >>> from pagebot.toolbox.units import pt
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
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
        """Compares @bs with self.

        >>> from pagebot.toolbox.units import pt
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs1 = BabelString('ABCD', style=dict(font='Verdana', fontSize=pt(18)), context=context)
        >>> bs2 = BabelString('ABCD', style=dict(font='Verdana', fontSize=pt(18)), context=context)
        >>> bs3 = BabelString('ABCD', style=dict(font='Verdana', fontSize=pt(20)), context=context)
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
        """Set / get the last run.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs = BabelString('ABCD', context=context)
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

    #  Attributes, based on current style (not cascading) If the current style
    #  does not include the attributes, then answer the default for that value.

    def _get_style(self):
        if self.runs:
            return self.runs[-1].style
        return {}

    def _set_style(self, style):
        if self.runs:
            self.runs[-1].style = style
        else:
            # No runs, create a new one, with style and empty string.
            self.runs.append(BabelRun(s='', style=style))

    style = property(_get_style, _set_style)

    def _get_language(self):
        """Answers the langauge value of the current style.

        >>> from pagebot.constants import LANGUAGE_NL
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs = BabelString('ABCD', dict(font='Roboto'), context=context)
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
        """Answers the hyphenation value of the current style.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs = BabelString('ABCD', dict(font='Roboto'), context=context)
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
        """Answers the font that is defined in the current style.  If the font
        is just a string, then find the font and answer it. Answers the default
        font, if the font name cannot be found.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs = BabelString('ABCD', dict(font='PageBot-Regular'), context=context)
        >>> bs.font
        <Font PageBot-Regular>
        >>> bs.font = 'Roboto-Regular'
        >>> bs.font # Answer the new defined Font instance
        <Font Roboto-Regular>
        >>> bs = BabelString('ABCD', context=context)
        >>> bs.font, isinstance(bs.font, Font) # Default font instance
        (<Font PageBot-Regular>, True)
        """
        return self.getFont()

    def _set_font(self, font):
        assert isinstance(font, (str, Font))
        self.style['font'] = font # Set the font in the current style
        self.reset() # Make sure context cache recalculates.
    font = property(_get_font, _set_font)

    def getFont(self, style=None):
        if not style:
            style = self.style
        fontName = style.get('font', DEFAULT_FONT)
        if fontName is None:
            fontName = DEFAULT_FONT
        return findFont(fontName)

    def _get_fontSize(self):
        """Answers the fontSize that is defined in the current style.

        >>> from pagebot.toolbox.units import mm
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs = BabelString('ABCD', dict(fontSize=12), context=context)
        >>> bs.fontSize # Converts to units
        12pt
        >>> bs.fontSize = mm(24)
        >>> bs.fontSize
        24mm
        >>> bs = BabelString(context=context)
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
        """Answers the leading that is defined in the current style.  Render
        relative leading units with self.fontSize as base. Note that this only
        refers to the leading of the last run.

        >>> from pagebot.toolbox.units import pt, em
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs = BabelString('ABCD', dict(leading=em(1), fontSize=pt(100)), context=context)
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
        """Answers the tracking that is defined in the current style.  Render
        relative tracking units with self.fontSize as base. Note that this
        only refers to the tracking of the last run.

        >>> from pagebot.toolbox.units import pt, em
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs = BabelString('ABCD', dict(tracking=em(0.1), fontSize=pt(100)), context=context)
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

    def _get_xAlign(self):
        """Answers the xAlign attribute, as defined in the current style. Note
        that this only refers to the alignments of the last run.

        >>> from pagebot.constants import CENTER, RIGHT, XHEIGHT
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs = BabelString('ABCD', dict(xTextAlign=CENTER), context=context)
        >>> bs.xAlign
        'center'
        >>> bs = BabelString('ABCD', dict(xAlign=XHEIGHT), context=context)
        >>> bs.xAlign
        'xHeight'
        >>> bs.xAlign = RIGHT
        >>> bs.xAlign
        'right'
        """
        style = self.style # Style of current run
        return style.get('xTextAlign') or style.get('xAlign', LEFT)

    def _set_xAlign(self, xAlign):
        style = self.style
        style['xTextAlign'] = style['xAlign'] = xAlign
        self.reset() # Make sure context cache recalculates.

    xAlign = property(_get_xAlign, _set_xAlign)

    def _get_yAlign(self):
        """Answers the yAlign attribute, as defined in the current style. Note
        that this only refers to the alignments of the last run.

        >>> from pagebot.constants import CENTER, RIGHT
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs = BabelString('ABCD', context=context)
        >>> bs.yAlign
        'baseline'
        >>> bs = BabelString('ABCD', dict(yAlign=CENTER), context=context)
        >>> bs.yAlign
        'center'
        >>> bs.yAlign = RIGHT
        >>> bs.yAlign
        'right'
        """
        return self.style.get('yAlign', BASELINE)
    def _set_yAlign(self, yAlign):
        self.style['yAlign'] = yAlign
        self.reset() # Make sure context cache recalculates.
    yAlign = property(_get_yAlign, _set_yAlign)

    def _get_baselineShift(self):
        """Answers the baselineShift attribute, as defined in the current
        style. Note that this only refers to the baselineShift of the last
        run.

        >>> from pagebot.toolbox.units import em, pt
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs = BabelString('ABCD', dict(baselineShift=em(0.2), fontSize=pt(100)), context=context)
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
        """Answers the openTypeFeatures attribute, as defined in the current
        style. Note that this only refers to the openTypeFeatures of the last
        run.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs = BabelString('ABCD', dict(openTypeFeatures=dict(smcp=True)), context=context)
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
        """Answers the underline attribute, as defined in the current style.
        Note that this only refers to the underline of the last run.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs = BabelString('ABCD', dict(underline=True), context=context)
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
        """Answers the indent attribute, as defined in the current style. Note
        that this only refers to the indent of the last run.

        >>> from pagebot.toolbox.units import em, pt
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs = BabelString('ABCD', dict(indent=em(0.2), fontSize=pt(100)), context=context)
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
        """Answers the tailIndent attribute, as defined in the current style.
        Note that this only refers to the tailIndent of the last run.

        >>> from pagebot.toolbox.units import em, pt
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs = BabelString('ABCD', dict(tailIndent=em(0.2), fontSize=pt(100)), context=context)
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
        """Answers the tailIndent attribute, as defined in the current style.
        Note that this only refers to the tailIndent of the last run.

        >>> from pagebot.toolbox.units import em, pt
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs = BabelString('ABCD', dict(firstLineIndent=em(0.2), fontSize=pt(100)), context=context)
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
        """Answers the textFill as defined in the current style.

        >>> from pagebot.toolbox.units import mm
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs = BabelString('ABCD', dict(textFill=color(1, 0, 0)), context=context)
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
        """Answers the textStroke as defined in the current style.

        >>> from pagebot.toolbox.units import mm
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs = BabelString('ABCD', dict(textStroke=color(1, 0, 0)), context=context)
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
        """Answers the textStrokeWidth as defined in the current style.

        >>> from pagebot.toolbox.units import mm
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs = BabelString('ABCD', dict(textStrokeWidth=2), context=context)
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
        """Answers the font capHeight as defined in the current style,
        in absolute measures, by calculating self.font.info.unisPerEm
        and self.fontSize ratio.

        >>> from pagebot.toolbox.units import mm
        >>> style = dict(font='PageBot-Regular', fontSize=12)
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs = BabelString('ABCD', style=style, context=context)
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
        """Answers the font capHeight as defined in the current style,
        in absolute measures, by calculating self.font.info.unisPerEm
        and self.fontSize ratio.

        >>> from pagebot.toolbox.units import mm
        >>> style = dict(font='PageBot-Regular', fontSize=12)
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs = BabelString('ABCD', style=style, context=context)
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
        """Answers the font ascender as defined in the current style,
        in absolute measures, by calculating self.font.info.unisPerEm
        and self.fontSize ratio.
        Use the self.info.typoAscender (from the [OS/2] table) instead of
        the self.info.ascender (which some from the [hhea] table.)

        >>> from pagebot.toolbox.units import mm
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> style = dict(font='PageBot-Regular', fontSize=1000)
        >>> bs = BabelString('ABCD', style=style, context=context)
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
        """Answers the font descender as defined in the current style,
        in absolute measures, by calculating self.font.info.unisPerEm
        and self.fontSize ratio.
        Use the self.info.typoDescender (from the [OS/2] table) instead of
        the self.info.ascender (which some from the [hhea] table.)
        Note that the descender is a position, not a distance, so it is
        a negative value.

        >>> from pagebot.toolbox.units import mm
        >>> style = dict(font='PageBot-Regular', fontSize=1000)
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs = BabelString('ABCD', style=style, context=context)
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
        """Answers the style at character index. If a run style is None,
        then answer the latest defined style.

        >>> from pagebot.toolbox.units import pt
        >>> style1 = dict(font='Verdana', fontSize=pt(12))
        >>> style2 = dict(font='Georgia', fontSize=pt(18))
        >>> style3 = dict(font='Verdana', fontSize=pt(10))
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs = BabelString('ABCD', style1, context=context)
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
