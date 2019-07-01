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
from pagebot.toolbox.color import spotColor

class SomethingInTheAir(BaseTheme):
    u"""The SomethingInTheAir theme is ..."""

    NAME = 'Something in the Air'
    BASE_COLORS = dict(
        base0=spotColor('reflexblueu'),
        base1=spotColor(540),
        base2=spotColor(542),
        base3=spotColor(306),
        base4=spotColor(245), # Supporter1
        base5=spotColor(190),
    )

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
