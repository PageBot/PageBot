#!/usr/bin/env python
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
#     nonebuilder.py
#
import os
from pagebot.toolbox.transformer import path2Name
from pagebot.contexts.builders.basebuilder import BaseBuilder

class NoneBezierPath:
    """Make NoneBezierPath with the same API for NoneDrawBotBuilder drawing
    texting."""

    def moveTo(self, p):
        pass

    lineTo = moveTo

    def quadTo(self, pcp, p):
        pass

    def curveTo(self, bcp1, bcp2, p):
        pass

    def closePath(self):
        pass

    def appendPath(self, path):
        pass

class NoneImageObject:
    """Make NoneImageObject with the same API got NonDrawBotBuilder."""
    def __init__(self, path):
        self.path = path

class NoneBuilder(BaseBuilder):
    """Make NoneBuilder with a general builder API for docTesting. Used for
    example when the platform does not support DrawBot. Methods need to be
    added here when DrawBotContext docTests fail with non-DrawBot platforms.

    NOTE: when completed this set of methods should match with DrawBot
    itself."""

    #BezierPath = NoneBezierPath

class NoneDrawBotBuilder(NoneBuilder):

    PB_ID = 'drawBot'

class NoneSvgBuilder(NoneBuilder):

    PB_ID = 'svg'

class NoneFlatBuilder(NoneBuilder):

    PB_ID = 'flat'

    def document(self, w, h, units):
        pass

if __name__ == '__main__':
    import doctest
    doctest.testmod()
