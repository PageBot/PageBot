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
import difflib

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
    """FlatString is a wrapper around the Flat string that should be
    functionally compatible with a Cocoa attributed string and the CoreText
    typesetter.
    
    * https://developer.apple.com/documentation/foundation/nsattributedstring
    * https://developer.apple.com/documentation/coretext/ctframesetter-2eg

    """

    BABEL_STRING_TYPE = 'flat'
    UNITS = 'pt'

    def __init__(self, s, context, style=None, strike=None):
        """Constructor of the FlatString, which is a wrapper around a Flat
        `text` class. Optionally stores the (latest) style that was used to
        produce the formatted string.

        >>> from pagebot import getContext
        >>> context = getContext('Flat')
        >>> fs = context.newString('ABC')
        >>> fs
        ABC
        >>> fs.style
        {'fallbackFont': 'Verdana', 'fontSize': 12, 'lineHeight': 16.8, 'fill': (0, 0, 0), 'stroke': None, 'underline': None}
        >>> # fs.font
        >>> # round(upt(fs.xHeight))
        >>> # fs.xHeight
        >>> # fs.capHeight
        >>> # fs.ascender
        >>> # fs.descender
        >>> fs.fontSize
        12
        >>> fs.lineHeight
        1.4em
        >>> pt(fs.lineHeight)
        16.8pt
        >>> from pagebot.toolbox.units import em
        >>> style = dict(font='Verdana', fontSize=pt(100), leading=em(1.4))
        >>> fs = context.newString('Example Text', style=style)
        >>> from pagebot.contexts.base.babelstring import BabelString
        >>> isinstance(fs, BabelString)
        True
        >>> fs2 = context.newString('Second Text', style=style)
        >>> #fs + fs2
        >>> #fs.fontPath
        >>> #'/Verdana'in bs.fontPath
        #True
        >>> #lines = fs.getTextLines(w=100)
        >>> #len(lines)
        #9
        >>> #line = lines[0]
        >>> #line.xHeight, line.capHeight # Max metrics of all runs in line as Em
        #(0.55em, 0.73em)
        >>> #run = line.textRuns[0]
        >>> #run.xHeight, run.capHeight
        #(0.55em, 0.73em)
        """
        # Some checking, in case we get something else here.
        assert style is None or isinstance(style, dict)
        assert isinstance(s, str)
    
        if style is None:
            style = {}

        self.data = []

        # For each block of text, stores the plain string, the Flat `strike`
        # stylings and the Flat `text` (which is comparable to the DrawBot
        # FormattedString which in turn wraps a Cocoa NSAttributedString).
        self.data.append(dict(s=s, strike=strike, text=strike.text(s),
                style=style))

        super().__init__(context)

    def copy(self):
        """

        >>> from pagebot import getContext
        >>> context = getContext('Flat')
        >>> fs = context.newString('ABC')
        >>> fs2 = fs.copy()
        >>> id(fs) == id(fs2)
        False
        """
        # FIXME: copy all data, instead of first block.
        s = self.data[0]['s']
        strike = self.data[0]['strike']
        style = self.data[0]['style']
        fs = FlatString(s, self.context, style=style, strike=strike)
        # TODO: copy the rest if there;
        return fs

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
        >>> fs[:5]
        blabl
        >>> fs[5]
        a
        """
        if isinstance(given, slice):
            fs = self.copy()
            s = fs.s
            fs.s = s[given.start:given.stop]
            return fs

        # Untouched.
        if isinstance(given, (list, tuple)):
            return self 

        # Single index.
        fs = self.copy()
        s = fs.s
        fs.s = s[given]
        return fs

    def __repr__(self):
        return self.s

    def _get_s(self):
        """Answers the plain string."""
        s = ''

        for d in self.data:
            s += d['s']
        return s

    def _set_s(self, s, i=0):
        d = self.data[i]
        strike = d['strike']
        d['s'] = s
        d['text'] = strike.text(s)

    s = property(_get_s, _set_s)

    def _get_style(self):
        """Answers the style."""
        #for d in self.data:
        return self.data[0]['style']

    def _set_style(self, style, i=0):
        self.data[i]['style'] = style

    style = property(_get_style, _set_style)

    def _get_strike(self):
        """Answers the strike."""
        #for d in self.data:
        return self.data[0]['strike']

    def _set_strike(self, strike, i=0):
        self.data[i]['strike'] = strike

    strike = property(_get_strike, _set_strike)

    def _get_text(self):
        """Answers the text."""
        #for d in self.data:
        if len(self.data) == 1:
            return self.data[0]['text']
        else:
            # TODO: needs a delta operator.
            return self.data[0]['text']

    def _set_text(self, text, i=0):
        self.data[i]['text'] = text

    text = property(_get_text, _set_text)

    def _get_font(self):
        """Answers the current state of fontName."""
        return self.style.get('font')

    def _set_font(self, fontName):
        if fontName is not None:
            self.context.font(fontName)

        self.style['font'] = fontName

    font = property(_get_font, _set_font)

    '''
    def _get_fontFilePath(self):
        """Return the path to the file of the current font."""
        return self.s.fontFilePath()

    fontPath = property(_get_fontFilePath)
    '''

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

    def _get_lineHeight(self):
        """Returns the current line height, based on the current font and
        fontSize. If a lineHeight is set, this value will be returned."""
        # FIXME: calculate instead? see BabelString.
        return self.style.get('leading', DEFAULT_LEADING)
        #fontSize = upt(self.fontSize)
        #return em(self.s.fontLineHeight() / fontSize, base=fontSize)

    # Compatibility with DrawBot API.
    fontLineHeight = lineHeight = property(_get_lineHeight) 

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
        return len(self.s)

    def asText(self):
        """Answers as unicode string.

        >>> from pagebot import getContext
        >>> context = getContext('Flat')
        >>> fs = context.newString('ABC')
        >>> fs.asText()
        'ABC'
        """
        return self.s 

    def textSize(self, w=None, h=None):
        """Answers the `(w, h)` size tuple for a given width, with the current
        text.
        
        >>> from pagebot import getContext
        >>> context = getContext('Flat')
        >>> style = dict(font='Roboto-Regular', fontSize=12)
        >>> fs = context.newString('ABC ', style=style)
        >>> fs
        ABC 
        >>> fs.textSize()
        (26.09, 16.8)
        """
        w = self.strike.width(self.s)
        fontSizePt = upt(self.style.get('fontSize', DEFAULT_FONT_SIZE))
        leadingPt = upt(self.style.get('leading', DEFAULT_LEADING), base=fontSizePt)
        h = leadingPt
        w = round(w, 2)
        h = round(h, 2)
        return w, h

    def textBox(self, page, box, align=LEFT):
        """
        Places text segments.
        """
        # TODO: should keep track of multiple text parts.
        # TODO: implement alignment.
        x, y, w, h = box
        placedText = page.place(self.text)
        placedText.frame(x, y, w, h)

        # Calculates text difference when overflow occurs.
        if placedText.overflow():
            s1 = self.getPlacedString(placedText)
            s2 = str(self)
            assert len(s1) <= len(s2)
            diff0, _ = self.getTextDiff(s1, s2)
            return diff0
        else:
            return ''

    def getPlacedString(self, placedText):
        # TODO: keep track of multiple placed text parts.
        return ''.join(placedText.lines())

    def getTextDiff(self, s1, s2):
        # TODO: keep track of multiple placed text parts.
        textDiff0 = ''
        textDiff1 = ''

        for i, s in enumerate(difflib.ndiff(s2, s1)):
            if s[0]==' ':
                continue
            elif s[0]=='-':
                textDiff0 += s[-1]
            elif s[0]=='+':
                textDiff1 += s[-1]

        return textDiff0, textDiff1

    def textOverflow(self, page, box, align=LEFT):
        """
        Calculates the overflowing text using the textBox function.

        NOTE: signature differs from DrawBotString, where the box is calcuted
        using width and height only.

        def textOverflow(self, page, w, h, align=LEFT):
            box = (0, 0, w, h)
            ...

        """
        s = self.textBox(page, box, align=align)
        return s

    def append(self, s):
        """
        Append string or FlatString to self.

        >>> from pagebot import getContext
        >>> context = getContext('Flat')
        >>> bla = context.newString('bla')
        >>> bla2 = context.newString('bla2')
        >>> bla + bla2
        blabla2
        """
        assert isinstance(s, (str, FlatString))

        if isinstance(s, str):
            fs = self.context.newString(s)
        else:
            fs = s

        self.data.extend(fs.data)

    def getStyleAtIndex(self, index):
        """

        >>> from pagebot import getContext
        >>> context = getContext('Flat')
        >>> bla = context.newString('bla')
        >>> style = bla.getStyleAtIndex(2)
        >>> style['fontSize']
        12
        >>> style = {'fontSize': 16}
        >>> bla2 = context.newString('bla2', style=style)
        >>> bla = bla + bla2
        >>> style = bla.getStyleAtIndex(4)
        >>> style['fontSize']
        16
        >>> bla.getStyleAtIndex(7)
        False
        """
        i = 0

        for j, value in enumerate(self.data):
            d = self.data[j]
            s = d['s']

            for char in s:
                if index == i:
                    return d['style']
                i += 1

        return False
        
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
    def getFSAttrs(cls, t, e=None, style=None, w=None, h=None,
            pixelFit=True):
        """Adds some defaults to the style."""
        fName = 'FlatString.getFSAttrs'
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

        lineHeight = upt(uLeading or DEFAULT_LEADING, base=fontSizePt)
        lineHeight = round(lineHeight, 2)
        fsAttrs['lineHeight'] = lineHeight

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

            msg = ('%s: Fill color "%s" is not Color in style %s' % (fName,
                cFill, style))

            assert isinstance(cFill, Color), msg

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
            msg = ('%s: strokeWidth %s must of type Unit' % (fName, strokeWidth))
            assert isUnit(strokeWidth), msg
            fsAttrs['strokeWidth'] = upt(strokeWidth, base=fontSizePt)

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
        style = cls.getFSAttrs(s, e=e, style=style, w=w, h=h,
                pixelFit=pixelFit)
        fontPath = cls.getFontPath(style)
        fontSizePt = upt(style.get('fontSize', DEFAULT_FONT_SIZE))
        leadingPt = upt(style.get('leading', DEFAULT_LEADING), base=fontSizePt)
        flatFont = context.b.font.open(fontPath)
        strike = context.b.strike(flatFont)
        color = cls.getColor(style)
        rgb = context.getFlatRGB(color)
        strike.color(rgb).size(fontSizePt, leadingPt, units=cls.UNITS)
        return cls(s, context=context, style=style, strike=strike)

    def getTextLines(self, w, h=None, align=LEFT):
        return []
        # TODO

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
