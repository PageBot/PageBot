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
#     babelstring.py
#
from pagebot.elements.views import stringTypes

class BabelString(object):
    u"""SuperString instances keep parallel (formatted) string representations for all strings
    needed by the available builder classes. Default behavior is to support all of them,
    but if builders are not in the current framework or indicated in the contructor,
    some types of strings may be left out."""

    def __init__(self, s, types=None, style=None):
        if types is None:
            types = stringTypes.keys() # Get the type tags for the kind of strings that are supported.
        if 'fs' in types:
            fs = s
            if isinstance(fs, basestring):
                fs = self.newString_fs(s, e=e, style=style)
            self.fs = fs
        else:
            self.fs = None

        # F L A T  S U P P O R T
        if 'flat' in types:
            self.flat = flatString = s # TODO: Needs formatting
        else:
            self.flat = None

        # H T M L  S U P P O R T
        if 'html' in types:
            self.html = s
        else:
            self.html = None

    def append_fs(self, s):
        if self.fs is not None:
            self.fs += s
        
    def append_flat(self, s):
        if self.flat is not None:
            self.flat += s
        
    def append_html(self, s):
        if self.html is not None:
            self.html += s
        
    def append(self, s):
        self.append_fs(s)
        self.append_flat(s)
        self.append_html(s)

    def newString_fs(self, t, e=None, style=None, w=None, h=None, fontSize=None, styleName=None, tagName=None):
        u"""Answer a *FormattedString* instance from valid attributes in *style*. Set all values after testing
        their existence, so they can inherit from previous style formats.
        If target width *w* or height *h* is defined, then *fontSize* is scaled to make the string fit *w* or *h*."""
        b = stringTypes['drawBot'].b
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
            setFillColor(None, sFill, fs)
        sCmykFill = css('cmykFill', e, style, NO_COLOR)
        if sCmykFill is not NO_COLOR:
            self.setFillColor_drawBot(None, sCmykFill, fs, cmyk=True)
        sStroke = css('textStroke', e, style, NO_COLOR)
        sStrokeWidth = css('textStrokeWidth', e, style)
        if sStroke is not NO_COLOR and sStrokeWidth is not None:
            setStrokeColor(None, sStroke, sStrokeWidth, fs)
        sCmykStroke = css('cmykStroke', e, style, NO_COLOR)
        if sCmykStroke is not NO_COLOR:
            setStrokeColor(None, sCmykStroke, sStrokeWidth, fs, cmyk=True)
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
            t = t.upper()
        elif sLowercase:
            t = t.lower()
        elif sCapitalized:
            t = t.capitalize()

        newt = fs + t # Format plain string t onto new formatted fs.
        if w is not None: # There is a target width defined, calculate again with the fontSize ratio correction. 
            tw, _ = textSize(newt)
            fontSize = w / tw * sFontSize
            newt = newFS(t, e, style, fontSize=fontSize, styleName=styleName, tagName=tagName)
        elif h is not None: # There is a target height defined, calculate again with the fontSize ratio correction. 
            _, th = textSize(newt)
            fontSize = h / th * sFontSize
            newt = newFS(t, e, style, fontSize=fontSize, styleName=styleName, tagName=tagName)

        return newt


