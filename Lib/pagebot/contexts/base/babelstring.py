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
from pagebot.toolbox.units import pt, RelativeUnit, Unit
from pagebot.constants import LEFT, DEFAULT_LANGUAGE, DEFAULT_FONT_SIZE

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
    (<class 'pagebot.contexts.flatcontext.flatstring.FlatString'>, <class 'pagebot.contexts.base.babelstring.BabelString'>, <class 'object'>)
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

    @classmethod
    def newString(cls, s, context, e=None, style=None, w=None, h=None,
            pixelFit=True):
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

    def getLineHeight(self):
        # FIXME: get from style instead? see FlatString.

        if isinstance(self.leading, RelativeUnit):
            textHeight = self.leading.byBase(self.fontSize)

        elif isinstance(self.leading, Unit):
            textHeight = self.leading.pt
        else:
            # Leading is scalar?
            textHeight = self.leading * self.fontSize.pt

        return textHeight

    # To be implemented:
    #def textSize(self, w=None, h=None):
    #def asText(self):
    #def bounds(self, language=None, hyphenation=None):
    #def fill(self, r, g=None, b=None, a=None, alpha=None):
    #def cmykFill(self, c, m=None, y=None, k=None, a=None, alpha=None):
    #def stroke(self, r, g=None, b=None, a=None, alpha=None):
    #def setStrokeWidth(self, w):

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
