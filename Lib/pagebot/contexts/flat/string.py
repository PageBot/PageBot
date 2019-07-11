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

from pagebot.contexts.strings.babelstring import BabelString
from pagebot.style import css
from pagebot.constants import LEFT, DEFAULT_FONT_SIZE, DEFAULT_LEADING
from pagebot.paths import DEFAULT_FONT_PATH
from pagebot.toolbox.units import upt
from pagebot.toolbox.color import Color

DEFAULT_COLOR = Color(0, 0, 0)

class FlatString(BabelString):
    """FlatString is a wrapper around the Flat string."""

    BABEL_STRING_TYPE = 'flat'
    UNITS = 'pt'

    def __init__(self, s, context, style=None):
        """Constructor of the DrawBotString, which is a wrapper around
        DrawBot.FormattedString. Optionally stores the (latest) style that was
        used to produce the formatted string.

        >>> from pagebot.contexts.flatcontext import FlatContext
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
        #s = ''

        #for  p in self.s.paragraphs:
        #    for span in p.spans:
        #        s += span.string

        return str(self.s)

    def _get_s(self):
        """Answers the embedded Flat equivalent of a OS X FormattedString by
        property to enforce checking type of the string."""
        return self._s

    def _set_s(self, s):
        if isinstance(s, str):
            s = s # TODO: Change to Flat equivalent of FormattedString.
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
        return self.style.get('fontSize')

    def _set_fontSize(self, fontSize):
        if fontSize is not None:
            self.context.font(fontSize)
        self.style['fontSize'] = fontSize

    fontSize = property(_get_fontSize, _set_fontSize)

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

        >>> from pagebot.contexts.flatcontext import FlatContext
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

        >>> from pagebot.contexts.flatcontext import FlatContext
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
    def newString(cls, s, context, e=None, style=None, w=None, h=None, pixelFit=True):
        """Answers a FlatString instance from valid attributes in *style*. Set
        all values after testing their existence, so they can inherit from
        previous style formats. If target width *w* or height *h* is defined,
        then *fontSize* is scaled to make the string fit *w* or *h*.

        >>> from pagebot.toolbox.units import pt
        >>> from pagebot.contexts.flatcontext import FlatContext
        >>> context = FlatContext()
        >>> bs = FlatString.newString('AAA', context, style=dict(fontSize=pt(30)))
        >>> #bs.s.lines()
        >>> 'flat.text.text' in str(bs)
        True
        """
        if style is None:
            style = {}

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
            font = DEFAULT_FONT_PATH

        fontSizePt = upt(style.get('fontSize', DEFAULT_FONT_SIZE))
        leadingPt = upt(style.get('leading', DEFAULT_LEADING), base=fontSizePt)
        flatFont = context.b.font.open(font)
        strike = context.b.strike(flatFont)
        c = style.get('color', DEFAULT_COLOR)
        assert isinstance(c, Color)
        rgb = context.getFlatRGB(c)
        strike.color(rgb).size(fontSizePt, leadingPt, units=cls.UNITS)

        # FIXME
        #if w is not None:
        #    strike.width = w

        return cls(strike.text(s), context=context, style=style)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
