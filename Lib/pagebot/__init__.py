# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     pagebot/__init__.py
#
from __future__ import division
__doc__ = """PageBot module"""

import CoreText
import AppKit
import Quartz

import re
from drawBot import FormattedString, cmykFill, fill, cmykStroke, stroke, strokeWidth, \
    hyphenation, cmykLinearGradient, linearGradient, cmykRadialGradient, radialGradient,\
    shadow

from drawBot.context.baseContext import BaseContext

from pagebot.style import NO_COLOR, LEFT
from pagebot.toolbox.transformer import point2D

#
# In order to let PageBot scripts and/applications exchange information, without the need to save
# data in files, the pbglobals module supports the storage of non-persistent information.
# This way, applications with Vanilla windows can be used as UI for scripts that perform as batch process.
# Note that it is up to the responsibilty of individual scripts to create uniqued ids for
# attributes. Also they need to know from each other, in case information is exchanges""".
#
# Key is script/application id, e.g. their __file__ value.
# Access as:
# from pagebot.toolbox.transformer import path2ScriptId
# scriptGlobals = pagebot.getGlobals(path2ScriptId(__file__))
# or direct as:

pbGlobals = {}

class Globals(object):
    # Allow adding by attribute and key.
    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

def getGlobals(scriptId):
    u"""In order to let PageBot scripts and/applications exchange information, without the
    need to save as files, the pbglobals module supports the storage of non-persistent information.
    This way, applications with Vanilla windows can be used as UI for scripts that perform as batch process.
    Note that it is up to the responsibilty of individual scripts to create uniqued ids for
    attributes. Also they need to know from each other, in case information is exchanged."""
    if not scriptId in pbGlobals:
        pbGlobals[scriptId] = Globals()
    return pbGlobals[scriptId]

def x2cx(x, e):
    u"""Transform from y value to column y value, using the e.css for colunn values."""
    gw = e.gw # Gutter
    cw = e.css('cw', 0)
    if cw + gw: # Check on division by 0
        return (x - e.parent.pl) / (cw + gw)
    return 0

def cx2x(cx, e):
    if cx is None:
        x = 0
    else:
        x = e.parent.pl + cx * (e.css('cw', 0) + e.gw)
    return x

def y2cy(y, e):
    u"""Transform from y value to column y value, using the e.css for colunn values."""
    gh = e.gh # Gutter
    ch = e.css('ch', 0)
    cy = 0
    if ch + gh: # Check on division by 0
        if e.originTop:
            paddingY = e.pt
        else:
            paddingY = e.pb
        cy = (y - paddingY) / (ch + gh)
    return cy

def cy2y(cy, e):
    u"""Transform from column y value to y value, using the e.css for colunn values."""
    if cy is None:
        y = 0
    else:
        if e.originTop:
            paddingY = e.pt
        else:
            paddingY = e.pb
        y = paddingY + cy * (e.css('ch', 0) + e.gh)
    return y

def z2cz(z, e):
    u"""Transform from z value to column z value, using the e.css for colunn values."""
    gd = e.gd # Gutter
    cd = e.css('cd', 0) # Column width
    cz = 0
    if cd + gd: # Check on division by 0
        cz = (z - e.parent.pzf) / (cd + gd)
    return cz

def cz2z(cz, e):
    if cz is None:
        z = 0
    else:
        z = e.parent.pzf + cz * (e.css('cd', 0) + e.gd)
    return z

# Number of cols, rows, lanes
# TODO Make this work
"""
def w2cols(w, e): # Answer the rounded amount of columns that fit in the given width.
    gw = e.gw
    cw = e.css('cw', 0)
    if cw + gw:
        return int((e.w - e.pl - e.pr + gw) / (cw + gw))

def cols2w(w, e): # Answer the col width for the give amount of colums
    gw = e.gw
    cw = e.css('cw', 0)
    if cw + gw:
        return int((e.w - e.pl - e.pr + gw) / (cw + gw))
    
def w2rows(w, e): # Answer the rounded amount of rows that fit in the given width.
    gh = e.gh
    ch = e.css('ch', 0)
    if ch + gh:
        return int((e.h - e.pt - e.pb + gh) / (ch + gh))

def rows2w(w, e): # Answer the row width for the give amount of colums
    gh = e.gh
    ch = e.css('ch', 0)
    if ch + gh:
        return int((e.h - e.pt - e.pr + e.gw) / (cw + gw))
    
def w2cols(w, e): # Answer the rounded amount of columns that fit in the given width.
    gw = e.gw
    cw = e.css('cw', 0)
    if cw + gw:
        return int((e.w - e.pl - e.pr + e.gw) / (cw + gw))

def cols2w(w, e): # Answer the col with for the give amount of colums
    gw = e.gw
    cw = e.css('cw', 0)
    if cw + gw:
        return int((e.w - e.pl - e.pr + e.gw) / (cw + gw))
"""    

# Size

def w2cw(w, e):
    gw = e.gw
    cw = e.css('cw', 0)
    if cw + gw: # Test for division by 0
        return (w + gw) / (cw + gw)
    return 0 # Undefined, not info about column width and gutter or zero division

def cw2w(cw, e):
    if cw is None:
        w = 0
    else:
        gw = e.gw
        w = cw * (e.css('cw', 0) + gw) - gw  # Overwrite style from here.
    return w

def h2ch(h, e):
    gh = e.gh
    ch = e.css('ch', 0)
    if ch + gh: # Test for division by 0
        return (h + gh) / (ch + gh)
    return 0 # Undefined, no info about column height and gutter or zero division

def ch2h(ch, e):
    if ch is None:
        h = 0
    else:
        gh = e.gh
        h = ch * (e.css('ch', 0) + gh) - gh  # Overwrite style from here.
    return h

def d2cd(d, e):
    guttgderD = e.gd
    cd = e.css('cd', 0)
    if cd + gd: # Test for division by 0
        return (d + gd) / (cd + gd)
    return 0 # Undefined, no info about column depth and gutter or zero division

def cd2d(cd, e):
    if cd is None:
        d = 0
    else:
        gutterD = e.gd
        d = cd * (e.css('cd', 0) + gd) - gd  # Overwrite style from here.
    return d

def baseline2y(yIndex, e):
    u"""Convert columns index and line index to page position. Answered (x, y) is point position based on
    marginTop + yIndex*baseLine."""
    padT = e.pt
    baseline = e.css('baseline')
    return padT + cy * baseline

def getRootPath():
    u"""Answer the root path of the pagebot module."""
    return '/'.join(__file__.split('/')[:-2]) # Path of this file with pagebot/__init__.py(c) removed.

def getFontPath():
    u"""Answer the standard font path of the pagebot module."""
    return getRootPath() + '/fonts/'

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

class Gradient(object):
    u"""
    As linear gradient (startRadius or endRadius not set):
    startPoint as (x, y)
    endPoint as (x, y)
    colors as a list of colors, described similary as fill
    locations of each color as a list of floats. (optionally)
    Setting a gradient will ignore the fill.

    As radial gradiens (startRadius and endRadius are set):
    startPoint as (x, y)
    endPoint as (x, y)
    colors as a list of colors, described similary as fill
    locations of each color as a list of floats. (optionally)
    startRadius radius around the startPoint in degrees (optionally)
    endRadius radius around the endPoint in degrees (optionally)
    Setting a gradient will ignore the fill.
    """
    def __init__(self, start=None, end=None, colors=None, cmykColors=None, locations=None,
        startRadius=None, endRadius=None):
        # TODO: Add assert test of locations has same length as colors.
        self.start = start or (0.5, 0) # Default to start a center of bottom.
        self.end = end or (0.5, 1) # Default to end at center of top.
        self.colors = colors or ((0,0,0), (1,1,1)) # Default to run between black and white.
        self.cmykColors = None
        self.locations = locations or [0,1]
        self.startRadius = startRadius
        self.endRadius = endRadius

    def _get_linear(self):
        return not self.radial
    linear = property(_get_linear)

    def _get_radial(self):
        return self.startRadius is not None and self.endRadius is not None
    radial = property(_get_radial)

def setGradient(gradient, origin, e):
    u"""Define the gradient call to match the size of element e., Gradient position
    is from the origin of the page, so we need the current origin of e."""
    assert isinstance(gradient, Gradient)
    start = origin[0] + gradient.start[0] * e.w, origin[1] + gradient.start[1] * e.h
    end = origin[0] + gradient.end[0] * e.w, origin[1] + gradient.end[1] * e.h

    if gradient.linear:
        if gradient.cmykColors is None:
            linearGradient(startPoint=start, endPoint=end,
                colors=gradient.colors, locations=gradient.locations)
        else:
            cmykLinearGradient(startPoint=start, endPoint=end,
                colors=gradient.cmykColors, locations=gradient.locations)
    else: # Gradient must be radial.
        if gradient.cmykColors is None:
            radialGradient(startPoint=start, endPoint=end,
                colors=gradient.colors, locations=gradient.locations,
                startRadius=gradient.startRadius, endRadius=gradient.endRadius)
        else:
            cmykRadialGradient(startPoint=start, endPoint=end,
                colors=gradient.cmykColors, locations=gradient.locations,
                startRadius=gradient.startRadius, endRadius=gradient.endRadius)

class Shadow(object):
    def __init__(self, offset=None, blur=None, color=None, cmykColor=None):
        self.offset = offset or (5, -5)
        self.blur = blur
        self.color = color
        self.cmykColor = cmykColor

def setShadow(eShadow):
    if eShadow.cmykColor is not None:
        shadow(eShadow.offset, blur=eShadow.blur, color=eShadow.cmykColor)
    else:
        shadow(eShadow.offset, blur=eShadow.blur, color=eShadow.color)

#   E L E M E N T

def deepFind(elements, name=None, pattern=None, result=None):
    u"""Perform a dynamic deep find the for all elements with the name. Don't include self.
    Either name or pattern should be defined."""
    assert name or pattern
    if result is None:
        result = []
    for e in elements:
        if pattern is not None and pattern in e.name: # Simple pattern match
            result.append(e)
        elif name is not None and name == e.name:
            result.append(e)
        deepFind(e.elements, name, pattern, result)
    return result

def find(elements, name=None, pattern=None, result=None):
    u"""Perform a dynamic find the named element(s) in self.elements. Don't include self.
    Either name or pattern should be defined."""
    result = []
    for e in elements:
        if pattern is not None and pattern in e.name: # Simple pattern match
            result.append(e)
        elif name is not None and name == e.name:
            result.append(e)
    return result

#   M A R K E R

MARKER_PATTERN = '==%s--%s=='
FIND_FS_MARKERS = re.compile('\=\=([a-zA-Z0-9_\:\.]*)\-\-([^=]*)\=\=')

def getMarker(markerId, arg=None):
    u"""Answer a formatted string with markerId that can be used as non-display marker.
    This way the Composer can find the position of markers in text boxes, after
    FS-slicing has been done. Note there is always a very small "white-space"
    added to the string, so there is a potential difference in width that matters.
    For that reason markers should not be changed after slicing (which would theoretically
    alter the flow of the FormattedString in an box) and the markerId and amount/length
    of args should be kept as small as possible.
    Note that there is a potential problem of slicing through the argument string at
    the end of a textBox. That is another reason to keep the length of the arguments short.
    And not to use any spaces, etc. inside the markerId.
    Possible slicing through line-endings is not a problem, as the raw string ignores them."""
    marker = MARKER_PATTERN % (markerId, arg or '')
    return FormattedString(marker, fill=None, stroke=None, fontSize=0.0000000000001)
    ###return FormattedString(marker, fill=(1, 0, 0), stroke=None, fontSize=10)

def findMarkers(fs, reCompiled=None):
    u"""Answer a dictionary of markers with their arguments in a given FormattedString."""
    if reCompiled is None:
        reCompiled= FIND_FS_MARKERS
    return reCompiled.findall(u'%s' % fs)

def css(name, e, styles=None, default=None):
    u"""Answer the named style values. Search in optional style dict first, otherwise up the
    parent tree of styles in element e. Both e and style can be None. In that case None is answered."""
    if styles is not None: # Can be single style or stack of styles.
        if not isinstance(styles, (tuple, list)):
            styles = [styles] # Make stack of styles.
        for style in styles:
            if name in style:
                return style[name]
    if e is not None:
        return e.css(name)
    return default

def newFS(t, e=None, style=None):
    u"""Answer a formatted string from valid attributes in Style. Set the all values after testing
    their existence, so they can inherit from previous style formats."""

    hyphenation(css('hyphenation', e, style)) # TODO: Should be text attribute, not global

    fs = FormattedString('')
    sFont = css('font', e, style)
    if sFont is not None:
        fs.font(sFont)
    sFontSize = css('fontSize', e, style)
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
        setFillColor(sFill, fs)
    sCmykFill = css('cmykFill', e, style, NO_COLOR)
    if sCmykFill is not NO_COLOR:
        setFillColor(sCmykFill, fs, cmyk=True)
    sStroke = css('textStroke', e, style, NO_COLOR)
    sStrokeWidth = css('textStrokeWidth', e, style)
    if sStroke is not NO_COLOR and strokeWidth is not None:
        setStrokeColor(sStroke, sStrokeWidth, fs)
    sCmykStroke = css('cmykStroke', e, style, NO_COLOR)
    if sCmykStroke is not NO_COLOR:
        setStrokeColor(sCmykStroke, sStrokeWidth, fs, cmyk=True)
    sAlign = css('xAlign', e, style)
    if sAlign is not None:
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

    return fs + t

def textBoxBaseLines(txt, box):
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

def textPositionSearch(fs, w, h, search, xAlign=LEFT, hyphenation=True):
    u"""
    """
    bc = BaseContext()
    path = CoreText.CGPathCreateMutable()
    CoreText.CGPathAddRect(path, None, CoreText.CGRectMake(0, 0, w, h))

    attrString = bc.attributedString(fs, align=xAlign)
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
