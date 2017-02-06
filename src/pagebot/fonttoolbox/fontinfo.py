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
from tnbits.compilers.f5.ttfTools import getBestCmap
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

    def __init__(self, fontOrPath):
        if isinstance(fontOrPath, basestring):
            path = fontOrPath
            font = TTFont(fontOrPath, lazy=True)
        else:
            path = None
            font = fontOrPath
        self.path = path
        self.font = font

    def _getNameTableEntry(self, nameId):
        nameTable = self.font["name"]
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
        cmap = getBestCmap(self.font)
        return sorted(cmap.keys())

    @cached_property
    def glyphSet(self):
        return sorted(self.font.getGlyphOrder())

    @cached_property
    def typoDescender(self):
        return self.font["OS/2"].sTypoDescender

    @cached_property
    def typoAscender(self):
        return self.font["OS/2"].sTypoAscender

    @cached_property
    def descender(self):
        return self.font["hhea"].descent

    @cached_property
    def ascender(self):
        return self.font["hhea"].ascent

    @cached_property
    def xHeight(self):
        return self.font["OS/2"].sxHeight

    @cached_property
    def capHeight(self):
        return self.font["OS/2"].sCapHeight

    @cached_property
    def subscriptYOffset(self):
        return self.font["OS/2"].ySubscriptYOffset

    @cached_property
    def lineGap(self):
        return self.font["OS/2"].sTypoLineGap

    @cached_property
    def superscriptXSize(self):
        return self.font["OS/2"].ySuperscriptXSize

    @cached_property
    def weightClass(self):
        return self.font["OS/2"].usWeightClass

    @cached_property
    def widthClass(self):
        return self.font["OS/2"].usWidthClass

    @cached_property
    def subscriptXOffset(self):
        return self.font["OS/2"].ySubscriptXOffset

    @cached_property
    def strikeoutPosition(self):
        return self.font["OS/2"].yStrikeoutPosition

    @cached_property
    def subscriptXSize(self):
        return self.font["OS/2"].ySubscriptXSize

    @cached_property
    def superscriptYOffset(self):
        return self.font["OS/2"].ySuperscriptYOffset

    @cached_property
    def strikeoutSize(self):
        return self.font["OS/2"].yStrikeoutSize

    @cached_property
    def subscriptYSize(self):
        return self.font["OS/2"].ySubscriptYSize

    @cached_property
    def superscriptYSize(self):
        return self.font["OS/2"].ySuperscriptYSize

    @cached_property
    def italicAngle(self):
        return self.font["post"].italicAngle

    @cached_property
    def unitsPerEm(self):
        return self.font["head"].unitsPerEm

    def _getOTLFeatures(self, tableTag):
        assert tableTag in ("GPOS", "GSUB")
        if tableTag not in self.font:
            return []
        table = self.font[tableTag].table
        return sorted(set(fr.FeatureTag for fr in table.FeatureList.FeatureRecord))

    @cached_property
    def gposFeatures(self):
        return self._getOTLFeatures("GPOS")

    @cached_property
    def gsubFeatures(self):
        return self._getOTLFeatures("GSUB")


def _test():
    r"""
        >>> from tnTestFonts import getFontPath
        >>> path = getFontPath("Condor-Bold.otf")
        >>> fontInfo = FontInfo(path)
        >>> fontInfo.psName
        u'Condor-Bold'
        >>> fontInfo.fullName
        u'Condor Bold Bold'
        >>> fontInfo.familyName
        u'Condor Bold'
        >>> fontInfo.styleName
        u'Bold'
        >>> fontInfo.gposFeatures
        ['kern']
        >>> fontInfo.gsubFeatures
        ['case', 'dlig', 'dnom', 'frac', 'lnum', 'locl', 'numr', 'ordn', 'ornm', 'pnum', 'salt', 'sinf', 'ss01', 'ss02', 'ss03', 'ss18', 'ss19', 'sups', 'zero']
        >>> fontInfo.charSet[:10]
        [32, 33, 34, 35, 36, 37, 38, 39, 40, 41]
        >>> fontInfo.glyphSet[:10]
        ['.notdef', 'A', 'AE', 'Aacute', 'Abreve', 'Acircumflex', 'Adieresis', 'Agrave', 'Amacron', 'Aogonek']
    """

def _runDocTests():
    import doctest
    return doctest.testmod()


if __name__ == "__main__":
    _runDocTests()
