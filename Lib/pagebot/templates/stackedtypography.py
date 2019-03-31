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
#     stackedtypography.py
#
#     D E P R E C A T E D
#     Don't use or develop here.
#     
#     Templates will be defined in Publications

from random import random
from pagebot.elements import *
from pagebot.toolbox.color import color

class StackedTypography(Template):

    def initialize(self, **kwargs):
        """Allow inheriting element classes to do extra initialization.
        Default behavior is to do nothing. Inheriting classes can implement
        their own version."""
        # Create a visible rect for debugging.
        self.w = self.parent.w
        self.h = self.parent.h
        S = 100
        for n in range(250):
            newRect(parent=self,
                x=random()*(self.w-S),
                y=random()*(self.h-S), w=S, h=S,
                fill=color(random(), random(), random(), 0.5))

