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

    def draw(self, style, content, size):
        height = 0
        nr = 1
        upem = style.info.unitsPerEm

        '''
        Before we start making the proof for a new font size:
        * calculate starting point based on previous proof height,
        * recalculate y0 when we're on a new page.
        '''
        ascenderHeight = getAscenderHeight(style, size, upem)
        dy = height + ascenderHeight * self.leading
        kwargs = {'dy': dy, 'size': size, 'nr': nr}
        self.drawGlyphs(style, content, size, **kwargs)
