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
        # Cached stems
        self._stems = None # Collect stems from H on property call.
        # Cached bars
        self._bars = None

    def __repr__(self):
        return '<Analyzer of %s>' % self.font.info.fullName

    def __getitem__(self, glyphName):
        u"""Answer the glyph analyzer of glyphName."""
        return self.font[glyphName].analyzer

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

    #   S T E M S

    def _get_stems(self):
        if self._stems is None:
            self._stems = self['H'].stems
        # If no stems found in H or not reliable amount, then do second guess with "I"
        if not self._stems or len(self._stems) != 2: 
            self._stems = self['I'].stems
        # No stems found by verticals, try beaming the I
        if not self._stems or len(self._stems) != 1:
            # This will still not catch on outlines or flourishes, but better that nothing.
            self._stems = self['I'].beamStems 
        return self._stems # If still empty, give up for now.
    stems = property(_get_stems)

    #    B A R S

    def _get_bars(self):
        if self._bars is None:
            self._bars = self['H'].bars
        return self._bars
    bars = property(_get_bars)

