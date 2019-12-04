# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     stylelib.py
#
#     Default CSS reset.
#     Library of predefined named styles.
#
#     D E P R E C A T E D
#
#     CSS is now implemented as SCSS files, using PageBot-generated variable.scss.
#     NOTE: still imported in pagebot.document.
#

from pagebot.toolbox.units import px, em
from pagebot.toolbox.color import whiteColor, blackColor, color

MARGIN = (0, 0, px(10), 0)

default = {
    'body': dict(
        font='Verdana, sans',
        fontStyle='normal', 
        fontWeight='normal',
        tracking=0,
        fontSize=px(12),
        leading=em(1.4),
        color=0,
        fill=whiteColor,
    ),
    'pre, code': dict(
        display='none',
    ),
    'a': dict(
        color=color('#828487'),
        textDecoration='none',
        transition='all 0.3s ease-in-out',
    ),
    'a:hover': dict(
        color=blackColor,
    ),
    'p': dict(
        margin=MARGIN,
        tracking=0,
    ),
    'em': dict(
        fontWeight='Bold',
    ),
    'h1, h2, h3, h4, h5': dict(
        fontWeight='Bold',
        fontStyle='Bold',
    ),
    'h2, h3, h4, h5': dict(
        margin=MARGIN,
    ),
}

styleLib = {
    'default': default,
}
