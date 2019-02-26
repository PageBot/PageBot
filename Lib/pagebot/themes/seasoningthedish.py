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
from pagebot.themes.basetheme import BaseTheme
from pagebot.toolbox.color import spot

class SeasoningTheDish(BaseTheme):
    u"""The SeasoningTheDish theme is ..."""

    NAME = 'Seasoning the Dish'
    BASE_COLORS = dict(
        base0=spot(412),
        base1=spot(214),
        base2=spot(369),
        base3=spot(389),
        base4=spot(401), # Supporter1
        base5=spot(103),
    )

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
