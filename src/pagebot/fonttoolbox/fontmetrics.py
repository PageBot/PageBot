# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     fontmetrics.py
#
#     Implements info functions on font metrics.

import os
from AppKit import NSFont
from CoreText import CTFontDescriptorCreateWithNameAndSize, CTFontDescriptorCopyAttribute, kCTFontURLAttribute
from fontTools.ttLib import TTFont


def getFontPathOfFont(fontName):
    font = NSFont.fontWithName_size_(fontName, 25)
    if font is not None:
        fontRef = CTFontDescriptorCreateWithNameAndSize(font.fontName(), font.pointSize())
        url = CTFontDescriptorCopyAttribute(fontRef, kCTFontURLAttribute)
        return url.path()
    return None
    
def getFontMetrics(fontPath):
    u"""Small collection of font metrics data as dictionary.
    For a more complete font.info implementation see the FontInfo class."""
    if not os.path.exists(fontPath): # Assume it is a font name instead of path)
        fontPath = getFontPathOfFont(fontPath)
    ttf = TTFont(fontPath)
    unitsPerEm = ttf["head"].unitsPerEm
    hhea = ttf["hhea"]
    os2 = ttf["OS/2"]
    
    return dict(typoDescender=os2.sTypoDescender, typoAscender=os2.sTypoAscender,
        descender=hhea.descent, ascender=hhea.ascent,
        xHeight=os2.sxHeight, capHeight=os2.sCapHeight, subscriptYOffset=os2.ySubscriptYOffset,
        lineGap=os2.sTypoLineGap, superscriptXSize=os2.ySuperscriptXSize,
        weightClass=os2.usWeightClass, widthClass=os2.usWidthClass, 
        subscriptXOffset=os2.ySubscriptXOffset, strikeoutPosition=os2.yStrikeoutPosition,
        subscriptXSize=os2.ySubscriptXSize, superscriptYOffset=os2.ySuperscriptYOffset,
        strikeoutSize=os2.yStrikeoutSize, subscriptYSize=os2.ySubscriptYSize,
        superscriptYSize=os2.ySuperscriptYSize, unitsPerEm=unitsPerEm
    )
    
