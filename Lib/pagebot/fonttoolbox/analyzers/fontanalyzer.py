# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#     
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     fontanalyzer.py
#
#     Implements a PageBot font analyzer class to get info from beyond a TTFont.
#
import weakref

class FontAnalyzer(object):

    def __init__(self, font):
        self.font = font

    # self.parent    Weakref to the parent (style) analyzer
    def _get_font(self):
        return self._font()
    def _set_font(self, font):
        # Set the weakref to the font
        self._font = weakref.ref(font)
    font = property(_get_font, _set_font)
