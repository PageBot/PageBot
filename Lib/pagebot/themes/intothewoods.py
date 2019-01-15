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
#     intothewoods.py
#
from pagebot.style import getRootStyle
from pagebot.themes.basetheme import BaseTheme
from pagebot.toolbox.color import spot, rgb

class IntoTheWoods(BaseTheme):
    u"""The IntoTheWoods theme is ..."""

    NAME = 'Into the Woods'
    COLORS = dict(
        c0=spot(350),   c1=spot(348),   c2=spot(381),   c3=spot(392),   c4=spot(398),   c5=spot(376),
        c6=spot('warmgray10u'),c7=spot('warmgray8u'),   c8=spot('warmgray4u'),     c9=spot(2975),  c10=spot(305),  c11=spot('processblue'),
    )

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
