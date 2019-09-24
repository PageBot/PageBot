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
from copy import copy
from pagebot.toolbox.units import pt
from pagebot.constants import LEFT, DEFAULT_LANGUAGE, DEFAULT_FONT_SIZE

class BabelString:
    """BabelString is the base class of all types of (formatted) string
    representations needed for the builder classes.

    TODO: add abstract functions for proper inheritance.
    TODO: add Flat class tests.
    >>> from pagebot import getContext
    >>> context = getContext()
    """

    """
    >>> bla = context.newString('bla')
    >>> from drawBotContext.string import DrawBotString
    >>> isinstance(bla, DrawBotString)
    True
    >>> type(bla)
    DrawBotString
    >>> isinstance(bla, BabelString)
    True
    >>> import inspect
    >>> inspect.getmro(DrawBotString)
    """

    def __init__(self, s, context, style=None):
        # Wraps the native string. Encloses the Flat, Drawbot or HTML string
        # in this wrapper.
        self.s = s

        # Some checking, in case we get something else here.
        assert style is None or isinstance(style, dict)

        # Optional style to set the context parameters. In case defined, store
        # current status here as property and set the current FormattedString
        # for future additions. Also the answered metrics will not be based on
        # these values.
        if style is None:
            style = {}

        self.style = style

        self.context = context
        self.language = DEFAULT_LANGUAGE
        self.hyphenation = False

        # Filled in case w or h are defined and depending if the font is a
        # variable font. Set to fitting font size, in case the size iterates
        # to find width.
        self.fittingFontSize = pt(0)
        # In case we are sampling with a Variable Font.
        self.fittingFont = None
        self.fittingLocation = None
        self.isFitting = False

    def __repr__(self):
        return '%s' % self.s

    def __add__(self, s):
        self.append(s)
        return self

    def __mul__(self, d):
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

        >>> from pagebotcocoa.contexts.drawbot.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> context.newString('blablabla')[2:]
        ablabla
        >>> context.newString('blablabla')[5]
        a
        """
        if isinstance(given, slice):
            bs = copy(self)
            bs.s = bs.s[given.start:given.stop]
            return bs
        if isinstance(given, (list, tuple)):
            return self # Untouched
        # Must be a single index
        bs = copy(self)
        bs.s = bs.s[given]
        return bs

    def append(self, s):
        """Appends string or BabelString to self."""
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
        else:
            return pt(0, 0)

    size = property(_get_size)

    def columnStart(self, firstColumnIndent):
        """Allows the string to set itself to firstLineIndex = firstColumnIndent
        if that makes sense for inheriting BabelString classes. Default is just
        to answer self."""
        return self

    def getStyleAtIndex(self, index):
        """Answer the constructed style of the string a position index of chars.
        """
        return {}

    @classmethod
    def newString(cls, s, context, e=None, style=None, w=None, h=None,
            pixelFit=True):
        raise NotImplementedError
        #return None

    def _get_fontSize(self):
        return self.style.get('fontSize', DEFAULT_FONT_SIZE)

    def _set_fontSize(self, fontSize):
        self.b.fontSize(fontSize)
        self.style['fontSize'] = fontSize

    fontSize = property(_get_fontSize, _set_fontSize)

    # To be implemented:
    #def texzetSize(self, w=None, h=None):
    #def asText(self):
    #def bounds(self, language=None, hyphenation=None):
    #def fill(self, r, g=None, b=None, a=None, alpha=None):
    #def cmykFill(self, c, m=None, y=None, k=None, a=None, alpha=None):
    #def stroke(self, r, g=None, b=None, a=None, alpha=None):
    #def setStrokeWidth(self, w):

    def getTextLines(self, w, h=None, align=LEFT):
        raise NotImplementedError

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
