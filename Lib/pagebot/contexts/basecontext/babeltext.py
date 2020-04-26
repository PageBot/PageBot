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
#     babeltext.py
#
#     BabelText is BabelLines, after rendering returned by a context from 
#     context.textLines()
#     It can be used by PageBot to probe rendered text attributes, but 
#     BabelLines contain elements (such as DrawBot FormattedString) that 
#     belong specific to one type of context, so cached drawing can be done from it.
#     BabelText/BabelLine are typically offering a standard API for PageBot.
#
import weakref

class BabelLine:
    def __init__(self, bs, x, y, cl, context):
        """Holds an estimated reconstruction of the line as BabelString, with
        reconstructed styles, so the caller can check on font, size, color, etc.
        Note that the reconstructed BabelString cannot be used again as text
        string, as feature replacements and glyphs without unicode are not represented.
        """
        self.bs = bs
        self.x = x
        self.y = y
        self.cl = cl # Storage of native context line, e.g. CTLine for DrawBotContext
        self.context = context

    def __repr__(self):
        s = '<%s %s x=%s y=%s' % (self.__class__.__name__, self.bs, self.x, self.y)
        if self.context is not None:
            s += ' '
            if self.cl is not None:
                s += '*' # Subtle mark that there is a native line stored
            s += '%s' % self.context.__class__.__name__
        return s + '>'

class BabelText:
    """BabelText is the result of a context.textlines() rendered BabelString.

    """
    def __init__(self, bs, w, h, ct, context):
        self.bs = bs # Holding the original BabelString of this render.
        self.w = w # Render width of the text column
        self.h = h
        self.lines = []
        self.ct = ct # Context native object that can draw the text column.
        self.context = context

    def _get_bs(self):
        return self._bs
    def _set_bs(self, bs):
        self._bs = bs
        self.lines = []
    bs = property(_get_bs, _set_bs)

    def _get_context(self):
        if self._context is not None:
            return self._context()
        return None
    def _set_context(self, context):
        self._context = weakref.ref(context)
        self.lines = []
    context = property(_get_context, _set_context)

    def __getitem__(self, index):
        return self.lines[index]

    def __len__(self):
        return len(self.lines)

    def __repr__(self):
        return '<%s %s w=%d lines=%d>' % (self.__class__.__name__, self.bs, self.w, len(self.lines))

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
