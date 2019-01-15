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
from pagebot.style import getRootStyle
from pagebot.themes.basetheme import BaseTheme
from pagebot.toolbox.color import spot, rgb

class SeasoningTheDish(BaseTheme):
    u"""The SeasoningTheDish theme is ..."""

    NAME = 'Seasoning the Dish'
    COLORS = dict(
        c0=spot(412),   c1=spot(404),   c2=spot(403),   c3=spot(401),   c4=spot(103),   c5=spot(124),
        c6=spot(158),   c7=spot(200),   c8=spot(314),   c9=spot(3272),  c10=spot(369),  c11=spot(389),
    )

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
