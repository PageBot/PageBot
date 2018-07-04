#!/usr/bin/env python
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
#     drawbotstring.py
#
import re
from copy import copy
try:
    #import AppKit
    import CoreText
    import Quartz
    from drawBot import BezierPath
except (ImportError, AttributeError):
    BezierPath = None

#from pagebot.contexts.basecontext import BaseContext # TODO: Solve this
from pagebot.contexts.strings.babelstring import BabelString
from pagebot.style import css, LEFT, DEFAULT_FONT_SIZE, DEFAULT_FONT_PATH
from pagebot.toolbox.future import chr
from pagebot.fonttoolbox.objects.font import getFont, getInstance
from pagebot.toolbox.color import Color, color, noColor, inheritColor, blackColor

def pixelBounds(fs):
    u"""Answer the pixel-bounds rectangle of the text, if formatted by the option (w, h).
    Note that @by can be a negative value, if there is text (e.g. overshoot) below the baseline.
    @bh is the amount of pixels above the baseline.
    For the total height of the pixel-map, calculate @ph - @py.
    For the total width of the pixel-map, calculate @pw - @px."""
    p = BezierPath()
    p.text(fs, (0, 0))
    # OSX answers bw and bh as difference with bx and by. That is not really intuitive, as the
    # the total (width, height) then always needs to be calculated by the caller.
    # So, instead, the width and height answered is the complete bounding box, and the (x, y)
    # is the position of the bounding box, compared to the (0, 0) of the string origin.
    bx, by, bw, bh = p.bounds()
    return pt(bx, by, bw - bx, bh - by)

class NoneDrawBotString(BabelString):
    u"""Used for testing DrawBotString doctest in non-DrawBot Environment."""
    BABEL_STRING_TYPE = 'fs'

    def __init__(self, s, context, style=None):
        self.context = context # Store context, in case we need more of its functions.
        self.s = s
        self.fontSize = DEFAULT_FONT_SIZE
        self.font = DEFAULT_FONT_PATH
        self.style = style

    @classmethod
    def newString(cls, s, context, e=None, style=None, w=None, h=None, pixelFit=True,
            fontSize=None, font=None, tagName=None):
        return cls(s, context=context, style=style)

    def textSize(self, w=None, h=None):
        u"""Answer the (w, h) size for a given width, with the current text, measured from bottom em-size
        to top-emsize (including ascender+ and descender+) and the string width (including margins)."""
        return w or 100, h or 100

    def setFillColor(self, color):
        pass

    fill = setFillColor

    def setStrokeColor(self, color):
        pass

    stroke = setStrokeColor
    
class DrawBotString(BabelString):

    BABEL_STRING_TYPE = 'fs'

    u"""DrawBotString is a wrapper around the standard DrawBot FormattedString."""
    def __init__(self, s, context, style=None):
        u"""Constructor of the DrawBotString, wrapper around DrawBot.FormattedString.
        Optionally store the (latest) style that was used to produce the formatted string.

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> context.isDrawBot
        True
        """

        """
        TODO: Get this docTest to work.
        >>> bs = DrawBotString('ABC', context)
        >>> bs
        ABC
        """
        self.context = context # Store context, in case we need more of its functions.
        self.s = s # Store the DrawBot FormattedString, as property to make sure it is a FormattedString,
        # otherwise create it.
        # In case defined, store current status here as property and set the current FormattedString
        # for future additions. Also the answered metrics will not be based on these values.
        self.style = style or {}
        self.fittingFontSize = 0 # Set to fitting font size, in case the size iterated to find width.

    def _get_s(self):
        u"""Answer the embedded FormattedString by property, to enforce checking type of the string."""
        return self._s
    def _set_s(self, s):
        u""" Check on the type of s. Three types are supported here: plain strings,
        DrawBot FormattedString and the class of self."""
        assert isinstance(s, (DrawBotString, str)) or s.__class__.__name__ == 'FormattedString'
        if isinstance(s, str):
            s = self.context.b.FormattedString(s)
        elif isinstance(s, DrawBotString):
            s = s.s
        self._s = s
    s = property(_get_s, _set_s)

    def _get_font(self):
        u"""Answer the current state of fontName."""
        return self.style.get('font')
    def _set_font(self, fontName):
        if fontName is not None:
            self.context.font(fontName)
        self.style['font'] = fontName
    font = property(_get_font, _set_font)

    def _get_fontSize(self):
        u"""Answer the current state of the fontSize."""
        return self.style.get('fontSize')
    def _set_fontSize(self, fontSize):
        if fontSize is not None:
            self.context.fontSize(fontSize)
        self.style['fontSize'] = fontSize
    fontSize = property(_get_fontSize, _set_fontSize)

    def asText(self):
        return u'%s' % self.s #  Convert to text

    def textSize(self, w=None, h=None):
        u"""Answer the (w, h) size for a given width, with the current text, measured from bottom em-size
        to top-emsize (including ascender+ and descender+) and the string width (including margins)."""
        # TODO: Add in case w is defined.
        return self.context.textSize(self, w=w, h=h)

    def bounds(self):
        u"""Answer the pixel-bounds rectangle of the text, if formatted by the option (w, h).
        Note that @by can be a negative value, if there is text (e.g. overshoot) below the baseline.
        @bh is the amount of pixels above the baseline.
        For the total height of the pixel-map, calculate @ph - @py.
        For the total width of the pixel-map, calculate @pw - @px."""
        return pixelBounds(self.s)

    def fontContainsCharacters(self, characters):
        u"""Return a bool if the current font contains the provided characters.
        Characters is a string containing one or more characters."""
        return self.s.fontContainsCharacters(characters)

    def fontFilePath(self):
        u"""Return the path to the file of the current font."""
        return self.s.fontFilePath()

    def listFontGlyphNames(self):
        """Return a list of glyph names supported by the current font."""
        return self.s.listFontGlyphNames()

    def ascender(self):
        u"""Returns the current font ascender, based on the current font and fontSize."""
        return self.s.fontAscender()
    fontAscender = ascender # Compatibility with DrawBot API

    def descender(self):
        u"""Returns the current font descender, based on the current font and fontSize."""
        return self.s.fontDescender()
    fontDescender = descender # Compatibility with DrawBot API

    def xHeight(self):
        u"""Returns the current font x-height, based on the current font and fontSize."""
        return self.s.fontXHeight()
    fontXHeight = xHeight # Compatibility with DrawBot API

    def capHeight(self):
        u"""Returns the current font cap height, based on the current font and fontSize."""
        return self.s.fontCapHeight()
    fontCapHeight = capHeight # Compatibility with DrawBot API

    def leading(self):
        u"""Returns the current font leading, based on the current font and fontSize."""
        return self.s.fontLeading()
    fontLeading = leading # Compatibility with DrawBot API

    def lineHeight(self):
        u"""Returns the current line height, based on the current font and fontSize.
        If a lineHeight is set, this value will be returned."""
        return self.s.fontLineHeight()
    fontLineHeight = lineHeight # Compatibility with DrawBot API

    def appendGlyph(self, *glyphNames):
        u"""Append a glyph by his glyph name using the current font. Multiple glyph names are possible."""
        self.s.appendGlyph(glyphNames)

    MARKER_PATTERN = '==%s@%s=='
    FIND_FS_MARKERS = re.compile('\=\=([a-zA-Z0-9_\:\.]*)\@([^=]*)\=\=')

    def appendMarker(self, markerId, arg):
        u"""Append a formatted string with markerId that can be used as non-display marker.
        This way the Composer can find the position of markers in text boxes, after
        FS-slicing has been done. Note there is always a very small "white-space"
        added to the string, so there is a potential difference in width that matters.
        For that reason markers should not be changed after slicing (which would theoretically
        alter the flow of the FormattedString in an box) and the markerId and amount/length
        of args should be kept as small as possible.
        Note that there is a potential problem of slicing through the argument string at
        the end of a textBox. That is another reason to keep the length of the arguments short.
        And not to use any spaces, etc. inside the markerId.
        Possible slicing through line-endings is not a problem, as the raw string ignores them.

        """
        marker = self.MARKER_PATTERN % (markerId, arg or '')
        fs = self.context.b.FormattedString(marker, fill=None, stroke=None, fontSize=0.0000000000001)
        self.append(fs)

    def findMarkers(self, reCompiled=None):
        u"""Answer a dictionary of markers with their arguments in self.s."""
        if reCompiled is None:
            reCompiled= self.FIND_FS_MARKERS
        return reCompiled.findall(u'%s' % self.s)

    def textOverflow(self, w, h, align=LEFT):
        return self.context.textOverflow(self, (0, 0, w, h), align)

    @classmethod
    def _newFitWidthString(cls, fs, context, fontSize, w, pixelFit):
        if pixelFit:
            tx, _, tw, _ = pixelBounds(fs)
        else:
            tx, tw = 0, context.b.textSize(fs)[0]
        return w * fontSize / (tw-tx)

    @classmethod
    def _newFitHeightString(cls, fs, context, fontSize, h, pixelFit):
        if pixelFit:
            _, ty, _, th = pixelBounds(fs)
        else:
            ty, th = 0, context.b.textSize(fs)[1]
        return h * fontSize / (th-ty)

    FITTING_TOLERANCE = 3

    @classmethod
    def fitString(cls, t, context, e=None, style=None, w=None, h=None, useXTRA=True, pixelFit=True):
        u"""Answer the DrawBotString instance from valid attributes in style. Set all values after testing
        their existence, so they can inherit from previous style formats in the string.
        If the target width w and height are defined, and if there is a [wdth] or [XTRA] axis in the
        current Variable Font, then values are iterated to make the best location/instance for the
        rectangle fit.
        In case the fontSize is set and the width w is set, then just use the [wdth] or [XTRA] to 
        make a horizontal fit, keeping the size. If the axes run to extreme, the string is return 
        without changing width.
        In case the a font path was supplied, then try to get a Font instance for that path, as we
        need to test it for existing axes as Variable Font.

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> #font = findFont('RobotoDelta-VF')
        >>> font = findFont('Fit-Variable_1')        
        >>> style = dict(font=font)
        >>> 'wdth' in font.axes.keys() or 'XTRA' in font.axes.keys() # One of them is there
        True
        >>> s = DrawBotString.newString('Hello', context, style=style, w=300)
        >>> int(round(s.bounds()[2])), int(round(s.fittingFontSize)) # Rounded width
        (297, 195)
        >>> s = DrawBotString.fitString('Hello', context, style=style, w=400, h=220)
        >>> int(round(s.bounds()[2]-s.bounds()[0])) # Rounded pixel width
        399
        >>> int(round(s.bounds()[3]-s.bounds()[1])) # Rounded pixel height
        220
        >>> #s.bounds()

        """
        style = copy(style)
        location = copy(css('', e, style, {})) # In case the used already supplied a VF location, use it.
        font = css('font', e, style)
        if isinstance(font, str): # Assuming it's a path, get the Font instance.
            font = getFont(font) # Make sure we gave a real Font instance.
        style['font'] = font
        # Get the flag if fit locations should be rounded (less cached instance) or accurate.
        roundVariableFitLocation = style.get('roundVariableFitLocation', True)
        # In case font is not a variable font, or not [wdth] or [XTRA] present, then using normal 
        # string fit is the best we can do. 
        if not 'wdth' in font.axes and not 'XTRA' in font.axes:
            return cls.newString(t, context, e=e, style=style, w=w, h=h, pixelFit=pixelFit)

        # Decide which axis to use for width adjustments and get the axis values.
        if not useXTRA or not 'XTRA' in font.axes: # Try to force usage of [XTRA] if it exists, otherwise use[wdth]
            axisTag = 'wdth'
        else:
            axisTag = 'XTRA'
        minValue, defaultValue, maxValue = font.axes[axisTag]
        #print(0, minValue, defaultValue, maxValue )
        if h is not None: # Fitting in heigt, calculate/iterate for the fitting font size.
            bs = cls.newString(t, context, e=e, style=style, h=h, pixelFit=pixelFit)
            style['fontSize'] = bs.fittingFontSize
        else: # Assuming there is a fontSize set, we'll use that as vertical requirement
            bs = cls.newString(t, context, e=e, style=style, pixelFit=pixelFit)
        
        # Now we have a formatted string with a given fontSize, guess to fit on the width. 
        tx, _, tw, _ = bs.bounds() # Get pixel bounds of the string
        tw = tw - tx # Pixel width of the current string.
        #print(0, tw, w, h)
        prevW = None # Testing if something changed, for extreme of axes.
        axisValue = defaultValue

        for n in range(100): # Limit the maximum amount of iterations as safeguard
            if tw > w: # Too wide, try iterate smaller in ratio of wdth/XTRA axis values
                #print(1, tw, w)
                maxValue = axisValue # Clip wide range to current
                # Guess the new axisvalue from the ratio of tw/w
                axisValue = (axisValue - minValue)/2 + minValue
                if roundVariableFitLocation:
                    axisValue = int(round(axisValue))
                #print(2, axisValue, minValue, defaultValue, maxValue)
                loc = copy(location)
                loc[axisTag] = axisValue
                loc['opsz'] = int(style['fontSize'])
                #print(3, loc, font.axes.keys())
                style['font'] = getInstance(font, loc)
                bs = cls.newString(t, context, e=e, style=style, pixelFit=pixelFit)
                tx, ty, tw, th = bs.bounds() # Get pixel bounds of the string
                tw = tw - tx # Total width for the current 
                #print(5, tw, w, th-ty, h)
                if prevW == tw: # Did not change, probably not able to get more condensed
                    break
                prevW = tw

            elif tw < w - cls.FITTING_TOLERANCE: # Too condensed, try to make wider.
                #print(11, tw, w)
                minValue = axisValue # Clip narrow range to current
                axisValue = (maxValue - axisValue)/2 + axisValue
                if roundVariableFitLocation:
                    axisValue = int(round(axisValue))
                loc = copy(location)
                loc[axisTag] = axisValue
                loc['opsz'] = int(style['fontSize'])
                style['font'] = getInstance(font, loc)
                bs = cls.newString(t, context, e=e, style=style, pixelFit=pixelFit)
                tx, ty, tw, th = bs.bounds() # Get pixel bounds of the string
                tw = tw - tx # Total width for the current 
                #print(15, tw, w, th-ty, h)
                if prevW == tw: # Did not change, probably not able to get more condensed
                    break
                prevW = tw

            else: # We found a fitting VF-location within tolerance. Back out.
                break
        #print('Number of iterations', n)
        return bs

    @classmethod
    def newString(cls, t, context, e=None, style=None, w=None, h=None, pixelFit=True):
        u"""Answer a DrawBotString instance from valid attributes in *style*. Set all values after testing
        their existence, so they can inherit from previous style formats in the string.
        If target width *w* or height *h* is defined, then *fontSize* is scaled to make the string fit *w* or *h*.
        In that case the pixelFit flag defines if the current width or height comes from the pixel image of em size.

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> font = findFont('Roboto-Black')
        >>> context = DrawBotContext()
        """

        """
        TODO: Get more docTests to work
        >>> bs = context.newString('ABC', style=dict(font=font.path, fontSize=22))
        >>> bs
        ABC
        >>> bs = context.newString('ABC', style=dict(font=font.path), w=100)
        >>> int(round(bs.fontSize))
        51
        >>> bs = context.newString('ABC', style=dict(font=font), w=100) # Use the font instance instead of path.
        >>> int(round(bs.fontSize))
        51
        """
        # Get the drawBotBuilder, no need to check, we already must be in context here.
        print('@#@#@#@##', t)
        if t is None:
            t = ''
        elif isinstance(t, str):
            t = str(t)

        b = context.b
        b.hyphenation(css('hyphenation', e, style)) # TODO: Should be text attribute, not global

        fs = b.FormattedString('') # Make an empty OSX-DrawBot FormattedString
        sFont = css('font', e, style)
        if sFont is not None:
            if hasattr(sFont, 'path'): # If the Font instance was supplied, then use it's path.
                sFont = sFont.path
            fs.font(sFont)
        # If there is a target (pixel) width or height defined, ignore the requested fontSize and try the width or
        # height first for fontSize = 100. The resulting width or height is then used as base value to
        # calculate the needed point size.
        # Forced fontSize, then this overwrites the style['fontSize'] if it is there.
        # TODO: add calculation of rFontSize (relative float based on root-fontSize) here too.
        if w is not None or h is not None:
            sFontSize = 100
        else:
            sFontSize = css('fontSize', e, style, DEFAULT_FONT_SIZE) # May be scaled to fit w or h if target is defined.
        sLeading = css('leading', e, style)
        rLeading = css('rLeading', e, style)
        if sLeading or (rLeading and sFontSize):
            lineHeight = (sLeading or 0) + (rLeading or 0) * (sFontSize or 0)
            if lineHeight:
                fs.lineHeight(lineHeight)
        if sFontSize is not None:
            fs.fontSize(sFontSize) # For some reason fontSize must be set after leading.
        sFallbackFont = css('fallbackFont', e, style)
        if sFallbackFont is not None:
            fs.fallbackFont(sFallbackFont)

        # Color values for text fill
        # Color: Fill the text with this color instance
        # noColor: Set the value to None, no fill will be drawn
        # inheritColor: Don't set color, inherit the current setting for fill
        sFill = css('textFill', e, style, blackColor) # Default is blackColor, not noColor
        print('FFFFFFF', sFill)
        """
        if sFill not in (None, inheritColor): # Test on this flag, None is valid value
            if sFill is noColor: # None is value to disable fill drawing.
                context.setTextFillColor(fs, None)
            else:
                assert isinstance(sFill, Color)
                context.setTextFillColor(fs, sFill.rgb)
        """
        # Color values for text stroke
        # Color: Stroke the text with this color instance
        # noColor: Set the value to None, no stroke will be drawn
        # inheritColor: Don't set color, inherit the current setting for stroke
        sStroke = css('textStroke', e, style, noColor)
        print('SAASSASAAS', sStroke)
        """
        sStrokeWidth = css('textStrokeWidth', e, style)
        if sStroke not in(None, inheritColor) and sStrokeWidth is not None:
            if sStroke is noColor: # None is value to disable stroke drawing
                context.setTextStrokeColor(fs, None)
            else:
                assert isinstance(sStroke, Color)
                context.setTextStrokeColor(fs, sStroke.rgb, w=sStrokeWidth)
        """
        sTextAlign = css('xTextAlign', e, style) # Warning: xAlign is used for element alignment, not text.
        if sTextAlign is not None: # yTextAlign must be solved by parent container element.
            fs.align(sTextAlign)
        sUnderline = css('underline', e, style)
        #if sUnderline in ('single', None): # Only these values work in FormattedString
        #    fs.underline(sUnderline)
        sParagraphTopSpacing = css('paragraphTopSpacing', e, style)
        rParagraphTopSpacing = css('rParagraphTopSpacing', e, style)
        if sParagraphTopSpacing or (rParagraphTopSpacing and sFontSize):
            fs.paragraphTopSpacing((sParagraphTopSpacing or 0) + (rParagraphTopSpacing or 0) * (sFontSize or 0))
        sParagraphBottomSpacing = css('paragraphBottomSpacing', e, style)
        rParagraphBottomSpacing = css('rParagraphBottomSpacing', e, style)
        if sParagraphBottomSpacing or (rParagraphBottomSpacing and sFontSize):
            fs.paragraphBottomSpacing((sParagraphBottomSpacing or 0) + (rParagraphBottomSpacing or 0) * (sFontSize or 0))
        sTracking = css('tracking', e, style)
        srTracking = css('rTracking', e, style)
        if sTracking or (srTracking and sFontSize):
            fs.tracking((sTracking or 0) + (srTracking or 0) * (sFontSize or 0))
        sBaselineShift = css('baselineShift', e, style)
        rBaselineShift = css('rBaselineShift', e, style)
        if sBaselineShift or (rBaselineShift and sFontSize):
            fs.baselineShift((sBaselineShift or 0) + (rBaselineShift or 0) * (sFontSize or 0))
        sOpenTypeFeatures = css('openTypeFeatures', e, style)
        if sOpenTypeFeatures is not None:
            fs.openTypeFeatures(**sOpenTypeFeatures)
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

        if style is None:
            style = dict(fontSize=sFontSize)

        newt = fs + t # Format plain string t onto new formatted fs.

        if w is not None: # There is a target width defined, calculate again with the fontSize ratio correction.
            # We use the enclosing pixel bounds instead of the context.textSide(newt) here, because it is much
            # more consistent for tracked text. context.textSize will add space to the right of the string.
            style = copy(style)
            style['fontSize'] = cls._newFitWidthString(newt, context, sFontSize, w, pixelFit)
            newS = cls.newString(t, context, style=style)
            # Test the width we got by linear interpolation. Scale back if still too large.
            # Iterate until it really fits.
            while newS.textSize()[0] > w and style['fontSize']:
                style['fontSize'] -= 0.1 # Incremental decrease the size until it fits
                newS = cls.newString(t, context, style=style)

        elif h is not None: # There is a target height defined, calculate again with the fontSize ratio correction.
            # We use the enclosing pixel bounds instead of the context.textSide(newt) here, because it is much
            # more consistent for tracked text. context.textSize will add space to the right of the string.
            style = copy(style)
            style['fontSize'] = cls._newFitHeightString(newt, context, sFontSize, h, pixelFit)
            newS = cls.newString(t, context, style=style)
        else:
            newS = cls(newt, context, style)
        # Store any aajust fitting parameters in the string, in case the caller wants to know.
        newS.fittingFontSize = style.get('fontSize')
        newS.fittingFont = style.get('font') # In case we are sampling with a Variable Font.
        newS.fittingLocation = style.get('location')
        
        return newS

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
        for index, part in enumerate(str(ctRun).split('"')[1].split('\\u')):
            if index == 0:
                self.string += part
            elif len(part) >= 4:
                self.string += chr(int(part[0:4], 16))
                self.string += part[4:]

        #print(gc, len(CoreText.CTRunGetStringIndicesPtr(ctRun)), CoreText.CTRunGetStringIndicesPtr(ctRun), ctRun)
        try:
            self.stringIndices = CoreText.CTRunGetStringIndicesPtr(ctRun)[0:gc]
        except TypeError:
            self.stringIndices = [0]
        #CoreText.CTRunGetStringIndices(ctRun._ctRun, CoreText.CFRange(0, 5), None)[4]
        self.advances = CoreText.CTRunGetAdvances(ctRun, CoreText.CFRange(0, 5), None)
        #self.positions = CoreText.CTRunGetPositionsPtr(ctRun)[0:gc]
        #CoreText.CTRunGetPositions(ctRun, CoreText.CFRange(0, 5), None)[4]
        #self.glyphFontIndices = CoreText.CTRunGetGlyphsPtr(ctRun)[0:gc]
        #print(CoreText.CTRunGetGlyphs(ctRun, CoreText.CFRange(0, 5), None)[0:5])
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

    #   Font metrics, based on self.nsFont. This can be different from
    #   self.fontAswcencender and self.fontDescender, etc. which are
    #   based on the current setting in the FormattedString

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
        #print(ctLine)
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

    def getIndexForPosition(self, xy):
        x, y = xy
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
        u"""Property that answers the bounding box (actual black shape) of the text line."""
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

'''
def getTextPositionSearch(bs, w, h, search, xTextAlign=LEFT, hyphenation=True):
    u"""
    """
    bc = BaseContext()
    path = CoreText.CGPathCreateMutable()
    CoreText.CGPathAddRect(path, None, CoreText.CGRectMake(0, 0, w, h))

    attrString = bc.attributedString(bs, align=xTextAlign)
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
'''
    #   F I N D

def findPattern(textLines, pattern):
    u"""Answer the point locations where this pattern occures in the Formatted String."""
    foundPatterns = [] # List of FoundPattern instances.
    for lineIndex, textLine in enumerate(textLines):
        for foundPattern in textLine.findPattern(pattern):
            foundPattern.y = textLine.y
            foundPattern.z = 0
            foundPatterns.append(foundPattern)
    return foundPatterns


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
