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
#     fontinfo.py
#
#     Implements info functions on font info.
#

# We should use getBestCmap() provided by fontTools.

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

    >>> from pagebot.fonttoolbox.objects.font import getFont
    >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
    >>> path = getTestFontsPath() + '/google/roboto/Roboto-Black.ttf'
    >>> font = getFont(path)
    >>> font.info.copyright
    'Copyright 2011 Google Inc. All Rights Reserved.'
    """
    def __init__(self, ttFont):
        self.ttFont = ttFont
        self._familyName = None
        self._styleName = None
        # Optional informaiton, set if instance is created from a VarFont
        self.opticalSize = None
        self.location = None
        self.varStyleName = None
        self.installedName = None # Storage for the installed (menu) name, e.g. DrawBotContext.font(path)
        self.cssFontUrl = 'fonts/' # Change if css fonts are in a different url.

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
        This is often wrong: return self._getNameTableEntry(4)
        So construct from self.familyName + ' ' + self.styleName

        >>> from pagebot.fonttoolbox.objects.font import getFont
        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> path = getTestFontsPath() + '/google/roboto/Roboto-Black.ttf' # We know this exists in the PageBot repository
        >>> font = getFont(path)
        >>> font.info.fullName
        'Roboto Black'
        """
        #fullName = self._getNameTableEntry(4)
        #if not fullName:
        return '%s %s' % (self.familyName, self.styleName)
    fullName = property(_get_fullName)

    def _get_familyName(self):
        """Should be this, but often wrong: return self._getNameTableEntry(1)
        So, for now we just look at the format of the file name.
        The first hyphen in the name is the split between family name and style name.
        Replace underscores in the name by spaces.

        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> from pagebot.fonttoolbox.objects.font import getFont
        >>> path = getTestFontsPath() + '/google/roboto/Roboto-Black.ttf' # We know this exists in the PageBot repository
        >>> font = getFont(path)
        >>> font.info.familyName
        'Roboto'
        """
        #if self._getNameTableEntry(1):
        #    return self._getNameTableEntry(1).split(' ')[0]
        # As name table often fails, try to guess from the file name
        if self._familyName is None and self.ttFont.reader:
            path = self.ttFont.reader.file.name
            self._familyName = path.split('/')[-1].split('-')[0].split('.')[0].replace('_', ' ')
        elif self._familyName is None:
            self._familyName = 'Untitled'
        return self._familyName
    familyName = property(_get_familyName)

    def _get_styleName(self):
        """Answers the style name of the font.
        Family name should be this, but often wrong: return self._getNameTableEntry(1)
        We take the first hyphen part as family name, and fill the rest here under style.
        So we add rest of family.

        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> from pagebot.fonttoolbox.objects.font import getFont
        >>> path = getTestFontsPath() + '/google/roboto/Roboto-Black.ttf' # We know this exists in the PageBot repository
        >>> font = getFont(path)
        >>> font.info.styleName
        'Black'
        >>> font.info.styleName = 'Bold'
        >>> font.info.styleName
        'Bold'
        """
        """
        if self._styleName is None:
            self._styleName = ''
            fullName = self._getNameTableEntry(1)
            if fullName:
                fullNameParts = fullName.split(' ')
                if len(fullNameParts) > 1:
                    self._styleName = ' '.join(fullNameParts[1:])
            if not self._styleName:
                fullName = self._getNameTableEntry(4)
                if fullName:
                    fullNameParts = fullName.split(' ')
                    if len(fullNameParts) > 1:
                        self._styleName = ' '.join(fullNameParts[1:])
        """
        if self._styleName is None and self.ttFont.reader:
            path = self.ttFont.reader.file.name
            self._styleName = '-'.join(path.split('/')[-1].split('-')[1:]).split('.')[0].replace('_', ' ')
        elif self._styleName is None:
            self._styleName = 'Untitled'
        return self._styleName
    def _set_styleName(self, styleName):
        self._styleName = styleName
    styleName = property(_get_styleName, _set_styleName)

    @cached_property
    def cssName(self):
        cssName = self.familyName.replace(' ', '_')
        if self.styleName:
            cssName += '-' + self.styleName.replace(' ', '_')
        return cssName

    @cached_property
    def eotName(self):
        eotName = self.cssFontUrl + self.familyName.replace(' ', '_')
        if self.styleName:
            eotName += '-' + self.styleName.replace(' ', '_')
        return eotName + '.eot'

    @cached_property
    def woff2Name(self):
        woff2Name = self.cssFontUrl + self.familyName.replace(' ', '_')
        if self.styleName:
            woff2Name += '-' + self.styleName.replace(' ', '_')
        return woff2Name + '.woff2'

    @cached_property
    def woffName(self):
        woffName = self.cssFontUrl + self.familyName.replace(' ', '_')
        if self.styleName:
            woffName += '-' + self.styleName.replace(' ', '_')
        return woffName + '.woff'

    @cached_property
    def ttfName(self):
        ttfName = self.cssFontUrl + self.familyName.replace(' ', '_')
        if self.styleName:
            ttfName += '-' + self.styleName.replace(' ', '_')
        return ttfName + '.ttf'

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

    '''
    @cached_property
    def charSet(self):
        cmap = getBestCmap(self.ttFont)
        return sorted(cmap.keys())
    '''

    @cached_property
    def glyphSet(self):
        return sorted(self.ttFont.getGlyphOrder())

    # About these settings in the font:
    # https://silnrsi.github.io/FDBP/en-US/Line_Metrics.html

    @cached_property
    def typoAscender(self):
        """Answer the relative typoAscender in em units.
        >>> from pagebot.toolbox.transformer import *
        >>> from pagebot.fonttoolbox.objects.font import Font
        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> fontPath = getTestFontsPath()
        >>> path = fontPath + '/djr/bungee/Bungee-Regular.ttf'
        >>> f = Font(path, lazy=False)
        >>> f.info.typoAscender
        860
        """
        return self.ttFont["OS/2"].sTypoAscender

    @cached_property
    def typoDescender(self):
        """Answer the relative typoDescender in em units.
        >>> from pagebot.toolbox.transformer import *
        >>> from pagebot.fonttoolbox.objects.font import Font
        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> fontPath = getTestFontsPath()
        >>> path = fontPath + '/djr/bungee/Bungee-Regular.ttf'
        >>> f = Font(path, lazy=False)
        >>> f.info.typoDescender
        -140
        """
        return self.ttFont["OS/2"].sTypoDescender

    @cached_property
    def descender(self):
        return self.ttFont["hhea"].descent

    @cached_property
    def ascender(self):
        """Answer the ascender in unitsPerEm.
        >>> from pagebot.toolbox.transformer import *
        >>> from pagebot.fonttoolbox.objects.font import Font, findFont
        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> fontPath = getTestFontsPath()
        >>> path = fontPath + '/djr/bungee/Bungee-Regular.ttf'
        >>> f = Font(path, lazy=False)
        >>> f.info.ascender, f.info.descender, f.info.ascender - f.info.descender == f.info.unitsPerEm
        (860, -140, True)
        >>> f = findFont('PageBot-Regular')
        >>> f.info.ascender, f.info.descender, f.info.ascender - f.info.descender == f.info.unitsPerEm
        (898, -302, False)
        """
        return self.ttFont["hhea"].ascent

    @cached_property
    def xHeight(self):
        """Answer the relative xHeight in em units.
        >>> from pagebot.toolbox.transformer import *
        >>> from pagebot.fonttoolbox.objects.font import Font
        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> fontPath = getTestFontsPath()
        >>> path = fontPath + '/djr/bungee/Bungee-Regular.ttf'
        >>> f = Font(path, lazy=False)
        >>> f.info.xHeight
        500
        """
        try:
            return self.ttFont["OS/2"].sxHeight
        except AttributeError:
            return 0

    @cached_property
    def capHeight(self):
        """Answer the relative xHeight in em units.
        >>> from pagebot.toolbox.transformer import *
        >>> from pagebot.fonttoolbox.objects.font import Font
        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> fontPath = getTestFontsPath()
        >>> path = fontPath + '/djr/bungee/Bungee-Regular.ttf'
        >>> f = Font(path, lazy=False)
        >>> f.info.capHeight
        720
        """
        try:
            return self.ttFont["OS/2"].sCapHeight
        except AttributeError:
            return 0

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
        return dict(typoAscender=self.typoAscender,
                    ascender=self.ascender,
                    capHeight=self.capHeight,
                    xHeight=self.xHeight,
                    descender=self.descender,
                    typoDescender=self.typoDescender,

                    subscriptYOffset=self.subscriptYOffset,
                    lineGap=self.lineGap,
                    superscriptXSize=self.superscriptXSize,
                    weightClass=self.weightClass,
                    widthClass=self.widthClass,
                    subscriptXOffset=self.subscriptXOffset,
                    strikeoutPosition=self.strikeoutPosition,
                    subscriptXSize=self.subscriptXSize,
                    superscriptYOffset=self.superscriptYOffset,
                    strikeoutSize=self.strikeoutSize,
                    subscriptYSize=self.subscriptYSize,
                    superscriptYSize=self.superscriptYSize,
                    unitsPerEm=self.unitsPerEm,)
    metrics = property(_get_metrics)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
