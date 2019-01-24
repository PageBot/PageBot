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
from pagebot.themes.basetheme import BaseTheme, Palette, Style, Mood
from pagebot.toolbox.color import spot, rgb, blackColor, whiteColor

class BackToTheCity(BaseTheme):
    u"""The BackToTheCity theme is ..."""

    NAME = 'Back to the City'
    PALETTE = Palette(
        black=spot(476),
        white=whiteColor,
        # Colors with gray tone function
        dark=spot(1405),
        middle=spot(500),
        light=spot(480),
        # Temperature
        warm=spot(1815), 
        cold=spot(423), 
        # Highlight
        hilite1=spot(193),
        hilite2=spot(157), 
        hilite3=spot(421),
        hilite4=spot(193),
        # Supporters
        supporter1=spot(139), 
        supporter2=spot(145), 
        supporter3=spot(478), 
        supporter4=spot(139), 
    )


if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
