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
from pagebot.toolbox.color import spotColor

class SeasoningTheDish(BaseTheme):
    u"""The SeasoningTheDish theme is ..."""

    NAME = 'Seasoning the Dish'
    BASE_COLORS = dict(
        base0=spotColor(412),
        base1=spotColor(214),
        base2=spotColor(369),
        base3=spotColor(389),
        base4=spotColor(401), # Supporter1
        base5=spotColor(103),
    )

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
