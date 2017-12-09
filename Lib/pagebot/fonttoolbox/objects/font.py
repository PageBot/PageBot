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
from fontTools.ttLib import TTFont
from pagebot.contexts import defaultContext

from pagebot.fonttoolbox.objects.glyph import Glyph
from pagebot.fonttoolbox.analyzers.fontanalyzer import FontAnalyzer
from pagebot.fonttoolbox.objects.fontinfo import FontInfo
from pagebot.fonttoolbox.variablefontaxes import axisDefinitions
from pagebot.contributions.adobe.kerndump.getKerningPairsFromOTF import OTFKernReader

def getFontByPath(fontPath, install=True):
    return Font(fontPath, install=install)

def getFontByName(fontName, install=True, context=None):
    if context is None:
        context = defaultContext
    return getFontByPath(context.getFontPathOfFont(fontName), install=install)

def findInstalledFonts(fontNamePatterns=None, context=None):
    u"""Answer a list of installed font names that include the fontNamePattern. The pattern
    search is not case sensitive. The pattern can be a string or a list of strings."""
    if context is None:
        context = defaultContext
    fontNames = []
    installedFontNames = context.installedFonts()
    if fontNamePatterns is not None and not isinstance(fontNamePatterns, (list, tuple)):
        fontNamePatterns = [fontNamePatterns]
    if fontNamePatterns is not None:
        for fontNamePattern in fontNamePatterns:
            for fontName in installedFontNames:
                if fontNamePattern in fontName:
                    fontNames.append(fontName)
    else:
        fontNames = installedFontNames
    return fontNames

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
    FONTANALYZER_CLASS = FontAnalyzer

    def __init__(self, path, name=None, install=True, opticalSize=None, location=None, styleName=None, lazy=True):
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
            self.installedName = None # Set to DrawBot name, if installing later.
        #try:
        if 1:
            self.ttFont = TTFont(path, lazy=lazy)
            # TTFont is available as lazy style.info.font
            self.info = FontInfo(self.ttFont)
            self.info.opticalSize = opticalSize # Optional optical size, to indicate where this Variable Font is rendered for.
            self.info.location = location # Store origina location of this instance of the font is derived from a Variable Font.
            # Stores optional custom name, otherwise use original DrawBot name.
            # Otherwise use from FontInfo.fullName
            self.name = name or self.installedName or self.info.fullName
            if styleName is not None:
                self.info.styleName = styleName # Overwrite default style name in the ttFont or Variable Font location
            self._kerning = None # Lazy reading.
            self._groups = None # Lazy reading.
            self._glyphs = {} # Lazy creation of self[glyphName]
            self._analyzer = None # Lazy creation.
        #except:# TTLibError:
        #    raise OSError('Cannot open font file "%s"' % path)

    def __repr__(self):
        return '<PageBot Font %s>' % (self.path or self.name)

    def __getitem__(self, glyphName):
        if not glyphName in self._glyphs:
            self._glyphs[glyphName] = self.GLYPH_CLASS(self, glyphName)
        return self._glyphs[glyphName]

    def __len__(self):
        if 'glyf' in self.ttFont:
            return len(self.ttFont['glyf'])
        return 0

    def keys(self):
        if 'glyf' in self.ttFont:
            return self.ttFont['glyf'].keys()
        return []

    def __contains__(self, glyphName):
        return glyphName in self.keys()

    def _get_analyzer(self):
        u"""Answer the style/font analyzer if it exists. Otherwise create one."""
        if self._analyzer is None:
            self._analyzer = self.FONTANALYZER_CLASS(self)
        return self._analyzer
    analyzer = property(_get_analyzer)

    def _get_axes(self): 
        u"""Answer dictionary of axes if self.ttFont is a Variable Font. Otherwise answer an empty dictioary."""
        try:
            # TODO: Change value to Axis dictionary instead of list
            axes = {a.axisTag: (a.minValue, a.defaultValue, a.maxValue) for a in self.ttFont['fvar'].axes}
        except KeyError:
            axes = {} # This is not a variable font.
        return axes
    axes = property(_get_axes)

    def _get_rawDeltas(self):
        u"""Answer the list of axis dictionaries with deltas for all glyphs and axes. Answer an empty dictionary
        if the [gvar] table does not exist."""
        try:
            return self.ttFont['gvar'].variations
        except:
            return {}
    rawDeltas = property(_get_rawDeltas)

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

    def install(self, context=None):
        u"""Install the font in DrawBot, if not already there. Answer the
        DrawBot name."""
        if context is None:
            context = defaultContext
        self.installedName = context.installFont(self.path)
        return self.installedName

    def save(self, path=None):
        u"""Save the font to optional path or to self.path."""
        self.ttFont.save(path or self.path)
