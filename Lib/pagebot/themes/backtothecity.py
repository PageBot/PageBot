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
from pagebot.themes.basetheme import BaseTheme
from pagebot.toolbox.color import spot, rgb, blackColor, whiteColor

class BackToTheCity(BaseTheme):
    u"""The BackToTheCity theme is ..."""

    NAME = 'Back to the City'
    BASE_COLORS = dict(
        base0=spot(476),
        base1=spot(1405),
        base2=spot(139),
        base3=spot(480),
        base4=spot(421), # Supporter1
        base5=spot(157),
    )

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
