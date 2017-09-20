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
from pagebot.elements.views.strings.babelstring import BabelString
from pagebot.style import css, NO_COLOR, LEFT

class FsString(BabelString):

    BABEL_STRING_TYPE = 'fs'

    u"""FsString is a wrapper around the standard DrawBot FormattedString."""
    def __init__(self, s, b):
        self.b = b # Store the builder, in case we need it.
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
        return self.b.textSize(self.s, w)

    def textOverflow(self, w, h, align=LEFT):
        print '@#@#@#@#@#', self.s, 111111, w, 22222222, h, 3333333, align
        return self.b.textOverflow(self.fs, (0, 0, w, h), align)

def newFsString(t, view=None, e=None, style=None, w=None, h=None, fontSize=None, styleName=None, tagName=None):
    u"""Answer a FsString instance from valid attributes in *style*. Set all values after testing
    their existence, so they can inherit from previous style formats.
    If target width *w* or height *h* is defined, then *fontSize* is scaled to make the string fit *w* or *h*."""
    if view is None:
        from pagebot.elements.views.drawbotview import DrawBotView
        view = DrawBotView # Class used as reference to access class methods and view related builder instance.
        b = view.b

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
        view.setTextFillColor(fs, sFill)
    sCmykFill = css('cmykFill', e, style, NO_COLOR)
    if sCmykFill is not NO_COLOR:
        view.setTextFillColor(fs, sCmykFill, cmyk=True)
    sStroke = css('textStroke', e, style, NO_COLOR)
    sStrokeWidth = css('textStrokeWidth', e, style)
    if sStroke is not NO_COLOR and sStrokeWidth is not None:
        view.setTextStrokeColor(fs, sStroke, sStrokeWidth)
    sCmykStroke = css('cmykStroke', e, style, NO_COLOR)
    if sCmykStroke is not NO_COLOR:
        view.setTextStrokeColor(fs, sCmykStroke, sStrokeWidth, cmyk=True)
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


