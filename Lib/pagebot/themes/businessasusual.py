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
from pagebot.style import getRootStyle
from pagebot.themes.basetheme import BaseTheme
from pagebot.toolbox.color import spot, rgb

class BusinessAsUsual(BaseTheme):
    u"""The BusinessAsUsual theme is a generic “woody cool gray” theme, with settings that
    can be used in environments when functionality is more important than “arty”
    appearance."""

    NAME = 'Business as Usual'
    COLORS = dict(
        c0=spot('blacku'),c1=spot(404),  c2=spot(877),   c3=spot(541),   c4=spot(542),   c5=spot(545),
        c6=spot(506),   c7=spot(111),   c8=spot(459),   c9=spot(568),   c10=spot(3145), c11=spot(139),
    )

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
