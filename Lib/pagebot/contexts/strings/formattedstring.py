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
#     formattedstring.py
#
import sys, os
import AppKit
import CoreText
from pagebot.contexts.color.color import *
from pagebot.errors import PageBotError
import logging
from drawBot.context.tools.openType import getFeatureTagsForFontName, featureMap
from drawBot.context.tools.variation import *

logger = logging.getLogger(__name__)
_FALLBACKFONT = "LucidaGrande"

class Warnings():
    # NOTE: Temporary solution for now, need to switch to logging.

    def __init__(self):
        self._warnMessages = set()
        self.shouldShowWarnings = False

    def resetWarnings(self):
        self._warnMessages = set()

    def warn(self, message):
        if not self.shouldShowWarnings:
            return
        if message in self._warnMessages:
            return
        sys.stderr.write("*** warning: %s ***\n" % message)
        self._warnMessages.add(message)

warnings = Warnings()

def _tryInstallFontFromFontName(fontName):
    # TODO: too much drawBot, need to port.
    try:
        from drawBot.drawBotDrawingTools import _drawBotDrawingTool
        return _drawBotDrawingTool._tryInstallFontFromFontName(fontName)
    except Exception as e:
        logger.error('_tryInstallFontFromFontName: %s', e)

class FormattedString:
    """FormattedString is a reusable object, if you want to draw the same over
    and over again. FormattedString objects can be drawn with the `text(txt,
    (x, y))` and `textBox(txt, (x, y, w, h))` methods."""

    _colorClass = Color
    _cmykColorClass = CMYKColor

    _textAlignMap = dict(
        center=AppKit.NSCenterTextAlignment,
        left=AppKit.NSLeftTextAlignment,
        right=AppKit.NSRightTextAlignment,
        justified=AppKit.NSJustifiedTextAlignment,
    )

    _textTabAlignMap = dict(
        center=AppKit.NSCenterTextAlignment,
        left=AppKit.NSLeftTextAlignment,
        right=AppKit.NSRightTextAlignment,
    )

    _textUnderlineMap = dict(
        single=AppKit.NSUnderlineStyleSingle,
        # thick=AppKit.NSUnderlineStyleThick,
        # double=AppKit.NSUnderlineStyleDouble,
        # solid=AppKit.NSUnderlinePatternSolid,
        # dotted=AppKit.NSUnderlinePatternDot,
        # dashed=AppKit.NSUnderlinePatternDash,
        # dotDashed=AppKit.NSUnderlinePatternDashDot,
        # dotDotted=AppKit.NSUnderlinePatternDashDotDot,
        # byWord=0x8000 # AppKit.NSUnderlineByWord,
    )

    _formattedAttributes = dict(
        font=_FALLBACKFONT,
        fallbackFont=None,
        fontSize=10,

        fill=(0, 0, 0),
        cmykFill=None,
        stroke=None,
        cmykStroke=None,
        strokeWidth=1,

        align=None,
        lineHeight=None,
        tracking=None,
        baselineShift=None,
        underline=None,
        openTypeFeatures=dict(),
        fontVariations=dict(),
        tabs=None,
        indent=None,
        tailIndent=None,
        firstLineIndent=None,
        paragraphTopSpacing=None,
        paragraphBottomSpacing=None,

        language=None,
    )

    def __init__(self, txt=None, **kwargs):
        self.clear()
        # create all _<attributes> in the formatted text object
        # with default values
        for key, value in self._formattedAttributes.items():
            if isinstance(value, dict):
                value = dict(value)
            if isinstance(value, list):
                value = list(value)
            setattr(self, "_%s" % key, value)
        attributes = self._validateAttributes(kwargs, addDefaults=False)
        if txt:
            self.append(txt, **attributes)
        else:
            # call each method with the provided value
            for key, value in attributes.items():
                self._setAttribute(key, value)
            self._setColorAttributes(attributes)

    def _setAttribute(self, attribute, value):
        method = getattr(self, attribute)
        if isinstance(value, (list, tuple)):
            method(*value)
        elif isinstance(value, dict):
            method(**value)
        else:
            method(value)

    def _setColorAttributes(self, attributes):
        colorAttributeNames = ("fill", "stroke", "cmykFill", "cmykStroke")
        for key in colorAttributeNames:
            value = attributes.get(key)
            if value is not None:
                setattr(self, "_%s" % key, value)

        if self._fill is not None:
            try:
                len(self._fill)
            except Exception:
                self._fill = (self._fill,)
        if self._stroke is not None:
            try:
                len(self._stroke)
            except Exception:
                self._stroke = (self._stroke,)
        if self._fill:
            self._cmykFill = None
        elif self._cmykFill:
            self._fill = None

        if self._stroke:
            self._cmykStroke = None
        elif self._cmykStroke:
            self._stroke = None

    def _validateAttributes(self, attributes, addDefaults=True):
        for attribute in attributes:
            if attribute not in self._formattedAttributes:
                raise TypeError("FormattedString got an unexpected keyword argument '%s'" % attribute)
        result = dict()
        if addDefaults:
            for key, value in self._formattedAttributes.items():
                if isinstance(value, dict):
                    value = dict(value)
                elif isinstance(value, list):
                    value = list(value)
                result[key] = value
        result.update(attributes)
        return result

    def clear(self):
        self._attributedString = AppKit.NSMutableAttributedString.alloc().init()
        self._openTypeFeatures = None

    def append(self, txt, **kwargs):
        """
        Add `txt` to the formatted string with some additional text formatting attributes:

        * `font`: the font to be used for the given text, if a font path is given the font will be installed and used directly.
        * `fallbackFont`: the fallback font
        * `fontSize`: the font size to be used for the given text
        * `fill`: the fill color to be used for the given text
        * `cmykFill`: the cmyk fill color to be used for the given text
        * `stroke`: the stroke color to be used for the given text
        * `cmykStroke`: the cmyk stroke color to be used for the given text
        * `strokeWidth`: the strokeWidth to be used for the given text
        * `align`: the alignment to be used for the given text
        * `lineHeight`: the lineHeight to be used for the given text
        * `tracking`: set tracking for the given text
        * `baselineShift`: set base line shift for the given text
        * `openTypeFeatures`: enable OpenType features
        * `fontVariations`: pick a variation by axes values
        * `tabs`: enable tabs
        * `indent`: the indent of a paragraph
        * `tailIndent`: the tail indent of a paragraph
        * `firstLineIndent`: the first line indent of a paragraph
        * `paragraphTopSpacing`: the spacing at the top of a paragraph
        * `paragraphBottomSpacing`: the spacing at the bottom of a paragraph
        * `language`: the language of the text

        All formatting attributes follow the same notation as other similar DrawBot methods.
        A color is a tuple of `(r, g, b, alpha)`, and a cmykColor is a tuple of `(c, m, y, k, alpha)`.

        Text can also be added with `formattedString += "hello"`. It will append the text with the current settings of the formatted string.
        """
        attributes = self._validateAttributes(kwargs, addDefaults=False)

        for key, value in attributes.items():
            self._setAttribute(key, value)

        self._setColorAttributes(attributes)

        if isinstance(txt, FormattedString):
            self._attributedString.appendAttributedString_(txt.getNSObject())
            return

        attributes = {}

        if self._font:
            font = AppKit.NSFont.fontWithName_size_(self._font, self._fontSize)
            if font is None:
                ff = self._fallbackFont
                if ff is None:
                    ff = _FALLBACKFONT
                warnings.warn("font: '%s' is not installed, back to the fallback font: '%s'" % (self._font, ff))
                font = AppKit.NSFont.fontWithName_size_(ff, self._fontSize)
            coreTextfeatures = []

            if self._openTypeFeatures:
                existingOpenTypeFeatures = getFeatureTagsForFontName(self._font)
                # sort features by their on/off state
                # set all disabled features first
                orderedOpenTypeFeatures = sorted(self._openTypeFeatures.items(), key=lambda kv: kv[1])
                for featureTag, value in orderedOpenTypeFeatures:
                    coreTextFeatureTag = featureTag
                    if not value:
                        coreTextFeatureTag = "%s_off" % featureTag
                    if coreTextFeatureTag in featureMap:
                        if value and featureTag not in existingOpenTypeFeatures:
                            # only warn when the feature is on and not existing for the current font
                            warnings.warn("OpenType feature '%s' not available for '%s'" % (featureTag, self._font))
                        feature = featureMap[coreTextFeatureTag]
                        coreTextfeatures.append(feature)
                    else:
                        warnings.warn("OpenType feature '%s' not available" % (featureTag))
            coreTextFontVariations = dict()
            if self._fontVariations:
                existingAxes = getVariationAxesForFontName(self._font)
                for axis, value in self._fontVariations.items():
                    if axis in existingAxes:
                        existinsAxis = existingAxes[axis]
                        # clip variation value within the min max value
                        if value < existinsAxis["minValue"]:
                            value = existinsAxis["minValue"]
                        if value > existinsAxis["maxValue"]:
                            value = existinsAxis["maxValue"]
                        coreTextFontVariations[convertVariationTagToInt(axis)] = value
                    else:
                        warnings.warn("variation axis '%s' not available for '%s'" % (axis, self._font))
            fontAttributes = {}
            if coreTextfeatures:
                fontAttributes[CoreText.NSFontFeatureSettingsAttribute] = coreTextfeatures
            if coreTextFontVariations:
                fontAttributes[CoreText.NSFontVariationAttribute] = coreTextFontVariations
            if self._fallbackFont:
                fontAttributes[CoreText.NSFontCascadeListAttribute] = [AppKit.NSFontDescriptor.fontDescriptorWithName_size_(self._fallbackFont, self._fontSize)]
            fontDescriptor = font.fontDescriptor()
            fontDescriptor = fontDescriptor.fontDescriptorByAddingAttributes_(fontAttributes)
            font = AppKit.NSFont.fontWithDescriptor_size_(fontDescriptor, self._fontSize)
            attributes[AppKit.NSFontAttributeName] = font
        elif self._fontSize:
            font = AppKit.NSFont.fontWithName_size_(_FALLBACKFONT, self._fontSize)
            attributes[AppKit.NSFontAttributeName] = font
        if self._fill or self._cmykFill:
            if self._fill:
                fillColor = self._colorClass.getColor(self._fill).getNSObject()
            elif self._cmykFill:
                fillColor = self._cmykColorClass.getColor(self._cmykFill).getNSObject()
            attributes[AppKit.NSForegroundColorAttributeName] = fillColor
        else:
            # Seems like the default foreground color is black. Set clear
            # color when the fill is None.
            attributes[AppKit.NSForegroundColorAttributeName] = AppKit.NSColor.clearColor()

        if self._stroke or self._cmykStroke:
            if self._stroke:
                strokeColor = self._colorClass.getColor(self._stroke).getNSObject()
            elif self._cmykStroke:
                strokeColor = self._cmykColorClass.getColor(self._cmykStroke).getNSObject()

            attributes[AppKit.NSStrokeColorAttributeName] = strokeColor

            # stroke width must be negative
            # Supply a negative value for NSStrokeWidthAttributeName
            # when you wish to draw a string that is both filled and stroked.
            # see https://developer.apple.com/library/content/qa/qa1531/_index.html
            attributes[AppKit.NSStrokeWidthAttributeName] = -abs(self._strokeWidth)

        para = AppKit.NSMutableParagraphStyle.alloc().init()

        if self._align:
            para.setAlignment_(self._textAlignMap[self._align])

        if self._tabs:
            for tabStop in para.tabStops():
                para.removeTabStop_(tabStop)

            if len(self._tabs) < 12:
                self._tabs = list(self._tabs)
                # add tab stops if there is not enough stops...
                # the default is 12 tabs, so lets add 12 in steps of 28
                lastTabValue = self._tabs[-1][0]
                for tabIndex in range(12 - len(self._tabs)):
                    self._tabs.append((lastTabValue + 28 * (tabIndex + 1), "left"))

            for tab, tabAlign in self._tabs:
                tabOptions = None
                if tabAlign in self._textTabAlignMap:
                    tabAlign = self._textTabAlignMap[tabAlign]
                else:
                    tabCharSet = AppKit.NSCharacterSet.characterSetWithCharactersInString_(tabAlign)
                    tabOptions = {AppKit.NSTabColumnTerminatorsAttributeName: tabCharSet}
                    tabAlign = self._textAlignMap["right"]
                tabStop = AppKit.NSTextTab.alloc().initWithTextAlignment_location_options_(tabAlign, tab, tabOptions)
                para.addTabStop_(tabStop)
        if self._lineHeight is not None:
            # para.setLineSpacing_(0.0)
            # para.setLineHeightMultiple_(1)
            para.setMinimumLineHeight_(self._lineHeight)
            para.setMaximumLineHeight_(self._lineHeight)

        if self._indent is not None:
            para.setHeadIndent_(self._indent)
            para.setFirstLineHeadIndent_(self._indent)
        if self._tailIndent is not None:
            para.setTailIndent_(self._tailIndent)
        if self._firstLineIndent is not None:
            para.setFirstLineHeadIndent_(self._firstLineIndent)

        if self._paragraphTopSpacing is not None:
            para.setParagraphSpacingBefore_(self._paragraphTopSpacing)
        if self._paragraphBottomSpacing is not None:
            para.setParagraphSpacing_(self._paragraphBottomSpacing)

        if self._tracking:
            attributes[AppKit.NSKernAttributeName] = self._tracking
        if self._baselineShift is not None:
            attributes[AppKit.NSBaselineOffsetAttributeName] = self._baselineShift
        if self._underline in self._textUnderlineMap:
            attributes[AppKit.NSUnderlineStyleAttributeName] = self._textUnderlineMap[self._underline]
        if self._language:
            attributes["NSLanguage"] = self._language
        attributes[AppKit.NSParagraphStyleAttributeName] = para
        txt = AppKit.NSAttributedString.alloc().initWithString_attributes_(txt, attributes)
        self._attributedString.appendAttributedString_(txt)

    def __add__(self, txt):
        new = self.copy()
        if isinstance(txt, self.__class__):
            new.getNSObject().appendAttributedString_(txt.getNSObject())
        else:
            if not isinstance(txt, str):
                raise TypeError("FormattedString requires a string, got '%s'" % type(txt))
            new.append(txt)
        return new

    def __getitem__(self, index):
        if isinstance(index, slice):
            start = index.start
            stop = index.stop
            textLength = len(self)

            if start is None:
                start = 0
            elif start < 0:
                start = textLength + start
            elif start > textLength:
                start = textLength

            if stop is None:
                stop = textLength
            elif stop < 0:
                stop = textLength + stop

            if start + (stop - start) > textLength:
                stop = textLength

            location = start
            length = stop - start

            if location < 0:
                location = 0
            if length > textLength:
                length = textLength
            elif length < 0:
                length = 0

            rng = location, length
            attributes = {key: getattr(self, "_%s" % key) for key in self._formattedAttributes}
            new = self.__class__(**attributes)
            try:
                new._attributedString = self._attributedString.attributedSubstringFromRange_(rng)
            except Exception:
                pass
            return new
        else:
            text = self._attributedString.string()
            return text[index]

    def __len__(self):
        return self._attributedString.length()

    def __repr__(self):
        return self._attributedString.string()

    def font(self, font, fontSize=None):
        """
        Set a font with the name of the font.
        If a font path is given the font will be installed and used directly.
        Optionally a `fontSize` can be set directly.
        The default font, also used as fallback font, is 'LucidaGrande'.
        The default `fontSize` is 10pt.

        The name of the font relates to the font's postscript name.

        The font name is returned, which is handy when the font was loaded
        from a path.
        """
        font = _tryInstallFontFromFontName(font)
        font = str(font)
        self._font = font
        if fontSize is not None:
            self._fontSize = fontSize
        return font

    def fallbackFont(self, font):
        """
        Set a fallback font, used whenever a glyph is not available in the normal font.
        If a font path is given the font will be installed and used directly.
        """
        if font:
            font = _tryInstallFontFromFontName(font)
            font = str(font)
            testFont = AppKit.NSFont.fontWithName_size_(font, self._fontSize)
            if testFont is None:
                raise PageBotError("Fallback font '%s' is not available" % font)
        self._fallbackFont = font
        return font

    def fontSize(self, fontSize):
        """
        Set the font size in points.
        The default `fontSize` is 10pt.
        """
        self._fontSize = fontSize

    def fill(self, *fill):
        """
        Sets the fill color with a `red`, `green`, `blue` and `alpha` value.
        Each argument must a value float between 0 and 1.
        """
        if fill and fill[0] is None:
            fill = None
        self._fill = fill
        self._cmykFill = None

    def stroke(self, *stroke):
        """
        Sets the stroke color with a `red`, `green`, `blue` and `alpha` value.
        Each argument must a value float between 0 and 1.
        """
        if stroke and stroke[0] is None:
            stroke = None
        self._stroke = stroke
        self._cmykStroke = None

    def cmykFill(self, *cmykFill):
        """
        Set a fill using a CMYK color before drawing a shape. This is handy if the file is intended for print.

        Sets the CMYK fill color. Each value must be a float between 0.0 and 1.0.
        """
        if cmykFill and cmykFill[0] is None:
            cmykFill = None
        self._cmykFill = cmykFill
        self._fill = None

    def cmykStroke(self, *cmykStroke):
        """
        Set a stroke using a CMYK color before drawing a shape. This is handy if the file is intended for print.

        Sets the CMYK stroke color. Each value must be a float between 0.0 and 1.0.
        """
        if cmykStroke and cmykStroke[0] is None:
            cmykStroke = None
        self._cmykStroke = cmykStroke
        self._stroke = None

    def strokeWidth(self, strokeWidth):
        """
        Sets stroke width.
        """
        self._strokeWidth = strokeWidth

    def align(self, align):
        """
        Sets the text alignment.
        Possible `align` values are: `left`, `center` and `right`.
        """
        self._align = align

    def lineHeight(self, lineHeight):
        """
        Set the line height.
        """
        self._lineHeight = lineHeight

    def tracking(self, tracking):
        """
        Set the tracking between characters.
        """
        self._tracking = tracking

    def baselineShift(self, baselineShift):
        """
        Set the shift of the baseline.
        """
        self._baselineShift = baselineShift

    def underline(self, underline):
        """
        Set the underline value.
        Underline must be `single` or `None`.
        """
        self._underline = underline

    def openTypeFeatures(self, *args, **features):
        """
        Enable OpenType features and return the current openType features settings.

        If no arguments are given `openTypeFeatures()` will just return the current openType features settings.

        .. downloadcode:: openTypeFeaturesFormattedString.py

            size(1000, 200)
            # create an empty formatted string object
            t = FormattedString()
            # set a font
            t.font("ACaslonPro-Regular")
            # set a font size
            t.fontSize(60)
            # add some text
            t += "0123456789 Hello"
            # enable some open type features
            t.openTypeFeatures(smcp=True, lnum=True)
            # add some text
            t += " 0123456789 Hello"
            # draw the formatted string
            text(t, (10, 80))
        """
        if args and features:
            raise PageBotError("Can't combine positional arguments and keyword arguments")
        if args:
            if len(args) != 1:
                raise PageBotError("There can only be one positional argument")
            if args[0] is not None:
                raise PageBotError("First positional argument can only be None")
            warnings.warn("openTypeFeatures(None) is deprecated, use openTypeFeatures(resetFeatures=True) instead.")
            self._openTypeFeatures.clear()
        else:
            if features.pop("resetFeatures", False):
                self._openTypeFeatures.clear()
            self._openTypeFeatures.update(features)
        currentFeatures = self.listOpenTypeFeatures()
        currentFeatures.update(self._openTypeFeatures)
        return currentFeatures

    def listOpenTypeFeatures(self, fontName=None):
        """
        List all OpenType feature tags for the current font.

        Optionally a `fontName` can be given. If a font path is given the font will be installed and used directly.
        """
        if fontName:
            fontName = _tryInstallFontFromFontName(fontName)
        else:
            fontName = self._font
        return getFeatureTagsForFontName(fontName)

    def fontVariations(self, *args, **axes):
        """
        Pick a variation by axes values and return the current font variations settings.

        If no arguments are given `fontVariations()` will just return the current font variations settings.
        """
        if args and axes:
            raise PageBotError("Can't combine positional arguments and keyword arguments")
        if args:
            if len(args) != 1:
                raise PageBotError("There can only be one positional argument")
            if args[0] is not None:
                raise PageBotError("First positional argument can only be None")
            warnings.warn("fontVariations(None) is deprecated, use fontVariations(resetVariations=True) instead.")
            self._fontVariations.clear()
        else:
            if axes.pop("resetVariations", False):
                self._fontVariations.clear()
            self._fontVariations.update(axes)
        defaultVariations = self.listFontVariations()
        currentVariation = {axis: data["defaultValue"] for axis, data in defaultVariations.items()}
        currentVariation.update(self._fontVariations)
        return currentVariation

    def listFontVariations(self, fontName=None):
        """
        List all variation axes for the current font.

        Optionally a `fontName` can be given. If a font path is given the font will be installed and used directly.
        """
        if fontName:
            fontName = _tryInstallFontFromFontName(fontName)
        else:
            fontName = self._font
        return getVariationAxesForFontName(fontName)

    def tabs(self, *tabs):
        """
        Set tabs,tuples of (`float`, `alignment`)
        Aligment can be `"left"`, `"center"`, `"right"` or any other character.
        If a character is provided the alignment will be `right` and centered on the specified character.

        .. downloadcode:: tabsFormattedString.py

            # create a new formatted string
            t = FormattedString()
            # set some tabs
            t.tabs((85, "center"), (232, "right"), (300, "left"))
            # add text with tabs
            t += " hello w o r l d".replace(" ", "\\t")
            # draw the string
            text(t, (10, 10))
        """
        if tabs and tabs[0] is None:
            self._tabs = None
        else:
            self._tabs = tabs

    def indent(self, indent):
        """
        Set indent of text left of the paragraph.

        .. downloadcode:: indent.py

            # setting up some variables
            x, y, w, h = 10, 10, 500, 600

            txtIndent = 100
            txtFirstLineIndent = 200
            txtTailIndent = -100
            txtFontSize = 22

            paragraphTop = 3
            paragraphBottom = 10

            txt = '''DrawBot is an ideal tool to teach the basics of programming. Students get colorful graphic treats while getting familiar with variables, conditional statements, functions and what have you. Results can be saved in a selection of different file formats, including as high resolution, scaleable PDF, svg, movie, png, jpeg, tiff...'''

            # a new page with preset size
            newPage(w+x*2, h+y*2)
            # draw text indent line
            stroke(1, 0, 0)
            line((x+txtIndent, y), (x+txtIndent, y+h))
            # draw text firstline indent line
            stroke(1, 1, 0)
            line((x+txtFirstLineIndent, y), (x+txtFirstLineIndent, y+h))
            # draw tail indent
            pos = txtTailIndent
            # tail indent could be negative
            if pos <= 0:
                # substract from width of the text box
                pos = w + pos
            stroke(0, 0, 1)
            line((x+pos, y), (x+pos, y+h))
            # draw a rectangle
            fill(0, .1)
            stroke(None)
            rect(x, y, w, h)

            # create a formatted string
            t = FormattedString(fontSize=txtFontSize)
            # set alignment
            t.align("justified")
            # add text
            t += txt
            # add hard return
            t += "\\n"
            # set style for indented text
            t.fontSize(txtFontSize*.6)
            t.paragraphTopSpacing(paragraphTop)
            t.paragraphBottomSpacing(paragraphBottom)
            t.firstLineIndent(txtFirstLineIndent)
            t.indent(txtIndent)
            t.tailIndent(txtTailIndent)
            # add text
            t += txt
            # add hard return
            t += "\\n"
            # reset style
            t.fontSize(txtFontSize)
            t.indent(None)
            t.tailIndent(None)
            t.firstLineIndent(None)
            t.paragraphTopSpacing(None)
            t.paragraphBottomSpacing(None)
            # add text
            t += txt
            # draw formatted string in a text box
            textBox(t, (x, y, w, h))
        """
        self._indent = indent

    def tailIndent(self, indent):
        """
        Set indent of text right of the paragraph.
        """
        self._tailIndent = indent

    def firstLineIndent(self, indent):
        """
        Set indent of the text only for the first line.
        """
        self._firstLineIndent = indent

    def paragraphTopSpacing(self, value):
        """
        set paragraph spacing at the top.
        """
        self._paragraphTopSpacing = value

    def paragraphBottomSpacing(self, value):
        """
        set paragraph spacing at the bottom.
        """
        self._paragraphBottomSpacing = value

    def language(self, language):
        """
        Set the preferred language as language tag or None to use the default language.
        """
        self._language = language

    def size(self):
        """
        Return the size of the text.
        """
        return self._attributedString.size()

    def getNSObject(self):
        return self._attributedString

    def copy(self):
        """
        Copy the formatted string.
        """
        attributes = {key: getattr(self, "_%s" % key) for key in self._formattedAttributes}
        new = self.__class__(**attributes)
        new._attributedString = self._attributedString.mutableCopy()
        return new

    def fontContainsCharacters(self, characters):
        """
        Return a bool if the current font contains the provided `characters`.
        Characters is a string containing one or more characters.
        """
        font = AppKit.NSFont.fontWithName_size_(self._font, self._fontSize)
        if font is None:
            return False
        result, glyphs = CoreText.CTFontGetGlyphsForCharacters(font, characters, None, len(characters))
        return result

    def fontContainsGlyph(self, glyphName):
        font = AppKit.NSFont.fontWithName_size_(self._font, self._fontSize)
        if font is None:
            return False
        glyph = font.glyphWithName_(glyphName)
        return bool(glyph)

    def fontFilePath(self):
        """
        Return the path to the file of the current font.
        """
        font = AppKit.NSFont.fontWithName_size_(self._font, self._fontSize)
        if font is not None:
            url = CoreText.CTFontDescriptorCopyAttribute(font.fontDescriptor(), CoreText.kCTFontURLAttribute)
            if url:
                return url.path()
        warnings.warn("Cannot find the path to the font '%s'." % self._font)
        return None

    def listFontGlyphNames(self):
        """
        Return a list of glyph names supported by the current font.
        """
        from fontTools.ttLib import TTFont, TTLibError
        from fontTools.misc.macRes import ResourceReader, ResourceError

        path = self.fontFilePath()
        if path is None:
            return []
        try:
            # load the font with fontTools
            # provide a fontNumber as lots of fonts are .ttc font files.
            # search for the res_name_or_index for .dfont files.
            res_name_or_index = None
            fontNumber = None
            ext = os.path.splitext(path)[-1].lower()
            if ext == ".ttc":
                def _getPSName(source):
                    # get PS name
                    name = source["name"]
                    psName = name.getName(6, 1, 0)
                    if psName is None:
                        psName.getName(6, 3, 1)
                    return psName.toStr()

                ttc = TTFont(path, lazy=True, fontNumber=0)
                numFonts = ttc.reader.numFonts
                foundPSName = False
                for fontNumber in range(numFonts):
                    source = TTFont(path, lazy=True, fontNumber=fontNumber)
                    psName = _getPSName(source)
                    if psName == self._font:
                        foundPSName = True
                        break
                if not foundPSName:
                    # fallback to the first font in the ttc.
                    fontNumber = 0

            elif ext == ".dfont":
                try:
                    reader = ResourceReader(path)
                    names = reader.getNames("sfnt")
                    if self._font in names:
                        res_name_or_index = self._font
                    else:
                        res_name_or_index = names[0]
                except ResourceError:
                    pass
            fontToolsFont = TTFont(path, lazy=True, fontNumber=fontNumber, res_name_or_index=res_name_or_index)
        except TTLibError:
            warnings.warn("Cannot read the font file for '%s' at the path '%s'" % (self._font, path))
            return []
        glyphNames = fontToolsFont.getGlyphOrder()
        fontToolsFont.close()
        # remove .notdef from glyph names
        if ".notdef" in glyphNames:
            glyphNames.remove(".notdef")
        return glyphNames

    def fontAscender(self):
        """
        Returns the current font ascender, based on the current `font` and `fontSize`.
        """
        font = AppKit.NSFont.fontWithName_size_(self._font, self._fontSize)
        if font is None:
            ff = self._fallbackFont or _FALLBACKFONT
            warnings.warn("font: '%s' is not installed, back to the fallback font: '%s'" % (self._font, ff))
            font = AppKit.NSFont.fontWithName_size_(ff, self._fontSize)
        return font.ascender()

    def fontDescender(self):
        """
        Returns the current font descender, based on the current `font` and `fontSize`.
        """
        font = AppKit.NSFont.fontWithName_size_(self._font, self._fontSize)
        if font is None:
            ff = self._fallbackFont or _FALLBACKFONT
            warnings.warn("font: '%s' is not installed, back to the fallback font: '%s'" % (self._font, ff))
            font = AppKit.NSFont.fontWithName_size_(ff, self._fontSize)
        return font.descender()

    def fontXHeight(self):
        """
        Returns the current font x-height, based on the current `font` and `fontSize`.
        """
        font = AppKit.NSFont.fontWithName_size_(self._font, self._fontSize)
        if font is None:
            ff = self._fallbackFont or _FALLBACKFONT
            warnings.warn("font: '%s' is not installed, back to the fallback font: '%s'" % (self._font, ff))
            font = AppKit.NSFont.fontWithName_size_(ff, self._fontSize)
        return font.xHeight()

    def fontCapHeight(self):
        """
        Returns the current font cap height, based on the current `font` and `fontSize`.
        """
        font = AppKit.NSFont.fontWithName_size_(self._font, self._fontSize)
        if font is None:
            ff = self._fallbackFont or _FALLBACKFONT
            warnings.warn("font: '%s' is not installed, back to the fallback font: '%s'" % (self._font, ff))
            font = AppKit.NSFont.fontWithName_size_(ff, self._fontSize)
        return font.capHeight()

    def fontLeading(self):
        """
        Returns the current font leading, based on the current `font` and `fontSize`.
        """
        font = AppKit.NSFont.fontWithName_size_(self._font, self._fontSize)
        if font is None:
            ff = self._fallbackFont or _FALLBACKFONT
            warnings.warn("font: '%s' is not installed, back to the fallback font: '%s'" % (self._font, ff))
            font = AppKit.NSFont.fontWithName_size_(ff, self._fontSize)
        return font.leading()

    def fontLineHeight(self):
        """
        Returns the current line height, based on the current `font` and `fontSize`.
        If a `lineHeight` is set, this value will be returned.
        """
        if self._lineHeight is not None:
            return self._lineHeight
        font = AppKit.NSFont.fontWithName_size_(self._font, self._fontSize)
        if font is None:
            ff = self._fallbackFont or _FALLBACKFONT
            warnings.warn("font: '%s' is not installed, back to the fallback font: '%s'" % (self._font, ff))
            font = AppKit.NSFont.fontWithName_size_(ff, self._fontSize)
        return font.defaultLineHeightForFont()

    def appendGlyph(self, *glyphNames):
        """
        Append a glyph by his glyph name using the current `font`.
        Multiple glyph names are possible.

        .. downloadcode:: appendGlyphFormattedString.py

            size(1000, 400)
            # create an empty formatted string object
            t = FormattedString()
            # set a font
            t.font("Menlo-Regular")
            # set a font size
            t.fontSize(300)
            # add some glyphs by glyph name
            t.appendGlyph("A", "ampersand", "Eng", "Eng.alt")
            # draw the formatted string
            text(t, (100, 100))
        """
        # use a non breaking space as replacement character
        baseString = chr(0xFFFD)
        font = None
        if self._font:
            font = AppKit.NSFont.fontWithName_size_(self._font, self._fontSize)
        if font is None:
            warnings.warn("font: '%s' is not installed, back to the fallback font: '%s'" % (self._font, _FALLBACKFONT))
            font = AppKit.NSFont.fontWithName_size_(_FALLBACKFONT, self._fontSize)

        # disable calt features, as this seems to be on by default
        # for both the font stored in the nsGlyphInfo as in the replacement character
        fontAttributes = {}
        fontAttributes[CoreText.NSFontFeatureSettingsAttribute] = [featureMap["calt_off"]]
        fontDescriptor = font.fontDescriptor()
        fontDescriptor = fontDescriptor.fontDescriptorByAddingAttributes_(fontAttributes)
        font = AppKit.NSFont.fontWithDescriptor_size_(fontDescriptor, self._fontSize)

        fallbackFont = self._fallbackFont
        self._fallbackFont = None
        _openTypeFeatures = dict(self._openTypeFeatures)
        self._openTypeFeatures = dict(calt=False)
        for glyphName in glyphNames:
            glyph = font.glyphWithName_(glyphName)
            if glyph:
                self.append(baseString)
                glyphInfo = AppKit.NSGlyphInfo.glyphInfoWithGlyph_forFont_baseString_(glyph, font, baseString)
                self._attributedString.addAttribute_value_range_(AppKit.NSGlyphInfoAttributeName, glyphInfo, (len(self) - 1, 1))
            else:
                warnings.warn("font '%s' has no glyph with the name '%s'" % (font.fontName(), glyphName))
        self.openTypeFeatures(**_openTypeFeatures)
        self._fallbackFont = fallbackFont

