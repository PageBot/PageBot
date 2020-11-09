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
#     babelrun.py

from pagebot.constants import (DEFAULT_LANGUAGE, DEFAULT_FONT_SIZE,
        DEFAULT_FONT, LEFT)
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.toolbox.units import units, em, upt
from pagebot.toolbox.color import color

class BabelRun:

    def __init__(self, s, style=None):
        """Answers the storage for string + style in BabelString. Note that the
        style values of sequential runs are *not* cascading. This is similar to
        the behavior of the DrawBot FormattedString attributes.


        >>> from pagebot.elements import *
        >>> BabelRun('ABCD', dict(font='PageBot-Regular'))
        <BabelRun "ABCD">
        >>> BabelRun('ABCD'*10) # Abbreviated for string > 10 characters.
        <BabelRun "ABCDABCDAB...">
        >>> len(BabelRun('ABCD'*10))
        40
        """
        assert isinstance(s, str)
        self.s = s

        if style is None:
            style = {}
        self.style = style

        self._cr = None # Optional cache of native context run (e.g. CTRun or FlatRunData)

    def __len__(self):
        return len(self.s)

    def __eq__(self, pbr):
        """
        >>> from pagebot.toolbox.units import pt
        >>> br1 = BabelRun('ABCD')
        >>> br2 = BabelRun('ABCD')
        >>> br1 == br2, br1 is br2
        (True, False)
        >>> br2.style['fontSize'] = pt(12)
        >>> br1 == br2
        False
        """
        if not isinstance(pbr, self.__class__):
            return False
        return self.s == pbr.s and self.style == pbr.style

    def __repr__(self):
        r = '<%s' % self.__class__.__name__
        if self.s:
            s = self.s[:10]
            if s != self.s:
                s += '...'
            r += ' "%s"' % s.replace('\n',' ')
        return r + '>'

    def getFont(self, style=None):
        if not style:
            style = self.style
        fontName = style.get('font', DEFAULT_FONT)
        if fontName is None:
            fontName = DEFAULT_FONT
        return findFont(fontName)

    def getFSStyle(self):
        # D E P R E C A T E D
        # FIXME - Petr The question is if we need to convert to FlatString at all.
        # Can't we just use the main data in Babelstring, until processing into
        # lines or text?

        # Instead of using e.g. bs.tracking, we need to process the styles
        # of all runs, not just the last one.
        style = self.style

        # DrawBot-OSX, setting the hyphenation is global, before a
        # FormattedString is created.
        hyphenation = style.get('hyphenation', False)

        # In case an error occurs in these parameters, DrawBot ignores all.
        #    upt(fontSize), upt(leading, base=fontSize),
        #    textColor.rgba, align)

        # Create the style for this text run.
        font = self.getFont()

        if font is None:
            fontPath = DEFAULT_FONT
        else:
            fontPath = font.path
        fontSize = style.get('fontSize', DEFAULT_FONT_SIZE)
        leading = style.get('leading', em(1, base=fontSize)) # Vertical space adding to fontSize.

        fsStyle = dict(
            font=fontPath,
            fontSize=upt(fontSize),
            lineHeight=upt(leading, base=fontSize),
            align=style.get('xTextAlign') or style.get('xAlign', LEFT),
            tracking=upt(style.get('tracking', 0), base=fontSize),
            strokeWidth=upt(style.get('strokeWidth')),
            baselineShift=upt(style.get('baselineShift'), base=fontSize),
            language=style.get('language', DEFAULT_LANGUAGE),
            indent=upt(style.get('indent', 0), base=fontSize),
            tailIndent=-abs(upt(style.get('tailIndent', 0), base=fontSize)), # DrawBot wants negative number)
            firstLineIndent=upt(style.get('firstLineIndent', 0), base=fontSize),
            underline={True:'single', False:None}.get(style.get('underline', False)),
            # Increasing value moves text up, decreasing the leading.
            paragraphTopSpacing=upt(style.get('paragraphTopSpacing', 0), base=fontSize),
            paragraphBottomSpacing=upt(style.get('paragraphBottomSpacing', 0), base=fontSize),
        )

        if 'textFill' in style:
            textFill = style['textFill']
            if textFill is not None:
                textFill = color(textFill)
            if textFill.isCmyk:
                fsStyle['cmykFill'] = textFill.cmyk
            else:
                fsStyle['fill'] = textFill.rgba

        if 'textStroke' in style:
            textStroke = style['textStroke']
            if textStroke is not None:
                textStroke = color(textStroke)

                if textStroke.isCmyk:
                    fsStyle['cmykStroke'] = textStroke.cmyk
                else:
                   fsStyle['stroke'] = textStroke.rgba

        if 'openTypeFeatures' in style:
            fsStyle['openTypeFeatures'] = style['openTypeFeatures']

        if 'fontVariations' in style:
            fsStyle['fontVariantions'] = style['fontVariations']

        if 'tabs' in style:
            tabs = [] # Render the tab values to points.
            tabsDict = style.get('tabs', {})
            if not tabsDict:
                tabsDict = {}
            for tx, alignment in tabsDict:
                tabs.append((upt(tx, base=fontSize), alignment))
            fsStyle['tabs'] = tabs

        return fsStyle, hyphenation

class BabelLineInfo:
    """BabelLineInfo is information decompiled from a native context text line
    run.  It resembles as close a possible to original source that generated
    the the text line/run, but it will never be the same. E.g. any OT-feature
    glyph replacement cannot be reconstructed to the original string."""

    def __init__(self, x, y, context, cLine=None):
        """Container for line info, after text wrapping by context."""
        self.x = units(x)
        self.y = units(y)
        self.runs = [] # List of BabelRunInfo instances.
        self.context = context # Just in case it is needed.
        # Optional native "context line" (e.g. DrawBot-->CTLine instance.
        # Flat-->the result of placedText.layout.runs() looping).
        self.cLine = cLine

    def __repr__(self):
        return '<%s y=%s>' % (self.__class__.__name__, self.y)


class BabelRunInfo:
    """BabelRunInfo is information decompiled from a native context text line.
    It resembles as close a possible to original source that generated the the
    text line/run, but it will never be the same. E.g. any OT-feature glyph
    replacement cannot be reconstructed to the original string."""

    def __init__(self, s, style, context, cRun=None):
        assert isinstance(s, str)
        self.s = s # Reconstructed string, may not be input for e.g. OT-features
        self.style = style # Reconstructed style of the run.
        #print(style)
        self.context = context # Just in case it is needed
        # Optional native "context run"
        # (e.g. DrawBot-->CTRun instance. Flat-->)
        self.cRun = cRun

    def __repr__(self):
        return '<%s "%s">' % (self.__class__.__name__, self.s)
