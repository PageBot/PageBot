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
#     backtothecity.py
#
from pagebot.style import getRootStyle
from pagebot.themes.basetheme import BaseTheme
from pagebot.toolbox.color import spot, rgb

class BackToTheCity(BaseTheme):
    u"""The BackToTheCity theme is ..."""

    NAME = 'Back to the City'
    COLORS = dict(
        c0=spot(476),   c1=spot(478),   c2=spot(500),   c3=spot(480),   c4=spot(1405),  c5=spot(139),
        c6=spot(145),   c7=spot(157),   c8=spot(1815),  c9=spot(193),   c10=spot(421),  c11=spot(423),
    )


if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
