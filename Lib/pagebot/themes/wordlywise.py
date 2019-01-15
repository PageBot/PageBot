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
#     wordlywise.py
#
from pagebot.style import getRootStyle
from pagebot.themes.basetheme import BaseTheme
from pagebot.toolbox.color import spot, rgb

class WordlyWise(BaseTheme):
    u"""The WordlyWise theme is ...

    >>> theme = WordlyWise()
    >>> theme.palette
    <Wordly Wise #0=195 #1=187 #2=214 #3=258 #4=270 #5=265 #6=280 #7=278 #8=286 #9=427 #10=429 #11=430>
    >>> from pagebot.elements.web.nanosite.nanostyle_css import cssPy
    >>> theme.cssPy2Css(cssPy)
    """

    NAME = 'Wordly Wise'
    COLORS = dict(
        c0=spot(195),   c1=spot(187),   c2=spot(214),   c3=spot(258),   c4=spot(270),   c5=spot(265),
        c6=spot(280),   c7=spot(278),   c8=spot(286),   c9=spot(427),   c10=spot(429),  c11=spot(430),
    )

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
