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
#     intothewoods.py
#
from pagebot.themes.basetheme import BaseTheme
from pagebot.toolbox.color import spot, rgb, blackColor, whiteColor

class IntoTheWoods(BaseTheme):
    u"""The IntoTheWoods theme is ...

    >>> theme = IntoTheWoods
    """

    NAME = 'Into the Woods'
    BASE_COLORS = dict(
        base0=spot('gray10u'),
        base1=spot(348),
        base2=spot(376),
        base3=spot(381),
        base4=spot(392), # Supporter1
        base5=spot(398),
    )
    
if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
