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
#     acomponent.py
#
from pagebot.toolbox.units import asFormatted

class AComponent:
    def __init__(self, ttComponent):
        self.ttComponent = ttComponent

    def _get_baseGlyph(self):
        return self.ttComponent.glyphName
    baseGlyph = property(_get_baseGlyph)

    def _get_flags(self):
        return self.ttComponent.flags
    flags = property(_get_flags)

    def _get_x(self):
        return self.ttComponent.x
    x = property(_get_x)

    def _get_y(self):
        return self.ttComponent.y
    y = property(_get_y)

    def __repr__(self):
        return 'Cmp(%s, %s, %s)' % (self.baseGlyph, asFormatted(self.x), asFormatted(self.y))

