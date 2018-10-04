#!/usr/bin/env python
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     04_Units.py

from pagebot.toolbox.units import Unit, mm, px, pt, fr, em, perc, col, units

def useUnits():
    """
    >>> mm(2), mm(2).rv # Showing the unit as instance and as rendered value
    (2mm, 2)
    >>> px(5), px(5).rv
    (5px, 5)
    >>> px(5), pt(5).rv
    (5px, 5)
    >>> fr(8, base=400), fr(8, base=400).rv # Fractional units, used in CSS-grid.
    (8fr, 50)
    >>> em(12, base=10), em(12, base=10).rv
    (12em, 120)
    >>> perc(12.5, base=400), perc(12.5, base=400).rv
    (12.5%, 50)
    >>> u = col(1/4, base=mm(200), g=mm(4))
    >>> u, u.rv
    (0.25col, 47mm)
    """
    print(mm(2))
    # Real value:
    print(mm(2).rv)
    print(px(5))
    print(px(5).rv)
    # TODO: etc...

useUnits()
