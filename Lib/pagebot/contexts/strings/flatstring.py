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
#     flatstring.py
#
#     https://github.com/xxyxyz/flat
#     http://xxyxyz.org/flat

import os
import re

from pagebot.contexts.strings.babelstring import BabelString
from pagebot.style import css, LEFT, DEFAULT_FONT_SIZE, DEFAULT_FONT_PATH, DEFAULT_LEADING

class FlatString(BabelString):

    BABEL_STRING_TYPE = 'flat'

    u"""FlatString is a wrapper around the Flat string."""
    def __init__(self, s, context, style=None):
        u"""Constructor of the DrawBotString, wrapper around DrawBot.FormattedString.
        Optionally store the (latest) style that was used to produce the formatted string.

        >>> from pagebot.contexts.flatcontext import FlatContext
        >>> context = FlatContext()
        >>> context.isFlat
        True
        >>> bs = context.newString('ABC')
        >>> #bs
        ABC
        """
        self.context = context # Store context, in case we need more of its functions.
        self.s = s # Store the Flat equivalent of the DrawBot FormattedString.
        # In case defined, store current status here as property and set the current FormattedString
        # for future additions. Also the answered metrics will not be based on these values.
        if style is None:
            style = {}
        self.style = style

    def _get_s(self):
        u"""Answer the embedded Flat equivalent of a OSX FormattedString by property, to enforce 
        checking type of the string."""
        return self._s
    def _set_s(self, s):
        if isinstance(s, str):
            s = s # TODO: Change to Flat equivalent of FormattedString.
        self._s = s
    s = property(_get_s, _set_s)

    def _get_font(self):
        u"""Answer the current state of fontName."""
        return self.style.get('font') 
    def _set_font(self, fontName):
        if fontName is not None:
            self.context.font(fontName)
        self.style['font'] = fontName
    font = property(_get_font, _set_font)

    def _get_fontSize(self):
        u"""Answer the current state of the fontSize."""
        return self.style.get('fontSize')
    def _set_fontSize(self, fontSize):
        if fontSize is not None:
            self.context.font(fontSize)
        self.style['fontSize'] = fontSize
    fontSize = property(_get_fontSize, _set_fontSize)

    def __len__(self):
        u"""Answer the number of characters in self.s

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
        u"""Answer as unicode string.

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
        u"""Answer the (w, h) size for a given width, with the current text."""
        return 100, 20
        # TODO: Make this work in Flat same as in DrawBot
        #return self.b.textSize(s)

    def textOverflow(self, w, h, align=LEFT):
        # TODO: Make this work in Flat same as in DrawBot
        # TODO: Some stuff needs to get here.
        return ''

    def append(self, s):
        u"""Append string or FlatString to self."""
        # TODO: Make this to work.
        #try:
        #    self.s += s.s
        #except TypeError:
        #    self.s += repr(s) # Convert to babel string, whatever it is.

    MARKER_PATTERN = '==%s@%s=='
    FIND_FS_MARKERS = re.compile('\=\=([a-zA-Z0-9_\:\.]*)\@([^=]*)\=\=')

    def appendMarker(self, markerId, arg):
        u"""Append an invisible marker string."""

    def findMarkers(self, reCompiled=None):
        u"""Answer a dictionary of markers with their arguments in self.s."""
        if reCompiled is None:
            reCompiled= self.FIND_FS_MARKERS
        return reCompiled.findall(u'%s' % self.s)


    @classmethod
    def newString(cls, s, context, e=None, style=None, w=None, h=None, pixelFit=True):
        u"""Answer a FlatString instance from valid attributes in *style*. Set all values after testing
        their existence, so they can inherit from previous style formats.
        If target width *w* or height *h* is defined, then *fontSize* is scaled to make the string fit *w* or *h*.

        >>> from pagebot.toolbox.units import pt
        >>> from pagebot.contexts.flatcontext import FlatContext
        >>> context = FlatContext()
        >>> bs = FlatString.newString('AAA', context, style=dict(fontSize=pt(30)))
        >>> #bs.s.lines()
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

        # Since Flat does not do font GSUB feature compile, we'll make the transformed string here,
        # using Tal's https://github.com/typesupply/compositor
        # This needs to be installed, in case PageBot is running outside of DrawBot.

        font = style.get('font')
        if font is not None and not isinstance(font, str):
            font = font.path
        if font is None or not os.path.exists(font):
            font = DEFAULT_FONT_PATH
        flatFont = context.b.font.open(font)
        strike = context.b.strike(flatFont)
        strike.size(style.get('fontSize', DEFAULT_FONT_SIZE).r,
            style.get('leading', DEFAULT_LEADING).r, units='pt')
        #if w is not None:
        #    strike.width = w
        return cls(strike.text(s), context=context, style=style) # Make real Flat flavor BabelString here.


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
