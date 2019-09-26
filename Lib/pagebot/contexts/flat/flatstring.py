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

from pagebot.constants import (LEFT, DEFAULT_FONT_SIZE, DEFAULT_LEADING,
        DEFAULT_FALLBACK_FONT_PATH)
from pagebot.contexts.base.babelstring import BabelString
from pagebot.fonttoolbox.objects.font import Font
from pagebot.paths import DEFAULT_FONT_PATH
from pagebot.style import css
from pagebot.toolbox.units import upt, pt, isUnit
from pagebot.toolbox.color import Color, blackColor, inheritColor, noColor, color

DEFAULT_COLOR = Color(0, 0, 0)

class FlatString(BabelString):
    """FlatString is a wrapper around the Flat string."""

    BABEL_STRING_TYPE = 'flat'
    UNITS = 'pt'

    def __init__(self, s, context, style=None):
        """Constructor of the FlatString, which is a wrapper around
        flat string. Optionally stores the (latest) style that was
        used to produce the formatted string.

        >>> from pagebot.contexts.flat.flatcontext import FlatContext
        >>> context = FlatContext()
        >>> bs = context.newString('ABC')
        >>> #bs
        ABC
        """
        self.context = context # Store context, in case we need more of its functions.
        self.s = s # Store the Flat equivalent of a DrawBot FormattedString.

        # In case defined, store current status here as property and set the
        # current FormattedString for future additions. Also the answered
        # metrics will not be based on these values.
        if style is None:
            style = {}

        self.style = style
        super().__init__(s, context, style=style)

    def __repr__(self):
        return str(self.s)

    def _get_s(self):
        """Answers the embedded Flat equivalent of a OS X FormattedString by
        property to enforce checking type of the string."""
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

        >>> from pagebot.contexts.flat.flatcontext import FlatContext
        >>> context = FlatContext()
        >>> fs = FlatString('ABC', context)
        >>> fs
        ABC
        >>> len(fs)
        3
        """
        return len(str(self.s))

    def asText(self):
        """Answers as unicode string.

        >>> from pagebot.contexts.flat.flatcontext import FlatContext
        >>> context = FlatContext()
        >>> fs = FlatString('ABC', context)
        >>> fs.s
        'ABC'
        >>> fs.asText()
        'ABC'
        """
        return str(self.s) # TODO: To be changed to Flat string behavior.

    def textSize(self, w=None, h=None):
        """Answers the (w, h) size for a given width, with the current text."""
        # TODO: Make this work in Flat same as in DrawBot
        #return self.b.textSize(s)
        return 100, 20

    def textOverflow(self, w, h, align=LEFT):
        # TODO: Make this work in Flat same as in DrawBot
        # TODO: Some stuff needs to get here.
        return ''

    def append(self, s):
        """Append string or FlatString to self."""
        # FIXME
        #try:
        #    self.s += s.s
        #except TypeError:
        #    self.s += repr(s) # Convert to babel string, whatever it is.

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
            assert isinstance(cFill, Color), ('FlatString.newString: Fill color "%s" is not Color in style %s' % (cFill, style))
            if cFill is noColor:
                fsAttrs['fill'] = None
            elif cFill.isCmyk:
                fsAttrs['cmykFill'] = cFill.cmyk
            elif cFill.isRgba:
                fsAttrs['fill'] = cFill.rgba
            else:
                fsAttrs['fill'] = cFill.rgb

        # Color values for text stroke
        # Color: Stroke the text with this color instance
        # noColor: Set the value to None, no stroke will be drawn
        # inheritColor: Don't set color, inherit the current setting for stroke
        cStroke = css('textStroke', e, style, default=noColor)
        strokeWidth = css('textStrokeWidth', e, style)

        if strokeWidth is not None:
            assert isUnit(strokeWidth), ('FlatString.newString: strokeWidth %s must of type Unit' % strokeWidth)
            fsAttrs['strokeWidth'] = upt(strokeWidth, base=fontSizePt)

        if cStroke is not inheritColor:
            if isinstance(cStroke, (tuple, list, int, float)):
                cStroke = color(cStroke)
            elif cStroke is None:
                cStroke = noColor

            assert isinstance(cStroke, Color), ('FlatString.newString] Stroke color "%s" is not Color in style %s' % (cStroke, style))

            if cStroke is noColor: # None is value to disable stroke drawing
                fsAttrs['stroke'] = None
            elif cStroke.isCmyk:
                fsAttrs['cmykStroke'] = cStroke.cmyk
            elif cStroke.isRgba:
                fsAttrs['stroke'] = cStroke.rgba
            else:
                fsAttrs['stroke'] = cStroke.rgb

        # NOTE: xAlign is used for element alignment, not text.
        sAlign = css('xTextAlign', e, style)

        if sAlign is not None: # yTextAlign must be solved by parent container element.
            fsAttrs['align'] = sAlign

        sUnderline = css('underline', e, style)

        if sUnderline in ('single', None): # Only these values work in FormattedString
            fsAttrs['underline'] = sUnderline

        uParagraphTopSpacing = css('paragraphTopSpacing', e, style)

        if uParagraphTopSpacing is not None:
            fsAttrs['paragraphTopSpacing'] = upt(uParagraphTopSpacing, base=fontSizePt) # Base for em or perc

        uParagraphBottomSpacing = css('paragraphBottomSpacing', e, style)

        if uParagraphBottomSpacing:
            fsAttrs['paragraphBottomSpacing'] = upt(uParagraphBottomSpacing, base=fontSizePt) # Base for em or perc

        uTracking = css('tracking', e, style)

        if uTracking is not None:
            fsAttrs['tracking'] = upt(uTracking, base=fontSizePt) # Base for em or perc

        uBaselineShift = css('baselineShift', e, style)

        if uBaselineShift is not None:
            fsAttrs['baselineShift'] = upt(uBaselineShift, base=fontSizePt) # Base for em or perc

        openTypeFeatures = css('openTypeFeatures', e, style)

        if openTypeFeatures is not None:
            fsAttrs['openTypeFeatures'] = openTypeFeatures

        tabs = []
        for tab in (css('tabs', e, style) or []): # Can be [(10, LEFT), ...] or [10, 20, ...]
            if not isinstance(tab, (list, tuple)):
                tab = upt(tab), LEFT
            else:
                tab = upt(tab[0]), tab[1]
            tabs.append(tab)
        if tabs:
            fsAttrs['tabs'] = tabs

        # Set the hyphenation flag from style, as in DrawBot this is set by a
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
            fsAttrs['firstLineIndent'] = upt(uFirstLineIndent, base=fontSizePt) # Base for em or perc

        uIndent = css('indent', e, style)

        if uIndent is not None:
            fsAttrs['indent'] = upt(uIndent, base=fontSizePt) # Base for em or perc

        uTailIndent = css('tailIndent', e, style)
        if uTailIndent is not None:
            fsAttrs['tailIndent'] = upt(uTailIndent, base=fontSizePt) # Base for em or perc

        sLanguage = css('language', e, style)

        if sLanguage is not None:
            fsAttrs['language'] = sLanguage

        return fsAttrs

    @classmethod
    def newString(cls, s, context, e=None, style=None, w=None, h=None, pixelFit=True):
        """Answers a FlatString instance from valid attributes in *style*. Set
        all values after testing their existence, so they can inherit from
        previous style formats. If target width *w* or height *h* is defined,
        then *fontSize* is scaled to make the string fit *w* or *h*.

        >>> from pagebot.toolbox.units import pt
        >>> from pagebot.contexts.flat.flatcontext import FlatContext
        >>> context = FlatContext()
        >>> bs = FlatString.newString('AAA', context, style=dict(fontSize=pt(30)))
        >>> 'flat.text.text' in str(bs)
        True
        """
        if style is None:
            style = {}

        fsAttrs = cls.getFSAttrs(s, context, e=e, style=style, w=w, h=h,
                pixelFit=pixelFit)

        sUpperCase = css('uppercase', e, style)
        sLowercase = css('lowercase', e, style)
        sCapitalized = css('capitalized', e, style)

        if sUpperCase:
            s = s.upper()
        elif sLowercase:
            s = s.lower()
        elif sCapitalized:
            s = s.capitalize()


        # TODO
        # Because Flat does not do font GSUB feature compile, we'll make the
        # transformed string here, using Tal's Compositor:
        #
        #     https://github.com/typesupply/compositor
        #
        # This needs to be installed, in case PageBot is running outside of
        # DrawBot.

        font = style.get('font')

        if font is not None and not isinstance(font, str):
            font = font.path

        if font is None or not os.path.exists(font):
            # TODO: get path from base context self._font.
            font = DEFAULT_FONT_PATH

        fontSizePt = upt(style.get('fontSize', DEFAULT_FONT_SIZE))
        leadingPt = upt(style.get('leading', DEFAULT_LEADING), base=fontSizePt)
        flatFont = context.b.font.open(font)
        strike = context.b.strike(flatFont)
        #c = style.get('color', DEFAULT_COLOR)

        if 'textFill' in style:
            c = style['textFill']
            if not isinstance(c, Color):
                if isinstance(c, tuple) and len(c) == 3:
                    c = Color(rgb=c)
                # TODO: extend list of options.
        else:
            c = style.get('color', DEFAULT_COLOR)

        assert isinstance(c, Color)
        rgb = context.getFlatRGB(c)
        strike.color(rgb).size(fontSizePt, leadingPt, units=cls.UNITS)

        # FIXME
        #if w is not None:
        #    strike.width = w

        return cls(strike.text(s), context=context, style=style)

    def getTextLines(self, w, h=None, align=LEFT):
        return []
        # TODO

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
