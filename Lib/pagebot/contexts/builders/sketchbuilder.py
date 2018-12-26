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
#     sketchbuilder.py
#
from pagebot.contexts.builders.basebuilder import BaseBuilder

class SketchBuilder(BaseBuilder):
    PB_ID = 'Sketch'

    def frameDuration(self, frameDuration):
        pass

    def save(self):
        pass

    def fill(self, e, g, b, alpha=None):
        pass

sketchBuilder = SketchBuilder()

