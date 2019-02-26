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
from pagebot.themes.basetheme import BaseTheme
from pagebot.toolbox.color import spot

class SomethingInTheAir(BaseTheme):
    u"""The SomethingInTheAir theme is ..."""

    NAME = 'Something in the Air'
    BASE_COLORS = dict(
        base0=spot('reflexblueu'),
        base1=spot(540),
        base2=spot(542),
        base3=spot(306),
        base4=spot(245), # Supporter1
        base5=spot(190),
    )
    
if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
