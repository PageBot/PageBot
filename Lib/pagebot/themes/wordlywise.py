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
from pagebot.themes.basetheme import BaseTheme
from pagebot.toolbox.color import spot

class WordlyWise(BaseTheme):
    u"""The WordlyWise theme is ...

    >>> theme = WordlyWise()
    >>> theme.palette
    <Palette colors=51>
    >>> from pagebot.elements.web.nanosite.nanostyle_css import cssPy
    """

    NAME = 'Wordly Wise'
    BASE_COLORS = dict(
        base0=spot('warmgray8u'),
        base1=spot(286),
        base2=spot(265),
        base3=spot(258),
        base4=spot(278), # Supporter1
        base5=spot(270),
    )

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
