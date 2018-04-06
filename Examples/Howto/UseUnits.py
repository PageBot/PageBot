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

    >>> mm(2)
    2mm
    >>> mm(2).u, mm(2)._v/MM # Unified to pt value stored in _v
    (2.0, 2.0)
    >>> px(5)
    5px
    >>> px(5).u, px(5)._v
    (5, 5)
    >>> pt(5)
    5pt
    >>> px(5).u, pt(5)._v
    (5, 5)
    >>> fr(8) # Fractional units, used in CSS-grid. 
    8fr
    >>> fr(8).u, fr(8)._v
    (8, 8)
    >>> em(12)
    12em
    >>> em(12).u, em(12)._v
    (12, 12)
    >>> perc(12.5)
    12.50%
    >>> perc(12.5).u, perc(12.5)._v
    (12.5, 12.5)
    """

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
