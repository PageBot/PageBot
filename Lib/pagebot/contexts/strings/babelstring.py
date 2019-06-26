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

class BabelString:
    """BabelString is the base class of all types of (formatted) string
    representations needed for the builder classes.

    TODO: add abstract functions for proper inheritance.
    >>> from pagebot import getContext
    >>> context = getContext()
    """

    """
    >>> bla = context.newString('bla')
    >>> from pagebot.contexts.strings.drawbotstring import DrawBotString
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
        # Wraps the native string.
        # Encloses the Flat/Drawbot/html string in this wrapper.
        self.s = s

        # Some checking, in case we get something else here.
        assert style is None or isinstance(style, dict)
        self.style = style # Optional style to set the context parameters.
        self.context = context

    def __repr__(self):
        return u'%s' % self.s

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
        """Answer a copy of self with sliced string or with single indexed character.

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
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

        FIXME: doesn't this mess with object inheritance?

        """
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
        """Allow the string to set itself to firstLineIndex = firstColumnIndent
        if that makes sense for inheriting BabelString classes. Default is just to answer self.
        """
        return self

    def getStyleAtIndex(self, index):
        """Answer the constructed style of the string a position index of chars.
        """
        return {}

    @classmethod
    def newString(cls, s, context, e=None, style=None, w=None, h=None,
            pixelFit=True):
        return None


    #def textSize(self, w=None, h=None):
    #def _get_fontSize(self):
    #def _set_fontSize(self, fontSize):
    #def asText(self):
    #def bounds(self, language=None, hyphenation=None):
    #def fill(self, r, g=None, b=None, a=None, alpha=None):
    #def cmykFill(self, c, m=None, y=None, k=None, a=None, alpha=None):
    #def stroke(self, r, g=None, b=None, a=None, alpha=None):
    #def setStrokeWidth(self, w):
    #def getTextLines(self, w, h=None, align=LEFT):
    #def _get_size(self):

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
