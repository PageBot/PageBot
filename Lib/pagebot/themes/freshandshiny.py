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
#     freshandshiny.py
#
from pagebot.style import getRootStyle
from pagebot.themes.basetheme import BaseTheme
from pagebot.toolbox.color import spot, rgb

class FreshAndShiny(BaseTheme):
    u"""The FreshAndShiny theme is ..."""

    NAME = 'Fresh and Shiny'
    COLORS = dict(
        c0=spot('coolgray11u'),c1=spot('coolgray9u'),c2=spot('coolgray6u'),c3=spot(165),   c4=spot(375),   c5=spot('rhodamineredu'), 
        c6=spot(2995),  c7=spot('yellow'),c8=spot(265),  c9=spot('processblacku'),     c10=spot('red032u'), c11=spot('processblacku'),
    )

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
