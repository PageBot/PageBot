#!/usr/bin/env python3
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

from pagebot.publications.typespecimens.proofing.proof import Proof
from pagebot.publications.typespecimens.proofing.tx import *

class PageWide(Proof):

    def draw(self, font, content, size):
        height = 0
        nr = 1
        ascenderHeight = getAscenderHeight(font, size)
        dy = height + ascenderHeight * self.leading
        kwargs = {'dy': dy, 'nr': nr}
        self.drawGlyphs(font, content, size, **kwargs)
