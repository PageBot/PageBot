#!/usr/bin/env python3
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
#     textline.py
#
import re
from pagebot.contexts.strings.textrun import TextRun
from pagebot.contexts.strings.pattern import FoundPattern
from pagebot.toolbox.units import pt, upt
try:
    from CoreText import (CGPoint, CTLineGetGlyphRuns,
            CTLineGetStringIndexForPosition, CTLineGetOffsetForStringIndex,
            CTLineGetStringRange, CTLineGetImageBounds,
            CTLineGetTypographicBounds, CTLineGetTrailingWhitespaceWidth)
except:
    CTLineGetGlyphRuns = None
    CTLineGetImageBounds = None
    CTLineGetStringIndexForPosition = None
    CTLineGetTrailingWhitespaceWidth = None
    CTLineGetTypographicBounds = None
    CGPoint = None

class TextLine:

    def __init__(self, ctLine, x, y, lineIndex):
        self._ctLine = ctLine
        self.x = x
        self.y = y # Relative from top of text box
        self.lineIndex = lineIndex # Vertical line index in TextBox.
        self.string = ''
        self.textRuns = []

        for runIndex, ctRun in enumerate(CTLineGetGlyphRuns(ctLine)):
            textRun = TextRun(ctRun, runIndex)
            self.textRuns.append(textRun)
            self.string += textRun.string

    def __repr__(self):
        return '<%s #%d y:%0.2f Runs:%d>' % (self.__class__.__name__, self.lineIndex, self.y, len(self.textRuns))

    def __len__(self):
        return self.glyphCount

    def __getitem__(self, index):
        return self.textRuns[index]

    def _get_ascender(self):
        """Returns the max ascender of all text runs as Em, based on the
        current font and fontSize."""
        ascender = 0
        for textRun in self.textRuns:
            ascender = max(ascender, textRun.ascender)
        return ascender
    fontAscender = ascender = property(_get_ascender) # Compatibility with DrawBot API

    def _get_descender(self):
        """Returns the max descender of all text runs as Em, based on the
        current font and fontSize."""
        descender = 0
        for textRun in self.textRuns:
            descender = min(descender, textRun.descender)
        return descender
    fontDescender = descender = property(_get_descender) # Compatibility with DrawBot API

    def _get_xHeight(self):
        """Returns the max x-height of all text runs as Em, based on the
        current font and fontSize."""
        xHeight = 0
        for textRun in self.textRuns:
            xHeight = max(xHeight, textRun.xHeight)
        return xHeight
    fontXHeight = xHeight = property(_get_xHeight) # Compatibility with DrawBot API

    def _get_capHeight(self):
        """Returns the max font cap height of all text runs as Em, based on the
        current font and fontSize."""
        capHeight = 0
        for textRun in self.textRuns:
            capHeight = max(capHeight, textRun.capHeight)
        return capHeight
    fontCapHeight = capHeight = property(_get_capHeight) # Compatibility with DrawBot API

    def _get_maximumLineHeight(self):
        """Returns the max font cap height of all text runs as Em, based on the
        current font and fontSize."""
        maximumLineHeight = 0
        for textRun in self.textRuns:
            maximumLineHeight = max(maximumLineHeight, textRun.maximumLineHeight)
        return maximumLineHeight
    maximumLineHeight = property(_get_maximumLineHeight) # Compatibility with DrawBot API

    def getIndexForPosition(self, x, y):
        xpt, ypt = upt(x, y)
        return CTLineGetStringIndexForPosition(self._ctLine, CGPoint(xpt, ypt))[0]

    def getOffsetForStringIndex(self, i):
        """Answers the z position that is closest to glyph string index i. If i
        is out of bounds, then answer the closest x position (left and right
        side of the string)."""
        return CTLineGetOffsetForStringIndex(self._ctLine, i, None)[0]

    def _get_stringIndex(self):
        return CTLineGetStringRange(self._ctLine).location
    stringIndex = property(_get_stringIndex)

    def getGlyphIndex2Run(self, glyphIndex):
        for run in self.runs:
            if run.iStart >= glyphIndex:
                return run
        return None

    #def _get_alignment(self):
    #    return CTTextAlignment(self._ctLine)
    #alignment = property(_get_alignment)

    def _get_imageBounds(self):
        """Property that answers the bounding box (actual black shape) of the
        text line."""
        (xpt, ypt), (wpt, hpt) = CTLineGetImageBounds(self._ctLine, None)
        return pt(xpt, ypt, wpt, hpt)
    imageBounds = property(_get_imageBounds)

    def _getBounds(self):
        return CTLineGetTypographicBounds(self._ctLine, None, None, None)

    def _get_bounds(self):
        """Property that returns the EM bounding box of the line."""
        return self._getBounds()
    bounds = property(_get_bounds)

    def _get_size(self):
        _, _, wpt, hpt = self._getBounds()
        return pt(wpt, hpt)
    size = property(_get_size)

    def _get_w(self):
        _, _, wpt, _ = self._getBounds()
        return pt(wpt)

    def _get_y(self):
        _, _, _, hpt = self._getBounds()
        return pt(hpt)

    def _get_x(self):
        xpt, _, _, _ = self._getBounds()
        return pt(xpt)

    def _get_y(self):
        _, ypt, _, _ = self._getBounds()
        return pt(ypt)

    def _get_trailingWhiteSpace(self):
        return CTLineGetTrailingWhitespaceWidth(self._ctLine)
    trailingWhiteSpace = property(_get_trailingWhiteSpace)

    def findPattern(self, pattern):
        founds = []
        if isinstance(pattern, str):
            pattern = re.compile(pattern)
            #pattern = re.compile('([a-ZA-Z0-9\.\-\_]*])
        for iStart, iEnd in [(m.start(0), m.end(0)) for m in re.finditer(pattern, self.string)]:
            xStart = self.getOffsetForStringIndex(iStart)
            xEnd = self.getOffsetForStringIndex(iEnd)
            #print('xStart, xEnd', xStart, xEnd)
            run = self.getGlyphIndex2Run(xStart)
            #print('iStart, xStart', iStart, xStart, iEnd, xEnd, run)
            founds.append(FoundPattern(self.string[iStart:iEnd], xStart, iStart, line=self, run=run))
        return founds

