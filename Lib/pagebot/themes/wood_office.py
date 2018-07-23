# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     wood_office.py
#
from pagebot.style import getRootStyle
from pagebot.themes.basetheme import BaseTheme

class WoodOffice(BaseTheme):
    u"""The WoodOffice theme is a generic “woody cool gray” theme, with settings that
    can be used in environments when functionality is more important than “arty”
    appearance."""

    NAME = 'Wood Office'
    SCSS_PATH = 'scss/office.scss'

    def initialize(self):
        u"""Theme styles are created here by inheriting them classes. If srcTheme is not None,
        start initialize with a copy of that one."""
        self.name = self.NAME
        self[self.ROOT] = getRootStyle()
        for headName in self.HEADS:
            self[headName] = getRootStyle() # Make sure there is something there for now.


