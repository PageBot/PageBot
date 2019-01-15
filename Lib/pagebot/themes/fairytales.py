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
#     fairytales.py
#
from pagebot.style import getRootStyle
from pagebot.themes.basetheme import BaseTheme
from pagebot.toolbox.color import spot, rgb

class FairyTales(BaseTheme):
    u"""The FairyTales theme is ..."""

    NAME = 'Fairy Tales'
    COLORS = dict(
        c0=spot(473),   c1=spot(373),   c2=spot(197),   c3=spot(278),   c4=spot(237),   c5=spot(305),
        c6=spot(465),   c7=spot(453),   c8=spot(420),   c9=spot(451),   c10=spot(422),  c11=spot(425),
    )

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
