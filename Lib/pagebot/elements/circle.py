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
#     circle.py
#


from pagebot.constants import MIDDLE, CENTER, ORIGIN
from pagebot.elements.oval import Oval


class Circle(Oval):

    def __init__(self, r=None, x=None, y=None, w=None, h=None, xAlign=None,
            yAlign=None, **kwargs):
        """Draws the circle in the current context. The default alignment of
        the circle is on its middle point (CENTER, MIDDLE). That makes it
        different from the Oval, which aligns default to bottom-left.

        >>> from pagebot.toolbox.units import pt
        >>> e = Circle(r=pt(30))
        >>> e.xy, e.size
        ((0pt, 0pt), (60pt, 60pt))
        >>> e.box, e.top, e.right, e.bottom, e.left
        ((0pt, 0pt, 60pt, 60pt), 30pt, 30pt, -30pt, -30pt)
        """
        if r is not None:
            w = h = 2*r
        if x is None:
            x = ORIGIN[0]
        if y is None:
            y = ORIGIN[1]
        Oval.__init__(self, x=x, y=y, w=w, h=h,
            xAlign=xAlign or CENTER, yAlign=yAlign or MIDDLE, **kwargs)

    def _get_h(self):
        """Answers the height of the element (same as self.w)."""
        return self.w

    def _set_h(self, r):
        self.w = r

    h = property(_get_h, _set_h)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
