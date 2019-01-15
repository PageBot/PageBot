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
#     somethingintheair.py
#
from pagebot.style import getRootStyle
from pagebot.themes.basetheme import BaseTheme
from pagebot.toolbox.color import spot, rgb

class SomethingInTheAir(BaseTheme):
    u"""The SomethingInTheAir theme is ..."""

    NAME = 'Something in the Air'
    COLORS = dict(
        c0=spot(540),   c1=spot(542),   c2=spot(544),   c3=spot(2985),  c4=spot('reflexblue'),c5=spot(307),
        c6=spot(306),   c7=spot(3005),  c8=spot('yellow'),c9=spot(137),  c10=spot(190),  c11=spot(245),
    )

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
