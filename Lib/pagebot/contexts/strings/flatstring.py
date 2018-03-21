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
#     http://xxyxyz.org/flat

from pagebot.contexts.platform import getFontPathOfFont
from pagebot.contexts.strings.babelstring import BabelString
from pagebot.style import css, LEFT

class FlatString(BabelString):

    BABEL_STRING_TYPE = 'flat'
    DEFAULT_FONT = getFontPathOfFont('Roboto-Regular') # Part of PageBot, we can assume it is there.
    DEFAULT_FONTSIZE = 12
    DEFAULT_LEADING = 0

    u"""FlatString is a wrapper around the Flat string."""

    def _get_s(self):
        u"""Answer the embedded Flat equivalent of a OSX FormattedString by property, to enforce checking type of the string."""
        return self._s
    def _set_s(self, s):
        if isinstance(s, basestring):
            s = s # TODO: Change to Flat equivalent of FormattedString.
        self._s = s
    s = property(_get_s, _set_s)

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

    @classmethod
    def newString(cls, s, context, e=None, style=None, w=None, h=None, pixelFit=True):
        u"""Answer a FlatString instance from valid attributes in *style*. Set all values after testing
        their existence, so they can inherit from previous style formats.
        If target width *w* or height *h* is defined, then *fontSize* is scaled to make the string fit *w* or *h*.

        >>> from pagebot.contexts.flatcontext import FlatContext
        >>> context = FlatContext()
        >>> bs = FlatString.newString('AAA', context, style=dict(font='Verdana', fontSize=30))
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

        fontPath = getFontPathOfFont(style.get('font'))
        if fontPath is None:
            fontPath = getFontPathOfFont(cls.DEFAULT_FONT)
        try:
            font = context.b.font.open(fontPath)
        except (ValueError, TypeError):
            fontPath = getFontPathOfFont(cls.DEFAULT_FONT)
            if fontPath is not None:
                font = context.b.font.open(fontPath)
        strike = context.b.strike(font)
        strike.size(style.get('fontSize', cls.DEFAULT_FONTSIZE),
            style.get('leading', cls.DEFAULT_LEADING), units='pt')
        #if w is not None:
        #    strike.width = w
        return cls(strike.text(s), context) # Make real Flat flavor BabelString here.


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
