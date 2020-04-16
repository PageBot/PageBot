#!/usr/bin/env python3 # -*- coding: UTF-8 -*-
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
#     pagebotstring.py
#
#     PageBotString is an intermediate conversion string format that the
#     various context string classes should be able to convert from and to by
#     implementing context.fromPageBotString and context.asPageBotString.
#

from pagebot.contexts.basecontext.babelstring import BabelString
from pagebot.constants import LEFT

class PageBotRun:
    def __init__(self, s, style=None):
        self.s = s
        self.style = style

    def __repr__(self):
        s = self.s[:10]
        if s != self.s:
            s += '...'
        return '<%s %s>' % (self.__class__.__name__, s)

class PageBotString(BabelString):
    """PageBotString is the generic intermediate string, that can be used
    for other context string classes to convert to and from.

    >>> pbs = PageBotString('ABCD', style=dict(fontSize=12))
    >>> pbs.runs
    [<PageBotRun ABCD>]
    >>> pbs2 = PageBotString('EFGH', style=dict(fontSize=16))
    >>> pbs3 = pbs + pbs2
    >>> pbs3
    ABCDEFGH
    >>> pbs3 is pbs
    True
    >>> pbs3.runs
    [<PageBotRun ABCD>, <PageBotRun EFGH>]
    """
    def __init__(self, s, context=None, style=None):
        """Constructor of PageBotString. @s is a plain string, style is a
        dictionary compatible with the document root style keys."""
        self.runs = [PageBotRun(s, style)]
        self.context = context
        super().__init__(context)

    def __add__(self, pbs):
        """If pbs is a plain string, then just add it to the last run."""
        if isinstance(pbs, str):
            self.runs[-1].s += pbs
        elif isinstance(pbs, PageBotString):
            for run in pbs.runs:
                self.runs.append(run)
        else:
            raise ValueError("@pbs much be string or other %s" % self.__class__.__name__)
        return self

    def _get_s(self):
        s = []
        for run in self.runs:
            s.append(run.s)
        return ''.join(s)

    def _set_s(self, s):
        if self.runs:
            style = self.runs[-1].style
        else:
            style = None

        self.runs = [PageBotRun(s, style)]

    s = property(_get_s, _set_s)

    def _get_style(self):
        if self.runs:
            return self.runs[-1].style
        return None

    style = property(_get_style)

    def getStyleAtIndex(self, index):
        # TODO: to be implemented.
        pass

    def getTextLines(self, w, h=None, align=LEFT):
        # TODO: to be implemented.
        pass

    def asPageBotString(self):
        """Construct a formatted PageBotString.newString() from self. Since
        self is already a PageBotString, answer self"""
        return self

    @classmethod
    def newString(cls, s, context=None, e=None, style=None, w=None, h=None,
            pixelFit=True):
        """Answer a new PageBotString instance.

        >>> from pagebot.toolbox.units import pt
        >>> pbs = PageBotString.newString('ABCD', style=dict(fontSize=pt(14)))
        >>> pbs
        ABCD
        >>> pbs.runs
        [<PageBotRun ABCD>]
        >>> pbs.runs[0].s
        'ABCD'
        >>> pbs.runs[0].style
        {'fontSize': 14pt}
        """
        return cls(s, style=style)

    @classmethod
    def fromPageBotString(cls, pbs):
        """Construct a formatted cls.newString() from PageBotString instance.
        Since pbs is already a PageBotString, answer it unchanged."""
        assert isinstance(pbs, PageBotString)
        return pbs

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
