# -*- coding: UTF-8 -*-
#-----------------------------------------------------------------------------
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
import re
from drawBot import FormattedString, cmykFill, fill, cmykStroke, stroke, strokeWidth
from style import NO_COLOR

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
    return (style.ml + cx * (style.cw + style.g),  
            style.mt + cy * (style.ch + style.g))
    
def cr2p(cx, cy, cw, ch, style):
    u"""Convert columns rect to page position/size."""
    return (
        style.ml + cx * (style.cw + style.g),  
        style.h - style.mt - (cy + ch) * (style.ch + style.g) + style.g, 
        cw * (style.cw + style.g) - style.g, 
        ch * (style.ch + style.g) - style.g) 

def getMarker(markerId, args=None):
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
    marker = '==%s--%s==' % (markerId, args or '') 
    return FormattedString(marker, fill=None, stroke=None, fontSize=0.0000000000001)  

FIND_FS_MARKERS = re.compile('\=\=([a-zA-Z0-9_]*)\-\-([^=]*)\=\=')

def findMarkers(fs):
    u"""Answer a dictionary of markers with their arguments that exist in a given FormattedString."""
    markers = {}
    for markerId, args in FIND_FS_MARKERS.findall(repr(fs)):
        if not markerId in markers:
            markers[markerId] = []
        markers[markerId].append(args)
    return markers
              
def getFormattedString(t, style=None):
    u"""Answer a formatted string from valid attributes in Style. Set the all values after testing,
    so they can inherit from previous style formats."""
    fs = FormattedString()
    if style is not None:
        if style.font is not None:
            fs.font(style.font)
        if style.fontSize is not None:
            fs.fontSize(style.fontSize)
        if style.fallbackFont is not None:
            fs.fallbackFont(style.fallbackFont)
        if style.fill is not NO_COLOR: # Test on this flag, None is valid value
            setFillColor(style.fill, fs)
        if style.cmykFill is not NO_COLOR:
            setFillColor(style.cmykFill, fs, cmyk=True)
        if style.stroke is not NO_COLOR:
            setStrokeColor(style.stroke, style.strokeWidth, fs)
        if style.cmykStroke is not NO_COLOR:
            setStrokeColor(style.cmykStroke, style.strokeWidth, fs, cmyk=True)
        if style.align is not None:
            fs.align(style.align)
        if style.leading is not None or style.rLeading is not None:
            fs.lineHeight((style.leading or 0) + (style.rLeading or 0) * style.fontSize)
        if style.paragraphTopSpacing is not None or style.rParagraphTopSpacing is not None:
            fs.paragraphTopSpacing((style.paragraphTopSpacing or 0) + (style.rParagraphTopSpacing or 0) * style.fontSize)
        if style.paragraphBottomSpacing is not None or style.rParagraphBottomSpacing is not None:
            fs.paragraphBottomSpacing((style.paragraphBottomSpacing or 0) + (style.rParagraphBottomSpacing or 0) * style.fontSize)
        if style.tracking is not None:
            fs.tracking((style.tracking or 0) + (style.rTracking or 0) * style.fontSize)
        if style.baselineShift is not None or style.rBaselineShift is not None:
            fs.baselineShift((style.baselineShift or 0) + (style.rBaselineShift or 0) * style.fontSize)
        if style.openTypeFeatures is not None:
            fs.openTypeFeatures(style.openTypeFeatures)
        if style.tabs is not None:
            fs.tabs(*style.tabs)
        if style.firstLineIndent is not None:
            fs.firstLineIndent((style.firstLineIndent or 0) + (style.rFirstLineIndent or 0) * style.fontSize)
        if style.indent is not None or style.rIndent is not None:
            fs.indent((style.indent or 0) + (style.rIndent or 0) * style.fontSize)
        if style.tailIndent is not None or style.rTailIndent is not None:
            fs.tailIndent((style.tailIndent or 0) + (style.rTailIndent or 0) * style.fontSize)
        if style.language is not None:
            fs.language(style.language)
        #fs.hyphenation(style.hyphenation)        
    fs.append(t)
    return fs
