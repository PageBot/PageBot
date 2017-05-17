# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     UseGlyphAnalyzer.py
#
#     Implements a PabeBot font classes to get info from a TTFont.
#   
import weakref
from AppKit import NSFont
from fontTools.ttLib import TTFont, TTLibError
from drawBot import BezierPath
from pagebot.fonttoolbox.objects.fontinfo import FontInfo
from pagebot.toolbox.transformer import point3D

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

class Vertical(object):
    pass
    
Horizontal = Vertical

class GlyphAnalyzer(object):

    VERTICAL_CLASS = Vertical # Allow inheriting classes to change this
    HORIZONTAL_CLASS = Horizontal

    def __init__(self, glyph):
        self._glyph = weakref.ref(glyph)
        self._analyzer = None

        self._verticals = None
        self._horizontals = None

    def _get_glyph(self):
        return self._glyph()
    glyph = property(_get_glyph)
        
    def __repr__(self):
        return '<Analyzer of "%s">' % self.glyph.name

    # self.verticals

    def _get_verticals(self):
        if self._verticals is None:
            self.findVerticals()
        return self._verticals
    verticals = property(_get_verticals)

    # self.horizontals

    def _get_horizontals(self):
        if self._horizontals is None:
            self.findHorizontals()
        return self._horizontals
    horizontals = property(_get_horizontals)

    def findVerticals(self):
        u"""The @findVerticals@ method answers a list of verticals.
        """
        self._verticals = verticals = {}

        for pc in self.glyph.pointContexts:
            if pc.isVertical():
                if not pc.x in verticals:
                    verticals[pc.x] = self.VERTICAL_CLASS()
                verticals[pc.x].append(pc)

    def findHorizontals(self):
        u"""
        The @findHorizontals@ method answers a list of horizontals where the
        main point is on curve.
        """
        self._horizontals = horizontals = {}

        for pc in self.glyph.pointContexts:
            if pc.isHorizontal():
                if not pc.y in horizontals:
                    horizontals[pc.y] = self.HORIZONTAL_CLASS()
                horizontals[pc.y].append(pc)


C = 0.5
import pagebot
from pagebot.fonttoolbox.objects.font import Font

W = H = 1000

PATH = u"/Library/Fonts/F5MultiLanguageFontVar.ttf"
cjkF = Font(PATH, install=False)
#print cjkF.info.familyName, cjkF.info.styleName
#print cjkF.ttFont.tables.keys()
glyphs = []
start = 16500
end = 16502

GLYPHS = ('cid05404.1', 'cid05405.1', 'cid05403.1', 'e', 'H', 'O')
GLYPHS = ('bullet', 'e','h', 'oe')
#GLYPHS = sorted( cjkF.keys())[start:end]
for name in GLYPHS:
    if name.startswith('.'):
        continue
    newPage(W, H)
    glyph = cjkF[name]
    glyph.ANALYZER_CLASS = GlyphAnalyzer
    print glyph.pointContexts
    print glyph.contours
    