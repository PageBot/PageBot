#!/usr/bin/evn python
# encoding: utf-8
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     TextLineTextRun.py
#
#     Needs Bitcount to be installed for best view.
#     See gallery.
#
#    Implements a demo version of TextLine and TextRun.
#    This code has been built into BabelString DrawBotString.
#

import re
import sys

from pagebot import getContext
from pagebot.elements import newTextBox
from pagebot.toolbox.color import color
from pagebot.document import Document

try:
    import CoreText
    import Quartz
except ImportError:
    sys.exit('Example only runs in DrawBot')

context = getContext()

class FoundPattern:
    def __init__(self, s, x, ix, y=None, w=None, h=None, line=None, run=None):
        self.s = s # Actual found string
        self.x = x
        self.ix = ix
        self.y = y
        self.w = w
        self.h = h
        self.line = line # TextLine instance that this was found in
        self.run = run # List of  of this strin,g

    def __repr__(self):
        return '[Found "%s" @ %s,%s]' % (self.s, self.x, self.y)

class TextRun:
    def __init__(self, ctRun, runIndex):
        self.runIndex = runIndex # Index of the run in the TextLine
        self._ctRun = ctRun
        self.glyphCount = gc = CoreText.CTRunGetGlyphCount(ctRun)

        attrs = CoreText.CTRunGetAttributes(ctRun)
        self.nsFont = attrs['NSFont']
        #self.fontDescriptor = f.fontDescriptor()
        self.fill = attrs['NSColor']
        self.nsParagraphStyle = attrs['NSParagraphStyle']


        self.iStart, self.iEnd = CoreText.CTRunGetStringRange(ctRun)
        self.string = u''
        # Hack for now to find the string in repr-string if self._ctLine.
        for index, part in enumerate(str(ctRun).split('"')[1].split('\\u')):
            if index == 0:
                self.string += part
            elif len(part) >= 4:
                self.string += unichr(int(part[0:4], 16))
                self.string += part[4:]

        self.stringIndices = CoreText.CTRunGetStringIndicesPtr(ctRun)[0:gc]
        #CoreText.CTRunGetStringIndices(ctRun._ctRun, CoreText.CFRange(0, 5), None)[4]
        self.advances = CoreText.CTRunGetAdvances(ctRun, CoreText.CFRange(0, 5), None)
        self.positions = CoreText.CTRunGetPositionsPtr(ctRun)[0:gc]
        #CoreText.CTRunGetPositions(ctRun, CoreText.CFRange(0, 5), None)[4]
        #self.glyphFontIndices = CoreText.CTRunGetGlyphsPtr(ctRun)[0:gc]
        #print(CoreText.CTRunGetGlyphs(ctRun, CoreText.CFRange(0, 5), None)[0:5])
        self.status = CoreText.CTRunGetStatus(ctRun)

    def __len__(self):
        return self.glyphCount

    def __repr__(self):
        return '[TextRun #%d "%s"]' % (self.runIndex, self.string)
    # Font stuff

    def _get_displayName(self):
        return self.nsFont.displayName()
    displayName = property(_get_displayName)

    def _get_familyName(self):
        return self.nsFont.familyName()
    familyName = property(_get_familyName)

    def _get_fontName(self):
        return self.nsFont.fontName()
    fontName = font = property(_get_fontName)

    def _get_isVertical(self):
        return self.nsFont.isVertical()
    isVertical = property(_get_isVertical)

    def _get_isFixedPitch(self):
        return self.nsFont.isFixedPitch()
    isFixedPitch = property(_get_isFixedPitch)

    def _get_boundingRectForFont(self):
        (x, y), (w, h) = self.nsFont.boundingRectForFont()
        return x, y, w, h
    boundingRectForFont = property(_get_boundingRectForFont)

    def _get_renderingMode(self):
        return self.nsFont.renderingMode()
    renderingMode = property(_get_renderingMode)

    #   Font metrics

    def _get_ascender(self):
        return self.nsFont.ascender()
    ascender = property(_get_ascender)

    def _get_descender(self):
        return self.nsFont.descender()
    descender = property(_get_descender)

    def _get_capHeight(self):
        return self.nsFont.capHeight()
    capHeight = property(_get_capHeight)

    def _get_xHeight(self):
        return self.nsFont.xHeight()
    xHeight = property(_get_xHeight)

    def _get_italicAngle(self):
        return self.nsFont.italicAngle()
    italicAngle = property(_get_italicAngle)

    def _get_fontSize(self):
        return self.nsFont.pointSize()
    fontSize = property(_get_fontSize)

    def _get_leading(self):
        return self.nsFont.leading()
    leading = property(_get_leading)

    def _get_fontMatrix(self):
        return self.nsFont.matrix()
    fontMatrix = property(_get_fontMatrix)

    def _get_textTransform(self):
        return self.nsFont.textTransform()
    textTransform = property(_get_textTransform)

    def _get_underlinePosition(self):
        return self.nsFont.underlinePosition()
    underlinePosition = property(_get_underlinePosition)

    def _get_underlineThickness(self):
        return self.nsFont.underlineThickness()
    underlineThickness = property(_get_underlineThickness)

    #   Paragraph attributes

    def _get_matrix(self):
        return CoreText.CTRunGetTextMatrix(self._ctRun)
    matrix = property(_get_matrix)

    def _get_alignment(self):
        return self.nsParagraphStyle.alignment()
    alignment = property(_get_alignment)

    def _get_lineSpacing(self):
        return self.nsParagraphStyle.lineSpacing()
    lineSpacing = property(_get_lineSpacing)

    def _get_paragraphSpacing(self):
        return self.nsParagraphStyle.paragraphSpacing()
    paragraphSpacing = property(_get_paragraphSpacing)

    def _get_paragraphSpacingBefore(self):
        return self.nsParagraphStyle.paragraphSpacingBefore()
    paragraphSpacingBefore = property(_get_paragraphSpacingBefore)

    def _get_headIndent(self):
        return self.nsParagraphStyle.headIndent()
    headIndent = property(_get_headIndent)

    def _get_tailIndent(self):
        return self.nsParagraphStyle.tailIndent()
    tailIndent = property(_get_tailIndent)

    def _get_firstLineHeadIndent(self):
        return self.nsParagraphStyle.firstLineHeadIndent()
    firstLineHeadIndent = property(_get_firstLineHeadIndent)

    def _get_leadingMultiple(self):
        return self.nsParagraphStyle.leadingMultiple()
    leadingMultiple = property(_get_leadingMultiple)

    def _get_lineSpacing(self):
        return self.nsParagraphStyle.lineSpacing()
    lineSpacing = property(_get_lineSpacing)

    def _get_maximumLeading(self):
        return self.nsParagraphStyle.maximumLeading()
    maximumLeading = property(_get_maximumLeading)

    def _get_minimumLeading(self):
        return self.nsParagraphStyle.minimumLeading()
    minimumLeading = property(_get_minimumLeading)


class TextLine:
    def __init__(self, ctLine, p, lineIndex):
        self._ctLine = ctLine
        self.x, self.y = p # Relative position from top of TextBox
        self.lineIndex = lineIndex # Vertical line index in TextBox.
        self.glyphCount = CoreText.CTLineGetGlyphCount(ctLine)

        self.string = ''
        self.runs = []
        for runIndex, ctRun in enumerate(CoreText.CTLineGetGlyphRuns(ctLine)):
            textRun = TextRun(ctRun, runIndex)
            self.runs.append(textRun)
            self.string += textRun.string

    def __repr__(self):
        return '[TextLine #%d Glyphs:%d Runs:%d]' % (self.lineIndex, self.glyphCount, len(self.runs))

    def __len__(self):
        return self.glyphCount

    def getIndexForPosition(self, xy):
        x, y = xy
        return CoreText.CTLineGetStringIndexForPosition(self._ctLine, CoreText.CGPoint(x, y))[0]

    def getOffsetForStringIndex(self, i):
        """Answer the z position that is closest to glyph string index i. If i is out of bounds,
        then answer the closest x position (left and right side of the string)."""
        return CoreText.CTLineGetOffsetForStringIndex(self._ctLine, i, None)[0]

    def _get_stringIndex(self):
        return CoreText.CTLineGetStringRange(self._ctLine).location
    stringIndex = property(_get_stringIndex)

    def getGlyphIndex2Run(self, glyphIndex):
        for run in self.runs:
            if run.iStart >= glyphIndex:
                return run
        return None

    #def _get_alignment(self):
    #    return CoreText.CTTextAlignment(self._ctLine)
    #alignment = property(_get_alignment)

    def _get_imageBounds(self):
        """Property that answers the bounding box (actual black shape) of the line."""
        (x, y), (w, h) = CoreText.CTLineGetImageBounds(self._ctLine, None)
        return x, y, w, h
    imageBounds = property(_get_imageBounds)

    def _get_bounds(self):
        """Property that returns the EM bounding box of the line."""
        return CoreText.CTLineGetTypographicBounds(self._ctLine, None, None, None)
    bounds = property(_get_bounds)

    def _get_trailingWhiteSpace(self):
        return CoreText.CTLineGetTrailingWhitespaceWidth(self._ctLine)
    trailingWhiteSpace = property(_get_trailingWhiteSpace)

    def findPattern(self, pattern):
        founds = []
        if isinstance(pattern, str):
            pattern = re.compile(pattern)
            #pattern = re.compile('([a-ZA-Z0-9\.\-\_]*])

        for iStart, iEnd in [(m.start(0), m.end(0)) for m in re.finditer(pattern, self.string)]:
            #print('fsdsdffsd', iStart, iEnd)
            xStart = self.getOffsetForStringIndex(iStart)
            xEnd = self.getOffsetForStringIndex(iEnd)
            print(xStart, xEnd)
            run = self.getGlyphIndex2Run(xStart)
            print(iStart, xStart, iEnd, xEnd, run)
            founds.append(FoundPattern(self.string[iStart:iEnd], xStart, iStart, line=self, run=run))
        return founds

class TextBox:
    """A TextBox holds a formatted string, as well as an ordered list of TextLine instances,
    that hold information about the sequence of TextRun instances (with their unique typographic
    properties). Also self.baseLines is available, ordered list of baseLine positions, relative
    to the origin of the TextBox element."""
    # @@@ This is a stand alone testing class. The real one is implemented as PageBot TextBox Element.
    def __init__(self, fs, x, y, w, h):
        self.x = x
        self.y = y
        self.z = 0
        self.w = w
        self.h = h
        self.d = 0
        self.fs = fs # Property will initialize the self.textLines upon setting self._fs

    def __len__(self):
        return len(self.textLines)

    def _get_fs(self):
        return self._fs
    def _set_fs(self, fs):
        self._fs = fs
        self.initializeTextLines()
    fs = property(_get_fs, _set_fs)

    def initializeTextLines(self):
        """Answer an ordered list of all baseline position, starting at the top."""
        self._box = self.x, self.y, self.w, self.h
        attrString = fs.getNSObject()
        setter = CoreText.CTFramesetterCreateWithAttributedString(attrString)
        path = Quartz.CGPathCreateMutable()
        Quartz.CGPathAddRect(path, None, Quartz.CGRectMake(*self._box))
        ctBox = CoreText.CTFramesetterCreateFrame(setter, (0, 0), path, None)
        self._ctLines = CoreText.CTFrameGetLines(ctBox)
        self.baseLines = [] # Contain (x, y) start position of line
        self.textLines = []
        for lineIndex, p in enumerate(CoreText.CTFrameGetLineOrigins(ctBox, (0, len(self._ctLines)), None)):
            x = p.x
            y = self.h - p.y
            ctLine = self._ctLines[lineIndex]
            textLine = TextLine(ctLine, (x, y), lineIndex)
            self.textLines.append(textLine)
            self.baseLines.append((x, y, textLine.string))

    def findPattern(self, pattern):
        """Answer the point locations where this pattern occures in the Formatted String."""
        foundPatterns = [] # List of FoundPattern instances.
        for lineIndex, textLine in enumerate(self.textLines):
            y = self.baseLines[lineIndex]
            for foundPattern in textLine.findPattern(pattern):
                foundPattern.y = y
                foundPattern.z = self.z
                foundPatterns.append(foundPattern)
        return foundPatterns

    def draw(self):
        context.textBox(self.fs, (self.x, self.y, self.w, self.h))

    def _drawBaselines(self, showIndex=False, showY=False, showLeading=False):
        # Let's see if we can draw over them in exactly the same position.
        fontSize = 8
        if showY:
            context.text(context.newString('0', style=dict(xAlign='left',
                                               font='Verdana',
                                               fontSize=8,
                                               fill=color(0, 0, 1))),
                   (self.x + self.w + 3, self.y + self.h - fontSize/4))

        prevY = 0
        for index in range(len(self)):
            _, y, _ = self.baseLines[index]
            context.line((self.x, self.y + self.h - y),
                   (self.x + self.w, self.y + self.h - y))
            if showIndex:
                context.text(context.newString('index', style=dict(xAlign='right',
                                                       font='Verdana',
                                                       fontSize=fontSize,
                                                       fill=color(0, 0, 1))),
                       (self.x-8, self.y + self.h - y - fontSize/3))
            if showY:
                context.text(context.newString('%d' % round(y),
                                   style=dict(xAlign='left',
                                              font='Verdana',
                                              fontSize=fontSize,
                                              fill=color(0, 0, 1))),
                       (self.x + self.w + 3, self.y + self.h - y - fontSize/4))
            if showLeading:
                leading = round(abs(y - prevY))
                context.text(context.newString('%d' % leading,
                                   style=dict(xAlign='left',
                                              font='Verdana',
                                              fontSize=fontSize,
                                              fill=color(1, 0, 0))),
                       (self.x + self.w + 3, self.y + self.h - prevY - leading/2 - fontSize/4))
            prevY = y

    def _drawFrame(self):
        context.stroke(0, 0, 1)
        context.fill(None)
        context.rect(self.x, self.y, self.w, self.h)


W = 400
H = 600
G = 40

context.Variable([
    dict(name='W', ui='Slider', args=dict(minValue=200, value=400, maxValue=1000)),
    dict(name='H', ui='Slider', args=dict(minValue=200, value=600, maxValue=1000)),
], globals())


fs = context.newString(u'This åéöøa hêädliñe rúns over one or more lines.\n',
                 style=dict(xAlign='left',
                            font='BitcountMonoDouble-RegularCircleItalic',
                            fontSize=24,
                            openTypeFeatures=dict(ss01=True,
                                                  ss02=True,
                                                  ss06=True),
                            leading=26,
                            tracking=1.2))
fs += context.newString(('This an example of TextLines and TextRuns'
                   ' and more and more. '),
                  style=dict(font='Verdana', fontSize=14, leading=22))
fs += context.newString('=== Find this. === ',
                  style=dict(font='Georgia-Bold', fontSize=16, leading=22))
fs += context.newString('This an example of larger TextLines and TextRuns. ',
                  style=dict(font='Georgia', fontSize=16, leading=22))
fs += context.newString('=== Find this. === ',
                  style=dict(font='Georgia-Bold', fontSize=16, leading=22))
fs += context.newString('This an example of TextLines and TextRuns. ',
                  style=dict(font='Verdana', fontSize=14, leading=22))

fittingWord = context.newString('Word\n', style=dict(font='Georgia',
                                               xAlign='left',
                                               fontSize=500))
w, _ = fittingWord.size
fittingSize = W/w*500
fittingWord = context.newString('Word\n', style=dict(font='Georgia',
                                               xAlign='left',
                                               fontSize=fittingSize,
                                               leading=fittingSize*1.2))
fs += fittingWord

fittingWord = context.newString('ABC\n',
                          style=dict(font='BitcountMonoDouble-RegularCircle',
                                     xAlign='left',
                                     fontSize=500))
w, _ = fittingWord.size
fittingSize = W/w*500
fittingWord = context.newString('ABC\n',
                          style=dict(font='BitcountMonoDouble-RegularCircle',
                                     xAlign='left',
                                     fontSize=fittingSize,
                                     leading=fittingSize))
fs += fittingWord

doc = Document(w=W+G*2, h=H + G*2, autoPages=1)
view = doc.view

page = doc[1]
myTextBox = newTextBox(fs, x=G, y=G, w=W, h=H, parent=page)
#myTextBox._drawBaselines(showIndex=True, showY=True, showLeading=True)

"""
FIX
for pattern in myTextBox.findPattern('Find'):
    #print(pattern)
    px = pattern.x
    py = pattern.y
    print(pattern)
    print(px, py[1])
    context.stroke(1, 0, 0)
    context.fill(None)
    context.oval(px-10, py[1]-10, 20, 20)

# Bitcount measures, pixels are 1/10 of Em
for yy in range(-3,10):
    context.stroke(1, 0, 0)
    context.fill(None)
    y = (myTextBox.y + myTextBox.h +
         yy*fittingSize/10 - myTextBox.baseLines[-1][1])
    context.line((myTextBox.x, y), (myTextBox.x + myTextBox.w, y))

context.saveImage('_export/testTextLineTextRun.pdf')
"""
