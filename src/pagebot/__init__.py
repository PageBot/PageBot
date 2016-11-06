# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in Drawbot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     __init__.py
#
import CoreText
import AppKit

import re
from drawBot import FormattedString, cmykFill, fill, cmykStroke, stroke, strokeWidth
from drawBot.context.baseContext import BaseContext

NO_COLOR = -1

def setFillColor(c, fs=None, cmyk=False):
    u"""Set the color for global or the color of the formatted string."""
    if c is NO_COLOR:
        pass # Color is undefined, do nothing.
    elif c is None or isinstance(c, (float, long, int)): # Because None is a valid value.
        if cmyk:
            if fs is None:
                cmykFill(c)
            else:
                fs.cmykFill(c)
        else:
            if fs is None:
                fill(c)
            else:
                fs.fill(c)
    elif isinstance(c, (list, tuple)) and len(c) in (3, 4):
        if cmyk:
            if fs is None:
                cmykFill(*c)
            else:
                fs.cmykFill(*c)
        else:
            if fs is None:
                fill(*c)
            else:
                fs.fill(*c)
    else:
        raise ValueError('Error in color format "%s"' % repr(c))
    
def setStrokeColor(c, w=1, fs=None, cmyk=False):
    u"""Set global stroke color or the color of the formatted string."""
    if c is NO_COLOR:
        pass # Color is undefined, do nothing.
    elif c is None or isinstance(c, (float, long, int)): # Because None is a valid value.
        if cmyk:
            if fs is None:
                cmykStroke(c)
            else:
                fs.cmykStroke(c)
        else:
            if fs is None:
                stroke(c)
            else:
                fs.stroke(c)
    elif isinstance(c, (list, tuple)) and len(c) in (3, 4):
        if cmyk:
            if fs is None:
                cmykStroke(*c)
            else:
                fs.cmykStroke(*c)
        else:
            if fs is None:
                stroke(*c)
            else:
                fs.stroke(*c)
    else:
        raise ValueError('Error in color format "%s"' % c)
    if w is not None:
        strokeWidth(w)

def cp2p(cx, cy, style):
    u"""Convert columns point to page position."""
    gutter = style['g']
    marginLeft = style['ml']
    marginTop = style['mt']
    columnWidth = style['cw']
    columnHeight = style['ch']
    return (marginLeft + cx * (columnWidth + gutter),
            marginTop + cy * (columnHeight + gutter))
    
def cr2p(cx, cy, cw, ch, style):
    u"""Convert columns rect to page position/size."""
    gutter = style['g']
    marginLeft = style['ml']
    marginTop = style['mt']
    columnWidth = style['cw']
    columnHeight = style['ch']
    w = style['w']
    h = style['h']

    return (
        marginLeft + cx * (columnWidth + gutter),
        h - marginTop - (cy + ch) * (columnHeight + gutter) + gutter,
        cw * (columnWidth + gutter) - gutter,
        ch * (columnHeight + gutter) - gutter)

MARKER_PATTERN = '==%s--%s=='
FIND_FS_MARKERS = re.compile('\=\=([a-zA-Z0-9_]*)\-\-([^=]*)\=\=')

def getMarker(markerId, arg=None):
    u"""Answer a formatted string with markerId that can be used as non-display marker. 
    This way the Composer can find the position of markers in text boxes, after
    FS-slicing has been done. Note there is always a very small "white-space"
    added to the string, so there is a potential difference in width that matters.
    For that reason markers should not be changed after slizing (which would theoretically
    alter the flow of the FormattedString in an box) and the markerId and amount/length 
    of args should be kept as small as possible.
    Note that there is a potential problem of slicing through the argument string at 
    the end of a textBox. That is another reason to keep the length of the arguments short.
    And not to use any spaces, etc. inside the markerId.
    Possible slicing through line-endings is not a problem, as the raw string ignores them."""
    marker = MARKER_PATTERN % (markerId, arg or '')
    return FormattedString(marker, fill=None, stroke=None, fontSize=0.0000000000001)
    ###return FormattedString(marker, fill=(1, 0, 0), stroke=None, fontSize=10)

def findMarkers(fs, w, h, align='left', hyphenation=True):
    u"""Answer a dictionary of markers with their arguments and their formatted text rectangles
    that exist in a given FormattedString."""
    return textSearch(fs, w, h, FIND_FS_MARKERS, align, hyphenation)

def getFormattedString(t, style=None):
    u"""Answer a formatted string from valid attributes in Style. Set the all values after testing,
    so they can inherit from previous style formats."""
    fs = FormattedString()
    if style is not None:
        sFont = style.get('font')
        if sFont is not None:
            fs.font(sFont)
        sFontSize = style.get('fontSize')
        if sFontSize is not None:
            fs.fontSize(sFontSize)
        sFallbackFont = style.get('fallbackFont')
        if sFallbackFont is not None:
            fs.fallbackFont(sFallbackFont)
        sFill = style.get('fill', NO_COLOR)
        if sFill is not NO_COLOR: # Test on this flag, None is valid value
            setFillColor(sFill, fs)
        sCmykFill = style.get('cmykFill', NO_COLOR)
        if sCmykFill is not NO_COLOR:
            setFillColor(sCmykFill, fs, cmyk=True)
        sStroke = style.get('stroke', NO_COLOR)
        sStrokeWidth = style.get('strokeWidth')
        if sStroke is not NO_COLOR and strokeWidth is not None:
            setStrokeColor(sStroke, sStrokeWidth, fs)
        sCmykStroke = style.get('cmykStroke', NO_COLOR)
        if sCmykStroke is not NO_COLOR:
            setStrokeColor(sCmykStroke, sStrokeWidth, fs, cmyk=True)
        sAlign = style.get('align')
        if sAlign is not None:
            fs.align(sAlign)
        sLeading = style.get('leading')
        rLeading = style.get('rLeading')
        print u'ASASASSS %s' % t, sLeading, rLeading
        if sLeading is not None or (rLeading is not None and sFontSize is not None):
            fs.lineHeight((sLeading or 0) + (rLeading or 0) * (sFontSize or 0))
        sParagraphTopSpacing = style.get('paragraphTopSpacing')
        rParagraphTopSpacing = style.get('rParagraphTopSpacing')
        if sParagraphTopSpacing is not None or (rParagraphTopSpacing is not None and sFontSize is not None):
            fs.paragraphTopSpacing((sParagraphTopSpacing or 0) + (rParagraphTopSpacing or 0) * (sFontSize or 0))
        sParagraphBottomSpacing = style.get('paragraphBottomSpacing')
        rParagraphBottomSpacing = style.get('rParagraphBottomSpacing')
        if sParagraphBottomSpacing is not None or (rParagraphBottomSpacing is not None and sFontSize is not None):
            fs.paragraphBottomSpacing((sParagraphBottomSpacing or 0) + (rParagraphBottomSpacing or 0) * (sFontSize or 0))
        sTracking = style.get('tracking')
        rTracking = style.get('rTracking')
        if sTracking is not None or (rTracking is not None and sFontSize is not None):
            fs.tracking((sTracking or 0) + (rTracking or 0) * (sFontSize or 0))
        sBaselineShift = style.get('baselineShift')
        rBaselineShift = style.get('rBaselineShift')
        if sBaselineShift is not None or (rBaselineShift is not None and sFontSize is not None):
            fs.baselineShift((sBaselineShift or 0) + (rBaselineShift or 0) * (sFontSize or 0))
        sOpenTypeFeatures = style.get('openTypeFeatures')
        if sOpenTypeFeatures is not None:
            fs.openTypeFeatures(sOpenTypeFeatures)
        sTabs = style.get('tabs')
        if sTabs is not None:
            fs.tabs(*sTabs)
        sFirstLineIndent = style.get('firstLineIndent')
        rFirstLineIndent = style.get('rFirstLineIndent')
        if sFirstLineIndent is not None:
            fs.firstLineIndent((sFirstLineIndent or 0) + (rFirstLineIndent or 0) * (sFontSize or 0))
        sIndent = style.get('indent')
        rIndent = style.get('rIndent')
        if sIndent is not None or (rIndent is not None and sFontSize is not None):
            fs.indent((sIndent or 0) + (rIndent or 0) * (sFontSize or 0))
        sTailIndent = style.get('tailIndent')
        rTailIndent = style.get('rTaildIndent')
        if sTailIndent is not None or (rTailIndent is not None and sFontSize is not None):
            fs.tailIndent((sTailIndent or 0) + (rTailIndent or 0) * (sFontSize or 0))
        sLanguage = style.get('language')
        if sLanguage is not None:
            fs.language(sLanguage)
        #fs.hyphenation(style.hyphenation)        
    fs.append(t)
    return fs

def textSearch(fs, w, h, search, align='left', hyphenation=True):
    u"""
    """
    bc = BaseContext()
    path = CoreText.CGPathCreateMutable()
    CoreText.CGPathAddRect(path, None, CoreText.CGRectMake(0, 0, w, h))

    attrString = bc.attributedString(fs, align=align)
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
                rectangles.append((minx, miny - descent, maxx - minx, height))

            if minx and maxx is None:
                rectangles.append((minx, miny - descent, bounds.size.width - minx, height))
                minx = 0

    return rectangles


