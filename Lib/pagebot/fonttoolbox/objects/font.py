#!/usr/bin/env python
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
import os
from fontTools.ttLib import TTFont
from pagebot.contexts import defaultContext as context

from pagebot.toolbox.transformer import path2FontName, path2Extension

from pagebot.fonttoolbox.objects.glyph import Glyph
from pagebot.fonttoolbox.analyzers.fontanalyzer import FontAnalyzer
from pagebot.fonttoolbox.objects.fontinfo import FontInfo
from pagebot.contributions.adobe.kerndump.getKerningPairsFromOTF import OTFKernReader
from pagebot.style import FONT_WEIGHT_MATCHES, FONT_WIDTH_MATCHES, FONT_ITALIC_MATCHES

def isFontPath(fontPath):
    u"""Answer the boolean flag if the path is a font path.
    For now, PageBot only supports ('ttf', 'otf')

    >>> from pagebot.contexts.platform import getRootFontPath
    >>> fontPath = getRootFontPath()
    >>> path = fontPath + '/fontbureau/AmstelvarAlpha-VF.ttf'
    >>> isFontPath(path)
    True
    >>> path = fontPath + '/fontbureau/AmstelvarAlpha-VF_XXX.ttf'
    >>> isFontPath(path)
    False
    >>> path = fontPath + '/fontbureau/AmstelvarAlpha-VF.UFO'
    >>> isFontPath(path)
    False
    """
    return os.path.exists(fontPath) and path2Extension(fontPath) in ('ttf', 'otf') 

def getFontByPath(fontPath, install=True):
    u"""Answer the Font instance, that connects to the fontPath. Note that there is no check if there
    is already anothe Font created on that path, as for PageBot purposes it is most likely for
    reading only.

    >>> from pagebot.contexts.platform import getRootFontPath
    >>> fontPath = getRootFontPath()
    >>> path = fontPath + '/fontbureau/AmstelvarAlpha-VF.ttf'
    >>> fontName = path2FontName(path)
    >>> font = getFontByPath(path)
    >>> font.path == path
    True
    """
    return Font(fontPath, install=install)

def getFontByName(fontName, install=True):
    u"""Answer the Font instance, that belongs to fontName. In DrawBotContext there is a 
    difference between the fontName (as installed) and the font path, which can be used
    both in DrawBotContext and FlatContext.

    >>> from pagebot.contexts.platform import getRootFontPath
    >>> fontPath = getRootFontPath()
    >>> path = fontPath + '/fontbureau/AmstelvarAlpha-VF.ttf'
    >>> font = getFontByName(path)
    >>> font.path == path
    True
    >>> font.name == 'AmstelvarAlpha-Default'
    True
    >>> font.installedName
    u'AmstelvarAlpha-Default'
    >>> path2FontName(font.path)
    'AmstelvarAlpha-VF'
    """
    return getFontByPath(context.fontName2FontPath(fontName), install=install)

def findInstalledFonts(fontNamePatterns=None):
    u"""Answer a list of installed font names that include the fontNamePattern. The pattern
    search is not case sensitive. The pattern can be a string or a list of strings.

    >>> findInstalledFonts('Amstel')
    ['AmstelvarAlpha-Default']
    >>> from pagebot.contexts.platform import getRootFontPath
    >>> fontPath = getRootFontPath()
    >>> path = fontPath + '/fontbureau/AmstelvarAlpha-VF.ttf'
    >>> font = getFontByName(path, install=True)
    >>> font.installedName
    u'AmstelvarAlpha-Default'
    >>> # TODO: findInstalledFonts('Amstel') # Cannot test this currently on non-DrawBot platform.
    """
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

    >>> from pagebot.toolbox.transformer import *
    >>> from pagebot.fonttoolbox.objects.font import Font
    >>> from pagebot.contexts.platform import getRootFontPath
    >>> fontPath = getRootFontPath()
    >>> path = fontPath + '/fontbureau/AmstelvarAlpha-VF.ttf'
    >>> f = Font(path, install=False, lazy=False)
    >>> f.name
    u'AmstelvarAlpha Default'
    >>> len(f)
    115
    >>> f.axes.keys()
    ['YOPQ', 'YTAS', 'YTRA', 'wdth', 'YTDE', 'YTSE', 'XTCH', 'opsz', 'YTLC', 'YTCH', 'XTRA', 'XOPQ', 'GRAD', 'wght', 'YTUC']
    >>> f.axes['wdth']
    (60.0, 402.0, 402.0)
    >>> variables = f.variables
    >>> features = f.features
    >>> f.groups
    >>> f.designSpace
    {}
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
            # Installs the font in DrawBot from self.path and initializes self.installedName.
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
            self._variables = None # Lazy creations of delta's dictionary per glyph per axis
        #except:# TTLibError:
        #    raise OSError('Cannot open font file "%s"' % path)

    def __repr__(self):
        """
        >>> from pagebot.contexts.platform import getRootFontPath
        >>> path = getRootFontPath() + '/google/roboto/Roboto-Black.ttf' # We know this exists in the PageBot repository
        >>> font = Font(path)
        >>> str(font)
        '<Font Roboto-Black>'
        """
        return '<Font %s>' % (path2FontName(self.path or self.name))

    def __getitem__(self, glyphName):
        u"""Answer the glyph with glyphName.

        >>> from pagebot.contexts.platform import getRootFontPath
        >>> path = getRootFontPath() + '/google/roboto/Roboto-Black.ttf' # We know this exists in the PageBot repository
        >>> font = Font(path)
        >>> g = font['A']
        >>> g.name, g.width
        ('A', 1395)
        """
        if not glyphName in self._glyphs:
            self._glyphs[glyphName] = self.GLYPH_CLASS(self, glyphName)
        return self._glyphs[glyphName]

    def __len__(self):
        u"""Answer the number of glyphs in the font.

        >>> from pagebot.contexts.platform import getRootFontPath
        >>> path = getRootFontPath() + '/google/roboto/Roboto-Black.ttf' # We know this exists in the PageBot repository
        >>> font = Font(path)
        >>> len(font)
        1294
        """
        if 'glyf' in self.ttFont:
            return len(self.ttFont['glyf'])
        return 0

    def weightMatch(self, weight):
        u"""Answer level of matching for the (abbreviated) weight name or number with font.

        >>> from pagebot.contexts.platform import getRootFontPath
        >>> path = getRootFontPath() + '/google/roboto/Roboto-Black.ttf' # We know this exists in the PageBot repository
        >>> font = Font(path)
        >>> font.info.weightClass
        900
        >>> font.weightMatch(0) # Bad match --> 0
        0
        >>> #font.weightMatch(800) # Close match --> 800
        240
        >>> font.weightMatch(900) # Exact match --> 1000
        1000
        >>> font.weightMatch(0) # Bad match --> 0
        0
        >>> font.weightMatch('Black') # Black --> Exact match, total depends on matching word length
        500
        >>> font.weightMatch('Light') # Light --> No match, total depends on matching word length
        0
        """
        match = 0
        if isinstance(weight, (float, int)): # Comparing by numbers
            # Compare the weight as number as max difference to what we already have.
            wf = self.info.weightClass
            for w in FONT_WEIGHT_MATCHES.get(weight, [weight]):
                if isinstance(w, (float, int)): # Then compare by numbers
                    match = max(match, 1000 - abs(w - wf)*10) # Remember best normalized match
        else: # Comparing by string
            fileName = path2FontName(self.path)
            for w in FONT_WEIGHT_MATCHES.get(weight, [weight]):
                if not isinstance(w, (float, int)) and (w in fileName or w in self.info.styleName):
                    match = max(match, len(w)*100) # Longer weight name is better match
        return match

    def widthMatch(self, width):
        u"""Answer level of matchting for the (abbreviated) width name or number with font.

        >>> from pagebot.contexts.platform import getRootFontPath
        >>> path = getRootFontPath() + '/google/roboto/Roboto-Black.ttf' # We know this exists in the PageBot repository
        >>> font = Font(path)
        >>> font.info.widthClass
        5
        >>> font.widthMatch(0) # Bad match --> 0
        0
        >>> font.widthMatch(4) # Close match --> 800
        800
        >>> font.widthMatch(5) # Exact match --> 1000
        1000
        >>> font.widthMatch(6) # Close match --> 800
        800
        >>> font.widthMatch(10) # Bad match --> 0
        0
        >>> #font.widthMatch(500) # Exact match -->1000 in case font weight values range beteween 0-->1000
        1000
        >>> #font.widthMatch(501) # Near match --> 1000
        1000
        >>> #font.widthMatch(650) # Close match --> 800
        800
        >>> font.widthMatch('Cond') # No match --> 0
        0
        >>> path = getRootFontPath() + '/google/robotocondensed/RobotoCondensed-Bold.ttf' # We know this exists in the PageBot repository
        >>> font = Font(path)
        >>> font.info.widthClass
        5
        >>> font.widthMatch(5) # Wrong exact match --> 1000 due to wrong font.info.widthClass 
        1000
        >>> font.widthMatch('Wide') # No match on "Wide"
        0
        >>> #font.widthMatch('Cond') # Exact match on "Cond"
        180
        """
        match = 0
        if isinstance(width, (float, int)):
            # Compare the width as number as max difference to what we already have.
            wf = self.info.widthClass 
            if wf <= 10: # Normalize to 1000
                wf *= 10
            for w in FONT_WIDTH_MATCHES.get(width, [width]):
                if isinstance(w, (float, int)): 
                    if w <= 10: # Normalize to 1000
                        w *= 10
                    match = max(match, 1000 - abs(w - wf)*20) # Remember best normalized match
        else: # Comparing by string
            fileName = path2FontName(self.path)
            for w in FONT_WIDTH_MATCHES.get(width, [width]):
                if not isinstance(w, (float, int)) and (w in fileName or w in self.info.styleName):
                    match = max(match, len(w)*20) # Longer width name is better match
        return match

    def isItalic(self):
        u"""Answer the boolean flag if this font should be considered to be italic.

        >>> from pagebot.fonttoolbox.objects.font import Font
        >>> from pagebot.contexts.platform import getRootFontPath
        >>> fontPath = getRootFontPath()
        >>> path = getRootFontPath() + '/google/roboto/Roboto-BlackItalic.ttf' # We know this exists in the PageBot repository
        >>> f = Font(path, install=False)
        >>> f.isItalic()
        True
        """
        if self.info.italicAngle:
            return True
        for i in FONT_ITALIC_MATCHES['Italic']:
            if i in path2FontName(self.path) or i in self.info.styleName:
                return True
        return False

    def keys(self):
        u"""Answer the glyph names of the font.

        >>> from pagebot.fonttoolbox.objects.font import Font
        >>> from pagebot.contexts.platform import getRootFontPath
        >>> fontPath = getRootFontPath()
        >>> path = fontPath + '/fontbureau/AmstelvarAlpha-VF.ttf'
        >>> f = Font(path, install=False, lazy=False)
        >>> 'A' in f.keys()
        True
        """
        if 'glyf' in self.ttFont:
            return self.ttFont['glyf'].keys()
        return []

    def __contains__(self, glyphName):
        u"""Allow direct testing. 

        >>> from pagebot.toolbox.transformer import *
        >>> from pagebot.fonttoolbox.objects.font import Font
        >>> from pagebot.contexts.platform import getRootFontPath
        >>> fontPath = getRootFontPath()
        >>> path = fontPath + '/fontbureau/AmstelvarAlpha-VF.ttf'
        >>> f = Font(path, install=False, lazy=False)
        >>> 'A' in f
        True
        """
        return glyphName in self.keys()

    def _get_analyzer(self):
        u"""Answer the style/font analyzer if it exists. Otherwise create one.

        >>> from pagebot.toolbox.transformer import *
        >>> from pagebot.fonttoolbox.objects.font import Font
        >>> from pagebot.contexts.platform import getRootFontPath
        >>> fontPath = getRootFontPath()
        >>> path = fontPath + '/fontbureau/AmstelvarAlpha-VF.ttf'
        >>> f = Font(path, install=False, lazy=False)
        >>> #f.analyzer.stems # TODO: Needs bezier path for pixel test.
        
        """
        if self._analyzer is None:
            self._analyzer = self.FONTANALYZER_CLASS(self)
        return self._analyzer
    analyzer = property(_get_analyzer)

    def _get_axes(self): 
        u"""Answer dictionary of axes if self.ttFont is a Variable Font. Otherwise answer an empty dictioary.

        >>> from pagebot.toolbox.transformer import *
        >>> from pagebot.fonttoolbox.objects.font import Font
        >>> from pagebot.contexts.platform import getRootFontPath
        >>> fontPath = getRootFontPath()
        >>> path = fontPath + '/fontbureau/AmstelvarAlpha-VF.ttf'
        >>> f = Font(path, install=False, lazy=False)
        >>> f.axes['XTRA']
        (42.0, 402.0, 402.0)
         """
        try:
            # TODO: Change value to Axis dictionary instead of list
            axes = {a.axisTag: (a.minValue, a.defaultValue, a.maxValue) for a in self.ttFont['fvar'].axes}
        except KeyError:
            axes = {} # This is not a variable font.
        return axes
    axes = property(_get_axes)

    def getDefaultVarLocation(self):
        u"""Answer the location dictionary with the default axes values.
        
        >>> from pagebot.toolbox.transformer import *
        >>> from pagebot.fonttoolbox.objects.font import Font
        >>> from pagebot.contexts.platform import getRootFontPath
        >>> fontPath = getRootFontPath()
        >>> path = fontPath + '/fontbureau/AmstelvarAlpha-VF.ttf'
        >>> font = Font(path, install=False)
        >>> len(font.getDefaultVarLocation().keys())
        15
        """
        defaultVarLocation = {}
        for axisName, axis in self.axes.items():
            defaultVarLocation[axisName] = axis[1]
        return defaultVarLocation

    def _get_rawDeltas(self):
        u"""Answer the list of axis dictionaries with deltas for all glyphs and axes. Answer an empty dictionary
        if the [gvar] table does not exist.

        >>> from pagebot.fonttoolbox.objects.font import Font
        >>> from pagebot.contexts.platform import getRootFontPath
        >>> fontPath = getRootFontPath()
        >>> path = fontPath + '/fontbureau/AmstelvarAlpha-VF.ttf'
        >>> font = Font(path)
        >>> len(font.rawDeltas['A'])
        17
        """
        try:
            return self.ttFont['gvar'].variations
        except:
            return {}
    rawDeltas = property(_get_rawDeltas)

    def _get_designSpace(self):
        u"""Answer the design space in case this is a variable font.

        >>> from pagebot.contexts.platform import getRootFontPath
        >>> fontPath = getRootFontPath()
        >>> path = fontPath + '/fontbureau/AmstelvarAlpha-VF.ttf'
        >>> font = Font(path)
        >>> font.designSpace # Basically the "cvar" table.
        {}
        """
        try:
            designSpace = self.ttFont['cvar']
        except KeyError:
            designSpace = {}
        return designSpace
    designSpace = property(_get_designSpace)

    def _get_variables(self):
        u"""Answer the gvar-table (if it exists) translated into plain Python dictionaries 
        of deltas per glyph and per axis if this is a Var-fonts. Otherwise answer an empty dictionary

        >>> from pagebot.contexts.platform import getRootFontPath
        >>> fontPath = getRootFontPath()
        >>> path = fontPath + '/fontbureau/AmstelvarAlpha-VF.ttf'
        >>> font = Font(path)
        >>> len(font.variables)
        115
        >>> variables = font.variables['H']
        >>> sorted(variables.keys())
        ['GRAD', 'XOPQ', 'XTRA', 'YOPQ', 'YTRA', 'YTSE', 'YTUC', 'opsz', 'wdth', 'wght']
        >>> axis, deltas = variables['GRAD']
        >>> axis
        {'GRAD': (0.0, 1.0, 1.0)}
        >>> deltas[:6]
        [(0, 0), None, (52, 0), None, None, (89, 0)]
        >>> font.variables.get('wrongGlyphName') is None
        True
        """
        if self._variables is None:
            try:
                gvar = self.ttFont['gvar'] # Get the raw fonttools gvar table if it exists.
                self._variables = {} 
                for glyphName, tupleVariations in gvar.variations.items():
                    self._variables[glyphName] = axisDeltas = {}
                    for tupleVariation in tupleVariations:
                        axisKey = '_'.join(tupleVariation.axes.keys()) #{'GRAD': (0.0, 1.0, 1.0)} Make unique key, in case multiple
                        axisDeltas[axisKey] = tupleVariation.axes, tupleVariation.coordinates # ({'GRAD': (0.0, 1.0, 1.0)}, [(0, 0), None, (52, 0), None, None, (89, 0), ...])
            except KeyError:
                pass # No gvar table, just answer the current self._variables as None.
        return self._variables
    variables = property(_get_variables)

    def _get_features(self):

        return context.listOpenTypeFeatures(self.installedName)
    features = property(_get_features)

    def _get_kerning(self):
        u"""Answer the (expanded) kerning table of the font.

        >>> from pagebot.toolbox.transformer import *
        >>> from pagebot.contexts.platform import getRootFontPath
        >>> fontPath = getRootFontPath()
        >>> path = fontPath + '/djr/bungee/Bungee-Regular.ttf'
        >>> f = Font(path, install=False, lazy=False)
        >>> len(f.kerning.keys())
        22827
        """
        if self._kerning is None: # Lazy read.
            self._kerning = OTFKernReader(self.path).kerningPairs
        return self._kerning
    kerning =  property(_get_kerning)

    def _get_groups(self):
        u"""Answer the groups dictionary of the font.

        >>> from pagebot.toolbox.transformer import *
        >>> from pagebot.fonttoolbox.objects.font import Font
        >>> from pagebot.contexts.platform import getRootFontPath
        >>> fontPath = getRootFontPath()
        >>> path = fontPath + '/djr/bungee/Bungee-Regular.ttf'
        >>> f = Font(path, install=False, lazy=False)
        >>> g = f['A']
        >>> f.groups is None
        True
        """
        return self._groups
    groups = property(_get_groups)

    def getFeaturedString(self, s, featureSettings):
        u"""Compile the string s into glyph names, corresponding to the
        settings in featureSettings."""
        return s

    def install(self):
        u"""Install the font in DrawBot, if not already there. Answer the
        DrawBot name."""
        self.installedName = context.installFont(self.path)
        return self.installedName

    def save(self, path=None):
        u"""Save the font to optional path or to self.path."""
        self.ttFont.save(path or self.path)



if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
