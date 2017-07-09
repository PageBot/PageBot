# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     font.py
#
#     Implements a PageBot font style to get info from a TTFont.
#     The Style instance is a convenience caching storage, similar to RoboFont Font.
#     Using the Family/Font/Glyph classes, allows page layout in PageBot to access
#     all information in a font purpose of typography and layout.
#
#     We'll call this class "Font" instead of "Style" (as in other TypeNetwerk tool code),
#     to avoid confusion with the PageBot style dictionary, which hold style parameters.
#
from AppKit import NSFont
from fontTools.ttLib import TTFont, TTLibError
from CoreText import CTFontDescriptorCreateWithNameAndSize, CTFontDescriptorCopyAttribute, kCTFontURLAttribute
try:
    from drawBot import installFont, listOpenTypeFeatures, installedFonts
except ImportError:
    installFont =  listOpenTypeFeatures = None

from pagebot.fonttoolbox.objects.glyph import Glyph
from pagebot.fonttoolbox.objects.fontinfo import FontInfo
from pagebot.fonttoolbox.variablefontaxes import axisDefinitions
from pagebot.contributions.adobe.kerndump.getKerningPairsFromOTF import OTFKernReader

def getFontPathOfFont(fontName):
    font = NSFont.fontWithName_size_(fontName, 25)
    if font is not None:
        fontRef = CTFontDescriptorCreateWithNameAndSize(font.fontName(), font.pointSize())
        url = CTFontDescriptorCopyAttribute(fontRef, kCTFontURLAttribute)
        return url.path()
    return None

def findInstalledFonts(fontNamePatterns):
    u"""Answer a list of installed font names that include the fontNamePattern. The pattern
    search is not case sensitive. The pattern can be a string or a list of strings."""
    fontNames = []
    if not isinstance(fontNamePatterns, (list, tuple)):
        fontNamePatterns = [fontNamePatterns]
    for fontNamePattern in fontNamePatterns:
        for fontName in installedFonts():
            if fontNamePattern in fontName:
                fontNames.append(fontName)
    return fontNames

def getFontByName(fontName, install=True):
    return getFontByPath(getFontPathOfFont(fontName), install=install)

def getFontByPath(fontPath, install=True):
    return Font(fontPath, install=install)

class Font(object):
    u"""
    Storage of font information while composing the pages.


    >>> import pagebot
    >>> from pagebot.toolbox.transformer import *
    >>> p = module2Path(pagebot)
    >>> pp = path2ParentPath(p)
    >>> p = pp + '/fonts/fontbureau/AmstelvarAlpha-Variations.ttf'
    >>> from pagebot.fonttoolbox.objects.font import Font
    >>> f = Font(p, install=False)
    >>> f.name
    u'BitcountGrid'
    >>> len(f)
    101
    >>> f.keys()[-1]
    'y'
    >>> f.axes
    {'rndi': (0.0, 1000.0, 1000.0), 'rndo': (0.0, 1000.0, 1000.0), 'sqri': (0.0, 1000.0, 1000.0), 'sqro': (0.0, 1000.0, 1000.0), 'line': (0.0, 1000.0, 1000.0), 'open': (0.0, 0.0, 1000.0), 'wght': (0.0, 500.0, 1000.0)}
    >>> variables = f.variables
    >>> features = f.features
    >>> f.groups
    >>> f.designSpace
    {}
    >>> f.install()
    u'BitcountGrid-SingleCircleSquare-wght500rndi1000rndo1000line1000sqri1000sqro1000open0'
    >>> f.save()
    """
    GLYPH_CLASS = Glyph

    def __init__(self, path, name=None, install=True, opticalSize=None, location=None):
        u"""Initialize the TTFont, for which Font is a wrapper. Default is to
        install the font in DrawBot.

        self.name is supported, in case the caller wants to use a different
        name than the DrawBot installing name."""
        self.path = path # File path of the font file.
        if install:
            # Installs the font in DrawBot from self.path and initializes
            # self.installedName.
            self.install()
        else:
            self.installedName = None # Set to DrawBot name, when installed later.
        try:
            self.ttFont = TTFont(path, lazy=True)
            # TTFont is available as lazy style.info.font
            self.info = FontInfo(self.ttFont)
            self.info.opticalSize = opticalSize # Optional optical size, to indicate where this Variable Font is rendered for.
            self.info.location = location # Store origina location of this instance of the font is derived from a Variable Font.
            # Stores optional custom name, otherwise use original DrawBot name.
            # Otherwise use from FontInfo.fullName
            self.name = name or self.installedName or self.info.fullName
            self.path = path
            self._kerning = None # Lazy reading.
            self._groups = None # Lazy reading.
        except TTLibError:
            raise OSError('Cannot open font file "%s"' % path)

    def __repr__(self):
        return '<PageBot Font %s>' % (self.path or self.name)

    def __getitem__(self, glyphName):
        return self.GLYPH_CLASS(self, glyphName)

    def __len__(self):
        return len(self.ttFont['glyf'])

    def keys(self):
        return self.ttFont['glyf'].keys()

    def _get_axes(self): # Answer dictionary of axes
        try:
            # TODO: Change value to Axis dictionary instead of list
            axes = {a.axisTag: (a.minValue, a.defaultValue, a.maxValue) for a in self.ttFont['fvar'].axes}
        except KeyError:
            axes = {} # This is not a variable font.
        return axes
    axes = property(_get_axes)

    def _get_designSpace(self):
        try:
            designSpace = self.ttFont['cvar']
        except KeyError:
            designSpace = {}
        return designSpace
    designSpace = property(_get_designSpace)

    def _get_variables(self):
        try:
            variables = self.ttFont['gvar']
        except KeyError:
            variables = {}
        return variables
    variables = property(_get_variables)

    def _get_features(self):
        return listOpenTypeFeatures(self.installedName)
    features = property(_get_features)

    def _get_kerning(self):
        if self._kerning is None: # Lazy read.
            self._kerning = OTFKernReader(self.path).kerningPairs
        return self._kerning
    kerning =  property(_get_kerning)

    def _get_groups(self):
        return self._groups
    groups = property(_get_groups)

    def getFeaturedString(self, s, featureSettings):
        u"""Compile the string s into glyph names, corresponding to the
        settings in featureSettings."""
        return s

    def install(self):
        u"""Install the font in DrawBot, if not already there. Answer the
        DrawBot name."""
        self.installedName = installFont(self.path)
        return self.installedName

    def save(self, path=None):
        u"""Save the font to optional path or to self.path."""
        self.ttFont.save(path or self.path)
