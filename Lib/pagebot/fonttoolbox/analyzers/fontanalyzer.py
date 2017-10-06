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
from pagebot.toolbox.transformer import path2Name

class FontAnalyzer(object):

    def __init__(self, font):
        self.font = font
        self._stems = [] # Collect stems of H

    def __repr__(self):
        return '<Analyzer of %s>' % self.font.info.fullName

    def __getitem__(self, glyphName):
        u"""Answer the glyph analyzer of glyphName."""
        return self[glyphName].analyzer

    def _get_name(self):
        return path2Name(self.font.path)
    name = property(_get_name)

    # self.parent    Weakref to the parent (style) analyzer
    def _get_font(self):
        return self._font()
    def _set_font(self, font):
        # Set the weakref to the font
        self._font = weakref.ref(font)
    font = property(_get_font, _set_font)

    def _get_stems(self):
        if self._stems is None:
            self._stems = self['H'].stems
        return self._stems
    stems = property(_get_stems)