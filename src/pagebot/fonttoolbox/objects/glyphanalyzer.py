# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     glyphanalyzer.py
#
#     Implements a PabeBot font classes to get info from a TTFont.
#   
import weakref

class GlyphAnalyzer(object):
    def __init__(self, glyph):
        self.glyph = weakref.ref(glyph)


