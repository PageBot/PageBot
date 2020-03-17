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

import re
import difflib
from fontTools.pens.boundsPen import BoundsPen

from pagebot.constants import LEFT, DEFAULT_FONT_SIZE, DEFAULT_LEADING
from pagebot.contexts.basecontext.babelstring import getFontPath, getLineHeight, BabelString
from pagebot.fonttoolbox.objects.font import Font
from pagebot.toolbox.units import upt
from pagebot.contexts.flatcontext.flattextline import FlatTextLine

NEWLINE = '<NEWLINE>'

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

        >>> from pagebot import getContext, getFontByName
        >>> from pagebot.toolbox.units import pt, em
        >>> context = getContext('Flat')
        >>> bungee = getFontByName('Bungee-Regular')
        >>> style = {'font': bungee, 'fontSize': pt(12), 'leading': em(1.5)}
        >>> fs = context.newString('ABC', style=style)
        >>> fs
        ABC
        >>> #fs.style
        #{'fallbackFont': 'Verdana', 'fontSize': 12, leading: em(1.5), 'fill': (0, 0, 0)}
        >>> fs.font.endswith('Bungee-Regular.ttf')
        True
        >>> fs.fontSize
        12
        >>> fs.leading
        1.5em
        >>> fs.lineHeight
        18.0
        >>> pt(fs.lineHeight)
        18pt
        >>> # TODO: add these for multiple style, i.e. fs.xHeight[-1]
        >>> fs.descender
        -1.68
        >>> fs.ascender
        10.32
        >>> fs.upem
        1000
        >>> fs.capHeight
        8.64
        >>> fs.xHeight
        6.0
        >>> from pagebot.toolbox.units import em
        >>> style = dict(font='Verdana', fontSize=pt(100), leading=em(1.4))
        >>> fs = context.newString('Example text', style=style)
        >>> from pagebot.contexts.basecontext.babelstring import BabelString
        >>> isinstance(fs, BabelString)
        True
        >>> fs2 = context.newString(' plus second text', style=style)
        >>> fs + fs2
        Example text plus second text
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
        self.data = []

        # Some checking, in case we get something else here.
        assert style is None or isinstance(style, dict)
        assert isinstance(s, str)

        if style is None:
            style = {}

        fontPath = getFontPath(style)

        # FIXME: should use s.lineHeight.
        fontSize = style.get('fontSize', DEFAULT_FONT_SIZE)
        leading = style.get('leading', DEFAULT_LEADING)
        lineHeight = getLineHeight(leading, fontSize)
        flatFont = context.b.font.open(fontPath)
        strike = context.b.strike(flatFont)
        color = BabelString.getColor(style)
        rgb = context.getFlatRGB(color)
        self._lines = []
        self._numberOfLines = 0

        parts = []

        if '\n' in s:
            #for c in s:
            #    print(c)
            parts = s.split('\n')
            s = parts[0]

        strike.color(rgb).size(fontSize, lineHeight, units=self.UNITS)

        # For each block of text, stores the plain string, the Flat `strike`
        # stylings and the Flat `text` (which is comparable to the DrawBot
        # FormattedString which in turn wraps a Cocoa NSAttributedString).
        self.data.append(dict(s=s, strike=strike, text=strike.text(s),
                style=style))
        self.previousStyle = style

        super().__init__(context)

        if len(parts) > 0:
            for part in parts[1:]:
                self.append(NEWLINE)
                self.append(part)


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
            part = d['s']
            if part == NEWLINE:
                s += '\n'
            else:
                s += part
        return s

    def _set_s(self, s, i=0, strike=None):
        d = self.data[i]
        if strike:
            d['dstrike'] = strike
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
        text = []

        # TODO: needs a ... operator.
        for d in self.data:
            text.append(d['text'])

        return text

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
        fontSize."""
        return getLineHeight(self.leading, self.fontSize)

    # Compatibility with DrawBot API.
    fontLineHeight = lineHeight = property(_get_lineHeight)

    def _get_descender(self):
        return self.getDescender(self.style)

    descender = property(_get_descender)

    def _get_ascender(self):
        return self.getAscender(self.style)

    ascender = property(_get_ascender)

    def _get_upem(self):
        return self.getUpem(self.style)

    upem = property(_get_upem)

    def _get_capHeight(self):
        return self.getCapHeight(self.style)

    capHeight = property(_get_capHeight)

    def _get_xHeight(self):
        return self.getXHeight(self.style)

    xHeight = property(_get_xHeight)

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

    def place(self, page, x, y):
        """Places the styled Flat text on a page.

        TODO: keep track of multiple text parts.
        """
        for d in self.data:
            s = d['s']
            if s == NEWLINE:
                continue
            text = d['text']
            strike =d['strike']
            w = strike.width(s)
            placedText = page.place(text)
            placedText.position(x, y)
            x += w

    def asText(self):
        """Answers as unicode string.

        >>> from pagebot import getContext
        >>> context = getContext('Flat')
        >>> fs = context.newString('ABC')
        >>> fs.asText()
        'ABC'
        """
        return self.s

    def getBounds(self, glyphName, location, parent):
        # NOTE: bounds are none in case of whitespace.
        # TODO: test.
        otfGlyph = self.getOTFGlyph(glyphName, location)
        pen = BoundsPen(parent)
        otfGlyph.draw(pen)
        return pen.bounds

    def textBox(self, page, box, align=LEFT):
        """Places text segments
        TODO: implement alignment.
        TODO: store fonts in context cache.

        #fontPath = getFontPath(style)
        #font = Font(fontPath)
        #upem = font.getUpem()
        #ascender = font.getAscender()
        #descender = font.getDescender()
        #descender = ((fontSize / float(upem)) * descender)

        >>> from pagebot import getContext
        >>> from pagebot.style import makeStyle
        >>> from pagebot.contributions.filibuster.blurb import Blurb
        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> context = getContext('Flat')
        >>> context.newPage(800, 600)
        >>> font = findFont('Roboto-Regular')
        >>> style = {'font': font, 'fontSize': 14}
        >>> style = makeStyle(style=style)
        >>> blurb = Blurb()
        >>> s = blurb.getBlurb('stylewars_bluray')
        >>> fs = context.newString(s, style=style)
        >>> r = (10, 262, 400, 313)
        >>> of = fs.textBox(context.page, r)
        >>> of.startswith('fortune, we engaged Chris Woods who did the digital restoration')
        True
        """
        x0, y0, w0, h0 = box
        x0 = round(x0)
        y0 = round(y0)
        w0 = round(w0)
        h0 = round(h0)

        fontSize0 = upt(self.style.get('fontSize', DEFAULT_FONT_SIZE))
        lineHeight0 = upt(self.style.get('leading', DEFAULT_LEADING), base=fontSize0)
        dl0 = lineHeight0 - fontSize0
        descender0 = self.getDescender(self.style)

        assert h0 >= lineHeight0

        x = x0
        y = self.context.height - y0 - h0 + dl0
        w = w0
        h = round(lineHeight0)
        h1 = round(lineHeight0)
        overflow = ''
        baseline = h1 + descender0

        for i, d in enumerate(self.data):
            s = d['s']

            if s == NEWLINE:
                x = x0
                w = w0
                y += h1
                continue

            text = d['text']
            style = d['style']
            fontSize = upt(style.get('fontSize', DEFAULT_FONT_SIZE))
            lineHeight = upt(style.get('leading', DEFAULT_LEADING), base=fontSize)
            h1 = round(lineHeight)

            strike = d['strike']
            w1 = strike.width(s)
            descender = self.getDescender(style)


            placedText = page.place(text)
            s0 = s

            if h > h0:
                s1 = self.getPlacedString(placedText)
                overflow += self.getDiff(s0, s1)
                break

            # Debugging. If line height / h1 too small, text won't show because
            # the placed text frame is too low.
            #print(h1)
            #print(lineHeight)
            #assert h1 >= lineHeight
            placedText.frame(x, y, w, h1)
            self.addToLines(x, baseline, placedText)

            # Overflow, looks up difference and creates a new strike until
            # there's no more overflow or the textbox is too small.
            while placedText.overflow():
                x = x0
                y += h1
                h += h1
                w = w0

                if h > h0:
                    s1 = self.getPlacedString(placedText)
                    overflow += self.getDiff(s0, s1)
                    break

                s1 = self.getPlacedString(placedText)
                diff = self.getDiff(s0, s1)
                text = strike.text(diff)
                w1 = strike.width(diff)
                placedText = page.place(text)
                s0 = diff
                baseline += h1
                placedText.frame(x, y, w, h1)
                self.addToLines(x, baseline, placedText)

                if not placedText.overflow():
                    break

            x += w1
            w -= w1

        # TODO: calculate overflow for all textparts.
        return overflow

    def addToLines(self, x, y, placedText):
        for line in self._lines:
            if y == line.y:
                line.append(placedText)
                return

        line = FlatTextLine(self._numberOfLines, x, y, placedText)
        self._lines.append(line)
        self._numberOfLines += 1

    def getDiff(self, s0, s1):
        assert len(s1) <= len(s0)
        diff0, diff1 = self.getTextDiff(s1, s0)
        return diff0

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

    def textSize(self, w=None, h=None):
        """Answers the `(w, h)` size tuple for a given width, with the current
        text.

        >>> from pagebot import getContext
        >>> context = getContext('Flat')
        >>> style = dict(font='Roboto-Regular', fontSize=12)
        >>> fs = context.newString('ABC', style=style)
        >>> fs
        ABC
        >>> size = fs.textSize()
        >>> size
        (23.115, 16.8)
        """
        w = self.strike.width(self.s)
        h = self.lineHeight
        w = round(w, ndigits=3)
        h = round(h, ndigits=3)
        return w, h

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

        # If a plain string is appended, creates a new string with the previous
        # style.

        if s == '':
            return
        if s == NEWLINE:
            data = dict(s=NEWLINE)
            self.data.append(data)
            return
        if isinstance(s, str):
            fs = self.context.newString(s, style=self.previousStyle)
        else:
            fs = s

        # Now adds it to data list.
        self.data.extend(fs.data)


    def getStyleByIndex(self, index):
        """Should return style at data index.


        for example:

            ...

        """

    def getStyleAtIndex(self, index):
        """
        Returns style at character index.

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

    #

    def appendMarker(self, markerId, arg):
        """Append an invisible marker string."""

    def findMarkers(self, reCompiled=None):
        """Answers a dictionary of markers with their arguments in self.s."""
        if reCompiled is None:
            reCompiled= self.FIND_FS_MARKERS
        return reCompiled.findall(u'%s' % self.s)

    # Fonts.

    def getFont(self, style):
        # TODO: store fonts in context cache.
        fontPath = getFontPath(style)
        return Font(fontPath)

    def getDescender(self, style):
        font = self.getFont(style)
        upem = font.getUpem()
        fontSize = upt(style.get('fontSize', DEFAULT_FONT_SIZE))
        descender = font.getDescender()
        return (fontSize / float(upem)) * descender

    def getAscender(self, style):
        font = self.getFont(style)
        upem = font.getUpem()
        fontSize = upt(style.get('fontSize', DEFAULT_FONT_SIZE))
        ascender = font.getAscender()
        return (fontSize / float(upem)) * ascender

    def getUpem(self, style):
        font = self.getFont(style)
        return font.getUpem()

    def getCapHeight(self, style):
        font = self.getFont(style)
        upem = font.getUpem()
        fontSize = upt(style.get('fontSize', DEFAULT_FONT_SIZE))
        capHeight = font.getCapHeight()
        return (fontSize / float(upem)) * capHeight

    def getXHeight(self, style):
        font = self.getFont(style)
        upem = font.getUpem()
        fontSize = upt(style.get('fontSize', DEFAULT_FONT_SIZE))
        xHeight = font.getXHeight()
        return (fontSize / float(upem)) * xHeight

    #

    def getTextLines(self, w, h=None, align=LEFT):
        page = self.context.getTmpPage(w, h)
        box = (0, 0, w, h)
        tb = self.textBox(page, box, align=align)
        return self._lines

    @classmethod
    def newString(cls, s, context, e=None, style=None, w=None, h=None, **kwargs):
        """Answers a FlatString instance from valid attributes in *style*. Sets
        all values after testing their existence so they can inherit from
        previous style formats. If target width *w* or height *h* is defined,
        then *fontSize* is scaled to make the string fit *w* or *h*.

        * FIXME: implement pixelFit for Flat.
        * TODO: implement GSUB feature compile in Flat; make the transformed
        string using Tal's Compositor::

            https://github.com/typesupply/compositor

        >>> from pagebot.toolbox.units import pt
        >>> from pagebot import getContext
        >>> context = getContext('Flat')
        >>> bs = context.newString('AAA', style=dict(fontSize=pt(30)))
        >>> str(bs) == 'AAA'
        True
        """
        assert isinstance(s, str)

        if style is None:
            style = {}
        else:
            assert isinstance(style, dict)

        s = cls.addCaseToString(s, e, style)
        style = cls.getStringAttributes(s, e=e, style=style, w=w, h=h)
        return cls(s, context=context, style=style)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
