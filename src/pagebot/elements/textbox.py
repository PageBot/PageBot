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
#     textbox.py
#
import re
import CoreText
import Quartz

from drawBot import textOverflow, hyphenation, textBox, rect, textSize, FormattedString, line

from pagebot.style import LEFT, RIGHT, CENTER, NO_COLOR, MIN_WIDTH, MIN_HEIGHT, makeStyle
from pagebot.elements.element import Element
from pagebot.toolbox.transformer import pointOffset
from pagebot import getFormattedString, setStrokeColor, setFillColor

class FoundPattern(object):
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
        return '[Found "%s" @ %d,%d]' % (self.s, self.x, self.y) 

class TextRun(object):
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
        for index, part in enumerate(`ctRun`.split('"')[1].split('\\u')):
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
        #print CoreText.CTRunGetGlyphs(ctRun, CoreText.CFRange(0, 5), None)[0:5]
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

    def _get_lineHeightMultiple(self):
        return self.nsParagraphStyle.lineHeightMultiple()
    lineHeightMultiple = property(_get_lineHeightMultiple)

    def _get_lineSpacing(self):
        return self.nsParagraphStyle.lineSpacing()
    lineSpacing = property(_get_lineSpacing)

    def _get_maximumLineHeight(self):
        return self.nsParagraphStyle.maximumLineHeight()
    maximumLineHeight = property(_get_maximumLineHeight)

    def _get_minimumLineHeight(self):
        return self.nsParagraphStyle.minimumLineHeight()
    minimumLineHeight = property(_get_minimumLineHeight)

        
class TextLine(object):
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

    def getIndexForPosition(self, (x, y)):
        return CoreText.CTLineGetStringIndexForPosition(self._ctLine, CoreText.CGPoint(x, y))[0]
    
    def getOffsetForStringIndex(self, i):
        u"""Answer the z position that is closest to glyph string index i. If i is out of bounds,
        then answer the closest x position (left and right side of the string)."""
        #print '=====', self._ctLine
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
        u"""Property that answers the bounding box (actual black shape) of the line."""
        (x, y), (w, h) = CoreText.CTLineGetImageBounds(self._ctLine, None)
        return x, y, w, h
    imageBounds = property(_get_imageBounds)
    
    def _get_bounds(self):
        u"""Property that returns the EM bounding box of the line."""
        return CoreText.CTLineGetTypographicBounds(self._ctLine, None, None, None)
    bounds = property(_get_bounds)
    
    def _get_trailingWhiteSpace(self):
        return CoreText.CTLineGetTrailingWhitespaceWidth(self._ctLine)
    trailingWhiteSpace = property(_get_trailingWhiteSpace)

    def findPattern(self, pattern):
        founds = []
        if isinstance(pattern, basestring):
            pattern = re.compile(pattern)
            #pattern = re.compile('([a-ZA-Z0-9\.\-\_]*])
        #print '3321123123', self.string
        for iStart, iEnd in [(m.start(0), m.end(0)) for m in re.finditer(pattern, self.string)]:
            #print 'fsdsdffsd', iStart, iEnd
            xStart = self.getOffsetForStringIndex(iStart)
            xEnd = self.getOffsetForStringIndex(iEnd)
            print xStart, xEnd
            run = self.getGlyphIndex2Run(xStart)
            print iStart, xStart, iEnd, xEnd, run
            founds.append(FoundPattern(self.string[iStart:iEnd], xStart, iStart, line=self, run=run))
        return founds
           
class TextBox(Element):

    # Initialize the default behavior tags as different from Element.
    isText = True  # This element is capable of handling text.
    isTextBox = True

    TEXT_MIN_WIDTH = 24 # Absolute minumum with of a text box.

    def __init__(self, fs, minW=None, **kwargs):
        Element.__init__(self,  **kwargs)
        # Make sure that this is a formatted string. Otherwise create it with the current style.
        # Note that in case there is potential clash in the double usage of fill and stroke.
        if isinstance(fs, basestring):
            fs = getFormattedString(fs, self)
        self.fs = fs # Keep as plain string, in case parent is not set yet.
        self.minW = max(minW or 0, MIN_WIDTH, self.TEXT_MIN_WIDTH)

    def _get_h(self):
        u"""Answer the height of the textBox. If self.style['elasticH'] is set, then answer the 
        vertical space that the text needs. This overwrites the setting of self._h."""
        if self.style.get('elasticH'):
            h = self.getTextSize()[1]
        else:
            h = self.css('h', MIN_HEIGHT)
        return min(self.maxH, max(self.minH, h)) # Should not be 0 or None
    def _set_h(self, h):
        self.style['h'] = h # Overwrite style from here, unless self.style['vacuum'] is True
    h = property(_get_h, _set_h)

    def __getitem__(self, lineIndex):
        return self.textLines[lineIndex]

    def __len__(self):
        return len(self.textLines)
            
    def _get_fs(self):
        return self._fs
    def _set_fs(self, fs):
        self._fs = fs
        self.initializeTextLines()
    fs = property(_get_fs, _set_fs)
  
    def setText(self, s):
        u"""Set the formatted string to s, using self.style."""
        self.fs = getFormattedString(s, self)

    def appendString(self, fs):
        u"""Append s to the running formatted string of the self. Note that the string
        is already assumed to be styled or can be added as plain string."""
        assert fs is not None
        if self.fs is None:
            self.fs = fs
        else:
            self.fs += fs
        return self.getOverflow(self.w, self.h)

    def appendMarker(self, markerId, arg=None):
        self.appendString(getMarker(markerId, arg=arg))

    def initializeTextLines(self):
        u"""Answer an ordered list of all baseline position, starting at the top."""
        self._box = self.x, self.y, self.w, self.h
        attrString = self._fs.getNSObject()
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
 
    def getTextSize(self, fs=None, w=None):
        """Figure out what the width/height of the text self.fs is, with or given width or
        the styled width of this text box. If fs is defined as external attribute, then the
        size of the string is answers, as if it was already inside the text box."""
        if fs is None:
            fs = self.fs
        return textSize(self.fs, width=w or self.w)

    def getOverflow(self, w=None, h=None):
        """Figure out what the overflow of the text is, with the given (w,h) or styled
        (self.w, self.h) of this text box. If self.style['vacuumH'] is True, then by
        definintion overflow will allways be empty."""
        if self.css('vacuumH'): # In case vacuumH, box will aways fit the content.
            return ''
        return textOverflow(self.fs, (0, 0, w or self.w, h or self.h), LEFT)

    def getBaselinePositions(self, y=0, w=None, h=None):
        u"""Answer the list vertical baseline positions, relative to y (default is 0)
        for the given width and height. If omitted use (self.w, self.h)"""
        baselines = []
        for _, baselineY in textBoxBaseLines(self.fs, (0, y, w or self.w, h or self.h)):
            baselines.append(baselineY)
        return baselines

    #   D R A W 

    def draw(self, origin, view):
        u"""Draw the text on position (x, y). Draw background rectangle and/or frame if
        fill and/or stroke are defined."""
        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(p)    
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.
   
        # First draw optional fill rectangle.
        sFill = self.css('fill', NO_COLOR)
        if sFill != NO_COLOR:
            setStrokeColor(None)
            setFillColor(sFill)
            rect(px, py, self.w, self.h)
        # Draw the text.    
        textBox(self.fs, (px, py, self.w, self.h))
        # Draw options stroke rectangle.
        sStroke = self.css('stroke', NO_COLOR)
        sStrokeWidth = self.css('strokeWidth')
        if sStroke != NO_COLOR and sStrokeWidth is not None:
            setStrokeColor(sStroke, sStrokeWidth)
            setFillColor(None)
            rect(px, py, self.w, self.h)

        # If there are child elements, draw them over the text.
        self._drawElements(p, view)

        # Draw markers on TextLine and TextRun positions.
        self.drawFrame(origin, view)
        self._drawBaselines(view)
 
        self._restoreScale()
        view.drawElementMetaInfo(self, origin) # Depends on css flag 'showElementInfo'

    def _drawBaselines(self, view):
        # Let's see if we can draw over them in exactly the same position.
        if not view.showTextBoxBaselines:
            return

        fontSize = self.css('baseLineMarkerSize')
        if view.showTextBoxY:
            text(FormattedString(`0`, xAlign=LEFT, 
                font='Verdana', fontSize=8, 
                fill=(0, 0, 1)), (self.x + self.w + 3,  self.y + self.h - fontSize/4))

        prevY = 0
        for index in range(len(self)):
            _, y, _ = self.baseLines[index]
            line((self.x, self.y + self.h - y), (self.x + self.w, self.y + self.h - y))
            if view.showTextBoxIndex:
                text(FormattedString(`index`, xAlign=RIGHT, font='Verdana', fontSize=fontSize, 
                    fill=(0, 0, 1)), (self.x-8, self.y + self.h - y - fontSize/3))
            if view.showTextBoxY:
                text(FormattedString('%d' % round(y), xlign=LEFT, 
                    font='Verdana', fontSize=fontSize, 
                    fill=(0, 0, 1)), (self.x + self.w + 3, self.y + self.h - y - fontSize/4))
            if view.showTextBoxLeading:
                leading = round(abs(y - prevY))
                text(FormattedString('%d' % leading, xAlign=LEFT, 
                    font='Verdana', fontSize=fontSize, 
                    fill=(1, 0, 0)), (self.x + self.w + 3, self.y + self.h - prevY - leading/2 - fontSize/4))
            prevY = y
  
    #   F I N D

    def findPattern(self, pattern):
        u"""Answer the point locations where this pattern occures in the Formatted String."""
        foundPatterns = [] # List of FoundPattern instances. 
        for lineIndex, textLine in enumerate(self.textLines):
            y = self.baseLines[lineIndex]
            for foundPattern in textLine.findPattern(pattern):
                foundPattern.y = y
                foundPattern.z = self.z
                foundPatterns.append(foundPattern)
        return foundPatterns
                


