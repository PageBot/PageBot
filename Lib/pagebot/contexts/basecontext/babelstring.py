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
#     BabelString is an intermediate conversion string format that the
#     various contexts should be able to convert from and to, by
#     implementing context.fromBabelString and context.asBabelString.
#
from copy import copy, deepcopy
import weakref

from pagebot.constants import DEFAULT_LANGUAGE, DEFAULT_FONT_SIZE, DEFAULT_FONT, LEFT
from pagebot.fonttoolbox.objects.font import findFont, Font
from pagebot.toolbox.units import units
from pagebot.toolbox.color import color

class BabelRun:
    def __init__(self, s=None, style=None):
        """Answer the storage for string + style in BabelString.
        Note that the styles values of sequential runs are *not* cascading.
        This is similar to the behavior of the DrawBot FormattedString attributes.

        >>> from pagebot.elements import *
        >>> BabelRun('ABCD', dict(font='PageBot-Regular'))
        <BabelRun ABCD>
        >>> BabelRun() # String with empty runs is allowed.
        <BabelRun>
        >>> BabelRun('ABCD'*10) # Abbreviated for string > 10 characters.
        <BabelRun ABCDABCDAB...>
        >>> len(BabelRun('ABCD'*10))
        40
        """
        self.s = str(s or '')
        if style is None:
            style = {}
        self.style = style
        self.markers = {} # Place to store user defined info, such as a marker in the text.

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
        s = self.s[:10]
        if s:
            if s != self.s:
                s += '...'
            r += ' '+s
        r += '>'
        return r

class BabelLine:
    """BabelLine holds the BabelString with some additional information
    when generating a Text.textLines list.

    """
    def __init__(self, bs, x, y, index):
        self.bs = bs # Holding the BabelRuns of this text line.
        self.x = units(x) # Relative position inside a Text element.
        self.y = units(y) # Relative from top of text box
        self.index = index # Vertical line index in Text.textLines list.

    def __repr__(self):
        s = '<%s #%s' % (self.__class__.__name__, self.index)
        if self.x:
            s += ' x=%s' % self.x
        if self.y:
            s += ' y=%s' % self.y
        return s + '>'

    def __len__(self):
        return len(self.bs)

class BabelString:
    """BabelString is the generic intermediate string, that can be used
    for other context string classes to convert to and from.
    Note that the styles values of sequential runs are *not* cascading.
    This is similar to the behavior of the DrawBot FormattedString attributes.

    >>> bs1 = BabelString('ABCD', style=dict(fontSize=12))
    >>> bs1.runs
    [<BabelRun ABCD>]
    >>> bs2 = BabelString('ABCD', style=dict(fontSize=12))
    >>> bs2.runs
    [<BabelRun ABCD>]
    >>> bs1 == bs2, bs1 is bs2
    (True, False)
    >>> bs2 = BabelString('EFGH', style=dict(fontSize=16))
    >>> bs3 = bs1 + bs2
    >>> bs3
    $ABCDEFGH$
    >>> bs3.runs
    [<BabelRun ABCD>, <BabelRun EFGH>]
    """
    def __init__(self, s=None, style=None, e=None, context=None):
        """Constructor of BabelString. @s is a plain string, style is a
        dictionary compatible with the document root style keys to add one
        PageBotRun as default. Otherwise self.runs is created as empty list.
        @s should be a plain string, but gets cast by str(s) otherwise.
        @e is a optional reference for cascading style, proportion and context

        >>> bs = BabelString()
        >>> len(bs.runs)
        0
        >>> bs.add('ABCD')
        >>> len(bs), len(bs.runs)
        (4, 1)
        >>> bs.add('EFGH') # Without style, adding to the last run
        >>> len(bs), len(bs.runs)
        (8, 1)
        >>> bs = BabelString(style=dict(font='Roboto'))
        >>> bs.s
        ''
        >>> from pagebot.elements import Element
        >>> e = Element(name='Test')
        >>> bs = BabelString('ABCD', e=e)
        >>> bs.e.name
        'Test'
        >>> e = None # Delete original element
        >>> bs.e is None # Weakref property now answers None
        True
        """
        # Context instance @context and Element instance @e
        # are used for text size rendering methods.
        self.e = e # Store optional reference as weakref property.
        self.context = context # Store optional as weakref property.
        self.runs = [] # List of BabelRun instances.
        if s is not None or style is not None or e is not None:
            self.runs.append(BabelRun(s, style))

    def _get_e(self):
        """Answer the optional weakref element, for use of cascading style,
        proportions and context.

        >>> from pagebot.elements import Element
        >>> e = Element(name='Test')
        >>> bs = BabelString('ABCD', e=e)
        >>> bs.e.name
        'Test'
        >>> e = None # Delete element reference
        >>> bs.e is None
        True
        """
        if self._e is not None:
            return self._e()
        return None
    def _set_e(self, e):
        if e is not None:
            e = weakref.ref(e)
        self._e = e
    e = property(_get_e, _set_e)

    def appendMarker(self, markerId, arg):
        """Add a marker to the last run. Code can run through the
        self.runs to mark a run with additional information.
        """
        if self.runs:
            self.runs[-1].markers[markerId] = arg

    def getMarkerRuns(self, markerId):
        """Answer the list of filtered runs that contain the marker.
        """
        runs = []
        for run in self.runs:
            if markerId in run.markers:
                runs.append(run)
        return run

    def _get_context(self):
        """Answer the context if it is defined by self.e.context.

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
        if context is None:
            e = self.e
            if e:
                context = e.context
        return context
    def _set_context(self, context):
        if context is not None:
            context = weakref.ref(context)
        self._context = context
    context = property(_get_context, _set_context)

    def _get_textSize(self):
        """Answer the text size of self, rendered by the defined context.
        Raise an error if the context is not defined.

        >>> from pagebot.toolbox.units import pt
        >>> from pagebot.contexts import getContext
        >>> context = getContext('DrawBot')
        >>> style = dict(font='PageBot-Regular', fontSize=pt(100))
        >>> bs = context.newString('ABCD', style)
        >>> bs.textSize
        (250.9pt, 140pt)
        """
        context = self.context
        assert context is not None
        return context.textSize(self)
    textSize = property(_get_textSize)

    def textLines(self, w=None, h=None):
        """Answer the dictionary of Babelstring, as result of wrapping the self
        on colomn width @w. If the width is not defined, thatn take the with
        if self.e.

        >>> from pagebot.toolbox.units import pt
        >>> from pagebot.contexts import getContext
        >>> context = getContext('DrawBot')
        >>> style = dict(font='PageBot-Regular', fontSize=pt(12))
        >>> bs = context.newString('ABCD '*100, style)
        >>> bs.textLines(w=300)[0]
        <BabelLine #0 y=487.2pt>
        """
        context = self.context
        assert context is not None
        if w is None:
            if self.e is not None and self.e.w:
                w = self.e.w
        return context.textLines(self, w=w, h=h)

    def __getitem__(self, given):
        """Answers a copy of self with a sliced string or with a single indexed
        character. We can't just slice the concatenated string, as there may be
        overlapping runs and styles.
        Note that the styles are copied within slice range. No cascading
        style values are taken from previous runs.

        >>> from pagebot.toolbox.units import pt
        >>> style1 = dict(fontSize=pt(12))
        >>> style2 = dict(fontSize=pt(18))
        >>> style3 = dict(fontSize=pt(24))
        >>> bs = BabelString('ABCD', style1)
        >>> bs += BabelString('EFGH', style2)
        >>> bs += BabelString('IJKL', style3)
        >>> bs # Show concatinated string, spanning the 2 styles
        $ABCDEFGHIJ...$
        >>> bs[3], bs[3].runs # Take indexed character from the first run
        ($D$, [<BabelRun D>])
        >>> bs[7], bs[7].runs # Spanning into the second run
        ($H$, [<BabelRun H>])
        >>> bs[2:], bs[2:].runs
        ($CDEFGHIJKL$, [<BabelRun CD>, <BabelRun EFGH>, <BabelRun IJKL>])
        >>> bs[:5], bs[:5].runs
        ($ABCDE$, [<BabelRun ABCD>, <BabelRun E>])
        >>> bs[2:9], bs[2:9].runs
        ($CDEFGHI$, [<BabelRun CD>, <BabelRun EFGH>, <BabelRun I>])
        >>> bs[2:-5], bs[2:-5].runs
        ($CDEFG$, [<BabelRun CD>, <BabelRun EFG>])
        >>> bs[-6:-2], bs[-6:-2].runs
        ($GHIJ$, [<BabelRun GH>, <BabelRun IJ>])
        """
        if isinstance(given, slice):
            start = given.start or 0
            if start < 0:
                start += len(self)
            stop = given.stop or len(self)+1
            if stop < 0:
                stop += len(self)
            slicedBs = BabelString(e=self.e, context=self.context)
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
            return BabelString(run.s[given-i], copy(run.style))
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
        return '$%s$' % s

    def add(self, s, style=None):
        """Create a new PabeBotRun instance and add it to self.runs.

        >>> from pagebot.toolbox.units import pt
        >>> style1 = dict(fontSize=pt(12))
        >>> style2 = dict(fontSize=pt(18))
        >>> bs = BabelString('ABCD', style1)
        >>> bs.style
        {'fontSize': 12pt}
        >>> bs.add('EFGH') # No style, adds to the last run
        >>> bs.add('IJKL') # Same style, adds to the last run
        >>> bs.add('XYZ', style2) # Different style creates a new run
        >>> len(bs), len(bs.runs) # Total number of characters and number of runs
        (15, 2)
        """
        # If styles are matching, then just add.
        if self.runs and (style is None or self.style == style):
            self.runs[-1].s += str(s)
        else: # With incompatible styles, make a new run.
            self.runs.append(BabelRun(s, style))

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

        >>> from pagebot.toolbox.units import pt
        >>> bs1 = BabelString('ABCD', dict(fontSize=pt(18)))
        >>> bs2 = BabelString('EFGH', dict(fontSize=pt(18)))
        >>> bs3 = bs1 + bs2 # Create new instance, concatenated from both
        >>> bs1 is not bs2 and bs1 is not bs3 and bs2 is not bs3
        True
        """
        bsResult = BabelString()
        for run in self.runs:
            bsResult.runs.append(deepcopy(run))
        if isinstance(bs, str):
            bsResult.add(bs) # Add to last run or create new PageBotRun
        elif isinstance(bs, BabelString):
            for run in bs.runs:
                bsResult.runs.append(deepcopy(run))
        else:
            raise ValueError("@bs must be string or other %s" % self.__class__.__name__)
        return bsResult

    def __eq__(self, bs):
        """Compare @bs with self.

        >>> from pagebot.toolbox.units import pt
        >>> bs1 = BabelString('ABCD', style=dict(font='Verdana', fontSize=pt(18)))
        >>> bs2 = BabelString('ABCD', style=dict(font='Verdana', fontSize=pt(18)))
        >>> bs3 = BabelString('ABCD', style=dict(font='Verdana', fontSize=pt(20)))
        >>> bs1 == bs2, bs1 is bs2
        (True, False)
        >>> bs2 == bs3
        False
        >>> bs4 = bs1 + bs3

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
        return not (self == bs)

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
        return units(self.style.get('leading', 0), base=self.fontSize)

    def _set_leading(self, leading):
        # Set the leading in the current style
        self.style['leading'] = units(leading, base=self.fontSize)

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

    tracking = property(_get_tracking, _set_tracking)

    def _get_xAlign(self):
        """Answer the xAlign attribute, as defined in the current style.
        Note that this only refers to the alignments of the last run.

        >>> from pagebot.constants import CENTER, RIGHT
        >>> bs = BabelString('ABCD', dict(xAlign=CENTER))
        >>> bs.xAlign
        'center'
        >>> bs.xAlign = RIGHT
        >>> bs.xAlign
        'right'
        """
        return self.style.get('xAlign', LEFT)

    def _set_xAlign(self, xAlign):
        self.style['xAlign'] = xAlign

    xAlign = property(_get_xAlign, _set_xAlign)

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

        >>> from pagebot.toolbox.units import mm
        >>> style = dict(font='PageBot-Regular', fontSize=12)
        >>> bs = BabelString('ABCD', style=style)
        >>> bs.ascender # Converts to absolute units
        10.78pt
        >>> bs.fontSize = 100
        >>> bs.ascender
        89.8pt
        >>> bs.fontSize = mm(50)
        >>> bs.ascender # xheight converts to absolute mm.
        44.9mm
        """
        font = self.font
        return self.fontSize * font.info.ascender / font.info.unitsPerEm

    ascender = property(_get_ascender)

    def _get_descender(self):
        """Answer the font descender as defined in the current style,
        in absolute measures, by calculating self.font.info.unisPerEm
        and self.fontSize ratio.

        >>> from pagebot.toolbox.units import mm
        >>> style = dict(font='PageBot-Regular', fontSize=12)
        >>> bs = BabelString('ABCD', style=style)
        >>> bs.descender # Converts to absolute units
        -3.62pt
        >>> bs.fontSize = 100
        >>> bs.descender
        -30.2pt
        >>> bs.fontSize = mm(50)
        >>> bs.descender # xheight converts to absolute mm.
        -15.1mm
        """
        font = self.font
        return self.fontSize * font.info.descender / font.info.unitsPerEm

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
