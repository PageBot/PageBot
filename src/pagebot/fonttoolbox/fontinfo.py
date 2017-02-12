# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     inspectfont.py
#
#     Implements info functions on font info.
#
from ttftools import getBestCmap
from fontTools.ttLib import TTFont

class cached_property(object):
    """
    A property that is only computed once per instance and then replaces itself
    with an ordinary attribute. Deleting the attribute resets the property.
    Source: https://github.com/bottlepy/bottle/commit/fa7733e075da0d790d809aa3d2f53071897e6f76
    """  # noqa
    # TODO what would be a good place for this in tnBits?

    def __init__(self, func):
        self.__doc__ = getattr(func, '__doc__')
        self.func = func

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value


class FontInfo(object):

    """Read-only access to font information, such as names, character set and supported
    OpenType features.
    """

    def __init__(self, ttFont):
        self.ttFont = ttFont

    def _getNameTableEntry(self, nameId):
        nameTable = self.ttFont["name"]
        nameEntry = nameTable.getName(nameId, 3, 1)
        if nameEntry is not None:
            return nameEntry.toUnicode()
        else:
            return None

    @cached_property
    def fullName(self):
        return self._getNameTableEntry(4)

    @cached_property
    def familyName(self):
        return self._getNameTableEntry(1)

    @cached_property
    def styleName(self):
        return self._getNameTableEntry(2)

    @cached_property
    def psName(self):
        return self._getNameTableEntry(6)

    @cached_property
    def designer(self):
        return self._getNameTableEntry(9)

    @cached_property
    def description(self):
        return self._getNameTableEntry(10)

    @cached_property
    def trademark(self):
        return self._getNameTableEntry(7)

    @cached_property
    def license(self):
        return self._getNameTableEntry(13)

    @cached_property
    def charSet(self):
        cmap = getBestCmap(self.ttFont)
        return sorted(cmap.keys())

    @cached_property
    def glyphSet(self):
        return sorted(self.ttFont.getGlyphOrder())

    @cached_property
    def typoDescender(self):
        return self.ttFont["OS/2"].sTypoDescender

    @cached_property
    def typoAscender(self):
        return self.ttFont["OS/2"].sTypoAscender

    @cached_property
    def descender(self):
        return self.ttFont["hhea"].descent

    @cached_property
    def ascender(self):
        return self.ttFont["hhea"].ascent

    @cached_property
    def xHeight(self):
        return self.ttFont["OS/2"].sxHeight

    @cached_property
    def capHeight(self):
        return self.ttFont["OS/2"].sCapHeight

    @cached_property
    def subscriptYOffset(self):
        return self.ttFont["OS/2"].ySubscriptYOffset

    @cached_property
    def lineGap(self):
        return self.ttFont["OS/2"].sTypoLineGap

    @cached_property
    def superscriptXSize(self):
        return self.ttFont["OS/2"].ySuperscriptXSize

    @cached_property
    def weightClass(self):
        return self.ttFont["OS/2"].usWeightClass

    @cached_property
    def widthClass(self):
        return self.ttFont["OS/2"].usWidthClass

    @cached_property
    def subscriptXOffset(self):
        return self.ttFont["OS/2"].ySubscriptXOffset

    @cached_property
    def strikeoutPosition(self):
        return self.ttFont["OS/2"].yStrikeoutPosition

    @cached_property
    def subscriptXSize(self):
        return self.ttFont["OS/2"].ySubscriptXSize

    @cached_property
    def superscriptYOffset(self):
        return self.ttFont["OS/2"].ySuperscriptYOffset

    @cached_property
    def strikeoutSize(self):
        return self.ttFont["OS/2"].yStrikeoutSize

    @cached_property
    def subscriptYSize(self):
        return self.ttFont["OS/2"].ySubscriptYSize

    @cached_property
    def superscriptYSize(self):
        return self.ttFont["OS/2"].ySuperscriptYSize

    @cached_property
    def italicAngle(self):
        return self.ttFont["post"].italicAngle

    @cached_property
    def unitsPerEm(self):
        return self.ttFont["head"].unitsPerEm

    def _getOTLFeatures(self, tableTag):
        assert tableTag in ("GPOS", "GSUB")
        if tableTag not in self.ttFont:
            return []
        table = self.ttFont[tableTag].table
        return sorted(set(fr.FeatureTag for fr in table.FeatureList.FeatureRecord))

    @cached_property
    def gposFeatures(self):
        return self._getOTLFeatures("GPOS")

    @cached_property
    def gsubFeatures(self):
        return self._getOTLFeatures("GSUB")

    def _get_metrics(self):
        u"""Small collection of font metrics info data as dictionary."""        
        return dict(typoDescender=self.typoDescender, typoAscender=self.typoAscender,
            descender=hhea.descent, ascender=hhea.ascent,
            xHeight=os2.sxHeight, capHeight=os2.sCapHeight, subscriptYOffset=os2.ySubscriptYOffset,
            lineGap=os2.sTypoLineGap, superscriptXSize=os2.ySuperscriptXSize,
            weightClass=os2.usWeightClass, widthClass=os2.usWidthClass, 
            subscriptXOffset=os2.ySubscriptXOffset, strikeoutPosition=os2.yStrikeoutPosition,
            subscriptXSize=os2.ySubscriptXSize, superscriptYOffset=os2.ySuperscriptYOffset,
            strikeoutSize=os2.yStrikeoutSize, subscriptYSize=os2.ySubscriptYSize,
            superscriptYSize=os2.ySuperscriptYSize, unitsPerEm=unitsPerEm
        )
    metrics = property(_get_metrics) 


