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
#     stackedtypography.py
#
from random import random
from pagebot.elements import *

class StackedTypography(Template):
    
    def initialize(self, **kwargs):
        u"""Allow inheriting element classes to do extra initialization stuff. Default behavior is to do nothing. 
        Inheriting classes can implmenet their own version."""
        # Create a visible rect for debugging.
        self.w = self.parent.w
        self.h = self.parent.h
        S = 100
        for n in range(250):
            newRect(parent=self, 
                x=random()*(self.w-S), 
                y=random()*(self.h-S), w=S, h=S, 
                fill=color(random(), random(), random(), 0.5))

