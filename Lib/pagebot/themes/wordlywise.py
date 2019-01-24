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
from pagebot.themes.basetheme import BaseTheme, Palette, Style, Mood
from pagebot.toolbox.color import spot, rgb, blackColor, whiteColor

class WordlyWise(BaseTheme):
    u"""The WordlyWise theme is ...

    >>> theme = WordlyWise()
    >>> theme.palette
    <Wordly Wise #0=195 #1=187 #2=214 #3=258 #4=270 #5=265 #6=280 #7=278 #8=286 #9=427 #10=429 #11=430>
    >>> from pagebot.elements.web.nanosite.nanostyle_css import cssPy
    >>> theme.cssPy2Css(cssPy)
    """

    NAME = 'Wordly Wise'
    PALETTE = Palette(
        black=spot('blacku'),
        white=whiteColor,
        # Colors with gray tone function
        dark=spot(280),
        middle=spot(265),
        light=spot(270),
        # Temperature
        warm=spot(187), 
        cold=spot(278), 
        # Highlight
        hilite1=spot(286),
        hilite2=spot(258), 
        hilite3=spot(214),
        hilite4=spot(258),
        # Supporters
        supporter1=spot(195), 
        supporter2=spot(429), 
        supporter3=spot(430), 
        supporter4=spot(195), 
    )

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
