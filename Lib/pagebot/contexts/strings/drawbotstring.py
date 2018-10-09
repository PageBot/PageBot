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
#     drawbotstring.py
#
import re
from copy import copy

try:
    from CoreText import CTFramesetterCreateWithAttributedString, CTFramesetterCreateFrame, \
        CTFrameGetLines, CTFrameGetLineOrigins, CTRunGetGlyphCount, \
        CTRunGetStringRange, CTRunGetStringIndicesPtr, CTRunGetAdvances, \
        CTRunGetStatus, CTRunGetPositions, CTRunGetGlyphs, CTRunGetAttributes, \
        CFRange, CTRunGetTextMatrix, CTLineGetGlyphRuns, CGPoint, \
        CTLineGetStringIndexForPosition, CTLineGetOffsetForStringIndex, \
        CTLineGetStringRange, CTLineGetImageBounds, CTLineGetTypographicBounds, \
        CTLineGetTrailingWhitespaceWidth
    from Quartz import CGPathAddRect, CGPathCreateMutable, CGRectMake
    import drawBot

    drawBotBuilder = drawBot
except (AttributeError, ImportError):
    NSFont = None
    CGPathAddRect = CGPathCreateMutable = CGRectMake = None
    CTFramesetterCreateWithAttributedString = None
    CTFrameGetLines = None
    CTRunGetStringRange = None
    CTFrameGetLineOrigins = None
    CTFramesetterCreateFrame = None
    CTRunGetGlyphCount = None
    CTRunGetStringIndicesPtr = None
    CTRunGetAdvances = None
    CTRunGetStatus = None
    CTRunGetPositions = None
    CTRunGetGlyphs = None
    CTRunGetAttributes = None
    CFRange = CGPoint = None
    CTRunGetTextMatrix = None
    CTLineGetGlyphRuns = None
    CTLineGetImageBounds = None
    CTLineGetStringIndexForPosition = None
    CTLineGetTrailingWhitespaceWidth = None
    CTLineGetTypographicBounds = None
    from pagebot.contexts.builders.nonebuilder import NoneDrawBotBuilder as drawBotBuilder

from pagebot.contexts.strings.babelstring import BabelString
from pagebot.style import css
from pagebot.constants import LEFT, DEFAULT_FONT_SIZE, DEFAULT_LEADING
from pagebot.paths import DEFAULT_FONT_PATH
from pagebot.constants import DEFAULT_FALLBACK_FONT_PATH, XXXL, DEFAULT_LANGUAGE
from pagebot.toolbox.future import chr
from pagebot.fonttoolbox.objects.font import Font, getFont, getInstance
from pagebot.toolbox.color import color, Color, noColor, inheritColor, blackColor
from pagebot.toolbox.units import pt, upt, isUnit, units, em

def pixelBounds(fs):
    """Answers the pixel-bounds rectangle of the text.

    Note that @by can be a negative value, if there is text (e.g. overshoot)
    below the baseline.
    @bh is the amount of pixels above the baseline.
    For the total height of the pixel-map, calculate @ph - @py.
    For the total width of the pixel-map, calculate @pw - @px."""
    if not fs:
        return pt(0, 0, 0, 0)
    p = drawBotBuilder.BezierPath()
    p.text(fs, (0, 0))
    # OSX answers bw and bh as difference with bx and by. That is not really
    # intuitive, as the the total (width, height) then always needs to be
    # calculated by the caller. So, instead, the width and height answered is
    # the complete bounding box, and the (x, y) is the position of the bounding
    # box, compared to the (0, 0) of the string origin.
    bx, by, bw, bh = p.bounds()
    return pt(bx, by, bw - bx, bh - by)

class NoneDrawBotString(BabelString):
    """Used for testing DrawBotString doctest in non-DrawBot Environment."""
    BABEL_STRING_TYPE = 'fs'

    def __init__(self, s, context, style=None):
        self.context = context # Store context, in case we need more of its functions.
        self.s = s
        self.fontSize = DEFAULT_FONT_SIZE
        self.font = DEFAULT_FONT_PATH
        assert style is None or isinstance(style, dict) # Some checking, in case we get something else here.
        self.style = style
        self.language = DEFAULT_LANGUAGE
        self.hyphenation = False

        self.fittingFont = None # In case we are sampling with a Variable Font.
        self.fittingLocation = None
        self.isFitting = False

    @classmethod
    def newString(cls, s, context, e=None, style=None, w=None, h=None, pixelFit=True,
            fontSize=None, font=None, tagName=None):
        assert style is None or isinstance(style, dict) # Some checking, in case we get something else here.
        return cls(s, context=context, style=style)

    def textSize(self, w=None, h=None):
        """Answers the (w, h) size for a given width, with the current text,
        measured from bottom em-size to top-emsize (including ascender+ and
        descender+) and the string width (including margins)."""
        return w or 100, h or 100

    def __repr__(self):
        return self.s

    def fill(self, r, g=None, b=None, a=None, alpha=None):
        pass

    setFillColor = fill

    def cmykFill(self, c, m=None, y=None, k=None, a=None, alpha=None):
        pass

    cmykStroke = cmykFill

    def stroke(self, r, g=None, b=None, a=None, alpha=None):
        pass

    setStrokeColor = stroke

    def setStrokeWidth(self, w):
        pass

    strokeWidth = setStrokeWidth

    def getTextLines(self, w, h=None, align=LEFT):
        return {}

    def _get_size(self):
        return pt(0, 0)
    size = property(_get_size)

class DrawBotString(BabelString):

    BABEL_STRING_TYPE = 'fs'

    """DrawBotString is a wrapper around the standard DrawBot FormattedString."""
    def __init__(self, s, context, style=None):
        """Constructor of the DrawBotString, wrapper around DrawBot.FormattedString.
        Optionally store the (latest) style that was used to produce the
        formatted string.

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> context.isDrawBot
        True
        >>> style = dict(font='Verdana', fontSize=pt(80))
        >>> bs = context.newString('Example Text', style=style)
        >>> bs.font, bs.fontSize, round(upt(bs.xHeight)), bs.xHeight, bs.capHeight, bs.ascender, bs.descender
        ('Verdana', 80pt, 44, 0.55em, 0.73em, 1.01em, -0.21em)
        >>> '/Verdana'in bs.fontPath
        True
        >>> style = dict(font='Verdana', fontSize=pt(100), leading=em(1.4))
        >>> bs = context.newString('Example Text', style=style)
        >>> lines = bs.getTextLines(w=100)
        >>> len(lines)
        9
        >>> line = lines[0]
        >>> line.xHeight, line.capHeight # Max metrics of all runs in line as Em
        (0.55em, 0.73em)
        >>> run = line.textRuns[0]
        >>> run.xHeight, run.capHeight
        (0.55em, 0.73em)
        """
        self.context = context # Store context, in case we need more of its functions.
        # Store the DrawBot FormattedString, as property to make sure it is a
        # FormattedString, otherwise create it.
        self.s = s
        # In case defined, store current status here as property and set the
        # current FormattedString for future additions. Also the answered
        # metrics will not be based on these values.
        if style is None:
            style = {}
        self.style = style

        # Filled in case w or h are defined, end depending if the font is a
        # variable font.
        self.fittingFontSize = pt(0) # Set to fitting font size, in case the size iterates to find width.
        self.fittingFont = None # In case we are sampling with a Variable Font.
        self.fittingLocation = None
        self.isFitting = False

        self.language = DEFAULT_LANGUAGE
        self.hyphenation = False
        print('drawbot string init')
        super(DrawBotString, self).__init__(s, context, style=style)

    def _get_s(self):
        """Answers the embedded FormattedString by property, to enforce checking
        type of the string."""
        return self._s

    def _set_s(self, s):
        """ Check on the type of s. Three types are supported here: plain strings,
        DrawBot FormattedString and the class of self."""
        assert isinstance(s, (DrawBotString, str)) or s.__class__.__name__ == 'FormattedString'
        if isinstance(s, str):
            s = self.context.b.FormattedString(s)
        elif isinstance(s, DrawBotString):
            s = s.s
        self._s = s
    s = property(_get_s, _set_s)

    def _get_font(self):
        """Answers the current state of fontName."""
        return self.style.get('font')

    def _set_font(self, fontName):
        if fontName is not None:
            self.context.font(fontName)
        self.style['font'] = fontName
    font = property(_get_font, _set_font)

    def _get_fontSize(self):
        """Answers the current state of the fontSize.

        >>> from pagebot.toolbox.units import mm
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> style = dict(font='Verdana', fontSize=pt(85), leading=em(1.4))
        >>> bs = context.newString('Example Text', style=style)
        >>> bs.fontSize
        85pt
        >>> bs.fontSize = 96 # Auto-convert to points
        >>> bs.fontSize
        96pt
        >>> bs.fontSize = mm(5) # Set at unit.
        >>> bs.fontSize
        5mm
        >>> #bs.leading
        1.4em
        """
        return units(self.style.get('fontSize'))
    def _set_fontSize(self, fontSize):
        if fontSize is not None:
            self.context.fontSize(upt(fontSize))
        self.style['fontSize'] = fontSize
    fontSize = property(_get_fontSize, _set_fontSize)

    def asText(self):
        """Answers the text string.

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> bs = context.newString('Example Text')
        >>> bs.asText()
        'Example Text'
        """
        return str(self.s) #  Convert to text

    def textSize(self, w=None, h=None):
        """Answers the (w, h) size for a given width, with the current text,
        measured from bottom em-size to top-emsize (including ascender+ and
        descender+) and the string width (including margins).

        >>> from pagebot.toolbox.units import mm, uRound
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> style = dict(font='Verdana', fontSize=pt(12))
        >>> bs = context.newString('Example Text ' * 20, style=style)
        >>> len(bs.getTextLines(w=100))
        20
        >>> uRound(bs.textSize(w=300))
        [251pt, 118pt]
        """
        b = self.context.b
        if w is not None:
            wpt = upt(w)
            return b.textSize(self.s, width=wpt)
        if h is not None:
            hpt = upt(h)
            return b.textSize(self.s, height=hpt)
        return b.textSize(self.s)

    def bounds(self, language=None, hyphenation=None):
        """Answers the pixel-bounds rectangle of the text, if formatted by the
        option (w, h).

        Note that @by can be a negative value, if there is text (e.g.
        overshoot) below the baseline.
        @bh is the amount of pixels above the baseline.
        For the total height of the pixel-map, calculate @ph - @py.
        For the total width of the pixel-map, calculate @pw - @px."""
        # Set the hyphenation flag and language from style, as in DrawBot this is set by a global function,
        # not as FormattedString attribute.
        if language is None:
            language = self.language
        if hyphenation is None:
            hyphenation = self.hyphenation
        self.context.language(language)
        self.context.hyphenation(hyphenation)
        return pixelBounds(self.s)

    def fontContainsCharacters(self, characters):
        """Return a bool if the current font contains the provided characters.
        Characters is a string containing one or more characters."""
        return self.s.fontContainsCharacters(characters)

    def _get_fontFilePath(self):
        """Return the path to the file of the current font."""
        return self.s.fontFilePath()
    fontPath = property(_get_fontFilePath)

    def listFontGlyphNames(self):
        """Return a list of glyph names supported by the current font."""
        return self.s.listFontGlyphNames()

    def _get_ascender(self):
        """Returns the current font ascender as relative Em, based on the
        current font and fontSize."""
        fontSize = upt(self.fontSize)
        return em(self.s.fontAscender()/fontSize, base=fontSize)
    fontAscender = ascender = property(_get_ascender) # Compatibility with DrawBot API

    def _get_descender(self):
        """Returns the current font descender as Em, based on the current font
        and fontSize."""
        fontSize = upt(self.fontSize)
        return em(self.s.fontDescender()/fontSize, base=fontSize)
    fontDescender = descender = property(_get_descender) # Compatibility with DrawBot API

    def _get_xHeight(self):
        """Returns the current font x-height as Em, based on the current font
        and fontSize."""
        fontSize = upt(self.fontSize)
        return em(self.s.fontXHeight()/fontSize, base=fontSize)
    fontXHeight = xHeight = property(_get_xHeight) # Compatibility with DrawBot API

    def _get_capHeight(self):
        """Returns the current font cap height as Em, based on the current font
        and fontSize."""
        fontSize = upt(self.fontSize)
        return em(self.s.fontCapHeight()/fontSize, base=fontSize)
    fontCapHeight = capHeight = property(_get_capHeight) # Compatibility with DrawBot API

    def _get_leading(self):
        """Returns the current font leading, based on the current font and fontSize."""
        fontSize = upt(self.fontSize)
        return em(self.s.fontLeading()/fontSize, base=fontSize)
    fontLeading = leading = property(_get_leading) # Compatibility with DrawBot API

    def _get_lineHeight(self):
        """Returns the current line height, based on the current font and fontSize.
        If a lineHeight is set, this value will be returned."""
        fontSize = upt(self.fontSize)
        return em(self.s.fontLineHeight()/fontSize, base=fontSize)
    fontLineHeight = lineHeight = property(_get_lineHeight) # Compatibility with DrawBot API

    def appendGlyph(self, *glyphNames):
        """Append a glyph by his glyph name using the current font. Multiple glyph names are possible."""
        self.s.appendGlyph(glyphNames)

    MARKER_PATTERN = '==%s@%s=='
    FIND_FS_MARKERS = re.compile('\=\=([a-zA-Z0-9_\:\.]*)\@([^=]*)\=\=')

    def appendMarker(self, markerId, arg):
        """Appends a formatted string with markerId that can be used as
        non-display marker. This way the Composer can find the position of
        markers in text boxes, after FS-slicing has been done. Note there is
        always a very small "white-space" added to the string, so there is a
        potential difference in width that matters. For that reason markers
        should not be changed after slicing (which would theoretically alter
        the flow of the FormattedString in an box) and the markerId and
        amount/length of args should be kept as small as possible.

        NOTE that there is a potential problem of slicing through the argument
        string at the end of a textBox. That is another reason to keep the
        length of the arguments short. And not to use any spaces, etc. inside
        the markerId. Possible slicing through line-endings is not a problem,
        as the raw string ignores them.

        """
        marker = self.MARKER_PATTERN % (markerId, arg or '')
        fs = self.context.b.FormattedString(marker, fill=noColor, stroke=noColor, fontSize=0.0000000000001)
        self.append(fs)

    def findMarkers(self, reCompiled=None):
        """Answers a dictionary of markers with their arguments in self.s."""
        if reCompiled is None:
            reCompiled= self.FIND_FS_MARKERS
        return reCompiled.findall(u'%s' % self.s)

    def textOverflow(self, w, h, align=LEFT):
        """Answers the overflowing of from the box (0, 0, w, h)
        as new DrawBotString in the current context."""
        b = self.context.b
        wpt, hpt = upt(w, h)
        # Set the hyphenation flag from style, as in DrawBot this is set by a global function,
        # not as FormattedString attribute.
        self.context.language(self.language)
        self.context.hyphenation(bool(self.hyphenation))
        overflow = self.__class__(b.textOverflow(self.s, (0, 0, wpt, hpt), align), self.context)
        self.context.hyphenation(False)
        return overflow

    def getBaselines(self, w, h=None):
        """Answers the dictionary of vertical baseline positions for the self.s
        FormattedString and for the given width and height. Value is the
        TextLine instance at that position.

        """
        """
        FIX
        >>> from pagebot.toolbox.units import mm, uRound
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> style = dict(font='Verdana', fontSize=pt(12))
        >>> bs = context.newString('Example Text ' * 10, style=style)
        >>> baselines = bs.getBaselines(w=200)
        >>> baselines
        """
        baselines = {}
        for textLine in self.getTextLines(w, h):
            baselines[textLine.y] = textLine
        return baselines

    def getTextLines(self, w, h=None, align=LEFT):
        """Answers the dictionary of TextLine instances. Key is y position of
        the line.

        >>> from pagebot.toolbox.units import mm, uRound
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> style = dict(font='Verdana', fontSize=pt(12))
        >>> bs = context.newString('Example Text ' * 10, style=style)
        >>> lines = bs.getTextLines(w=200)
        >>> len(lines)
        5
        >>> line = lines[0]
        >>> line.maximumLineHeight
        1.4em
        >>>
        """
        assert w
        if not h:
            h = XXXL
        wpt, hpt = upt(w, h)
        textLines = []

        attrString = self.s.getNSObject()
        setter = CTFramesetterCreateWithAttributedString(attrString)
        path = CGPathCreateMutable()
        CGPathAddRect(path, None, CGRectMake(0, 0, wpt, hpt))
        ctBox = CTFramesetterCreateFrame(setter, (0, 0), path, None)
        ctLines = CTFrameGetLines(ctBox)
        origins = CTFrameGetLineOrigins(ctBox, (0, len(ctLines)), None)

        for lIndex, ctLine in enumerate(ctLines):
            origin = origins[lIndex]
            textLine = TextLine(ctLine, pt(origin.x), pt(origin.y), lIndex)
            textLines.append(textLine)
        return textLines

    @classmethod
    def _newFitWidthString(cls, fs, context, fontSize, w, pixelFit):
        if pixelFit:
            tx, _, tw, _ = pixelBounds(fs)
        else:
            tx, tw = 0, context.b.textSize(fs)[0]
        fspt, wpt, txpt, twpt = upt(fontSize, w, tx, tw)
        dxpt = twpt - txpt # Render the units, to compare for zero division
        if dxpt:
            return wpt * fspt / dxpt
        return None # Zero division, cannot calculate

    @classmethod
    def _newFitHeightString(cls, fs, context, fontSize, h, pixelFit):
        if pixelFit:
            _, ty, _, th = pixelBounds(fs)
        else:
            ty, th = 0, context.b.textSize(fs)[1]
        fspt, hpt, typt, thpt = upt(fontSize, h, ty, th)
        dypt = thpt - typt # Render the units, to compare for zero division
        if dypt:
            return hpt * fspt / dypt
        return None # Zero division, cannot calculate

    FITTING_TOLERANCE = 3

    @classmethod
    def fitString(cls, t, context, e=None, style=None, w=None, h=None,
            useXTRA=True, pixelFit=True):
        """Answers the DrawBotString instance from valid attributes in style.
        Set all values after testing their existence, so they can inherit from
        previous style formats in the string. If the target width w and height
        are defined, and if there is a [wdth] or [XTRA] axis in the current
        Variable Font, then values are iterated to make the best location /
        instance for the rectangle fit. In case the fontSize is set and the
        width w is set, then just use the [wdth] or [XTRA] to make a horizontal
        fit, keeping the size. If the axes run to extreme, the string is return
        without changing width. In case a font path was supplied, then try
        to get a Font instance for that path, as we need to test it for
        existing axes as Variable Font.

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> font = findFont('RobotoDelta-VF')
        >>> #font = findFont('Fit-Variable_1') # DJR-Fit needs to be installed.
        >>> style = dict(font=font, textFill=blackColor, textStroke=noColor)

        >>> 'wdth' in font.axes.keys() or 'XTRA' in font.axes.keys() # One of them is there
        True

        """

        """
        FIXME: Fitting does not work anymore.
        >>> s = DrawBotString.newString('Hello', context, style=style, w=pt(300))
        >>> s.bounds() # Rounded width
        (297, 195)
        >>> s = DrawBotString.fitString('Hello', context, style=style, w=pt(400), h=pt(220))
        >>> int(round(s.bounds()[2]-s.bounds()[0])) # Rounded pixel width
        399
        >>> int(round(s.bounds()[3]-s.bounds()[1])) # Rounded pixel height
        220
        >>> #s.bounds()

        """
        style = copy(style)
        location = copy(css('', e, style, default={})) # In case the used already supplied a VF location, use it.
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
                loc['opsz'] = upt(style['fontSize'])
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
                loc['opsz'] = upt(style['fontSize'])
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
        """Answers a DrawBotString instance from valid attributes in *style*.
        Set all values after testing their existence, so they can inherit from
        previous style formats in the string.

        If target width *w* or height *h* is defined, then *fontSize* is scaled
        to make the string fit *w* or *h*.  In that case the pixelFit flag
        defines if the current width or height comes from the pixel image of em
        size.

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> font = findFont('Roboto-Black')
        >>> context = DrawBotContext()
        """

        """
        TODO: Get more docTests to work
        >>> bs = context.newString('ABC', style=dict(font=font.path, fontSize=pt(22)))
        >>> bs
        ABC
        >>> bs = context.newString('ABC', style=dict(font=font.path, w=pt(100))
        >>> int(round(bs.fontSize))
        51
        >>> bs = context.newString('ABC', style=dict(font=font, w=pt(100)) # Use the font instance instead of path.
        >>> int(round(bs.fontSize))
        0.56em
        """
        # Get the drawBotBuilder, no need to check, we already must be in context here.
        if t is None:
            t = ''
        elif isinstance(t, str):
            t = str(t)

        fsAttrs = {}

        b = context.b

        # Set the hyphenation flag from style, as in DrawBot this is set by a global function,
        # not as FormattedString attribute.
        language = css('language', e, style)
        hyphenation = bool(css('hyphenation', e, style))
        b.language(language)
        b.hyphenation(hyphenation)

        # Font selection

        sFont = css('font', e, style)
        if sFont is not None:
            if hasattr(sFont, 'path'): # If the Font instance was supplied, then use it's path.
                sFont = sFont.path
            fsAttrs['font'] = sFont

        sFallbackFont = css('fallbackFont', e, style)
        if isinstance(sFallbackFont, Font):
            sFallbackFont = sFallbackFont.path
        elif sFallbackFont is None:
            sFallbackFont = DEFAULT_FALLBACK_FONT_PATH
        fsAttrs['fallbackFont'] = sFallbackFont

        # If there is a target (pixel) width or height defined, ignore the
        # requested fontSize and try the width or height first for fontSize =
        # 100. The resulting width or height is then used as base value to
        # calculate the needed point size.
        # Forced fontSize, then this overwrites the style['fontSize'] if it is
        # there.  TODO: add calculation of rFontSize (relative float based on
        # root-fontSize) here too.
        if w is not None or h is not None:
            uFontSize = pt(100) # Start with large font size to scale for fitting.
        else:
            # May be scaled to fit w or h if target is defined.
            uFontSize = css('fontSize', e, style, default=DEFAULT_FONT_SIZE)
        if uFontSize is not None:
            fsAttrs['fontSize'] = fontSizePt = upt(uFontSize) # Remember as base for relative units
        else:
            fontSizePt = DEFAULT_FONT_SIZE

        uLeading = css('leading', e, style)
        fsAttrs['lineHeight'] = upt(uLeading or DEFAULT_LEADING, base=fontSizePt) # Base for em or perc

        # Color values for text fill
        # Color: Fill the text with this color instance
        # noColor: Set the value to None, no fill will be drawn
        # inheritColor: Don't set color, inherit the current setting for fill
        cFill = css('textFill', e, style, default=blackColor) # Default is blackColor, not noColor
        if cFill is not inheritColor:
            if isinstance(cFill, (tuple, list, int, float)):
                cFill = color(cFill)
            elif cFill is None:
                cFill = noColor
            assert isinstance(cFill, Color), ('DrawBotString.newString: Fill color "%s" is not Color in style %s' % (cFill, style))
            if cFill is noColor:
                fsAttrs['fill'] = None
            elif cFill.isCmyk:
                fsAttrs['cmykFill'] = cFill.cmyk
            else:
                fsAttrs['fill'] = cFill.rgb

        # Color values for text stroke
        # Color: Stroke the text with this color instance
        # noColor: Set the value to None, no stroke will be drawn
        # inheritColor: Don't set color, inherit the current setting for stroke
        cStroke = css('textStroke', e, style, default=noColor)
        strokeWidth = css('textStrokeWidth', e, style)
        if strokeWidth is not None:
            assert isUnit(strokeWidth), ('DrawBotString.newString: strokeWidth %s must of type Unit' % strokeWidth)
            fsAttrs['strokeWidth'] = upt(strokeWidth, base=fontSizePt)
        if cStroke is not inheritColor:
            if isinstance(cStroke, (tuple, list, int, float)):
                cStroke = color(cStroke)
            elif cStroke is None:
                cStroke = noColor
            assert isinstance(cStroke, Color), ('DrawBotString.newString] Stroke color "%s" is not Color in style %s' % (cStroke, style))
            if cStroke is noColor: # None is value to disable stroke drawing
                fsAttrs['stroke'] = None
            elif cFill.isCmyk:
                fsAttrs['cmykFill'] = cFill.cmyk
            else:
                fsAttrs['fill'] = cFill.rgb

        sAlign = css('xTextAlign', e, style) # Warning: xAlign is used for element alignment, not text.
        if sAlign is not None: # yTextAlign must be solved by parent container element.
            fsAttrs['align'] = sAlign

        sUnderline = css('underline', e, style)
        if sUnderline in ('single', None): # Only these values work in FormattedString
            fsAttrs['underline'] = sUnderline

        uParagraphTopSpacing = css('paragraphTopSpacing', e, style)
        if uParagraphTopSpacing is not None:
            fsAttrs['paragraphTopSpacing'] = upt(uParagraphTopSpacing, base=fontSizePt) # Base for em or perc

        uParagraphBottomSpacing = css('paragraphBottomSpacing', e, style)
        if uParagraphBottomSpacing:
            fsAttrs['paragraphBottomSpacing'] = upt(uParagraphBottomSpacing, base=fontSizePt) # Base for em or perc

        uTracking = css('tracking', e, style)
        if uTracking is not None:
            fsAttrs['tracking'] = upt(uTracking, base=fontSizePt) # Base for em or perc

        uBaselineShift = css('baselineShift', e, style)
        if uBaselineShift is not None:
            fsAttrs['baselineShift'] = upt(uBaselineShift, base=fontSizePt) # Base for em or perc

        openTypeFeatures = css('openTypeFeatures', e, style)
        if openTypeFeatures is not None:
            fsAttrs['openTypeFeatures'] = openTypeFeatures

        tabs = css('tabs', e, style)
        if tabs is not None:
            fsAttrs['tabs'] = tabs

        # Set the hyphenation flag from style, as in DrawBot this is set by a global function,
        # not as FormattedString attribute.
        # FIX IN DRAWBOT fsAttrs['language'] = bool(css('language', e, style))
        # FIX IN DRAWBOT fsAttrs['hyphenation'] = bool(css('hyphenation', e, style))

        uFirstLineIndent = css('firstLineIndent', e, style)
        # TODO: Use this value instead, if current tag is different from
        # previous tag. How to get this info?
        # sFirstParagraphIndent = style.get('firstParagraphIndent')
        # TODO: Use this value instead, if currently on top of a new string.
        if uFirstLineIndent is not None:
            fsAttrs['firstLineIndent'] = upt(uFirstLineIndent, base=fontSizePt) # Base for em or perc

        uIndent = css('indent', e, style)
        if uIndent is not None:
            fsAttrs['indent'] = upt(uIndent, base=fontSizePt) # Base for em or perc

        uTailIndent = css('tailIndent', e, style)
        if uTailIndent is not None:
            fsAttrs['tailIndent'] = upt(uTailIndent, base=fontSizePt) # Base for em or perc

        sLanguage = css('language', e, style)
        if sLanguage is not None:
            fsAttrs['language'] = sLanguage

        if css('uppercase', e, style):
            t = t.upper()
        elif css('lowercase', e, style):
            t = t.lower()
        elif css('capitalized', e, style):
            t = t.capitalize()

        newT = b.FormattedString(t, **fsAttrs) # Format plain string t onto new formatted fs.

        isFitting = True
        if w is not None:
            # There is a target width defined, calculate again with the
            # fontSize ratio correction. We use the enclosing pixel bounds
            # instead of the context.textSide(newt) here, because it is much
            # more consistent for tracked text. context.textSize will add space
            # to the right of the string.
            fsAttrs = copy(fsAttrs)
            fittingFontSize = cls._newFitWidthString(newT, context, uFontSize, w, pixelFit)
            if fittingFontSize is not None: # Chedked on zero division
                fsAttrs['fontSize'] = fittingFontSize
                newS = cls.newString(t, context, style=fsAttrs)
                # Test the width we got by linear interpolation. Scale back if still too large.
                # Iterate until it really fits.
                while newS.size[0] > w and fsAttrs['fontSize']:
                    fsAttrs['fontSize'] -= 0.1 # Incremental decrease the size until it fits
                    newS = cls.newString(t, context, style=fsAttrs)
            else:
                newS = cls(newT, context, fsAttrs) # Cannot fit, answer untouched.
                isFitting = False
        elif h is not None:
            # There is a target height defined, calculate again with the
            # fontSize ratio correction. We use the enclosing pixel bounds
            # instead of the context.textSide(newt) here, because it is much
            # more consistent for tracked text. context.textSize will add space
            # to the right of the string.
            fsAttrs = copy(fsAttrs)
            fittingFontSize = cls._newFitHeightString(newT, context, uFontSize, h, pixelFit)
            if fittingFontSize is not None:
                fsAttrs['fontSize'] = fittingFontSize
                newS = cls.newString(t, context, style=fsAttrs)
                didFit = True
            else:
                newS = cls(newT, context, fsAttrs) # Cannot fit, answer untouched.
                isFitting = False
        else:
            newS = cls(newT, context, fsAttrs)
            fittingStyle = {}

        # Store any adjust fitting parameters in the string, in case the caller
        # wants to know.
        newS.fittingFontSize = pt(fsAttrs.get('fontSize'))
        newS.fittingFont = fsAttrs.get('font') # In case we are sampling with a Variable Font.
        newS.fittingLocation = fsAttrs.get('location')
        newS.isFitting = isFitting
        newS.language = language
        newS.hyphenation = hyphenation

        return newS

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
        return '[Found "%s" @ %d,%d]' % (self.s, self.x, self.y)

class TextRun:
    u"""The ctRun object contains the chunk of text that combines a single style.


    """
    def __init__(self, ctRun, runIndex):
        self.runIndex = runIndex # Index of the run in the TextLine
        self._ctRun = ctRun
        self._style = None # Property cash for constructed style from run parameters.
        self.glyphCount = gc = CTRunGetGlyphCount(ctRun)
        # Reverse the style from
        attrs = CTRunGetAttributes(ctRun)
        self.nsFont = attrs['NSFont']
        #self.fontDescriptor = f.fontDescriptor()
        self.fill = attrs['NSColor']
        self.nsParagraphStyle = attrs['NSParagraphStyle']
        self.attrs = attrs # Save, in case the caller want to query run parameters.

        self.iStart, self.iEnd = CTRunGetStringRange(ctRun)
        self.string = u''
        # Hack for now to find the string in repr-string if self._ctLine.
        # TODO: Make a better conversion here, not relying on the format of the repr-string.
        for index, part in enumerate(str(ctRun).split('"')[1].split('\\u')):
            if index == 0:
                self.string += part
            elif len(part) >= 4:
                self.string += chr(int(part[0:4], 16))
                self.string += part[4:]

        #print(gc, len(CTRunGetStringIndicesPtr(ctRun)), CTRunGetStringIndicesPtr(ctRun), ctRun)
        try:
            self.stringIndices = CTRunGetStringIndicesPtr(ctRun)[0:gc]
        except TypeError:
            self.stringIndices = [0]
        #CTRunGetStringIndices(ctRun._ctRun, CFRange(0, 5), None)[4]
        self.advances = CTRunGetAdvances(ctRun, CFRange(0, 5), None)
        #self.positions = CTRunGetPositionsPtr(ctRun)[0:gc]
        #CTRunGetPositions(ctRun, CFRange(0, 5), None)[4]
        #self.glyphFontIndices = CTRunGetGlyphsPtr(ctRun)[0:gc]
        #print(CTRunGetGlyphs(ctRun, CFRange(0, 5), None)[0:5])
        self.status = CTRunGetStatus(ctRun)

        # get all positions
        self.positions = CTRunGetPositions(ctRun, (0, gc), None)
        # get all glyphs
        self.glyphs = CTRunGetGlyphs(ctRun, (0, gc), None)

    def __len__(self):
        return self.glyphCount

    def __repr__(self):
        return '[TextRun #%d "%s"]' % (self.runIndex, self.string)

    def __getitem__(self, index):
        return self.string[index]

    def _get_style(self):
        """Answers the constructed style dictionary, with names that fit the
        standard PageBot style."""
        if self._style is None:
            self._style = dict(
                textFill=self.fill,
                pl=self.headIndent,
                pr=self.tailIndent,
                fontSize=self.fontSize,
                font=self.fontPath,
                leading=self.leading
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

    # Font metrics, based on self.nsFont. This can be different from
    # self.fontAswcencender and self.fontDescender, etc. which are based on the
    # current setting in the FormattedString

    def _get_ascender(self):
        fontSize = self.nsFont.pointSize()
        return em(self.nsFont.ascender()/fontSize, base=fontSize)
    ascender = property(_get_ascender)

    def _get_descender(self):
        fontSize = self.nsFont.pointSize()
        return em(self.nsFont.descender()/fontSize, base=fontSize)
    descender = property(_get_descender)

    def _get_capHeight(self):
        fontSize = self.nsFont.pointSize()
        return em(self.nsFont.capHeight()/fontSize, base=fontSize)
    capHeight = property(_get_capHeight)

    def _get_xHeight(self):
        fontSize = self.nsFont.pointSize()
        return em(self.nsFont.xHeight()/fontSize, base=fontSize)
    xHeight = property(_get_xHeight)

    def _get_italicAngle(self):
        return self.nsFont.italicAngle()
    italicAngle = property(_get_italicAngle)

    def _get_fontSize(self):
        return pt(self.nsFont.pointSize())
    fontSize = property(_get_fontSize)

    #def _get_leading(self):
    #    return self.nsFont.leading()
    #leading = property(_get_leading)

    def _get_fontMatrix(self):
        return self.nsFont.matrix()
    fontMatrix = property(_get_fontMatrix)

    def _get_textTransform(self):
        return self.nsFont.textTransform()
    textTransform = property(_get_textTransform)

    def _get_underlinePosition(self):
        fontSize = self.nsFont.pointSize()
        return em(self.nsFont.underlinePosition()/fontSize, base=fontSize)
    underlinePosition = property(_get_underlinePosition)

    def _get_underlineThickness(self):
        fontSize = self.nsFont.pointSize()
        return em(self.nsFont.underlineThickness()/fontSize, base=fontSize)
    underlineThickness = property(_get_underlineThickness)

    #   Paragraph attributes

    def _get_matrix(self):
        return CTRunGetTextMatrix(self._ctRun)
    matrix = property(_get_matrix)

    def _get_alignment(self):
        return self.nsParagraphStyle.alignment()
    alignment = property(_get_alignment)

    def _get_lineSpacing(self):
        fontSize = self.nsFont.pointSize()
        return em(self.nsParagraphStyle.lineSpacing()/fontSize, base=fontSize)
    lineSpacing = property(_get_lineSpacing)

    def _get_paragraphSpacing(self):
        fontSize = self.nsFont.pointSize()
        return em(self.nsParagraphStyle.paragraphSpacing()/fontSize, base=fontSize)
    paragraphSpacing = property(_get_paragraphSpacing)

    def _get_paragraphSpacingBefore(self):
        fontSize = self.nsFont.pointSize()
        return em(self.nsParagraphStyle.paragraphSpacingBefore()/fontSize, base=fontSize)
    paragraphSpacingBefore = property(_get_paragraphSpacingBefore)

    def _get_headIndent(self):
        fontSize = self.nsFont.pointSize()
        return em(self.nsParagraphStyle.headIndent()/fontSize, base=fontSize)
    headIndent = property(_get_headIndent)

    def _get_tailIndent(self):
        fontSize = self.nsFont.pointSize()
        return em(self.nsParagraphStyle.tailIndent()/fontSize, base=fontSize)
    tailIndent = property(_get_tailIndent)

    def _get_firstLineHeadIndent(self):
        fontSize = self.nsFont.pointSize()
        return em(self.nsParagraphStyle.firstLineHeadIndent()/fontSize, base=fontSize)
    firstLineHeadIndent = property(_get_firstLineHeadIndent)

    def _get_lineHeightMultiple(self):
        fontSize = self.nsFont.pointSize()
        return em(self.nsParagraphStyle.lineHeightMultiple()/fontSize, base=fontSize)
    lineHeightMultiple = property(_get_lineHeightMultiple)

    def _get_maximumLineHeight(self):
        fontSize = self.nsFont.pointSize()
        return em(self.nsParagraphStyle.maximumLineHeight()/fontSize, base=fontSize)
    maximumLineHeight = leading = property(_get_maximumLineHeight)

    def _get_minimumLineHeight(self):
        fontSize = self.nsFont.pointSize()
        return em(self.nsParagraphStyle.minimumLineHeight()/fontSize, base=fontSize)
    minimumLineHeight = property(_get_minimumLineHeight)


class TextLine:
    def __init__(self, ctLine, x, y, lineIndex):
        self._ctLine = ctLine
        self.x = x
        self.y = y
        self.lineIndex = lineIndex # Vertical line index in TextBox.
        self.string = ''
        self.textRuns = []

        for runIndex, ctRun in enumerate(CTLineGetGlyphRuns(ctLine)):
            textRun = TextRun(ctRun, runIndex)
            self.textRuns.append(textRun)
            self.string += textRun.string

    def __repr__(self):
        return '<%s #%d Runs:%d>' % (self.__class__.__name__, self.lineIndex, len(self.textRuns))

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

'''
def getTextLines(txt, box):
    """Answers a list of (x,y) positions of all line starts in the box. This function may become part
    of standard DrawBot in the near future."""
    x, y, w, h = box
    attrString = txt.getNSObject()
    setter = CoreText.CTFramesetterCreateWithAttributedString(attrString)
    path = Quartz.CGPathCreateMutable()
    Quartz.CGPathAddRect(path, None, Quartz.CGRectMake(x, y, w, h))
    box = CoreText.CTFramesetterCreateFrame(setter, (0, 0), path, None)
    ctLines = CoreText.CTFrameGetLines(box)
    return ctLines

def getBaselines(txt, box):
    """Answers a list of (x,y) positions of all line starts in the box. This function may become part
    of standard DrawBot in the near future."""
    x, y, w, h = box
    attrString = txt.getNSObject()
    setter = CoreText.CTFramesetterCreateWithAttributedString(attrString)
    path = Quartz.CGPathCreateMutable()
    Quartz.CGPathAddRect(path, None, Quartz.CGRectMake(x, y, w, h))
    box = CoreText.CTFramesetterCreateFrame(setter, (0, 0), path, None)
    ctLines = CoreText.CTFrameGetLines(box)
    #print(ctLines)
    origins = CoreText.CTFrameGetLineOrigins(box, (0, len(ctLines)), None)
    #print(origins)
    return [(x + o.x, y + o.y) for o in origins]

def getTextPositionSearch(bs, w, h, search, xTextAlign=LEFT, hyphenation=True):
    from AppKit import NSLocationInRange
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

    setter = CTFramesetterCreateWithAttributedString(attrString)
    box = CTFramesetterCreateFrame(setter, (0, 0), path, None)

    ctLines = CTFrameGetLines(box)
    origins = CTFrameGetLineOrigins(box, (0, len(ctLines)), None)

    rectangles = []
    for startLocation, endLocation in locations:
        minx = miny = maxx = maxy = None
        for i, (originX, originY) in enumerate(origins):
            ctLine = ctLines[i]
            bounds = CTLineGetImageBounds(ctLine, None)
            if bounds.size.width == 0:
                continue
            _, ascent, descent, leading = CTLineGetTypographicBounds(ctLine, None, None, None)
            height = ascent + descent
            lineRange = CTLineGetStringRange(ctLine)
            miny = maxy = originY

            if NSLocationInRange(startLocation, lineRange):
                minx, _ = CTLineGetOffsetForStringIndex(ctLine, startLocation, None)

            if NSLocationInRange(endLocation, lineRange):
                maxx, _ = CTLineGetOffsetForStringIndex(ctLine, endLocation, None)
                rectangles.append((ctLine, (minx, miny - descent, maxx - minx, height)))

            if minx and maxx is None:
                rectangles.append((ctLine, (minx, miny - descent, bounds.size.width - minx, height)))
                minx = 0

    return rectangles
'''

    #   F I N D

def findPattern(textLines, pattern):
    """Answers the point locations where this pattern occures in the Formatted
    String."""
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
