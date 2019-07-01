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
from pagebot.themes.basetheme import BaseTheme
from pagebot.toolbox.color import spotColor, rgbColor

class FreshAndShiny(BaseTheme):
    u"""The FreshAndShiny theme is ...

    >>> theme = FreshAndShiny()
    >>> theme.mood['h1.color']
    'hilite2'
    >>> theme.selectMood('dark') # Select another mode
    >>> theme.mood['h1.color']
    'hilite2'
    """
    NAME = 'Fresh and Shiny'
    BASE_COLORS = dict(
        base0=spotColor('coolgray11u'),
        base1=spotColor('rhodamineredu'),
        base2=spotColor(265),
        base3=spotColor(3005),
        base4=spotColor(375), # Supporter1
        base5=rgbColor('red'),#spotColor('red032u'),
    )

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
