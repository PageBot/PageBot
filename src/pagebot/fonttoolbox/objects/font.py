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
#     font.py
#
#     Implements a PabeBot font style to get info from a TTFont.
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
    from drawBot import installFont, listOpenTypeFeatures
except ImportError:
    installFont =  listOpenTypeFeatures = None

from pagebot.fonttoolbox.objects.glyph import Glyph
from pagebot.fonttoolbox.objects.fontinfo import FontInfo
from pagebot.contributions.adobe.kerndump.getKerningPairsFromOTF import OTFKernReader

AXES = {
    # Registered axes
    'wght': dict(name='Weight', tag='wght', description='Description of registered wght axis here'),
    'wdth': dict(name='Width', tag='wdth', description='Description of registered wdth axis here'),
    'opsz': dict(name='Optical size', tag='opsz', description='Description of registered opsz axis here'),
    # PageBot defined axes.
    'YOPQ': dict(name='????', tag='YOPQ', description='Description of YOPQ here'),
    'YTSE': dict(name='????', tag='YTSE', description='Description of YTSE here'),
    'YTLC': dict(name='????', tag='YTLC', description='Description of YTLC here'),
    'XTRA': dict(name='????', tag='XTRA', description='Description of XTRA here'),
    'XOPQ': dict(name='????', tag='XOPQ', description='Description of XOPQ here'),
    'GRAD': dict(name='????', tag='GRAD', description='Description of GRAD here'),
    # Decovar (temp names?)
    'wmx2': dict(name='????', tag='wmx2', description='Description of wmx2 here'),
    'bldB': dict(name='????', tag='bldB', description='Description of bldB here'),
    'bldA': dict(name='????', tag='bldA', description='Description of bldA here'),
    'sklA': dict(name='Skeleton A', tag='sklA', description='Description of sklA here'),
    'sklB': dict(name='Skeleton B', tag='sklB', description='Description of sklB here'),
    'sklD': dict(name='Skeleton D', tag='sklD', description='Description of sklD here'),
    'trmA': dict(name='Terminal A', tag='trmA', description='Description of trmA here'),
    'trmB': dict(name='Terminal B', tag='trmB', description='Description of trmB here'),
    'trmC': dict(name='Terminal C', tag='trmC', description='Description of trmC here'),
    'trmD': dict(name='Terminal D', tag='trmD', description='Description of trmD here'),
    'trmE': dict(name='Terminal E', tag='trmE', description='Description of trmE here'),
    'trmF': dict(name='Terminal F', tag='trmF', description='Description of trmF here'),
    'trmG': dict(name='Terminal G', tag='trmG', description='Description of trmG here'),
    'trmK': dict(name='Terminal K', tag='trmK', description='Description of trmK here'),
    'trmL': dict(name='Terminal L', tag='trmL', description='Description of trmL here'),

}
def getFontPathOfFont(fontName):
    font = NSFont.fontWithName_size_(fontName, 25)
    if font is not None:
        fontRef = CTFontDescriptorCreateWithNameAndSize(font.fontName(), font.pointSize())
        url = CTFontDescriptorCopyAttribute(fontRef, kCTFontURLAttribute)
        return url.path()
    return None

class Font(object):
    # Storage of font information while composing the pages.
    GLYPH_CLASS = Glyph

    def __init__(self, path, name=None, install=True):
        u"""Initialize the TTFont, for which Font is a wrapper. Default is to
        install the font in DrawBot.

        self.name is supported, in case the caller wants to use a different
        name than the DrawBot installing name."""
        self.path = path # File path of the font file.
        if install:
            self.install() # Installs the font in DrawBot from self.path and initializes self.installedName.
        else:
            self.installedName = None # Set to DrawBot name, when installed later.
        try:
            self.ttFont = TTFont(path, lazy=True)
            self.info = FontInfo(self.ttFont) # TTFont is available as lazy style.info.font
            # Store optional custom name, otherwise use original DrawBot name. Otherwise use from FontInfo.fullName
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
            axes = {a.axisTag: (a.minValue, a.defaultValue, a.maxValue) for a in self.ttFont['fvar'].axes}
        except KeyError:
            axes = {} # This is not a var font.
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
        u"""Compile the string s into glyph names, corresponding to the settings in featureSettings."""
        return s

    def install(self):
        u"""Install the font in DrawBot, if not already there. Answer the DrawBot name."""
        self.installedName = installFont(self.path)
        return self.installedName

    def save(self, path=None):
        u"""Save the font to optional path or to self.path."""
        self.ttFont.save(path or self.path)

