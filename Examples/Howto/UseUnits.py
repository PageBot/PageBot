#!/usr/bin/env python
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
from pagebot.constants import INCH, MM
from pagebot.toolbox.units import Unit, mm, px, pt, fr, em, perc

def useUnits():
    u"""

    >>> mm(2), mm(2)._v # Unified to pt value stored in _v
    (2mm, 2)
    >>> px(5), px(5)._v
    (5px, 5)
    >>> px(5), pt(5)._v
    (5px, 5)
    >>> fr(8), fr(8)._v # Fractional units, used in CSS-grid. 
    (8fr, 8)
    >>> em(12), em(12)._v
    (12em, 12)
    >>> perc(12.5), perc(12.5)._v
    (12.50%, 12.5)
    """

if __name__ == '__main__':
    import doctest
    doctest.testmod()
