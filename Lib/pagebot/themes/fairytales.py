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
from pagebot.themes.basetheme import BaseTheme
from pagebot.toolbox.color import spotColor

class FairyTales(BaseTheme):
    u"""The FairyTales theme is ..."""

    NAME = 'Fairy Tales'
    BASE_COLORS = dict(
        base0=spotColor(425),
        base1=spotColor(237),
        base2=spotColor(278),
        base3=spotColor(373),
        base4=spotColor(422), # Supporter1
        base5=spotColor(473),
    )

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
