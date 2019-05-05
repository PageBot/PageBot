#!/usr/bin/env python3
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
#     See pagebot.toolbox.units for example docstring too.
#
from pagebot.toolbox.units import Unit, mm, px, pt, fr, em, perc, col, units

def useUnits():
    # 2mm, 2
    print(mm(2), mm(2).rv) # Showing the unit as instance and as rendered value
    # 5px, 5
    print(px(5), px(5).rv)
    # 5px, 5
    print(px(5), pt(5).rv)
    # 8fr, 50
    print(fr(8, base=400), fr(8, base=400).rv) # Fractional units, used in CSS-grid.
    # 12em, 120
    print(em(12, base=10), em(12, base=10).rv)
    # 12.5%, 50
    print(perc(12.5, base=400), perc(12.5, base=400).rv)
    u = col(1/4, base=mm(200), g=mm(4))
    # 0.25col, 47mm
    print(u, u.rv)
    print(mm(2), 'Real value:', mm(2).rv)
    print(px(5), px(5).rv)
    # TODO: etc...

useUnits()
