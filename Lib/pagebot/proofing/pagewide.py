#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------

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
#     pagewide.py
#

from pagebot.proofing.proof import Proof
from pagebot.proofing.tx import *

class PageWide(Proof):

    def __init__(self, context, **kwargs):
        super(PageWide, self).__init__(context, **kwargs)

    def draw(self, style, content, size):
        height = 0
        nr = 1
        ascenderHeight = getAscenderHeight(style, size)
        dy = height + ascenderHeight * self.leading
        kwargs = {'dy': dy, 'nr': nr}
        self.drawGlyphs(style, content, size, **kwargs)
