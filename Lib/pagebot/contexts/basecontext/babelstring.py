#!/usr/bin/env python3 # -*- coding: UTF-8 -*-
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

import os
from copy import copy
from pagebot.constants import (LEFT, DEFAULT_LANGUAGE, DEFAULT_FONT_SIZE,
        DEFAULT_FALLBACK_FONT_PATH, DEFAULT_LEADING)
from pagebot.filepaths import DEFAULT_FONT_PATH
from pagebot.fonttoolbox.objects.font import Font
from pagebot.style import css
from pagebot.toolbox.color import (Color, blackColor, inheritColor, noColor,
        color)
from pagebot.toolbox.units import em, pt, RelativeUnit, Unit, upt, isUnit
from pagebot.fonttoolbox.objects.font import findFont

DEFAULT_COLOR = Color(0, 0, 0)

def getFontPath(style):
    font = style.get('font')

    if font is not None and not isinstance(font, str):
        fontPath = font.path
    else:
        fontPath = font

    if fontPath is None or not os.path.exists(fontPath):
        # TODO: get path from base context self._font.
        fontPath = DEFAULT_FONT_PATH

    return fontPath

def getLineHeight(leading, fontSize):
    """
    >>> getLineHeight(em(1.5), pt(12))
    18
    >>> getLineHeight(pt(15), pt(12))
    15
    >>> getLineHeight(pt(19), None)
    19
    >>> getLineHeight(15, pt(16))
    240
    """
    assert leading is not None

    if isinstance(leading, RelativeUnit):
        lineHeight = upt(leading.byBase(fontSize))
    elif isinstance(leading, Unit):
        lineHeight = upt(leading)
    elif isUnit(fontSize):
        # Leading is scalar?
        lineHeight = leading * fontSize.pt
    else:
        # Both scalar?
        lineHeight = leading * fontSize

    return lineHeight

class BabelString:
    """BabelString is the base class of all types of (formatted) string
    representations needed for the builder classes.

    TODO: add abstract functions for proper inheritance.

    >>> from pagebot import getContext
    >>> context = getContext('Flat')
    >>> bla = context.newString('bla')
    >>> from pagebot.contexts.flatcontext.flatstring import FlatString
    >>> isinstance(bla, FlatString)
    True
    >>> type(bla)
    <class 'pagebot.contexts.flatcontext.flatstring.FlatString'>
    >>> import inspect
    >>> inspect.getmro(FlatString)
    (<class 'pagebot.contexts.flatcontext.flatstring.FlatString'>, <class 'pagebot.contexts.basecontext.babelstring.BabelString'>, <class 'object'>)
    """

    def __init__(self, context):
        # Wraps the native string. Encloses the Flat, Drawbot or HTML string
        # in this wrapper.

        self.context = context
        self.language = DEFAULT_LANGUAGE
        self.hyphenation = False

        # In case we are sampling with a Variable Font. Filled in case w or h
        # are defined and depending on if the font is a variable font. Set to
        # fitting font size, in case the size iterates to find width.
        self.fittingFontSize = pt(0)
        self.fittingFont = None
        self.fittingLocation = None
        self.isFitting = False

    def __repr__(self):
        return '%s' % self.s

    def __add__(self, s):
        self.append(s)
        return self

    def __mul__(self, d):
        """
        >>> from pagebot import getContext
        >>> context = getContext('Flat')
        >>> fs = context.newString('ABC')
        >>> fs
        ABC
        >>> fs * 3
        ABCABCABC
        """
        s = self.s

        for n in range(d-1):
            s += self.s

        self.s = s
        # Something to do with the HTML?
        return self

    def __len__(self):
        return len(self.s)

    def __contains__(self, s):
        return s in self.s

    def __getitem__(self, given):
        """Answers a copy of self with a sliced string or with a single indexed
        character.

        >>> from pagebot import getContext
        >>> context = getContext('Flat')
        >>> fs = context.newString('blablabla')
        >>> fs
        blablabla
        >>> bs = fs[2:]
        >>> bs
        ablabla
        >>> fs
        blablabla
        >>> #fs[:5]
        #blabl
        >>> #fs[5]
        #a
        """
        if isinstance(given, slice):
            bs = copy(self)
            s = bs.s
            bs.s = s[given.start:given.stop]
            return bs

        # Untouched.
        if isinstance(given, (list, tuple)):
            return self

        # Single index.
        bs = copy(self)
        s = bs.s
        bs.s = s[given]
        return bs

    def append(self, s):
        """Appends string or BabelString to self.

        TODO: what about differently formatted strings?
        """

        if isinstance(s, str):
            self.s += s
        elif isinstance(s, BabelString):
            self.s += s.s

    def _get_type(self):
        """Answers the ID of the class, in case a caller wants to know what
        kind of BabelString this is.

        FIXME: doesn't this mess with object inheritance?"""
        return self.BABEL_STRING_TYPE

    type = property(_get_type)

    def _get_w(self):
        """Answers measure as point units."""
        return pt(self.size[0])
    w = property(_get_w)

    def _get_h(self):
        """Answers measure as point units."""
        return pt(self.size[1])

    h = property(_get_h)

    def _get_size(self):
        """Answers the size tuple (w, h) of the string."""
        if hasattr(self.context.b, 'textSize'):
            ts = self.context.b.textSize(self.s)
            return pt(ts)
        elif hasattr(self, 'textSize'):
            ts = self.textSize(self.s)
            return pt(ts)
        else:
            raise NotImplementedError

    size = property(_get_size)

    def columnStart(self, firstColumnIndent):
        """Allows the string to set itself to

            `firstLineIndex = firstColumnIndent`

        if that makes sense for inheriting BabelString classes. Default is just
        to answer `self`."""
        return self

    def getStyleAtIndex(self, index):
        """Answers the constructed style of the string as position index of
        chars."""
        raise NotImplementedError

    def _get_fontSize(self):
        """Answers the current state of the fontSize."""
        return self.style.get('fontSize', DEFAULT_FONT_SIZE)

    def _set_fontSize(self, fontSize):
        self.b.fontSize(fontSize)
        self.style['fontSize'] = fontSize

    fontSize = property(_get_fontSize, _set_fontSize)

    def getTextLines(self, w, h=None, align=LEFT):
        raise NotImplementedError

    def _get_lineHeight(self):
        """Get line height based on font size and leading."""
        return getLineHeight(self.leading, self.fontSize)

    # Compatibility with DrawBot API.
    fontLineHeight = lineHeight = property(_get_lineHeight)

    # To be implemented:
    #def textSize(self, w=None, h=None):
    #def asText(self):
    #def bounds(self, language=None, hyphenation=None):
    #def fill(self, r, g=None, b=None, a=None, alpha=None):
    #def cmykFill(self, c, m=None, y=None, k=None, a=None, alpha=None):
    #def stroke(self, r, g=None, b=None, a=None, alpha=None):
    #def setStrokeWidth(self, w):

    @classmethod
    def getFontAttributes(cls, css, e, style, attrs):
        # Font selection.
        sFont = css('font', e, style)

        # TODO: move font lookup to separate function, reuse for fallback font.
        # FIXME: Use Font object instead of path?
        if sFont is not None:
            # If the Font instance was supplied, then use it's path.
            if hasattr(sFont, 'path'):
                attrs['font'] = sFont.path
            else:
                # If the name was supplied, look it up and use it's path.

                #print(font)
                font = findFont(sFont)
                #print(font)

                # FIXME: lookup is done twice:
                # PageBot-Regular
                # <Font PageBot-Regular>
                #/Users/michiel/VirtualEnvironments/pagebot/lib/python3.8/site-packages/pagebot/resources/testfonts/typetr/PageBot-Regular.ttf
                # None


                if font:
                    attrs['font'] = font.path
                else:
                    # Font not found.
                    # TODO: add to logger.
                    #print('Warning: defaulting to %s' % DEFAULT_FONT_PATH)
                    attrs['font'] = DEFAULT_FONT_PATH

        else:
            # TODO: add to logger.
            #print('Warning: defaulting to %s' % DEFAULT_FONT_PATH)
            attrs['font'] = DEFAULT_FONT_PATH

        sFallbackFont = css('fallbackFont', e, style)

        if isinstance(sFallbackFont, Font):
            sFallbackFont = sFallbackFont.path
        elif sFallbackFont is None:
            sFallbackFont = DEFAULT_FALLBACK_FONT_PATH

        attrs['fallbackFont'] = sFallbackFont

    @classmethod
    def getStringAttributes(cls, t, e=None, style=None, w=None, h=None):
        """Adds some defaults to the style.

        If there is a target (pixel) width or height defined, ignore the
        requested fontSize and try the width or height first for fontSize =
        100. The resulting width or height is then used as base value to
        calculate the needed point size.

        Forced fontSize, then this overwrites the style['fontSize'] if it is
        there.

        TODO: add calculation of rFontSize (relative float based on
        root-fontSize) here too.
        TODO: split up into smaller functions.
        """

        fName = 'BabelString.getStringAttributes'
        attrs = {}


        cls.getFontAttributes(css, e, style, attrs)


        if w is not None or h is not None:
            # Start with large font size to scale for fitting.
            uFontSize = pt(100)
        else:
            # May be scaled to fit w or h if target is defined.
            uFontSize = css('fontSize', e, style, default=DEFAULT_FONT_SIZE)

        if uFontSize is not None:
            # Remember as base for relative units.
            attrs['fontSize'] = fontSizePt = upt(uFontSize)
        else:
            fontSizePt = DEFAULT_FONT_SIZE

        # FIXME: shouldn't become None.
        uLeading = css('leading', e, style, default=DEFAULT_LEADING)


        if not isUnit(uLeading):
            uLeading = em(uLeading)

        if uLeading is None:
            uLeading = em(1.0)

        attrs['leading'] = uLeading
        assert isUnit(uLeading)

        # TODO: separate colorAttrs function, reuse for fill & stroke.
        # Color values for text fill
        # Color: Fill the text with this color instance
        # noColor: Set the value to None, no fill will be drawn
        # inheritColor: Don't set color, inherit the current setting for fill

        if 'textFill' in style:
            cFill = css('textFill', e, style, default=blackColor)
        elif 'fill' in style:
            cFill = css('fill', e, style, default=blackColor)
        else:
            cFill = blackColor

        if cFill is not inheritColor:
            if isinstance(cFill, (tuple, list, int, float)):
                cFill = color(cFill)
            elif cFill is None:
                cFill = noColor

            msg = ('%s: Fill color "%s" is not Color in style %s' % (fName,
                cFill, style))

            assert isinstance(cFill, Color), msg

            if cFill is noColor:
                attrs['fill'] = None
            elif cFill.isCmyk:
                attrs['cmykFill'] = cFill.cmyk
            elif cFill.isRgba:
                attrs['fill'] = cFill.rgba
            else:
                attrs['fill'] = cFill.rgb

        # Color values for text stroke.
        # Color: Stroke the text with this color instance.
        # noColor: Set the value to None, no stroke will be drawn.
        # inheritColor: Don't set color, inherit the current setting for stroke.
        cStroke = css('textStroke', e, style, default=noColor)
        strokeWidth = css('textStrokeWidth', e, style)

        if strokeWidth is not None:
            msg = ('%s: strokeWidth %s must of type Unit' % (fName, strokeWidth))
            assert isUnit(strokeWidth), msg
            attrs['strokeWidth'] = upt(strokeWidth, base=fontSizePt)

        if cStroke is not inheritColor:
            if isinstance(cStroke, (tuple, list, int, float)):
                cStroke = color(cStroke)
            elif cStroke is None:
                cStroke = noColor

            msg = '%s: Stroke color "%s" is not Color in style %s' % (fName,
                    cStroke, style)
            assert isinstance(cStroke, Color), msg

            # None is value to disable stroke drawing.
            if cStroke is noColor:
                attrs['stroke'] = None
            elif cStroke.isCmyk:
                attrs['cmykStroke'] = cStroke.cmyk
            elif cStroke.isRgba:
                attrs['stroke'] = cStroke.rgba
            else:
                attrs['stroke'] = cStroke.rgb

        # NOTE: xAlign is used for element alignment, not text.
        #sAlign = css('xTextAlign', e, style)

        # FIXME: not an allowed style in the PB approach?
        # yTextAlign must be solved by parent container element.
        #if sAlign is not None:
        #    attrs['align'] = sAlign

        # FIXME: not an allowed style in the PB approach?
        #sUnderline = css('underline', e, style)

        # Only these values work in FormattedString.
        #if sUnderline in ('single', None):
        #    attrs['underline'] = sUnderline

        uParagraphTopSpacing = css('paragraphTopSpacing', e, style)

        if uParagraphTopSpacing is not None:
            # Base for em or percent.
            attrs['paragraphTopSpacing'] = upt(uParagraphTopSpacing,
                    base=fontSizePt)

        uParagraphBottomSpacing = css('paragraphBottomSpacing', e, style)

        if uParagraphBottomSpacing:
            # Base for em or percent.
            attrs['paragraphBottomSpacing'] = upt(uParagraphBottomSpacing, base=fontSizePt)

        uTracking = css('tracking', e, style)

        if uTracking is not None:
            # Base for em or percent.
            attrs['tracking'] = upt(uTracking, base=fontSizePt)

        uBaselineShift = css('baselineShift', e, style)

        if uBaselineShift is not None:
            # Base for em or percent.
            attrs['baselineShift'] = upt(uBaselineShift, base=fontSizePt)

        openTypeFeatures = css('openTypeFeatures', e, style)

        if openTypeFeatures is not None:
            attrs['openTypeFeatures'] = openTypeFeatures

        # Can be [(10, LEFT), ...] or [10, 20, ...]
        tabs = []

        for tab in (css('tabs', e, style) or []):
            if not isinstance(tab, (list, tuple)):
                tab = upt(tab), LEFT
            else:
                tab = upt(tab[0]), tab[1]
            tabs.append(tab)
        if tabs:
            attrs['tabs'] = tabs

        attrs['hyphenation'] = bool(css('hyphenation', e, style))

        uFirstLineIndent = css('firstLineIndent', e, style)

        # TODO: Use this value instead, if current tag is different from
        # previous tag. How to get this info?
        # firstTagIndent = style.get('firstTagIndent')
        # TODO: Use this value instead, if currently on top of a new string.
        if uFirstLineIndent is not None:
            # Base for em or percent.
            attrs['firstLineIndent'] = upt(uFirstLineIndent, base=fontSizePt)

        uIndent = css('indent', e, style)

        if uIndent is not None:
            # Base for em or percent.
            attrs['indent'] = upt(uIndent, base=fontSizePt)

        uTailIndent = css('tailIndent', e, style)
        if uTailIndent is not None:
            # Base for em or percent.
            attrs['tailIndent'] = upt(uTailIndent, base=fontSizePt)

        sLanguage = css('language', e, style)

        if sLanguage is not None:
            attrs['language'] = sLanguage

        return attrs

    @classmethod
    def addCaseToString(cls, s, e, style):
        sUpperCase = css('uppercase', e, style)
        sLowercase = css('lowercase', e, style)
        sCapitalized = css('capitalized', e, style)

        if sUpperCase:
            s = s.upper()
        elif sLowercase:
            s = s.lower()
        elif sCapitalized:
            s = s.capitalize()

        return s

    @classmethod
    def getColor(cls, style):
        c = None

        if 'fill' in style:
            c = style['fill']

            if not isinstance(c, Color):
                # TODO: extend list of options, ie rgba, cmyk, etc.
                if isinstance(c, tuple) and len(c) == 3:
                    c = Color(rgb=c)
                else:
                    c = DEFAULT_COLOR

        elif 'color' in style:
            c = Color(style.get('color'))

        if c is None:
            c = DEFAULT_COLOR

        assert isinstance(c, Color)
        return c

    @classmethod
    def newString(cls, s, context, e=None, style=None, w=None, h=None,
            pixelFit=True):
        raise NotImplementedError

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
