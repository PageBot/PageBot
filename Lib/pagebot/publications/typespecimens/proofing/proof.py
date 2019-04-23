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
#     proof.py
#
from fontTools.pens.cocoaPen import CocoaPen
from pagebot.publications.typespecimens.proofing.tx import *

class Proof:

    leading = 1.2

    def __init__(self, context, **kwargs):
        self.context = context

    def drawGlyphs(self, font, content, size, **kwargs):
        scale = getScale(font, size)
        ascender = getAscenderHeight(font, size)
        self.context.scale(scale)

        x = 0
        y = self.context.b.height() - (ascender + size) * scale * self.leading

        for c in content:
            pen = CocoaPen(font)
            self.context.fill(0)
            self.context.stroke(None)
            glyph = font[c]
            self.context.translate(x, y)
            self.context.drawGlyphPath(glyph)
            self.context.translate(-x, -y)
            x += glyph.width
