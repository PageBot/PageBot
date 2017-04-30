
import CoreText
import Quartz


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
        self.string = self.lineString[i1:i2]

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
        return '[TextLine Glyphs:%d Runs:%d]' % (self.glyphCount, len(self.runs))

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
           
class TextBox(object):
    def __init__(self, fs, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.fs = fs
    
    def __len__(self):
        return len(self.textLines)
            
    def _get_fs(self):
        return self._fs
    def _set_fs(self, fs):
        self._fs = fs
        self.initializeLineRuns()
    fs = property(_get_fs, _set_fs)
       
    def initializeLineRuns(self):
        u"""Answer an ordered list of all baseline position, starting at the top."""
        self._box = 0, 0, self.w, self.h
        attrString = fs.getNSObject()
        setter = CoreText.CTFramesetterCreateWithAttributedString(attrString)
        path = Quartz.CGPathCreateMutable()
        Quartz.CGPathAddRect(path, None, Quartz.CGRectMake(*self._box))
        ctBox = CoreText.CTFramesetterCreateFrame(setter, (0, 0), path, None)
        self._ctLines = CoreText.CTFrameGetLines(ctBox)
        self.textLines = []
        for ctLine in self._ctLines:
            self.textLines.append(TextLine(ctLine))
        self.baseLines = []
        for p in CoreText.CTFrameGetLineOrigins(ctBox, (0, len(self._ctLines)), None):
            self.baseLines.append(p.y+self.y)
    
    def draw(self):
        textBox(self.fs, (self.x, self.y, self.w, self.h))
      
    def _drawBaseline(self):
        # Let's see if we can draw over them in exactly the same position.
        for index in range(len(self)):
            y = self.baseLines[index]
            line((self.x, y), (self.x+self.w, y))

    def _drawFrame(self):
        stroke(0, 0, 1)
        fill(None)
        rect(self.x, self.y, self.w, self.h)
        
  
fs = FormattedString(u'This åéöøa hêädliñe rúns over two lines.\n', align='left', font='BitcountMonoDouble-MediumCircleItalic', fontSize=24, openTypeFeatures=dict(ss01=True, ss02=True, ss06=True), lineHeight=28, tracking=1.2)
fs = fs + FormattedString('This an example of TextLines and TextRuns. ' * 4, font='Verdana', fontSize=14, lineHeight=22)
fs = fs + FormattedString('This an example of larger TextLines and TextRuns. ' * 4, font='Georgia', fontSize=16, lineHeight=22)
fs = fs + FormattedString('This an example of TextLines and TextRuns. ' * 4, font='Verdana', fontSize=14, lineHeight=22)

W = 350
H = 500
X = 20
Y = 20
G = 20
newPage(W*2+G*3, H + G*2)
myTextBox1 = TextBox(fs, G, G, W, H)
myTextBox2 = TextBox(fs, G+W+G, G, W, H)
myTextBox1.draw()
myTextBox2.draw()
myTextBox2._drawFrame()
myTextBox2._drawBaseline()

print 'TextLines in textBox:', len(myTextBox1) # 7 text lines
for textLine in myTextBox1.textLines:
    print textLine
textLine = myTextBox1.textLines[0]
print 'TextLines[0] has %d glyphs and %d textRuns.' % (len(textLine), len(textLine.runs))   


   