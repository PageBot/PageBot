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
from pagebot.themes.basetheme import BaseTheme, Palette, Style, Mood
from pagebot.toolbox.color import spot, rgb, blackColor, whiteColor

class FairyTales(BaseTheme):
    u"""The FairyTales theme is ..."""

    NAME = 'Fairy Tales'
    BASE_COLORS = dict(
        base0=spot(425),
        base1=spot(237),
        base2=spot(278),
        base3=spot(373),
        base4=spot(422), # Supporter1
        base5=spot(473),
    )

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
