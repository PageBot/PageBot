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
#     canvasbuilder.py
#

import AppKit
import CoreText
import Quartz
import traceback
from pagebot.contexts.builders.basebuilder import BaseBuilder
from pagebot.contexts.graphics.graphic import Graphic
from pagebot.contexts.strings.formattedstring import FormattedString
from pagebot.contexts.bezierpaths.bezierpath import BezierPath
from pagebot.contexts.color.color import *
from pagebot.errors import PageBotError
from pagebot.apps.canvas.canvas import Canvas
from pagebot.toolbox.color import noColor, cmyk2Rgb

# FIXME: using drawBot for now.
def _tryInstallFontFromFontName(fontName):
    from drawBot.drawBotDrawingTools import _drawBotDrawingTool
    return _drawBotDrawingTool._tryInstallFontFromFontName(fontName)

class CanvasBuilder(BaseBuilder):

    fileExtensions = []
    saveImageOptions = []
    validateSaveImageOptions = True

    _lineJoinStylesMap = dict(
        miter=Quartz.kCGLineJoinMiter,
        round=Quartz.kCGLineJoinRound,
        bevel=Quartz.kCGLineJoinBevel
    )

    _lineCapStylesMap = dict(
        butt=Quartz.kCGLineCapButt,
        square=Quartz.kCGLineCapSquare,
        round=Quartz.kCGLineCapRound,
    )

    _textAlignMap = FormattedString._textAlignMap
    _textTabAlignMap = FormattedString._textTabAlignMap
    _textUnderlineMap = FormattedString._textUnderlineMap

    _colorSpaceMap = dict(
        genericRGB=AppKit.NSColorSpace.genericRGBColorSpace,
        adobeRGB1998=AppKit.NSColorSpace.adobeRGB1998ColorSpace,
        sRGB=AppKit.NSColorSpace.sRGBColorSpace,
        genericGray=AppKit.NSColorSpace.genericGrayColorSpace,
        genericGamma22Gray=AppKit.NSColorSpace.genericGamma22GrayColorSpace,
    )

    _blendModeMap = dict(
        normal=Quartz.kCGBlendModeNormal,
        multiply=Quartz.kCGBlendModeMultiply,
        screen=Quartz.kCGBlendModeScreen,
        overlay=Quartz.kCGBlendModeOverlay,
        darken=Quartz.kCGBlendModeDarken,
        lighten=Quartz.kCGBlendModeLighten,
        colorDodge=Quartz.kCGBlendModeColorDodge,
        colorBurn=Quartz.kCGBlendModeColorBurn,
        softLight=Quartz.kCGBlendModeSoftLight,
        hardLight=Quartz.kCGBlendModeHardLight,
        difference=Quartz.kCGBlendModeDifference,
        exclusion=Quartz.kCGBlendModeExclusion,
        hue=Quartz.kCGBlendModeHue,
        saturation=Quartz.kCGBlendModeSaturation,
        color=Quartz.kCGBlendModeColor,
        luminosity=Quartz.kCGBlendModeLuminosity,
        clear=Quartz.kCGBlendModeClear,
        copy=Quartz.kCGBlendModeCopy,
        sourceIn=Quartz.kCGBlendModeSourceIn,
        sourceOut=Quartz.kCGBlendModeSourceOut,
        sourceAtop=Quartz.kCGBlendModeSourceAtop,
        destinationOver=Quartz.kCGBlendModeDestinationOver,
        destinationIn=Quartz.kCGBlendModeDestinationIn,
        destinationOut=Quartz.kCGBlendModeDestinationOut,
        destinationAtop=Quartz.kCGBlendModeDestinationAtop,
        xOR=Quartz.kCGBlendModeXOR,
        plusDarker=Quartz.kCGBlendModePlusDarker,
        plusLighter=Quartz.kCGBlendModePlusLighter,
    )

    _softHypen = 0x00AD

    def __init__(self):
        self.width = None
        self.height = None
        self.hasPage = False

        # Color values.
        self.fillColor = None
        self.cmykFillColor = None
        self.cmykStrokeColor = None
        self.strokeColor = None
        self.gradient = None
        self._shadow = None
        #self._cmykShadow = None
        self.strokeWidthValue = None
        self.reset()

    def _newPage(self, width, height):
        self.size(width, height)

    def _save(self):
        pass

    def _restore(self):
        pass

    def _blendMode(self, operation):
        pass

    def _clipPath(self):
        pass

    def _transform(self, matrix):
        pass

    def _textBox(self, txt, box, align):
        pass

    def _image(self, path, xy, alpha, pageNumber):
        pass

    def _frameDuration(self, seconds):
        pass

    def _reset(self, other=None):
        pass

    def _saveImage(self, path, options):
        pass

    def _printImage(self, pdf=None):
        pass

    def _linkDestination(self, name, xy):
        pass

    def _linkRect(self, name, xywh):
        pass

    #

    def reset(self):
        self._stack = []
        self._state = []
        self._graphic = Graphic()
        Color.colorSpace = self._colorSpaceMap['genericRGB']
        self._reset()

    def size(self, width=None, height=None):
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height

    def newPage(self, width=None, height=None):
        if self.width is None:
            if width is None:
                raise PageBotError("A page must have a width")
            self.width = width

        if self.height is None:
            if height is None:
                raise PageBotError("A page must have a height")
            self.height = height

        self.hasPage = True

        self.page = Canvas((0, 0, -0, -0), delegate=self,
            canvasSize=(self.width, self.height), acceptsMouseMoved=True,
            hasHorizontalScroller=True, hasVerticalScroller=True,
            autohidesScrollers=False, backgroundColor=None,
            drawsBackground=True, flipped=True)
        self._newPage(width, height)
        return self.page

    def draw(self, rect):
        try:
            for graphic in self._state:
                if graphic.path:
                    if graphic.fillColor:
                        graphic.fillColor.set()
                        graphic.path._path.fill()
                    if graphic.strokeColor:
                        graphic.strokeColor.set()
                        graphic.path._path.stroke()


        except Exception as e:
            print(traceback.format_exc())

    def update(self):
        self.page.update()

    def saveImage(self, path, options):
        if not self.hasPage:
            raise PageBotError("can't save image when no page is set")
        self._saveImage(path, options)

    def printImage(self, pdf=None):
        self._printImage(pdf)

    def frameDuration(self, seconds):
        self._frameDuration(seconds)

    def copyState(self):
        copiedState = []

        for graphic in self._state:
            copiedState.append(graphic.copy())

        return copiedState

    def save(self):
        copiedState = self.copyState()
        self._stack.append(copiedState)
        self._save()

    def restore(self):
        if not self._stack:
            raise PageBotError("can't restore graphics state: no matching save()")
        self._state = self._stack.pop()
        #self._state.update(self)
        self._restore()

    def rect(self, x, y, w, h):
        graphic = Graphic()
        path = BezierPath()
        path.rect(x, y, w, h)
        graphic.setPath(path)
        self.setColor(graphic)
        self._state.append(graphic)

    def oval(self, x, y, w, h):
        graphic = Graphic()
        path = BezierPath()
        path.oval(x, y, w, h)
        graphic.setPath(path)
        self.setColor(graphic)
        self._state.append(graphic)

    def newPath(self):
        graphic = Graphic()
        graphic.newPath()
        self.setColor(graphic)
        self._state.append(graphic)

    def getGraphic(self):
        return self._state[-1]

    def getPath(self):
        graphic = self.getGraphic()

        if graphic.path is None:
            raise PageBotError("Create a new path first")

        return graphic.path

    def moveTo(self, pt):
        path = self.getPath()
        path.moveTo(pt)

    def lineTo(self, pt):
        path = self.getPath()
        path.lineTo(pt)

    def curveTo(self, pt1, pt2, pt):
        path = self.getPath()
        path.curveTo(pt1, pt2, pt)

    def qCurveTo(self, points):
        path = self.getPath()
        path.qCurveTo(*points)

    def arc(self, center, radius, startAngle, endAngle, clockwise):
        path = self.getPath()
        path.arc(center, radius, startAngle, endAngle, clockwise)

    def arcTo(self, pt1, pt2, radius):
        path = self.getPath()
        path.arcTo(pt1, pt2, radius)

    def closePath(self):
        path = self.getPath()
        path.closePath()

    def drawPath(self, path):
        # deprecated.
        pass

    def clipPath(self, path):
        if path is not None:
            self._state.path = path
        self._clipPath()

    def colorSpace(self, colorSpace):
        if colorSpace is None:
            colorSpace = 'genericRGB'
        if colorSpace not in self._colorSpaceMap:
            raise PageBotError("'%s' is not a valid colorSpace, argument must be '%s'" % (colorSpace, "', '".join(self._colorSpaceMap.keys())))
        colorSpace = self._colorSpaceMap[colorSpace]
        self._state.setColorSpace(colorSpace)

    def blendMode(self, operation):
        self._state.blendMode = operation
        self._blendMode(operation)

    def fill(self, r, g=None, b=None, alpha=1):
        if r is None or r is noColor:
            self.fillColor = None
            print('nonoe')
            return

        self.cmykFillColor = None
        self.fillColor = Color(r, g, b, alpha)
        self.gradient = None

    def setColor(self, graphic):
        if self.fillColor:
            graphic.fillColor = self.fillColor.copy()
        if self.strokeColor:
            graphic.strokeColor = self.strokeColor.copy()
        #graphic.cmykFillColor = self.cmykFillColor
        #graphic.cmykStrokeColor = self.cmykStrokeColor
        #graphic.gradient = self.gradient
        graphic.strokeWidth = self.strokeWidthValue
        #self._state.text.strokeWidth(value)
        #graphic.text.fill(r, g, b, a)
        #graphic.text.cmykFill(c, m, y, k, a)
        #graphic.text.cmykStroke(c, m, y, k, a)
        #graphic.text.stroke(r, g, b, a)

    def cmykFill(self, c, m, y, k, a=1):

        if c is None:
            self.fill(None)
        else:
            self.cmykFillColor = CMYKColor(c, m, y, k, a)
            r, g, b = cmyk2Rgb(c, m, y, k)
            self.fillColor = Color(r, g, b, a)
            self.gradient = None

    def stroke(self, r, g=None, b=None, a=1):
        self.cmykStrokeColor = None

        if r is None:
            self.strokeColor = None
            return

        self.strokeColor = Color(r, g, b, a)

    def cmykStroke(self, c, m, y, k, a=1):

        if c is None:
            self.stroke(None)
        else:
            self.cmykStrokeColor = CMYKColor(c, m, y, k, a)
            r, g, b = cmyk2Rgb(c, m, y, k)
            self.strokeColor = Color(r, g, b, a)

    def shadow(self, offset, blur, color):
        if offset is None:
            self._shadow = None
            return
        self._shadow = Shadow(offset, blur, color)

    def cmykShadow(self, offset, blur, color):
        if offset is None:
            self._state.shadow = None
            return
        rgbColor = cmyk2Rgb(color[0], color[1], color[2], color[3])
        self._state.shadow = Shadow(offset, blur, rgbColor)
        self._state.shadow.cmykColor = self.CMYKColor(*color)

    def linearGradient(self, startPoint=None, endPoint=None, colors=None, locations=None):
        if startPoint is None:
            self._state.gradient = None
            self.fill(0)
            return
        self._state.gradient = Gradient("linear", startPoint, endPoint, colors, locations)
        self.fill(None)

    def cmykLinearGradient(self, startPoint=None, endPoint=None, colors=None, locations=None):
        if startPoint is None:
            self._state.gradient = None
            self.fill(0)
            return
        rgbColors = [cmyk2Rgb(color[0], color[1], color[2], color[3]) for color in colors]
        self._state.gradient = Gradient("linear", startPoint, endPoint, rgbColors, locations)
        self._state.gradient.cmykColors = [self.CMYKColor(*color) for color in colors]
        self.fill(None)

    def radialGradient(self, startPoint=None, endPoint=None, colors=None, locations=None, startRadius=0, endRadius=100):
        if startPoint is None:
            self._state.gradient = None
            self.fill(0)
            return
        self._state.gradient = Gradient("radial", startPoint, endPoint, colors, locations, startRadius, endRadius)
        self.fill(None)

    def cmykRadialGradient(self, startPoint=None, endPoint=None, colors=None, locations=None, startRadius=0, endRadius=100):
        if startPoint is None:
            self._state.gradient = None
            self.fill(0)
            return
        rgbColors = [cmyk2Rgb(color[0], color[1], color[2], color[3]) for color in colors]
        self._state.gradient = Gradient("radial", startPoint, endPoint, rgbColors, locations, startRadius, endRadius)
        self._state.gradient.cmykColors = [self.CMYKColor(*color) for color in colors]
        self.fill(None)

    def strokeWidth(self, value):
        self.strokeWidthValue = value

    def miterLimit(self, value):
        self._state.miterLimit = value

    def lineJoin(self, join):
        if join is None:
            self._state.lineJoin = None
        if join not in self._lineJoinStylesMap:
            raise PageBotError("lineJoin() argument must be 'bevel', 'miter' or 'round'")
        self._state.lineJoin = self._lineJoinStylesMap[join]

    def lineCap(self, cap):
        if cap is None:
            self._state.lineCap = None
        if cap not in self._lineCapStylesMap:
            raise PageBotError("lineCap() argument must be 'butt', 'square' or 'round'")
        self._state.lineCap = self._lineCapStylesMap[cap]

    def lineDash(self, dash):
        if dash[0] is None:
            self._state.lineDash = None
            return
        self._state.lineDash = list(dash)

    def transform(self, matrix):
        self._transform(matrix)

    def font(self, fontName, fontSize):
        return self._state.text.font(fontName, fontSize)

    def fallbackFont(self, fontName):
        self._state.text.fallbackFont(fontName)

    def fontSize(self, fontSize):
        self._state.text.fontSize(fontSize)

    def lineHeight(self, lineHeight):
        self._state.text.lineHeight(lineHeight)

    def tracking(self, tracking):
        self._state.text.tracking(tracking)

    def baselineShift(self, baselineShift):
        self._state.text.baselineShift(baselineShift)

    def underline(self, underline):
        self._state.text.underline(underline)

    def hyphenation(self, value):
        self._state.hyphenation = value

    def tabs(self, *tabs):
        self._state.text.tabs(*tabs)

    def language(self, language):
        self._state.text.language(language)

    def openTypeFeatures(self, *args, **features):
        return self._state.text.openTypeFeatures(*args, **features)

    def fontVariations(self, *args, **axes):
        return self._state.text.fontVariations(*args, **axes)

    def attributedString(self, txt, align=None):
        if isinstance(txt, FormattedString):
            return txt.getNSObject()
        self._state.text.clear()
        self._state.text.append(txt, align=align)
        return self._state.text.getNSObject()

    def hyphenateAttributedString(self, attrString, path):
        # add soft hyphens
        attrString = attrString.mutableCopy()
        mutString = attrString.mutableString()
        wordRange = AppKit.NSMakeRange(mutString.length(), 0)
        while wordRange.location > 2:
            wordRange = attrString.doubleClickAtIndex_(wordRange.location - 2)
            hyphenIndex = AppKit.NSMaxRange(wordRange)
            while hyphenIndex != AppKit.NSNotFound:
                hyphenIndex = attrString.lineBreakByHyphenatingBeforeIndex_withinRange_(hyphenIndex, wordRange)
                if hyphenIndex != AppKit.NSNotFound:
                    mutString.insertString_atIndex_(chr(self._softHypen), hyphenIndex)

        # get the lines
        lines = self._getTypesetterLinesWithPath(attrString, path)
        # get all lines justified
        justifiedLines = self._getTypesetterLinesWithPath(self._justifyAttributedString(attrString), path)

        # loop over all lines
        i = 0
        while i < len(lines):
            # get the current line
            line = lines[i]
            # get the range in the text for the current line
            rng = CoreText.CTLineGetStringRange(line)
            # get the substring from the range
            subString = attrString.attributedSubstringFromRange_(rng)
            # get the string
            subStringText = subString.string()
            # check if the line ends with a softhypen
            if subStringText and subStringText[-1] == chr(self._softHypen):
                # here we go
                # get the justified line and get the max line width
                maxLineWidth, a, d, l = CoreText.CTLineGetTypographicBounds(justifiedLines[i], None, None, None)
                # get the last attributes
                hyphenAttr, _ = subString.attributesAtIndex_effectiveRange_(0, None)
                # create a hyphen string
                hyphenAttrString = AppKit.NSAttributedString.alloc().initWithString_attributes_("-", hyphenAttr)
                # get the width of the hyphen
                hyphenWidth = hyphenAttrString.size().width
                # get all line break location of that line
                lineBreakLocation = len(subString)
                possibleLineBreaks = [lineBreakLocation]
                while lineBreakLocation:
                    lineBreakLocation = subString.lineBreakBeforeIndex_withinRange_(lineBreakLocation, (0, len(subString)))
                    if lineBreakLocation:
                        possibleLineBreaks.append(lineBreakLocation)
                breakFound = False
                # loop over all possible line breaks
                while possibleLineBreaks:
                    lineBreak = possibleLineBreaks.pop(0)
                    # get a possible line
                    breakString = subString.attributedSubstringFromRange_((0, lineBreak))
                    # get the width
                    stringWidth = breakString.size().width
                    # add hyphen width if required
                    if breakString.string()[-1] == chr(self._softHypen):
                        stringWidth += hyphenWidth
                    # found a break
                    if stringWidth <= maxLineWidth:
                        breakFound = True
                        break

                if breakFound and len(breakString.string()) > 2 and breakString.string()[-1] == chr(self._softHypen):
                    # if the break line ends with a soft hyphen
                    # add a hyphen
                    attrString.replaceCharactersInRange_withString_((rng.location + lineBreak, 0), "-")
                # remove all soft hyphens for the range of that line
                mutString.replaceOccurrencesOfString_withString_options_range_(chr(self._softHypen), "", AppKit.NSLiteralSearch, rng)
                # reset the lines, from the adjusted attribute string
                lines = self._getTypesetterLinesWithPath(attrString, path)
                # reset the justifed lines form the adjusted attributed string
                justifiedLines = self._getTypesetterLinesWithPath(self._justifyAttributedString(attrString), path)
            # next line
            i += 1
        # remove all soft hyphen
        mutString.replaceOccurrencesOfString_withString_options_range_(chr(self._softHypen), "", AppKit.NSLiteralSearch, (0, mutString.length()))
        # done!
        return attrString

    def clippedText(self, txt, box, align):
        path, origin = self._getPathForFrameSetter(box)
        attrString = self.attributedString(txt, align=align)
        if self._state.hyphenation:
            hyphenIndexes = [i for i, c in enumerate(attrString.string()) if c == "-"]
            attrString = self.hyphenateAttributedString(attrString, path)
        setter = CoreText.CTFramesetterCreateWithAttributedString(attrString)
        box = CoreText.CTFramesetterCreateFrame(setter, (0, 0), path, None)
        visibleRange = CoreText.CTFrameGetVisibleStringRange(box)
        clip = visibleRange.length
        if self._state.hyphenation:
            subString = attrString.string()[:clip]
            for i in hyphenIndexes:
                if i < clip:
                    clip += 1
                else:
                    break
            clip -= subString.count("-")
        return txt[clip:]

    def _justifyAttributedString(self, attr):
        # create a justified copy of the attributed string
        attr = attr.mutableCopy()

        def changeParaAttribute(para, rng, _):
            para = para.mutableCopy()
            para.setAlignment_(AppKit.NSJustifiedTextAlignment)
            attr.addAttribute_value_range_(AppKit.NSParagraphStyleAttributeName, para, rng)

        attr.enumerateAttribute_inRange_options_usingBlock_(AppKit.NSParagraphStyleAttributeName, (0, len(attr)), 0, changeParaAttribute)
        return attr

    def _getTypesetterLinesWithPath(self, attrString, path, offset=None):
        # get lines for an attribute string with a given path
        if offset is None:
            offset = 0, 0
        setter = CoreText.CTFramesetterCreateWithAttributedString(attrString)
        frame = CoreText.CTFramesetterCreateFrame(setter, offset, path, None)
        return CoreText.CTFrameGetLines(frame)

    def _getPathForFrameSetter(self, box):
        if isinstance(box, BezierPath):
            path = box._getCGPath()
            (x, y), (w, h) = CoreText.CGPathGetPathBoundingBox(path)
        else:
            x, y, w, h = box
            path = CoreText.CGPathCreateMutable()
            CoreText.CGPathAddRect(path, None, CoreText.CGRectMake(x, y, w, h))
        return path, (x, y)

    def textSize(self, txt, align, width, height):
        attrString = self.attributedString(txt, align)
        if width is None:
            w, h = attrString.size()
        else:
            if width is None:
                width = CoreText.CGFLOAT_MAX
            if height is None:
                height = CoreText.CGFLOAT_MAX
            if self._state.hyphenation:
                path = CoreText.CGPathCreateMutable()
                CoreText.CGPathAddRect(path, None, CoreText.CGRectMake(0, 0, width, height))
                attrString = self.hyphenateAttributedString(attrString, path)
            setter = CoreText.CTFramesetterCreateWithAttributedString(attrString)
            (w, h), _ = CoreText.CTFramesetterSuggestFrameSizeWithConstraints(setter, (0, 0), None, (width, height), None)
        return w, h

    def textBox(self, txt, box, align="left"):
        self._state.path = None
        self._textBox(txt, box, align)

    def image(self, path, xy, alpha, pageNumber):
        x, y = xy
        self._image(path, (x, y), alpha, pageNumber)

    def installFont(self, path):
        url = AppKit.NSURL.fileURLWithPath_(path)
        success, error = CoreText.CTFontManagerRegisterFontsForURL(url, CoreText.kCTFontManagerScopeProcess, None)
        if not success:
            error = error.localizedDescription()
        return success, error

    def uninstallFont(self, path):
        url = AppKit.NSURL.fileURLWithPath_(path)
        success, error = CoreText.CTFontManagerUnregisterFontsForURL(url, CoreText.kCTFontManagerScopeProcess, None)
        if not success:
            error = error.localizedDescription()
        return success, error

    def _fontNameForPath(self, path):
        from fontTools.ttLib import TTFont, TTLibError
        try:
            font = TTFont(path, fontNumber=0)  # in case of .ttc, use the first font
            psName = font["name"].getName(6, 1, 0)
            if psName is None:
                psName = font["name"].getName(6, 3, 1)
            font.close()
        except IOError:
            raise PageBotError("Font '%s' does not exist." % path)
        except TTLibError:
            raise PageBotError("Font '%s' is not a valid font." % path)
        if psName is not None:
            psName = psName.toUnicode()
        return psName

    def linkDestination(self, name, xy):
        x, y = xy
        self._linkDestination(name, (x, y))

    def linkRect(self, name, xywh):
        x, y, w, h = xywh
        self._linkRect(name, (x, y, w, h))
