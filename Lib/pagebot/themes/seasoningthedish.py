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
#     seasoningthedish.py
#
from pagebot.themes.basetheme import BaseTheme, Palette, Style, Mood
from pagebot.toolbox.color import spot, rgb, blackColor, whiteColor

class SeasoningTheDish(BaseTheme):
    u"""The SeasoningTheDish theme is ..."""

    NAME = 'Seasoning the Dish'
    PALETTE = Palette(
        black=spot(403),
        white=whiteColor,
        # Colors with gray tone function
        dark=spot(412),
        middle=spot(404),
        light=spot(401),
        # Temperature
        warm=spot(103), 
        cold=spot(314), 
        # Highlight
        hilite1=spot(200),
        hilite2=spot(158), 
        hilite3=spot(124),
        hilite4=spot(158),
        # Supporters
        supporter1=spot(3272), 
        supporter2=spot(369), 
        supporter3=spot(389), 
        supporter4=spot(369), 
    )

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
