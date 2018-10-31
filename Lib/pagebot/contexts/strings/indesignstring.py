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
#     Supporting Indesign, xxyxyz.org/indesign
# -----------------------------------------------------------------------------
#
#     indesignstring.py
#

import os
import re

from pagebot.contexts.strings.babelstring import BabelString
from pagebot.style import css
from pagebot.constants import LEFT, DEFAULT_FONT_SIZE, DEFAULT_LEADING
from pagebot.paths import DEFAULT_FONT_PATH
from pagebot.toolbox.units import isUnit
from pagebot.fonttoolbox.objects.font import findFont

class InDesignString(BabelString):

    BABEL_STRING_TYPE = 'indesign'

    """InDesignString is a wrapper around the Indesign string."""
    def __init__(self, s, context, style=None):
        """Constructor of the DrawBotString, wrapper around
        DrawBot.FormattedString. Optionally store the (latest) style that was
        used to produce the formatted string.

        >>> from pagebot.contexts.indesigncontext import InDesignContext
        >>> context = InDesignContext()
        >>> bs = context.newString('ABC')
        >>> #bs
        ABC
        """
        self.context = context # Store context, in case we need more of its functions.
        self.s = s # Store the Indesign equivalent of the DrawBot FormattedString.
        # In case defined, store current status here as property and set the current FormattedString
        # for future additions. Also the answered metrics will not be based on these values.
        if style is None:
            style = {}
        self.style = style
        super().__init__(s, context, style=style)

    def _get_s(self):
        """Answers the embedded Indesign equivalent of a OSX FormattedString by
        property, to enforce checking type of the string."""
        return self._s

    def _set_s(self, s):
        if isinstance(s, str):
            s = s # TODO: Change to Indesign equivalent of FormattedString.
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

    def __len__(self):
        """Answers the number of characters in self.s

        >>> from pagebot.contexts.indesigncontext import InDesignContext
        >>> context = InDesignContext()
        >>> fs = InDesignString('ABC', context)
        >>> fs
        ABC
        >>> len(fs)
        3
        """
        return len(str(self.s))

    def asText(self):
        """Answers as unicode string.

        >>> from pagebot.contexts.indesigncontext import InDesignContext
        >>> context = InDesignContext()
        >>> fs = InDesignString('ABC', context)
        >>> fs.s
        'ABC'
        >>> fs.asText()
        'ABC'
        """
        return str(self.s) # TODO: To be changed to Indesign string behavior.

    def textSize(self, w=None, h=None):
        """Answers the (w, h) size for a given width, with the current text."""
        return 100, 20
        # TODO: Make this work in Indesign same as in DrawBot
        #return self.b.textSize(s)

    def textOverflow(self, w, h, align=LEFT):
        # TODO: Make this work in Indesign same as in DrawBot
        # TODO: Some stuff needs to get here.
        return ''

    def append(self, s):
        """Append string or InDesignString to self."""
        # TODO: Make this to work.
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
        """Answers a InDesignString instance from valid attributes in *style*.
        Set all values after testing their existence, so they can inherit from
        previous style formats. If target width *w* or height *h* is defined,
        then *fontSize* is scaled to make the string fit *w* or *h*.

        >>> from pagebot.toolbox.units import pt
        >>> from pagebot.contexts.indesigncontext import InDesignContext
        >>> context = InDesignContext()
        >>> bs = InDesignString.newString('AAA', context, style=dict(fontSize=pt(30)))
        >>> #bs.s.lines()
        >>> #'indesign.text.text' in str(bs)
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

        # Since Indesign does not do font GSUB feature compile, we'll make the transformed string here,
        # using Tal's https://github.com/typesupply/compositor
        # This needs to be installed, in case PageBot is running outside of DrawBot.

        font = style.get('font')
        if font is not None and not isinstance(font, str):
            font = font.path
        if font is None or not os.path.exists(font):
            font = DEFAULT_FONT_PATH
        fontSize = style.get('fontSize', DEFAULT_FONT_SIZE)
        assert isUnit(fontSize), ('%s.newString: FontSize %s must be of type Unit' % (cls.__name__, fontSize))
        leading = style.get('leading', DEFAULT_LEADING)
        assert isUnit(leading), ('%s.newString: Leading %s must be of type Unit' % (cls.__name__, leading))
        inDesignFont = findFont(font)
        #strike = context.b.strike(indesignFont)
        #strike.size(fontSize.pt, leading.pt, units='pt')
        #if w is not None:
        #    strike.width = w
        #s = strike.text(s)
        s = ''
        return cls(s, context=context, style=style) # Make real Indesign flavor BabelString here.


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
