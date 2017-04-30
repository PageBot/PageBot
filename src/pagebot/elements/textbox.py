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
import CoreText
import Quartz

from drawBot import textOverflow, hyphenation, textBox, rect, textSize, FormattedString

from pagebot.style import LEFT, RIGHT, CENTER, NO_COLOR, MIN_WIDTH, makeStyle
from pagebot.elements.element import Element
from pagebot.toolbox.transformer import pointOffset
from pagebot import getFormattedString, setStrokeColor, setFillColor


import CoreText
import Quartz

#for name in installedFonts():
#    if 'Bitcount' in name:
#        print name
        
class TextRun(object):
    def __init__(self, ctRun, string):
        self.lineString = string
        self._ctRun = ctRun
        self.glyphCount = gc = CoreText.CTRunGetGlyphCount(ctRun)

        attrs = CoreText.CTRunGetAttributes(ctRun)
        self.nsFont = attrs['NSFont']
        #self.fontDescriptor = f.fontDescriptor()
        self.fill = attrs['NSColor']
        self.nsParagraphStyle = attrs['NSParagraphStyle']


        i1, i2 = CoreText.CTRunGetStringRange(ctRun)
        self.string = self.lineString[i1, i2]

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

    # Font stuff

    def _get_displayName(self):
        return self.nsFont.displayName()
    displayName = property(_get_displayName)

    def _get_familyName(self):
        return self.nsFont.familyName()
    familyName = property(_get_familyName)

    def _get_fontName(self):
        return self.nsFont.fontName()
    fontName = property(_get_fontName)

    def _get_isVertical(self):
        return self.nsFont.isVertical()
    isVertical = property(_get_isVertical)

    def _get_isFixedPitch(self):
        return self.nsFont.isFixedPitch()
    isFixedPitch = property(_get_isFixedPitch)

    def _get_boundingRectForFont(self):
        (x, y), (w, h) = self.nsFont.boundingRectForFont()
        return x, y, w, h
    boundingRectForFont = propert(_get_boundingRectForFont)

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
        return self.nsFont._get_fontSize()
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
    def __init__(self, ctLine):
        self._ctLine = ctLine
        self.glyphCount = CoreText.CTLineGetGlyphCount(ctLine)
        # Hack for now to find the string.
        s = []
        for index, part in enumerate(`self._ctLine`.split('"')[1].split('\\u')):
            if index == 0:
                s.append(part)
            elif len(part) >= 4:
                s.append(unichr(int(part[0:4], 16)))
                s.append(part[4:])
        self.string = ''.join(s)

        self.runs = []
        for ctRun in CoreText.CTLineGetGlyphRuns(ctLine):
            self.runs.append(TextRun(ctRun, self.string))

    def __repr__(self):
        print self._ctLine

    def __len__(self):
        return self.glyphCount

    def getIndexForPosition(self, (x, y)):
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
    u"""Answer an ordered list of all baseline position, starting at the top."""
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
#print o
#print
for tl in textLines:
    #print 'Bounds:', tl.bounds, tl.imageBounds, tl.trailingWhiteSpace, 'Len:', len(tl), 'Index:', tl.stringIndex, 
    #tl.alignment
    #print 'Index at position (100, 10):', tl.getIndexForPosition((100, 10))
    #print 'Offset at string index (0):', tl.runs
    print 'Runs:', len(tl.runs)
    print 'String:', tl.string
    for textRun in tl.runs:
        """
        print CoreText.CTRunGetTextMatrix(ctRun._ctRun)
        print CoreText.CTRunGetStringRange(ctRun._ctRun)
        print CoreText.CTRunGetStringIndicesPtr(ctRun._ctRun)[20]
        print CoreText.CTRunGetStringIndices(ctRun._ctRun, CoreText.CFRange(0, 5), None)[4]
        print CoreText.CTRunGetAdvances(ctRun._ctRun, CoreText.CFRange(0, 5), None)
        print CoreText.CTRunGetPositionsPtr(ctRun._ctRun)[20]
        print CoreText.CTRunGetPositions(ctRun._ctRun, CoreText.CFRange(0, 5), None)[4]
        print CoreText.CTRunGetGlyphsPtr(ctRun._ctRun)[20]
        print CoreText.CTRunGetGlyphs(ctRun._ctRun, CoreText.CFRange(0, 5), None)[0:5]
        print CoreText.CTRunGetStatus(ctRun._ctRun)
        print CoreText.CTRunGetAttributes(ctRun._ctRun)['NSColor']
        print CoreText.CTRunGetAttributes(ctRun._ctRun)['NSParagraphStyle']
        print CoreText.CTRunGetAttributes(ctRun._ctRun)['NSFont']
        print ctRun._ctRun
        """
        print textRun.nsFont, textRun.glyphFontIndices, textRun.positions
        print '========'
        print textRun.displayName
        print textRun.familyName
        print textRun.fontName
        print textRun.glyphCount
        print textRun.fontDescriptor
        print textRun.isFixedPitch
        print textRun.renderingMode
        print textRun.capHeight
        print textRun.ascender
        print textRun.descender
        print textRun.fontBoundingRect
        print textRun.italicAngle
        print
        #print CoreText.CTLineGetGlyphRuns(tl._ctLine)
    print #CoreText.CTLineGetStringRange(tl._ctLine)
    #print tl.string       
class TextBox(Element):

    # Initialize the default behavior tags as different from Element.
    isText = True  # This element is capable of handling text.
    isTextBox = True

    TEXT_MIN_WIDTH = 24 # Absolute minumum with of a text box.

    def __init__(self, fs, minW=None, **kwargs):
        Element.__init__(self,  **kwargs)
        # Make sure that this is a formatted string. Otherwise create it with the current style.
        # Note that in case there is potential clash in the double usage of fill and stroke.
        if isinstance(fs, str):
            fs = getFormattedString(fs, self)
        self.fs = fs
        self.minW = max(minW or 0, MIN_WIDTH, self.TEXT_MIN_WIDTH)

    def _get_h(self):
        u"""Answer the height of the textBox. If self.style['vacuumH'] is set, then answer the 
        vertical space that the text needs. This overwrites the setting of self._h."""
        if self.style.get('vacuumH'):
            return self.getTextSize()[1]
        return self.css('h')
    def _set_h(self, h):
        self.style['h'] = h # Overwrite style from here, unless self.style['vacuum'] is True
    h = property(_get_h, _set_h)

    def __len__(self):
        return len(self.fs)

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

    def getBaseLines(self):
        u"""Answer an ordered list of all baseline position, starting at the top."""
        origins = []
        box = 0, 0, self.w, self.h
        attrString = self.fs.getNSObject()
        setter = CoreText.CTFramesetterCreateWithAttributedString(attrString)
        path = Quartz.CGPathCreateMutable()
        Quartz.CGPathAddRect(path, None, Quartz.CGRectMake(*box))
        box = CoreText.CTFramesetterCreateFrame(setter, (0, 0), path, None)
        ctLines = CoreText.CTFrameGetLines(box)
        for ctLine in ctLines:
            print ctLine
        #origins = CoreText.CTFrameGetLineOrigins(box, (0, len(ctLines)), None)
        return [o.y for o in origins]

    def getTextLines(self):
        u"""Answer an ordered list of all baseline position, starting at the top."""
        box = 0, 0, self.w, self.h
        attrString = self.fs.getNSObject()
        setter = CoreText.CTFramesetterCreateWithAttributedString(attrString)
        path = Quartz.CGPathCreateMutable()
        Quartz.CGPathAddRect(path, None, Quartz.CGRectMake(*box))
        box = CoreText.CTFramesetterCreateFrame(setter, (0, 0), path, None)
        textLines = []
        for ctLine in CoreText.CTFrameGetLines(box)
            textLine.append(TextLine(ctLine))
        #origins = CoreText.CTFrameGetLineOrigins(box, (0, len(ctLines)), None)
        return textLines

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

    def draw(self, origin, view):
        u"""Draw the text on position (x, y). Draw background rectangle and/or frame if
        fill and/or stroke are defined."""
        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(p)    
        px, py, _ = self._applyAlignment(p) # Ignore z-axis for now.
   
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
        else: # If debugging,then draw the rectangle. Only self.css('showElementBox') is True
            self.drawFrame(origin)

        # If there are child elements, draw them over the text.
        self._drawElements(origin, view)

        self._restoreScale()
        view.drawElementMetaInfo(self, origin) # Depends on css flag 'showElementInfo'

        

