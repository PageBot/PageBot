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
#     flatstring.py
#

import os
import re
from flat.text import text

from pagebot.constants import (LEFT, DEFAULT_FONT_SIZE, DEFAULT_LEADING,
        DEFAULT_FALLBACK_FONT_PATH)
from pagebot.contexts.base.babelstring import BabelString
from pagebot.fonttoolbox.objects.font import Font
from pagebot.filepaths import DEFAULT_FONT_PATH
from pagebot.style import css
from pagebot.toolbox.units import upt, pt, isUnit
from pagebot.toolbox.color import Color, blackColor, inheritColor, noColor, color

DEFAULT_COLOR = Color(0, 0, 0)

class FlatString(BabelString):
    """FlatString is a wrapper around the Flat string."""

    BABEL_STRING_TYPE = 'flat'
    UNITS = 'pt'

    def __init__(self, s, context, style=None, strike=None):
        """Constructor of the FlatString, which is a wrapper around a Flat
        `text` class. Optionally stores the (latest) style that was used to
        produce the formatted string.

        >>> from pagebot import getContext
        >>> context = getContext('Flat')
        >>> fs = context.newString('ABC')
        >>> print(fs)
        ABC
        >>> #bs.font, bs.fontSize, round(upt(bs.xHeight)), bs.xHeight, bs.capHeight, bs.ascender, bs.descender
        #('Verdana', 80pt, 44, 0.55em, 0.73em, 1.01em, -0.21em)
        >>> #'/Verdana'in bs.fontPath
        #True
        >>> #style = dict(font='Verdana', fontSize=pt(100), leading=em(1.4))
        >>> #bs = context.newString('Example Text', style=style)
        >>> #from pagebot.contexts.base.babelstring import BabelString
        >>> #isinstance(bs, BabelString)
        #True
        >>> #lines = bs.getTextLines(w=100)
        >>> #len(lines)
        #9
        >>> #line = lines[0]
        >>> #line.xHeight, line.capHeight # Max metrics of all runs in line as Em
        #(0.55em, 0.73em)
        >>> #run = line.textRuns[0]
        >>> #run.xHeight, run.capHeight
        #(0.55em, 0.73em)
        """
        self.context = context # Store context, in case we need more of its functions.
        assert isinstance(s, text)
        self.s = s # Store the Flat equivalent `text` of a DrawBot FormattedString.

        if style is None:
            style = {}

        self.style = style
        self.strike = strike
        super().__init__(s, context, style=style)

    def __repr__(self):
        if isinstance(self.s, str):
            return self.s

        s = ''

        for paragraph in self.s.paragraphs:
            for span in paragraph.spans:
                s += span.string

        return s

    def _get_s(self):
        """Answers the embedded Flat `text` class (the equivalent of a OS X
        FormattedString) by property to enforce checking type of the string."""
        return self._s

    def _set_s(self, s):
        self._s = s

    s = property(_get_s, _set_s)

    def _get_font(self):
        """Answers the current state of fontName."""
        return self.style.get('font')

    def _set_font(self, fontName):
        if fontName is not None:
            self.context.font(fontName)
        self.style['font'] = fontName

    font = property(_get_font, _set_font)

    def _get_fontSize(self):
        """Answers the current state of the fontSize."""
        return self.style.get('fontSize', DEFAULT_FONT_SIZE)

    def _set_fontSize(self, fontSize):
        if fontSize is not None:
            self.context.font(fontSize)
        self.style['fontSize'] = fontSize

    fontSize = property(_get_fontSize, _set_fontSize)

    def _get_leading(self):
        """Answers the current leading value."""
        return self.style.get('leading', DEFAULT_LEADING)
        #leadingPt = upt(self.style.get('leading', DEFAULT_LEADING))
        #return leadingPt 

    leading = property(_get_leading)

    def _get_color(self):
        """Answers the current state of the color."""
        return self.style.get('color')

    def _set_color(self, color):
        #if color is not None:
        #    self.context.font(color)
        self.style['color'] = color

    color = property(_get_color, _set_color)

    def __len__(self):
        """Answers the number of characters in self.s

        >>> from pagebot import getContext
        >>> context = getContext('Flat')
        >>> fs = context.newString('ABC')
        >>> fs
        ABC
        >>> len(fs)
        3
        """
        return len(str(self))

    def asText(self):
        """Answers as unicode string.

        >>> from pagebot import getContext
        >>> context = getContext('Flat')
        >>> fs = context.newString('ABC')
        >>> isinstance(fs.s, text)
        True
        >>> fs.asText()
        'ABC'
        """
        return str(self) # TODO: To be changed to Flat string behavior.

    def textSize(self, w=None, h=None):
        """Answers the `(w, h)` size tuple for a given width, with the current
        text."""
        # FIXME: Make this work in Flat same as in DrawBot
        #return self.b.textSize(s)
        w = self.strike.width(str(self.s))
        fontSizePt = upt(self.style.get('fontSize', DEFAULT_FONT_SIZE))
        leadingPt = upt(self.style.get('leading', DEFAULT_LEADING), base=fontSizePt)
        h = leadingPt
        return w, h

    def textOverflow(self, w, h, align=LEFT):
        # FIXME: Make this work in Flat same as in DrawBot
        return ''

    def append(self, s):
        """Append string or FlatString to self."""
        # FIXME
        #try:
        #    self.s += s.s
        #except TypeError:
        #    self.s += repr(s) # Convert to babel string, whatever it is.
        raise NotImplementedError

    MARKER_PATTERN = '==%s@%s=='
    FIND_FS_MARKERS = re.compile('\=\=([a-zA-Z0-9_\:\.]*)\@([^=]*)\=\=')

    def appendMarker(self, markerId, arg):
        """Append an invisible marker string."""

    def findMarkers(self, reCompiled=None):
        """Answers a dictionary of markers with their arguments in self.s."""
        if reCompiled is None:
            reCompiled= self.FIND_FS_MARKERS
        return reCompiled.findall(u'%s' % self.s)

    @classmethod
    def getFSAttrs(cls, t, context, e=None, style=None, w=None, h=None, pixelFit=True):
        fsAttrs = {}

        # Font selection.
        sFont = css('font', e, style)

        if sFont is not None:
            # If the Font instance was supplied, then use it's path.
            if hasattr(sFont, 'path'):
                sFont = sFont.path
            fsAttrs['font'] = sFont

        sFallbackFont = css('fallbackFont', e, style)

        if isinstance(sFallbackFont, Font):
            sFallbackFont = sFallbackFont.path
        elif sFallbackFont is None:
            sFallbackFont = DEFAULT_FALLBACK_FONT_PATH

        fsAttrs['fallbackFont'] = sFallbackFont

        '''
        If there is a target (pixel) width or height defined, ignore the
        requested fontSize and try the width or height first for fontSize =
        100. The resulting width or height is then used as base value to
        calculate the needed point size.

        Forced fontSize, then this overwrites the style['fontSize'] if it is
        there.

        TODO: add calculation of rFontSize (relative float based on
        root-fontSize) here too.
        '''
        if w is not None or h is not None:
            uFontSize = pt(100) # Start with large font size to scale for fitting.
        else:
            # May be scaled to fit w or h if target is defined.
            uFontSize = css('fontSize', e, style, default=DEFAULT_FONT_SIZE)

        if uFontSize is not None:
            # Remember as base for relative units.
            fsAttrs['fontSize'] = fontSizePt = upt(uFontSize)
        else:
            fontSizePt = DEFAULT_FONT_SIZE

        uLeading = css('leading', e, style)

        # Base for em or percent.
        fsAttrs['lineHeight'] = upt(uLeading or DEFAULT_LEADING, base=fontSizePt)

        # Color values for text fill
        # Color: Fill the text with this color instance
        # noColor: Set the value to None, no fill will be drawn
        # inheritColor: Don't set color, inherit the current setting for fill
        cFill = css('textFill', e, style, default=blackColor)

        if cFill is not inheritColor:
            if isinstance(cFill, (tuple, list, int, float)):
                cFill = color(cFill)
            elif cFill is None:
                cFill = noColor
            assert isinstance(cFill, Color), ('FlatString.getFSAttrs: Fill color "%s" is not Color in style %s' % (cFill, style))
            if cFill is noColor:
                fsAttrs['fill'] = None
            elif cFill.isCmyk:
                fsAttrs['cmykFill'] = cFill.cmyk
            elif cFill.isRgba:
                fsAttrs['fill'] = cFill.rgba
            else:
                fsAttrs['fill'] = cFill.rgb

        # Color values for text stroke.
        # Color: Stroke the text with this color instance.
        # noColor: Set the value to None, no stroke will be drawn.
        # inheritColor: Don't set color, inherit the current setting for stroke.
        cStroke = css('textStroke', e, style, default=noColor)
        strokeWidth = css('textStrokeWidth', e, style)

        if strokeWidth is not None:
            assert isUnit(strokeWidth), ('FlatString.getFSAttrs: strokeWidth %s must of type Unit' % strokeWidth)
            fsAttrs['strokeWidth'] = upt(strokeWidth, base=fontSizePt)

        if cStroke is not inheritColor:
            if isinstance(cStroke, (tuple, list, int, float)):
                cStroke = color(cStroke)
            elif cStroke is None:
                cStroke = noColor

            msg = 'FlatString.getFSAttrs] Stroke color "%s" is not Color in style %s' % (cStroke, style)
            assert isinstance(cStroke, Color), msg

            # None is value to disable stroke drawing.
            if cStroke is noColor: 
                fsAttrs['stroke'] = None
            elif cStroke.isCmyk:
                fsAttrs['cmykStroke'] = cStroke.cmyk
            elif cStroke.isRgba:
                fsAttrs['stroke'] = cStroke.rgba
            else:
                fsAttrs['stroke'] = cStroke.rgb

        # NOTE: xAlign is used for element alignment, not text.
        sAlign = css('xTextAlign', e, style)

        # yTextAlign must be solved by parent container element.
        if sAlign is not None: 
            fsAttrs['align'] = sAlign

        sUnderline = css('underline', e, style)

        # Only these values work in FormattedString.
        if sUnderline in ('single', None): 
            fsAttrs['underline'] = sUnderline

        uParagraphTopSpacing = css('paragraphTopSpacing', e, style)

        if uParagraphTopSpacing is not None:
            # Base for em or percent.
            fsAttrs['paragraphTopSpacing'] = upt(uParagraphTopSpacing,
                    base=fontSizePt) 

        uParagraphBottomSpacing = css('paragraphBottomSpacing', e, style)

        if uParagraphBottomSpacing:
            # Base for em or percent.
            fsAttrs['paragraphBottomSpacing'] = upt(uParagraphBottomSpacing, base=fontSizePt) 

        uTracking = css('tracking', e, style)

        if uTracking is not None:
            # Base for em or percent.
            fsAttrs['tracking'] = upt(uTracking, base=fontSizePt) 

        uBaselineShift = css('baselineShift', e, style)

        if uBaselineShift is not None:
            # Base for em or percent.
            fsAttrs['baselineShift'] = upt(uBaselineShift, base=fontSizePt) 

        openTypeFeatures = css('openTypeFeatures', e, style)

        if openTypeFeatures is not None:
            fsAttrs['openTypeFeatures'] = openTypeFeatures

        # Can be [(10, LEFT), ...] or [10, 20, ...]
        tabs = []

        for tab in (css('tabs', e, style) or []): 
            if not isinstance(tab, (list, tuple)):
                tab = upt(tab), LEFT
            else:
                tab = upt(tab[0]), tab[1]
            tabs.append(tab)
        if tabs:
            fsAttrs['tabs'] = tabs

        # Sets the hyphenation flag from style, as in DrawBot this is set by a
        # global function, not as FormattedString attribute.
        # FIX IN DRAWBOT fsAttrs['language'] = bool(css('language', e, style))
        # FIX IN DRAWBOT
        #fsAttrs['hyphenation'] = bool(css('hyphenation', e, style))

        uFirstLineIndent = css('firstLineIndent', e, style)

        # TODO: Use this value instead, if current tag is different from
        # previous tag. How to get this info?
        # firstTagIndent = style.get('firstTagIndent')
        # TODO: Use this value instead, if currently on top of a new string.
        if uFirstLineIndent is not None:
            # Base for em or percent.
            fsAttrs['firstLineIndent'] = upt(uFirstLineIndent, base=fontSizePt) 

        uIndent = css('indent', e, style)

        if uIndent is not None:
            # Base for em or percent.
            fsAttrs['indent'] = upt(uIndent, base=fontSizePt) 

        uTailIndent = css('tailIndent', e, style)
        if uTailIndent is not None:
            # Base for em or percent.
            fsAttrs['tailIndent'] = upt(uTailIndent, base=fontSizePt) 

        sLanguage = css('language', e, style)

        if sLanguage is not None:
            fsAttrs['language'] = sLanguage

        return fsAttrs


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
    def getFontPath(cls, style):
        font = style.get('font')

        if font is not None and not isinstance(font, str):
            fontPath = font.path
        else:
            fontPath = font

        if fontPath is None or not os.path.exists(fontPath):
            # TODO: get path from base context self._font.
            fontPath = DEFAULT_FONT_PATH

        return fontPath

    @classmethod
    def getColor(cls, style):
        c = None

        if 'textFill' in style:
            c = style['textFill']

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
        """Answers a FlatString instance from valid attributes in *style*. Sets
        all values after testing their existence so they can inherit from
        previous style formats. If target width *w* or height *h* is defined,
        then *fontSize* is scaled to make the string fit *w* or *h*.

        TODO: Because Flat does not do font GSUB feature compile, we need to
        make the transformed string here, using Tal's Compositor:
        
            https://github.com/typesupply/compositor
        
        >>> from pagebot.toolbox.units import pt
        >>> from pagebot import getContext
        >>> context = getContext('Flat')
        >>> bs = context.newString('AAA', style=dict(fontSize=pt(30)))
        >>> str(bs) == 'AAA'
        True
        """
        if style is None:
            style = {}
        else:
            assert isinstance(style, dict)

        s = cls.addCaseToString(s, e, style)
        #fsAttrs = cls.getFSAttrs(s, context, e=e, style=style, w=w, h=h,
        #        pixelFit=pixelFit)
        fontPath = cls.getFontPath(style)
        fontSizePt = upt(style.get('fontSize', DEFAULT_FONT_SIZE))
        leadingPt = upt(style.get('leading', DEFAULT_LEADING), base=fontSizePt)
        flatFont = context.b.font.open(fontPath)
        strike = context.b.strike(flatFont)
        color = cls.getColor(style)
        rgb = context.getFlatRGB(color)
        strike.color(rgb).size(fontSizePt, leadingPt, units=cls.UNITS)
        return cls(strike.text(s), context=context, style=style, strike=strike)

    def getTextLines(self, w, h=None, align=LEFT):
        return []
        # TODO

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
