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
from pagebot.toolbox.units import pt

class BabelString:
    """BabelString is the base class of various types of (formatted) string
    representations needed for different builder classes."""

    def __init__(self, s, context, style=None):
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

    def append(self, s):
        """Appends string or FlatString to self."""
        try:
            self.s += s.s
        except (TypeError, AttributeError):
            self.s += s # Convert to babel string, whatever it is.

    def _get_type(self):
        """Answers the ID of the class, in case a caller wants to know what
        kind of BabelString this is."""
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

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
