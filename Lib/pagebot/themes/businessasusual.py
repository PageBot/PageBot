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
#     businesasusual.py
#
from pagebot.themes.basetheme import BaseTheme
from pagebot.toolbox.color import spot, rgb, blackColor, whiteColor

class BusinessAsUsual(BaseTheme):
    u"""The BusinessAsUsual theme is a generic “woody cool gray” theme, with settings that
    can be used in environments when functionality is more important than “arty”
    appearance."""

    NAME = 'Business as Usual'
    BASE_COLORS = dict(
        base0=spot('blacku'),
        base1=spot(404),
        base2=spot(541),
        base3=spot(542),
        base4=spot(139), # Supporter1
        base5=spot(877),
    )

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
