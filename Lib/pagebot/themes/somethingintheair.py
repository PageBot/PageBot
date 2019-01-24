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
from pagebot.themes.basetheme import BaseTheme, Palette, Style, Mood
from pagebot.toolbox.color import spot, rgb, blackColor, whiteColor

class SomethingInTheAir(BaseTheme):
    u"""The SomethingInTheAir theme is ..."""

    NAME = 'Something in the Air'
    PALETTE = Palette(
        black=spot(540),
        white=whiteColor,
        # Colors with gray tone function
        dark=spot('reflexblue'),
        middle=spot(542),
        light=spot(544),
        # Temperature
        warm=spot(245), 
        cold=spot(2985), 
        # Highlight
        hilite1=spot(190),
        hilite2=spot(137), 
        hilite3=spot('yellow'),
        hilite4=spot(190),
        # Supporters
        supporter1=spot(307), 
        supporter2=spot(3005), 
        supporter3=spot(3005), 
        supporter4=spot(306), 
    )

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
