# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#     
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
# 
#     glass_office.py
#
from pagebot.style import makeStyle, getRootStyle
from basetheme import BaseTheme

class GlassOffice(BaseTheme):
    u"""The GlassOffice theme is a generic “shiny cool gray” theme, with settings that
    can be used in environments when functionality is more important than “arty”
    appearance."""

	NAME = 'Glass Office'
    SCSS_PATH = 'scss/office.scss'

    def initialize(self):
        u"""Theme styles are created here by inheriting them classes. If srcTheme is not None,
        start initialize with a copy of that one."""
        self.name = self.NAME
        self[self.ROOT] = getRootStyle()
        for headName in self.HEADS:
            self[headName] = getRootStyle() # Make sure there is something there for now.
