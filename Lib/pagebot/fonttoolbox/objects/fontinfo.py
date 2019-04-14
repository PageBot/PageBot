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
#     inspectfont.py
#
#     Implements info functions on font info.
#
from pagebot.fonttoolbox.ttftools import getBestCmap

class cached_property:
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


class FontInfo:

    """Read-only access to font information, such as names, character set and supported
    OpenType features.

    >>> from pagebot.fonttoolbox.fontpaths import TEST_FONTS_PATH
    >>> from pagebot.fonttoolbox.objects.font import getFont
    >>> path = TEST_FONTS_PATH + '/google/roboto/Roboto-Black.ttf' # We know this exists in the PageBot repository
    >>> font = getFont(path)
    >>> font.info.copyright
    'Copyright 2011 Google Inc. All Rights Reserved.'
    """
    def __init__(self, ttFont):
        self.ttFont = ttFont
        self._styleName = None
        # Optional informaiton, set if instance is created from a VarFont
        self.opticalSize = None
        self.location = None
        self.varStyleName = None
        self.installedName = None # Storage for the installed (menu) name, e.g. DrawBotContext.font(path)

    def _getNameTableEntry(self, nameId):
        nameEntry = None
        if 'name' in self.ttFont:
            nameTable = self.ttFont["name"]
            nameEntry = nameTable.getName(nameId, 3, 1)
        if nameEntry is not None:
            return nameEntry.toUnicode()
        else:
            return None

    def _get_fullName(self):
        """Answers the full name of the font. Construct it from family name and style name
        if there is no full name defined.

        >>> from pagebot.fonttoolbox.fontpaths import TEST_FONTS_PATH
        >>> from pagebot.fonttoolbox.objects.font import getFont
        >>> path = TEST_FONTS_PATH + '/google/roboto/Roboto-Black.ttf' # We know this exists in the PageBot repository
        >>> font = getFont(path)
        >>> font.info.fullName
        'Roboto Black'
        """
        fullName = self._getNameTableEntry(4)
        if not fullName:
            fullName = '%s %s' % (self.familyName, self.styleName)
        return fullName
    fullName = property(_get_fullName)

    def _get_familyName(self):
        """Should be this, but often wrong: return self._getNameTableEntry(1)

        >>> from pagebot.fonttoolbox.fontpaths import TEST_FONTS_PATH
        >>> from pagebot.fonttoolbox.objects.font import getFont
        >>> path = TEST_FONTS_PATH + '/google/roboto/Roboto-Black.ttf' # We know this exists in the PageBot repository
        >>> font = getFont(path)
        >>> font.info.familyName
        'Roboto'
        """
        if self._getNameTableEntry(1):
            return self._getNameTableEntry(1).split(' ')[0]
        # If name table fails, try to guess from the file name
        if self.ttFont.reader:
            path = self.ttFont.reader.file.name
            return path.split('/')[-1].split('-')[0].split('.')[0]
        return 'Untitled'
    familyName = property(_get_familyName)

    def _get_styleName(self):
        """Answers the style name of the font.
        Family name should be this, but often wrong: return self._getNameTableEntry(1)
        We take the first spaced part as family name, and fill the rest here under style.
        So we add rest of family.

        >>> from pagebot.fonttoolbox.fontpaths import TEST_FONTS_PATH
        >>> from pagebot.fonttoolbox.objects.font import getFont
        >>> path = TEST_FONTS_PATH + '/google/roboto/Roboto-Black.ttf' # We know this exists in the PageBot repository
        >>> font = getFont(path)
        >>> font.info.styleName
        'Regular'
        >>> font.info.styleName = 'Bold'
        >>> font.info.styleName
        'Bold'
        """
        if self._styleName is None:
            self._styleName = ''
            if self._getNameTableEntry(1):
                familyNameParts = ' '.split(self._getNameTableEntry(1))
                if len(familyNameParts) > 1:
                    self._styleName = ' '.join(familyNameParts[1:])
            if self._getNameTableEntry(2):
                if self._styleName:
                    self._styleName += ' '
                self._styleName += self._getNameTableEntry(2)
        return self._styleName
    def _set_styleName(self, styleName):
        self._styleName = styleName
    styleName = property(_get_styleName, _set_styleName)

    @cached_property
    def cssName(self):
        return self.familyName + '-' + self.styleName

    @cached_property
    def copyright(self):
        return self.ttFont['name'].getDebugName(0)

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

    def _get_underlineThickness(self):
        return self.ttFont['post'].underlineThickness
    def _set_underlineThickness(self, v):
        self.ttFont['post'].underlineThickness = v
    underlineThickness = property(_get_underlineThickness, _set_underlineThickness)

    def _get_underlinePosition(self):
        return self.ttFont['post'].underlinePosition
    def _set_underlinePosition(self, v):
        self.ttFont['post'].underlinePosition = v
    underlinePosition = property(_get_underlinePosition, _set_underlinePosition)

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
        """Small collection of font metrics info data as dictionary."""
        # @@@ TODO Review this!
        return dict(typoDescender=self.typoDescender(),
                    typoAscender=self.typoAscender(),
                    descender=self.descender(),
                    ascender=self.ascender(),
                    xHeight=self.xHeight(),
                    capHeight=self.capHeight(),
                    subscriptYOffset=self.subscriptYOffset(),
                    lineGap=self.lineGap(),
                    superscriptXSize=self.superscriptXSize(),
                    weightClass=self.weightClass(),
                    widthClass=self.widthClass(),
                    subscriptXOffset=self.subscriptXOffset(),
                    strikeoutPosition=self.strikeoutPosition(),
                    subscriptXSize=self.subscriptXSize(),
                    superscriptYOffset=self.superscriptYOffset(),
                    strikeoutSize=self.strikeoutSize(),
                    subscriptYSize=self.subscriptYSize(),
                    superscriptYSize=self.superscriptYSize(),
                    unitsPerEm=self.unitsPerEm())
    metrics = property(_get_metrics)



if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
