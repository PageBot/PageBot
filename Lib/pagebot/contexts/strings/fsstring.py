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
#     fsstring.py
#
from pagebot.contexts.strings.babelstring import BabelString
from pagebot.style import css, NO_COLOR, LEFT

class FsString(BabelString):

    BABEL_STRING_TYPE = 'fs'

    u"""FsString is a wrapper around the standard DrawBot FormattedString."""
    def __init__(self, s, context):
        self.context = context # Store the context, in case we need it.
        self.fs = s # Enclose the DrawBot FormattedString

    def _get_fs(self):
        u"""Answer the embedded FormattedString by property, to enforce checking type of the string."""
        return self.s
    def _set_fs(self, fs):
        if isinstance(fs, basestring):
            fs = self.b.FormattedString(s)
        self.s = fs
    fs = property(_get_fs, _set_fs)

    def asText(self):
        return self.s.text

    def textSize(self, w=None):
        u"""Answer the (w, h) size for a given width, with the current text."""
        return self.context.textSize(self.s, w)

    def textOverflow(self, w, h, align=LEFT):
        return self.context.textOverflow(self.fs, (0, 0, w, h), align)

def newFsString(t, context, e=None, style=None, w=None, h=None, fontSize=None, styleName=None, tagName=None):
    u"""Answer a FsString instance from valid attributes in *style*. Set all values after testing
    their existence, so they can inherit from previous style formats.
    If target width *w* or height *h* is defined, then *fontSize* is scaled to make the string fit *w* or *h*."""
    # Get the drawBotBuilder, no need to check, we already must be in context here.

    b = context.b
    b.hyphenation(css('hyphenation', e, style)) # TODO: Should be text attribute, not global

    fs = b.FormattedString('')
    sFont = css('font', e, style)
    if sFont is not None:
        fs.font(sFont)
    # Forced fontSize, then this overwrites the style['fontSize'] if it is there.
    # TODO: add calculation of rFontSize (relative float based on root-fontSize) here too.
    sFontSize = fontSize or css('fontSize', e, style) or 16 # May be scaled to fit w or h if target is defined.
    sLeading = css('leading', e, style)
    rLeading = css('rLeading', e, style)
    if sLeading or (rLeading and sFontSize):
        print '344224224', sLeading, rLeading, sFontSize
        lineHeight = (sLeading or 0) + (rLeading or 0) * (sFontSize or 0)
        if lineHeight:
            fs.lineHeight(lineHeight)
    if sFontSize is not None:
        fs.fontSize(sFontSize) # For some reason fontSize must be set after leading.
    sFallbackFont = css('fallbackFont', e, style)
    if sFallbackFont is not None:
        fs.fallbackFont(sFallbackFont)
    sFill = css('textFill', e, style)
    if sFill is not NO_COLOR: # Test on this flag, None is valid value
        context.setTextFillColor(fs, sFill)
    sCmykFill = css('cmykFill', e, style, NO_COLOR)
    if sCmykFill is not NO_COLOR:
        context.setTextFillColor(fs, sCmykFill, cmyk=True)
    sStroke = css('textStroke', e, style, NO_COLOR)
    sStrokeWidth = css('textStrokeWidth', e, style)
    if sStroke is not NO_COLOR and sStrokeWidth is not None:
        context.setTextStrokeColor(fs, sStroke, sStrokeWidth)
    sCmykStroke = css('cmykStroke', e, style, NO_COLOR)
    if sCmykStroke is not NO_COLOR:
        context.setTextStrokeColor(fs, sCmykStroke, sStrokeWidth, cmyk=True)
    sAlign = css('xTextAlign', e, style) # Warning: xAlign is used for element alignment, not text.
    if sAlign is not None: # yTextAlign must be solved by parent container element.
        fs.align(sAlign)
    sParagraphTopSpacing = css('paragraphTopSpacing', e, style)
    rParagraphTopSpacing = css('rParagraphTopSpacing', e, style)
    if sParagraphTopSpacing or (rParagraphTopSpacing and sFontSize):
        fs.paragraphTopSpacing((sParagraphTopSpacing or 0) + (rParagraphTopSpacing or 0) * (sFontSize or 0))
    sParagraphBottomSpacing = css('paragraphBottomSpacing', e, style)
    rParagraphBottomSpacing = css('rParagraphBottomSpacing', e, style)
    if sParagraphBottomSpacing or (rParagraphBottomSpacing and sFontSize):
        fs.paragraphBottomSpacing((sParagraphBottomSpacing or 0) + (rParagraphBottomSpacing or 0) * (sFontSize or 0))
    sTracking = css('tracking', e, style)
    rTracking = css('rTracking', e, style)
    if sTracking or (rTracking and sFontSize):
        fs.tracking((sTracking or 0) + (rTracking or 0) * (sFontSize or 0))
    sBaselineShift = css('baselineShift', e, style)
    rBaselineShift = css('rBaselineShift', e, style)
    if sBaselineShift or (rBaselineShift and sFontSize):
        fs.baselineShift((sBaselineShift or 0) + (rBaselineShift or 0) * (sFontSize or 0))
    sOpenTypeFeatures = css('openTypeFeatures', e, style)
    if sOpenTypeFeatures is not None:
        fs.openTypeFeatures([], **sOpenTypeFeatures)
    sTabs = css('tabs', e, style)
    if sTabs is not None:
        fs.tabs(*sTabs)
    sFirstLineIndent = css('firstLineIndent', e, style)
    rFirstLineIndent = css('rFirstLineIndent', e, style)
    # TODO: Use this value instead, if current tag is different from previous tag. How to get this info?
    # sFirstParagraphIndent = style.get('firstParagraphIndent')
    # rFirstParagraphIndent = style.get('rFirstParagraphIndent')
    # TODO: Use this value instead, if currently on top of a new string.
    sFirstColumnIndent = css('firstColumnIndent', e, style)
    rFirstColumnIndent = css('rFirstColumnIndent', e, style)
    if sFirstLineIndent or (rFirstLineIndent and sFontSize):
        fs.firstLineIndent((sFirstLineIndent or 0) + (rFirstLineIndent or 0) * (sFontSize or 0))
    sIndent = css('indent', e, style)
    rIndent = css('rIndent', e, style)
    if sIndent is not None or (rIndent is not None and sFontSize is not None):
        fs.indent((sIndent or 0) + (rIndent or 0) * (sFontSize or 0))
    sTailIndent = css('tailIndent', e, style)
    rTailIndent = css('rTaildIndent', e, style)
    if sTailIndent or (rTailIndent and sFontSize):
        fs.tailIndent((sTailIndent or 0) + (rTailIndent or 0) * (sFontSize or 0))
    sLanguage = css('language', e, style)
    if sLanguage is not None:
        fs.language(sLanguage)

    sUpperCase = css('uppercase', e, style)
    sLowercase = css('lowercase', e, style)
    sCapitalized = css('capitalized', e, style)
    if sUpperCase:
        s = s.upper()
    elif sLowercase:
        s = s.lower()
    elif sCapitalized:
        s = s.capitalize()

    newt = fs + t # Format plain string t onto new formatted fs.
    if w is not None: # There is a target width defined, calculate again with the fontSize ratio correction. 
        tw, _ = b.textSize(newt)
        fontSize = w / tw * sFontSize
        newt = newFsString(t, view, e, style, fontSize=fontSize, styleName=styleName, tagName=tagName)
    elif h is not None: # There is a target height defined, calculate again with the fontSize ratio correction. 
        _, th = b.textSize(newt)
        fontSize = h / th * sFontSize
        newt = newFsString(t, view, e, style, fontSize=fontSize, styleName=styleName, tagName=tagName)

    return FsString(newt, b)


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
        self._style = None # Property cash for constructed style from run parameters.
        self.glyphCount = gc = CoreText.CTRunGetGlyphCount(ctRun)
        # Reverse the style from 
        attrs = CoreText.CTRunGetAttributes(ctRun)
        self.nsFont = attrs['NSFont']
        #self.fontDescriptor = f.fontDescriptor()
        self.fill = attrs['NSColor']
        self.nsParagraphStyle = attrs['NSParagraphStyle']
        self.attrs = attrs # Save, in case the caller want to query run parameters.

        self.iStart, self.iEnd = CoreText.CTRunGetStringRange(ctRun)
        self.string = u''    
        # Hack for now to find the string in repr-string if self._ctLine.
        # TODO: Make a better conversion here, not relying on the format of the repr-string.
        for index, part in enumerate(`ctRun`.split('"')[1].split('\\u')):
            if index == 0:
                self.string += part
            elif len(part) >= 4:
                self.string += unichr(int(part[0:4], 16))
                self.string += part[4:]

        #print gc, len(CoreText.CTRunGetStringIndicesPtr(ctRun)), CoreText.CTRunGetStringIndicesPtr(ctRun), ctRun
        try:
            self.stringIndices = CoreText.CTRunGetStringIndicesPtr(ctRun)[0:gc]
        except TypeError:
            self.stringIndices = [0]
        #CoreText.CTRunGetStringIndices(ctRun._ctRun, CoreText.CFRange(0, 5), None)[4]
        self.advances = CoreText.CTRunGetAdvances(ctRun, CoreText.CFRange(0, 5), None)
        #self.positions = CoreText.CTRunGetPositionsPtr(ctRun)[0:gc]
        #CoreText.CTRunGetPositions(ctRun, CoreText.CFRange(0, 5), None)[4]
        #self.glyphFontIndices = CoreText.CTRunGetGlyphsPtr(ctRun)[0:gc]
        #print CoreText.CTRunGetGlyphs(ctRun, CoreText.CFRange(0, 5), None)[0:5]
        self.status = CoreText.CTRunGetStatus(ctRun)

        # get all positions
        self.positions = CoreText.CTRunGetPositions(ctRun, (0, gc), None)
        # get all glyphs
        self.glyphs = CoreText.CTRunGetGlyphs(ctRun, (0, gc), None)

    def __len__(self):
        return self.glyphCount

    def __repr__(self):
        return '[TextRun #%d "%s"]' % (self.runIndex, self.string) 

    def __getitem__(self, index):
        return self.string[index]

    def _get_style(self):
        u"""Answer the constructed style dictionary, with names that fit the standard
        PageBot style."""
        if self._style is None:
            self._style = dict(
                textFill=self.fill,
                pl=self.headIndent,
                pr=self.tailIndent,
                fontSize=self.fontSize,
                font=self.displayName,
                leading=self.leading + self.fontSize, # ??
            )
        return self._style
    style = property(_get_style)

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
        #print ctLine
        for runIndex, ctRun in enumerate(CoreText.CTLineGetGlyphRuns(ctLine)):
            textRun = TextRun(ctRun, runIndex)
            self.runs.append(textRun)
            self.string += textRun.string

    def __repr__(self):
        return '[TextLine #%d Glyphs:%d Runs:%d]' % (self.lineIndex, self.glyphCount, len(self.runs))

    def __len__(self):
        return self.glyphCount

    def __getitem__(self, index):
        return self.runs[index]
        
    def getIndexForPosition(self, (x, y)):
        return CoreText.CTLineGetStringIndexForPosition(self._ctLine, CoreText.CGPoint(x, y))[0]
    
    def getOffsetForStringIndex(self, i):
        u"""Answer the z position that is closest to glyph string index i. If i is out of bounds,
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
        for iStart, iEnd in [(m.start(0), m.end(0)) for m in re.finditer(pattern, self.string)]:
            xStart = self.getOffsetForStringIndex(iStart)
            xEnd = self.getOffsetForStringIndex(iEnd)
            #print 'xStart, xEnd', xStart, xEnd
            run = self.getGlyphIndex2Run(xStart)
            #print 'iStart, xStart', iStart, xStart, iEnd, xEnd, run
            founds.append(FoundPattern(self.string[iStart:iEnd], xStart, iStart, line=self, run=run))
        return founds

def getBaseLines(txt, box):
    u"""Answer a list of (x,y) positions of all line starts in the box. This function may become part
    of standard DrawBot in the near future."""
    x, y, w, h = box
    attrString = txt.getNSObject()
    setter = CoreText.CTFramesetterCreateWithAttributedString(attrString)
    path = Quartz.CGPathCreateMutable()
    Quartz.CGPathAddRect(path, None, Quartz.CGRectMake(*box))
    box = CoreText.CTFramesetterCreateFrame(setter, (0, 0), path, None)
    ctLines = CoreText.CTFrameGetLines(box)
    origins = CoreText.CTFrameGetLineOrigins(box, (0, len(ctLines)), None)
    return [(x + o.x, y + o.y) for o in origins]

def getTextPositionSearch(fs, w, h, search, xTextAlign=LEFT, hyphenation=True):
    u"""
    """
    bc = BaseContext()
    path = CoreText.CGPathCreateMutable()
    CoreText.CGPathAddRect(path, None, CoreText.CGRectMake(0, 0, w, h))

    attrString = bc.attributedString(fs, align=xTextAlign)
    if hyphenation and bc._state.hyphenation:
        attrString = bc.hyphenateAttributedString(attrString, w)

    txt = attrString.string()
    searchRE = re.compile(search)
    locations = []
    for found in searchRE.finditer(txt):
        locations.append((found.start(), found.end()))

    setter = CoreText.CTFramesetterCreateWithAttributedString(attrString)
    box = CoreText.CTFramesetterCreateFrame(setter, (0, 0), path, None)

    ctLines = CoreText.CTFrameGetLines(box)
    origins = CoreText.CTFrameGetLineOrigins(box, (0, len(ctLines)), None)

    rectangles = []
    for startLocation, endLocation in locations:
        minx = miny = maxx = maxy = None
        for i, (originX, originY) in enumerate(origins):
            ctLine = ctLines[i]
            bounds = CoreText.CTLineGetImageBounds(ctLine, None)
            if bounds.size.width == 0:
                continue
            _, ascent, descent, leading = CoreText.CTLineGetTypographicBounds(ctLine, None, None, None)
            height = ascent + descent
            lineRange = CoreText.CTLineGetStringRange(ctLine)
            miny = maxy = originY
            if AppKit.NSLocationInRange(startLocation, lineRange):
                minx, _ = CoreText.CTLineGetOffsetForStringIndex(ctLine, startLocation, None)

            if AppKit.NSLocationInRange(endLocation, lineRange):
                maxx, _ = CoreText.CTLineGetOffsetForStringIndex(ctLine, endLocation, None)
                rectangles.append((ctLine, (minx, miny - descent, maxx - minx, height)))

            if minx and maxx is None:
                rectangles.append((ctLine, (minx, miny - descent, bounds.size.width - minx, height)))
                minx = 0

    return rectangles

    #   F I N D

def findPattern(textLines, pattern):
    u"""Answer the point locations where this pattern occures in the Formatted String."""
    foundPatterns = [] # List of FoundPattern instances. 
    for lineIndex, textLine in enumerate(stextLines):
        for foundPattern in textLine.findPattern(pattern):
            foundPattern.y = textLine.y
            foundPattern.z = 0
            foundPatterns.append(foundPattern)
    return foundPatterns
            

