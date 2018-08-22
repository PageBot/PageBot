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
from __future__ import division # Make integer division result in float.

#from pagebot.constants import MM
from pagebot.toolbox.units import Unit, mm, px, pt, fr, em, perc, col, units

# FIXME: visible example.
def useUnits():
    """
    >>> mm(2), pt(mm(2)) # Showing the unit as instance and as rendered value
    (2mm, 5.67pt)
    >>> px(5), pt(5)
    (5px, 5pt)
    >>> px(5), pt(5)
    (5px, 5pt)
    >>> fr(8, base=400), pt(fr(8, base=400)) # Fractional units, used in CSS-grid.
    (8fr, 50pt)
    >>> em(12, base=10), pt(em(12, base=10))
    (12em, 120pt)
    >>> perc(12.5, base=400), pt(perc(12.5, base=400))
    (12.5%, 50pt)
    >>> u = col(1/4, base=mm(200), g=mm(4))
    >>> u, pt(u)
    (0.25col, 141.73pt)
    """

if __name__ == '__main__':
    import doctest
    doctest.testmod()
