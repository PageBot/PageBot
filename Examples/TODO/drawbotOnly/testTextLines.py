#!/usr/bin/env python3
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Example written by Frederik Berlaen
#
#     Supporting DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     testTextLines.py
#
import sys
from pagebot import getContext
context = getContext()

if not context.isDrawBot:
    print('Example only runs on DrawBot.')
    sys.exit()


import CoreText
import Quartz

#    NOTE: Assumes TYPETR-Bitcount to be installed.

class TextRun:
    def __init__(self, ctRun, string):
        self.string = string
        self.glyphCount = gc = CoreText.CTRunGetGlyphCount(ctRun)
        self.matrix = CoreText.CTRunGetTextMatrix(ctRun)
        self.stringRange = CoreText.CTRunGetStringRange(ctRun)
        self.stringIndices = CoreText.CTRunGetStringIndicesPtr(ctRun)[0:gc]
        #CoreText.CTRunGetStringIndices(ctRun._ctRun, CoreText.CFRange(0, 5), None)[4]
        #self.advances = CoreText.CTRunGetAdvances(ctRun, CoreText.CFRange(0, 5), None)
        self.positions = CoreText.CTRunGetPositionsPtr(ctRun)[0:gc]
        #CoreText.CTRunGetPositions(ctRun, CoreText.CFRange(0, 5), None)[4]
        # Get list of glyph indices.
        self.glyphFontIndices = CoreText.CTRunGetGlyphsPtr(ctRun)[0:gc]
        #print(CoreText.CTRunGetGlyphs(ctRun, CoreText.CFRange(0, 5), None)[0:5])
        self.status = CoreText.CTRunGetStatus(ctRun)
        attrs = CoreText.CTRunGetAttributes(ctRun)
        # Font stuff
        self.nsFont = f = attrs['NSFont']
        self.fontDescriptor = f.fontDescriptor()
        self.displayName = f.displayName()
        self.familyName = f.familyName()
        self.fontName = f.fontName()
        self.isVertical = f.isVertical()
        (x, y), (w, h) = f.boundingRectForFont()
        self.fontBoundingRect = x, y, w, h
        self.isFixedPitch = f.isFixedPitch()
        self.renderingMode = f.renderingMode()
        self.ascender = f.ascender()
        self.descender = f.descender()
        self.capHeight = f.capHeight()
        self.italicAngle = f.italicAngle()
        self.leading = f.leading()
        self.matrix = f.matrix()
        self.fontSize = f.pointSize()
        self.textTransform = f.textTransform()
        self.underlinePosition = f.underlinePosition()
        self.underlineThickness = f.underlineThickness()
        self.xHeight = f.xHeight()
        # Paragraph stuff
        self.color = attrs['NSColor']
        nsParStyle = attrs['NSParagraphStyle']
        self.alignment = nsParStyle.alignment()
        self.lineSpacing = nsParStyle.lineSpacing()
        self.paragraphSpacing = nsParStyle.paragraphSpacing()
        self.paragraphSpacingBefore = nsParStyle.paragraphSpacingBefore()
        self.headIndent = nsParStyle.headIndent()
        self.paragraphSpacing = nsParStyle.paragraphSpacing()
        self.headIndent = nsParStyle.headIndent()
        self.tailIndent = nsParStyle.tailIndent()
        self.firstLineHeadIndent = nsParStyle.firstLineHeadIndent()
        self.lineHeightMultiple = nsParStyle.lineHeightMultiple()
        self.lineSpacing = nsParStyle.lineSpacing()
        self.maximumLineHeight = nsParStyle.maximumLineHeight()
        self.minimumLineHeight = nsParStyle.minimumLineHeight()

    def __len__(self):
        return self.glyphCount

class TextLine:
    def __init__(self, ctLine):
        self._ctLine = ctLine
        self.glyphCount = CoreText.CTLineGetGlyphCount(ctLine)
        # Hack for now to find the string.
        s = []
        for index, part in enumerate(repr(self._ctLine).split('"')[1].split('\\u')):
            if index == 0:
                s.append(part)
            elif len(part) >= 4:
                s.append(chr(int(part[0:4], 16)))
                s.append(part[4:])
        self.string = ''.join(s)

        self.runs = []
        for ctRun in CoreText.CTLineGetGlyphRuns(ctLine):
            self.runs.append(TextRun(ctRun, self.string))

    def __repr__(self):
        print(self._ctLine)

    def __len__(self):
        return self.glyphCount

    def getIndexForPosition(self, pos):
        x, y = pos
        return CoreText.CTLineGetStringIndexForPosition(self._ctLine, CoreText.CGPoint(x, y))

    def getOffsetForStringIndex(self, i):
        return CoreText.CTLineGetOffsetForStringIndex(self._ctLine, i, None)

    def _get_stringIndex(self):
        return CoreText.CTLineGetStringRange(self._ctLine).location
    stringIndex = property(_get_stringIndex)

    #def _get_alignment(self):
    #    return CoreText.CTTextAlignment(self._ctLine)
    #alignment = property(_get_alignment)

    def _get_imageBounds(self):
        (x, y), (w, h) = CoreText.CTLineGetImageBounds(self._ctLine,None)
        return x, y, w, h
    imageBounds = property(_get_imageBounds)

    def _get_bounds(self):
        return CoreText.CTLineGetTypographicBounds(self._ctLine,None,None,None)
    bounds = property(_get_bounds)

    def _get_trailingWhiteSpace(self):
        return CoreText.CTLineGetTrailingWhitespaceWidth(self._ctLine)
    trailingWhiteSpace = property(_get_trailingWhiteSpace)

def getTextLines(fs, w, h):
    """Answer an ordered list of all baseline position, starting at the top."""
    box = 0, 0, w, h
    attrString = fs.getNSObject()
    setter = CoreText.CTFramesetterCreateWithAttributedString(attrString)
    path = Quartz.CGPathCreateMutable()
    Quartz.CGPathAddRect(path, None, Quartz.CGRectMake(*box))
    box = CoreText.CTFramesetterCreateFrame(setter, (0, 0), path, None)
    ctLines = CoreText.CTFrameGetLines(box)
    textLines = []
    for ctLine in ctLines:
        tl = TextLine(ctLine)
        textLines.append(tl)
    origins = CoreText.CTFrameGetLineOrigins(box, (0, len(ctLines)), None)
    return textLines, origins

fs = FormattedString(u'This åéöøa', font='BitcountMonoDouble-MediumCircleItalic', fontSize=24)
fs = fs + FormattedString('This an example. ' * 20, font='Verdana', fontSize=16)

textLines, o = getTextLines(fs, 500, 200)
#print(o)
#print
for tl in textLines:
    #print('Bounds:', tl.bounds, tl.imageBounds, tl.trailingWhiteSpace, 'Len:', len(tl), 'Index:', tl.stringIndex, )
    #tl.alignment
    #print('Index at position (100, 10):', tl.getIndexForPosition((100, 10)))
    #print('Offset at string index (0):', tl.runs)
    print('Runs:', len(tl.runs))
    print('String:', tl.string)
    for textRun in tl.runs:
        """
        print(CoreText.CTRunGetTextMatrix(ctRun._ctRun))
        print(CoreText.CTRunGetStringRange(ctRun._ctRun))
        print(CoreText.CTRunGetStringIndicesPtr(ctRun._ctRun)[20])
        print(CoreText.CTRunGetStringIndices(ctRun._ctRun, CoreText.CFRange(0, 5), None)[4])
        print(CoreText.CTRunGetAdvances(ctRun._ctRun, CoreText.CFRange(0, 5), None))
        print(CoreText.CTRunGetPositionsPtr(ctRun._ctRun)[20])
        print(CoreText.CTRunGetPositions(ctRun._ctRun, CoreText.CFRange(0, 5), None)[4])
        print(CoreText.CTRunGetGlyphsPtr(ctRun._ctRun)[20])
        print(CoreText.CTRunGetGlyphs(ctRun._ctRun, CoreText.CFRange(0, 5), None)[0:5])
        print(CoreText.CTRunGetStatus(ctRun._ctRun))
        print(CoreText.CTRunGetAttributes(ctRun._ctRun)['NSColor'])
        print(CoreText.CTRunGetAttributes(ctRun._ctRun)['NSParagraphStyle'])
        print(CoreText.CTRunGetAttributes(ctRun._ctRun)['NSFont'])
        print(ctRun._ctRun)
        """
        print(textRun.nsFont, textRun.glyphFontIndices, textRun.positions)
        print('========')
        print(textRun.displayName)
        print(textRun.familyName)
        print(textRun.fontName)
        print(textRun.glyphCount)
        print(textRun.fontDescriptor)
        print(textRun.isFixedPitch)
        print(textRun.renderingMode)
        print(textRun.capHeight)
        print(textRun.ascender)
        print(textRun.descender)
        print(textRun.fontBoundingRect)
        print(textRun.italicAngle)
        print
        #print(CoreText.CTLineGetGlyphRuns(tl._ctLine))
    #print(CoreText.CTLineGetStringRange(tl._ctLine))
    #print(tl.string )
