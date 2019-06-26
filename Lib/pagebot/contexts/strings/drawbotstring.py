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
from pagebot.contexts.strings.babelstring import BabelString
from pagebot.style import css
from pagebot.constants import LEFT, DEFAULT_FONT_SIZE, DEFAULT_LEADING
from pagebot.constants import DEFAULT_FALLBACK_FONT_PATH, XXXL, DEFAULT_LANGUAGE
from pagebot.fonttoolbox.objects.font import Font, getFont, getInstance
from pagebot.toolbox.color import color, Color, noColor, inheritColor, blackColor
from pagebot.toolbox.units import pt, upt, isUnit, units, em
from pagebot.contexts.strings.textline import TextLine

try:
    import drawBot as drawBotBuilder
    from AppKit import NSAttributeDictionary, NSRange
    from CoreText import (CTFramesetterCreateWithAttributedString,
            CTFramesetterCreateFrame, CTFrameGetLines, CTFrameGetLineOrigins)
    from Quartz import CGPathAddRect, CGPathCreateMutable, CGRectMake
except (AttributeError, ImportError):
    from pagebot.contexts.builders.nonebuilder import NoneDrawBotBuilder as drawBotBuilder
    # When importing doesn't work because not on OS X, set variables to None.
    NSFont = None
    NSAttributeDictionary = NSRange = None
    CGPathAddRect = CGPathCreateMutable = CGRectMake = None
    CTFramesetterCreateWithAttributedString = None
    CTFrameGetLines = None

def pixelBounds(fs):
    """Answers the pixel-bounds rectangle of the text.

    NOTE that @by can be a negative value, if there is text (e.g. overshoot)
    below the baseline.
    @bh is the amount of pixels above the baseline.
    For the total height of the pixel-map, calculate @ph - @py.
    For the total width of the pixel-map, calculate @pw - @px."""
    if not fs:
        return pt(0, 0, 0, 0)
    p = drawBotBuilder.BezierPath()
    p.text(fs, (0, 0))
    # OS X answers bw and bh as difference with bx and by. That is not really
    # intuitive, as the the total (width, height) then always needs to be
    # calculated by the caller. So, instead, the width and height answered is
    # the complete bounding box, and the (x, y) is the position of the bounding
    # box, compared to the (0, 0) of the string origin.
    bx, by, bw, bh = p.bounds()
    return pt(bx, by, bw - bx, bh - by)

class DrawBotString(BabelString):
    """DrawBotString is a wrapper around the standard DrawBot FormattedString."""

    BABEL_STRING_TYPE = 'fs'

    def __init__(self, s, context, style=None):
        """Constructor of the DrawBotString, wrapper around DrawBot
        FormattedString. Optionally store the (latest) style that was used to
        produce the formatted string.

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
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

        # Filled in case w or h are defined and depending if the font is a
        # variable font.
        self.fittingFontSize = pt(0) # Set to fitting font size, in case the size iterates to find width.
        self.fittingFont = None # In case we are sampling with a Variable Font.
        self.fittingLocation = None
        self.isFitting = False

        self.language = DEFAULT_LANGUAGE
        self.hyphenation = False
        super().__init__(self.s, context, style=style)

    def _get_s(self):
        """Answers the embedded FormattedString by property, to enforce checking
        type of the string."""
        return self._s
    def _set_s(self, s):
        """ Check on the type of s. Three types are supported here: plain
        strings, DrawBot FormattedString and the class of self."""
        assert isinstance(s, (DrawBotString, str)) or s.__class__.__name__ == 'FormattedString'
        if isinstance(s, str):
            s = self.context.b.FormattedString(s)
        elif isinstance(s, DrawBotString):
            s = s.s
        self._s = s
    s = property(_get_s, _set_s)

    def columnStart(self, firstColumnIndent):
        bs = self
        style = self.getStyleAtIndex(0)
        if style.get('firstLineIndent') is not None or firstColumnIndent is not None: # Something going on at start?
            style['fontSize'] = pt(0.0001) # Really really small place holder period.
            style['textFill'] = color(1, 1, 1, 1) # Transparant, so it will never show.
            style['firstLineIndent'] = firstColumnIndent or 0 # Then make this one work
            bs = self.context.newString('.', style=style) + bs
        return bs

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

    def getStyleAtIndex(self, index):
        """Answer the style dictionary with values at position index of the string.

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> c1 = color(0.2, 0.3, 0.4)
        >>> c2 = color(1, 0, 0.22)
        >>> style = style=dict(font='Verdana', fontSize=17, leading=21, textFill=c1, textStroke=c2, textStrokeWidth=pt(3))
        >>> bs = context.newString('Example Text1', style=style)
        >>> bs.getStyleAtIndex(3)['fontSize']
        17pt
        >>> style = dict(font='Georgia', fontSize=20, leading=25, textFill=c2, textStroke=c1, textStrokeWidth=pt(2))
        >>> bs += context.newString('Another Text', style=style)
        >>> bs.getStyleAtIndex(20)['leading']
        25pt
        >>> bs.getStyleAtIndex(20)['textFill']
        Color(r=1.0, g=0, b=0.22)
        """
        attrString = self.s.getNSObject()
        cIndex = 0
        style = {}

        if attrString:
            for nsObject in attrString.attributesAtIndex_effectiveRange_(index, None):
                if isinstance(nsObject, NSAttributeDictionary):
                    nsColor = nsObject.get('NSColor')
                    if nsColor is not None:
                        style['textFill'] = color(nsColor.redComponent(), nsColor.greenComponent(), nsColor.blueComponent())

                    nsColor = nsObject.get('NSStrokeColor')

                    if nsColor is not None:
                        style['textStroke'] = color(nsColor.redComponent(), nsColor.greenComponent(), nsColor.blueComponent())

                    strokeWidth = nsObject.get('NSStrokeWidth')

                    if strokeWidth is not None:
                        style['strokeWidth'] = pt(strokeWidth)

                    nsFont = nsObject.get('NSFont')

                    if nsFont is not None:
                        style['font'] = nsFont.fontName()
                        style['fontSize'] = pt(nsFont.pointSize())

                    pgStyle = nsObject.get('NSParagraphStyle')
                    style['tabs'] = tabs = {}
                    #for tab in pgStyle.tabStops:
                    #    tabe[tab] = 'a'
                    style['leading'] = pt(pgStyle.minimumLineHeight())
                    style['firstLineIndent'] = pt(pgStyle.firstLineHeadIndent())
                    style['indent'] = pt(pgStyle.headIndent())
                    style['tailIndent'] = pt(pgStyle.tailIndent())
                    # MORE FROM: Alignment 4, LineSpacing 0, ParagraphSpacing 0, ParagraphSpacingBefore 0,
                    #  0, LineHeight 21/21, LineHeightMultiple 0, LineBreakMode 0, Tabs (), DefaultTabInterval 0,
                    # Blocks (), Lists (), BaseWritingDirection -1, HyphenationFactor 0, TighteningForTruncation NO, HeaderLevel 0
                elif isinstance(nsObject, NSRange):
                    if cIndex >= index: # Run through until matching index, so the style cumulates.
                        break
                    cIndex += nsObject.length
        return style

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
        measured from bottom em-size to top em-size (including ascender+ and
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

    def bounds(self):
        """Answers the pixel-bounds rectangle of the text, if formatted by the
        option (w, h).

        NOTE that @by can be a negative value, if there is text (e.g.
        overshoot) below the baseline.
        @bh is the amount of pixels above the baseline.
        For the total height of the pixel-map, calculate @ph - @py.
        For the total width of the pixel-map, calculate @pw - @px."""

        # Set the hyphenation flag and language from self, as in DrawBot this
        # is set by a global function, not as FormattedString attribute.
        self.context.language(self.language)
        self.context.hyphenation(self.hyphenation)
        return pixelBounds(self.s)

    def fontContainsCharacters(self, characters):
        """Return a boolean if the current font contains the provided
        characters.  Characters is a string containing one or more
        characters."""
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
        return em(self.s.fontAscender() / fontSize, base=fontSize)

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
        """Append a glyph by his glyph name using the current font. Multiple
        glyph names are possible."""
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
        # TODO: Attributes don't seem to maintain in the string or overfill copy.
        language = self.language or 'en'
        hyphenation = self.hyphenation or True
        b.language(language)
        b.hyphenation(hyphenation)
        overflow = self.__class__(b.textOverflow(self.s, (0, 0, wpt, hpt), align), self.context)
        # Pass on these parameters to the new constructed DrawBotString.
        overflow.language = language
        overflow.hyphenation = hyphenation
        #print('OVERFLOW', overflow.language, overflow.hyphenation, overflow[:30])
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

        # Get the flag if fit locations should be rounded (less cached
        # instance) or accurate.
        roundVariableFitLocation = style.get('roundVariableFitLocation', True)

        # In case font is not a variable font, or not [wdth] or [XTRA] present,
        # then using normal string fit is the best we can do.
        if not 'wdth' in font.axes and not 'XTRA' in font.axes:
            return cls.newString(t, context, e=e, style=style, w=w, h=h, pixelFit=pixelFit)

        # Decide which axis to use for width adjustments and get the axis
        # values.
        if not useXTRA or not 'XTRA' in font.axes: # Try to force usage of [XTRA] if it exists, otherwise use[wdth]
            axisTag = 'wdth'
        else:
            axisTag = 'XTRA'
        minValue, defaultValue, maxValue = font.axes[axisTag]

        if h is not None: # Fitting in heigt, calculate/iterate for the fitting font size.
            bs = cls.newString(t, context, e=e, style=style, h=h, pixelFit=pixelFit)
            style['fontSize'] = bs.fittingFontSize
        else: # Assuming there is a fontSize set, we'll use that as vertical requirement
            bs = cls.newString(t, context, e=e, style=style, pixelFit=pixelFit)

        # Now we have a formatted string with a given fontSize, guess to fit on the width.
        tx, _, tw, _ = bs.bounds() # Get pixel bounds of the string
        tw = tw - tx # Pixel width of the current string.
        prevW = None # Testing if something changed, for extreme of axes.
        axisValue = defaultValue

        for n in range(100): # Limit the maximum amount of iterations as safeguard
            if tw > w: # Too wide, try iterate smaller in ratio of wdth/XTRA axis values
                maxValue = axisValue # Clip wide range to current
                # Guess the new axisvalue from the ratio of tw/w
                axisValue = (axisValue - minValue)/2 + minValue
                if roundVariableFitLocation:
                    axisValue = int(round(axisValue))
                loc = copy(location)
                loc[axisTag] = axisValue
                loc['opsz'] = upt(style['fontSize'])
                style['font'] = getInstance(font, loc)
                bs = cls.newString(t, context, e=e, style=style, pixelFit=pixelFit)
                tx, ty, tw, th = bs.bounds() # Get pixel bounds of the string
                tw = tw - tx # Total width for the current
                if prevW == tw: # Did not change, probably not able to get more condensed
                    break
                prevW = tw

            elif tw < w - cls.FITTING_TOLERANCE: # Too condensed, try to make wider.
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
                if prevW == tw: # Did not change, probably not able to get more condensed
                    break
                prevW = tw

            else: # We found a fitting VF-location within tolerance. Back out.
                break
        #print('Number of iterations', n)
        return bs

    @classmethod
    def getFSAttrs(cls, t, context, e=None, style=None, w=None, h=None, pixelFit=True):
        fsAttrs = {}

        # Font selection.
        sFont = css('font', e, style)

        if sFont is not None:
            # If the Font instance was supplied, then use it's path.
            if hasattr(sFont, 'path'):
                sFont = sFont.path
            fsAttrs['font'] = sFont

        sFallbackFont = css('fallbackFont', e, style)

        if isinstance(sFallbackFont, Font):
            sFallbackFont = sFallbackFont.path
        elif sFallbackFont is None:
            sFallbackFont = DEFAULT_FALLBACK_FONT_PATH

        fsAttrs['fallbackFont'] = sFallbackFont

        '''
        If there is a target (pixel) width or height defined, ignore the
        requested fontSize and try the width or height first for fontSize =
        100. The resulting width or height is then used as base value to
        calculate the needed point size.

        Forced fontSize, then this overwrites the style['fontSize'] if it is
        there.

        TODO: add calculation of rFontSize (relative float based on
        root-fontSize) here too.
        '''
        if w is not None or h is not None:
            uFontSize = pt(100) # Start with large font size to scale for fitting.
        else:
            # May be scaled to fit w or h if target is defined.
            uFontSize = css('fontSize', e, style, default=DEFAULT_FONT_SIZE)

        if uFontSize is not None:
            # Remember as base for relative units.
            fsAttrs['fontSize'] = fontSizePt = upt(uFontSize)
        else:
            fontSizePt = DEFAULT_FONT_SIZE

        uLeading = css('leading', e, style)

        # Base for em or percent.
        fsAttrs['lineHeight'] = upt(uLeading or DEFAULT_LEADING, base=fontSizePt)

        # Color values for text fill
        # Color: Fill the text with this color instance
        # noColor: Set the value to None, no fill will be drawn
        # inheritColor: Don't set color, inherit the current setting for fill
        cFill = css('textFill', e, style, default=blackColor)

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
            elif cFill.isRgba:
                fsAttrs['fill'] = cFill.rgba
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
            elif cStroke.isCmyk:
                fsAttrs['cmykStroke'] = cStroke.cmyk
            elif cStroke.isRgba:
                fsAttrs['stroke'] = cStroke.rgba
            else:
                fsAttrs['stroke'] = cStroke.rgb

        # NOTE: xAlign is used for element alignment, not text.
        sAlign = css('xTextAlign', e, style)

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

        tabs = []
        for tab in (css('tabs', e, style) or []): # Can be [(10, LEFT), ...] or [10, 20, ...]
            if not isinstance(tab, (list, tuple)):
                tab = upt(tab), LEFT
            else:
                tab = upt(tab[0]), tab[1]
            tabs.append(tab)
        if tabs:
            fsAttrs['tabs'] = tabs

        # Set the hyphenation flag from style, as in DrawBot this is set by a
        # global function, not as FormattedString attribute.
        # FIX IN DRAWBOT fsAttrs['language'] = bool(css('language', e, style))
        # FIX IN DRAWBOT
        #fsAttrs['hyphenation'] = bool(css('hyphenation', e, style))

        uFirstLineIndent = css('firstLineIndent', e, style)
        # TODO: Use this value instead, if current tag is different from
        # previous tag. How to get this info?
        # firstTagIndent = style.get('firstTagIndent')
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

        return fsAttrs

    @classmethod
    def newString(cls, t, context, e=None, style=None, w=None, h=None, pixelFit=True):
        """Answers a DrawBotString instance from valid attributes in *style*.
        Set all values after testing their existence, so they can inherit from
        previous style formats in the string.

        If target width *w* or height *h* is defined, then *fontSize* is scaled
        to make the string fit *w* or *h*.  In that case the pixelFit flag
        defines if the current width or height comes from the pixel image of em
        size.

        TODO: move shared functionality to BabelString.

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
        if t is None:
            t = ''

        elif not isinstance(t, str):
            t = str(t)

        fsAttrs = cls.getFSAttrs(t, context, e=e, style=style, w=w, h=h, pixelFit=pixelFit)

        if css('uppercase', e, style):
            t = t.upper()
        elif css('lowercase', e, style):
            t = t.lower()
        elif css('capitalized', e, style):
            t = t.capitalize()

        # Format plain string t onto new formatted fs.
        newT = context.b.FormattedString(t, **fsAttrs)
        isFitting = True

        # @@@@ Disable string fitting here. Use fitString(...) instead.
        """
        if False and w is not None:
            # A target width is already defined, calculate again with the
            # fontSize ratio correction. We use the enclosing pixel bounds
            # instead of the context.textSide(newT) here, because it is more
            # consistent for tracked text. context.textSize will add space to
            # the right of the string.
            fsAttrs = copy(fsAttrs)
            fsAttrs['textFill'] = fsAttrs.get('fill')
            fsAttrs['textStroke'] = fsAttrs.get('stroke')
            fsAttrs['textStrokeWidth'] = fsAttrs.get('strokeWidth')

            fittingFontSize = cls._newFitWidthString(newT, context, fsAttrs.get('fontSize', DEFAULT_FONT_SIZE), w, pixelFit)
            if fittingFontSize is not None: # Checked on zero division
                # Repair the attrs to style, so it can be reused for new string
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
        elif False and h is not None:
            # A target height is already defined, calculate again with the
            # fontSize ratio correction. We use the enclosing pixel bounds
            # instead of the context.textSide(newT) here, because it is
            # more consistent for tracked text. context.textSize will add space
            # to the right of the string.
            fsAttrs = copy(fsAttrs)
            fsAttrs['fontSize'] = fittingFontSize
            fsAttrs['textFill'] = fsAttrs.get('fill')
            fsAttrs['textStroke'] = fsAttrs.get('stroke')
            fsAttrs['textStrokeWidth'] = fsAttrs.get('strokeWidth')

            fittingFontSize = cls._newFitHeightString(newT, context, fsAttrs.get('fontSize', DEFAULT_FONT_SIZE), h, pixelFit)

            if fittingFontSize is not None:
                # Repair the attrs to style, so it can be reused for new string
                newS = cls.newString(t, context, style=fsAttrs)
                didFit = True
            else:
                newS = cls(newT, context, fsAttrs) # Cannot fit, answer untouched.
                isFitting = False
        else:
        """
        newS = cls(newT, context, fsAttrs)
        fittingStyle = {}

        # Store any adjust fitting parameters in the string, in case the caller
        # wants to know.
        newS.fittingFontSize = pt(fsAttrs.get('fontSize'))
        newS.fittingFont = fsAttrs.get('font') # In case we are sampling with a Variable Font.
        newS.fittingLocation = fsAttrs.get('location')
        newS.isFitting = isFitting
        newS.language = css('language', e, style)
        newS.hyphenation = css('hyphenation', e, style)
        return newS

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
