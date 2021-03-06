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
#     font.py
#
#     Implements a PageBot font style to get info from a TTFont. Using the
#     Family / Font / Glyph classes, allows page layout in PageBot to access
#     all information in a font purpose of typography and layout.
#
#     We will call this class "Font" instead of "Style" , to avoid confusion
#     with the PageBot style dictionary, which hold style parameters.
#
import os

from fontTools.ttLib import TTFont, TTLibError
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
from fontTools.varLib.models import supportScalar, normalizeLocation
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.varLib.iup import iup_delta

from pagebot.constants import *
from pagebot.contributions.adobe.kerndump.getKerningPairsFromOTF import OTFKernReader
from pagebot.toolbox.transformer import path2FontName, path2Extension, asFormatted
from pagebot.fonttoolbox.analyzers.fontanalyzer import FontAnalyzer
from pagebot.fonttoolbox.fontpaths import getFontPaths
from pagebot.fonttoolbox.objects.glyph import Glyph
from pagebot.fonttoolbox.objects.fontinfo import FontInfo
from pagebot.toolbox.units import RelativeUnit, Unit, upt, isUnit

def asFontPath(fontPath):
    """Answers if the path is a font path. Check if there is a matching
    problem by lower case/upper case. If matching then answer the real path.
    If no match exists for the defined fontPath, then answer None.
    Case matching is only tested on the file name, not the whole path.

    For now, PageBot only supports ('ttf', 'otf')

    >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
    >>> fontPath = getTestFontsPath()
    >>> path1 = fontPath + '/fontbureau/Amstelvar-Roman-VF.ttf'
    >>> path1 == asFontPath(path1) # Path with capitals, nothing changed.
    True
    >>> path1_lc = fontPath + '/fontbureau/amstelvar-roman-vf.ttf'
    >>> path1 == asFontPath(path1_lc) # Matching witn lower case, answers the real path.
    True
    >>> path2 = fontPath + '/fontbureau/Amstelvar-Roman-VF_XXX.ttf'
    >>> path2 == asFontPath(path2)
    False
    >>> path3 = fontPath + '/fontbureau/Amstelvar-Roman-VF.UFO'
    >>> asFontPath(path3) is None # Font path does not exist
    True
    >>> asFontPath(None) is None # Not a valid font path
    True
    >>> asFontPath(123) is None # Not a valid font path
    True
    """
    try:
        if not path2Extension(fontPath) in ('ttf', 'otf'):
            return None

        pathParts = fontPath.split('/')
        dirPath = '/'.join(pathParts[:-1]) + '/'
        filePath = pathParts[-1].lower() # Match ignoring case
        for fn in os.listdir(dirPath):
            if fn.startswith('.'):
                continue
            if filePath == fn.lower():
                return dirPath + fn
        return None
    except AttributeError:
        pass
    return None

def getFont(fontOrPath, lazy=True):
    """Answers the Font instance, that connects to the fontPath. Note that
    there is no check if there is already anothe Font created on that path,
    as for PageBot purposes it is most likely for reading only.

    >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
    >>> fontPath = getTestFontsPath()
    >>> path = fontPath + '/fontbureau/Amstelvar-Roman-VF.ttf'
    >>> fontName = path2FontName(path)
    >>> font = getFont(path)
    >>> font.path == path
    True
    >>> # Answer the same font, if it is already one.
    >>> font == getFont(font)
    True
    """
    if isinstance(fontOrPath, Font):
        return fontOrPath

    fontOrPath = asFontPath(fontOrPath) # Find the real path, case corrected.
    if not fontOrPath:
        return None

    try:
        return Font(fontOrPath, lazy=lazy)
    except TTLibError:
        # Could not open font, due to bad font file.
        return None

def findFonts(pattern, lazy=True):
    """Answers a list of Font instances where the pattern fits the font path.
    If pattern is a list, all parts should have a match.


    # TODO: make case insensitive
    """
    """
    >>> findFonts('Roboto-Thi')
    [<Font Roboto-Thin>, <Font Roboto-ThinItalic>]
    >>> # Select on family and name parts.
    >>> findFonts(('Robo', 'Ita', 'Thi'))
    [<Font Roboto-ThinItalic>]
    >>> # Select on style parts only.
    >>> findFonts(('Ita', 'Bol', 'Con'))
    [<Font RobotoCondensed-BoldItalic>]
    """
    fontPaths = getFontPaths()
    fonts = []

    if not isinstance(pattern, (list, tuple)):
        pattern = [pattern]

    for fontPath in fontPaths:
        found = True
        for match in pattern:
             if not match in fontPath:
                found = False
                break
        if found:
            fonts.append(findFont(fontPath, lazy=lazy))
    return fonts

def findFont(fontPath, default=None, lazy=True):
    """Answers the font the has name fontName.

    >>> f = findFont('Roboto-Regular')
    >>> f
    <Font Roboto-Regular>
    >>> notSkiaFont = findFont('Skia-cannot-be-found')
    >>> notSkiaFont is None
    True
    >>> # Default is a font.
    >>> # Set RobotoFont as default.
    >>> notSkiaFont = findFont('Skia-cannot-be-found', default=f)
    >>> notSkiaFont is f # Found robotoFont instead
    True
    >>> # Default is a name.
    >>> f = findFont('Skia-cannot-be-found', default='Roboto-Regular') # Found default RobotoFont instead
    >>> f
    <Font Roboto-Regular>
    """
    if isinstance(fontPath, Font): # It's already a Font instance, just answer it.
        return fontPath

    fontPaths = getFontPaths() # Otherwise, let's see if we can find it by name.
    if fontPath in fontPaths:
        font = getFont(fontPaths[fontPath], lazy=lazy)
        if font is not None:
            return font

    font = getFont(fontPath)
    if font is not None:
        return font

    # A default is defined. If it's a string, try to find it. Avoid c76ircular
    # calls.
    if isinstance(default, str) and default != fontPath:
        return findFont(default, lazy=lazy)

    assert default is None or isinstance(default, Font)
    # Otherwise assume it is a Font instance or None.
    return default

def getFontPath(font):
    """Answer the font file path for @font.

    >>> path = getFontPath('PageBot-Regular')
    >>> path.endswith('PageBot-Regular.ttf')
    True
    """
    #assert isinstance(font, Font)

    fontPath = None
    if font is not None:
        if isinstance(font, str):
            f = findFont(font)
            if f is not None:
                fontPath =  f.path

    if not fontPath or not os.path.exists(fontPath):
        f = findFont(DEFAULT_FONT)
        if f is not None:
            fontPath = font.path
    return fontPath

def getLineHeight(leading, fontSize):
    """

    >>> from pagebot.toolbox.units import pt, em
    >>> getLineHeight(em(1.5), pt(12))
    18
    >>> getLineHeight(pt(15), pt(12))
    15
    >>> getLineHeight(pt(19), None)
    19
    >>> getLineHeight(15, pt(16))
    240
    """
    assert leading is not None

    if isinstance(leading, RelativeUnit):
        lineHeight = upt(leading.byBase(fontSize))
    elif isinstance(leading, Unit):
        lineHeight = upt(leading)
    elif isUnit(fontSize):
        # Leading is scalar?
        lineHeight = leading * fontSize.pt
    else:
        # Both scalar?
        lineHeight = leading * fontSize

    return lineHeight

def getMasterPath():
    """Answers the path to read master fonts, which typically is a
    <username>/Fonts/ folder. Default is at the same level as pagebot
    module."""
    return os.path.expanduser("~") + '/Fonts/'

def getInstancePath():
    """Answers the path to write instance fonts, which typically is the

    <username>/Fonts/_instances/

    folder."""
    return getMasterPath() + '_instances/'

def getScaledValue(vf, tag, value):
    """Answers the scaled value for the "tag" axis, where value (-1..0..1) is
    upscaled to ratio in (minValue, defaultValue, maxValue)."""
    if not tag in vf.axes:
        return None
    assert -1 <= value <= 1
    minValue, defaultValue, maxValue = vf.axes[tag]
    if not value:
        return defaultValue
    # Realative scale between minValue and default
    if value < 0:
        return defaultValue + (defaultValue - minValue)*value
    # else wdth > 0:  Relative scale between default and maxValue
    return defaultValue + (maxValue - defaultValue)*value

def getScaledLocation(vf, normalizedLocation):
    """Answers the instance of self, corresponding to the normalized location.
    (-1, 0, 1) values for axes as e.g. [wght] and [wdth].

    The optical size [opsz] is supposed to contain the font size, so it is not
    scaled. If [opsz] is not defined, then set it to default, if the axis
    exist.

    >>> from pagebot.fonttoolbox.objects.font import findFont
    >>> font = findFont('AmstelvarAlpha-VF')
    >>> getScaledLocation(font, dict(wght=0, opsz=24))['wght']
    400.0
    """
    scaledLocation = {}
    if normalizedLocation and vf.axes:

        for tag, value in normalizedLocation.items():
            if tag != 'opsz':
                value = getScaledValue(vf, tag, value)
            scaledLocation[tag] = value

        for axisTag, (_, defaultValue, _) in vf.axes.items():
            if axisTag not in scaledLocation:
                scaledLocation[axisTag] = defaultValue

    return scaledLocation

def getInstance2(vf, location=None, dstPath=None, name=None,
        opticalSize=None, styleName=None, cached=True, lazy=True):
    """Answers the VF-TTFont instance at location (created by
    fontTools.varLib.mutator.instantiateVariableFont) packed as Font instance.

    >>> vf = findFont('Amstelvar-Roman-VF')
    >>> instance = getInstance2(vf, opticalSize=8)
    >>> instance
    <Font Amstelvar-Roman-VF-opsz8>
    >>> instance.location
    {'opsz': 8}
    >>> instance['H'].width
    1740
    """
    """
    >>> instance = getInstance2(vf, location=dict(wght=300), cached=False, opticalSize=150)
    >>> instance.location
    {'wght': 300, 'opsz': 150}
    >>> instance['H'].width
    1740
    >>> instance = getInstance2(vf, path='/tmp/TestVariableFontInstance.ttf', opticalSize=8)
    >>> instance
    <Font TestVariableFontInstance>
    """

    if location is None:
        location = {}
    if opticalSize is not None:
        location['opsz'] = opticalSize

    #if path is None and cached:

    # Make a custom file name from the location e.g. VariableFont-wghtXXX-wdthXXX.ttf
    # Only add axis values to the name that are not default.
    instanceName = ""
    for tag, value in sorted(location.items()):
        if value != vf.axes[tag][1]:
            instanceName += "-%s%s" % (tag, asFormatted(value))
    instanceFileName = '.'.join(vf.path.split('/')[-1].split('.')[:-1]) + instanceName + '.ttf'

    targetDirectory = getInstancePath()
    if not os.path.exists(targetDirectory):
        os.makedirs(targetDirectory)
    path = targetDirectory + instanceFileName

    if cached and os.path.exists(path):
        instance = Font(path=path, name=name, location=location, opticalSize=opticalSize)
    else:
        ttFont = instantiateVariableFont(vf.ttFont, location) # Get instance from fontTools
        instance = Font(path=path, ttFont=ttFont, name=name, location=location, opticalSize=opticalSize,
            styleName=styleName, lazy=lazy)
        if instance.path.endswith('.ttf'):
            instance.save()

    return instance

def getInstance(pathOrFont, location, dstPath=None, styleName=None,
        opticalSize=None, normalize=True, cached=True, lazy=True,
        kerning=None):
    """The getInstance function refers to the file of the source variable font.
    The nLocation is dictionary axis locations of the instance with values
    between (0, 1000), e.g. dict(wght=0, wdth=1000) or values between (0, 1),
    e.g.  dict(wght=0.2, wdth=0.6). Set normalize to False if the values in
    location already are matching the axis min/max of the font. If there is a
    [opsz] Optical Size value defined, then store that information in the
    font.info.opticalSize.

    The optional *styleName* overwrites the *font.info.styleName* of the
    *ttFont* or the automatic location name.


    >>> vf = findFont('Amstelvar-Roman-VF')
    >>> instance = getInstance(vf, location={}, opticalSize=8)
    >>> instance
    <Font Amstelvar-Roman-VF-opsz8>
    """
    """
    >>> instance.location
    {'opsz': 8}
    >>> instance['H'].width
    1740
    >>> instance = getInstance(vf, location=dict(wght=300), cached=False, opticalSize=150)
    >>> instance.location
    {'wght': 300, 'opsz': 150}
    >>> instance['H'].width
    1740
    >>> instance = getInstance(vf, path='/tmp/TestVariableFontInstance.ttf', opticalSize=8)
    >>> instance
    <Font Amstelvar-Roman-VF-wght300>
    """
    # If forcing flag is undefined, then get info from location.
    if opticalSize is None:
        opticalSize = location.get('opsz')
    else:
        location['opsz'] = opticalSize

    instance = makeInstance(pathOrFont, location, dstPath=None, normalize=normalize, cached=cached,
        lazy=lazy, kerning=kerning)

    # Answers the generated Variable Font instance. Add [opsz] value if is
    # defined in the location, otherwise None.
    instance.info.opticalSize = opticalSize
    instance.info.location = location
    instance.info.varStyleName = styleName
    return instance

def makeInstance(pathOrVarFont, location, dstPath=None, normalize=True, cached=True,
        lazy=True, kerning=None):
    """Instantiate an instance of a variable font at the specified location.

    Keyword arguments:
    - varfilename -- a variable font file path
    - location -- a dictionary of axis tag and value {"wght": 0.75, "wdth": -0.5}

    >>> vf = findFont('RobotoDelta-VF')
    >>> print(vf)
    <Font RobotoDelta-VF>
    >>> print(len(vf))
    188
    >>> instance = makeInstance(vf.path, dict(opsz=8), cached=False)
    >>> instance
    <Font RobotoDelta-VF-opsz8>
    >>> len(instance) > 100
    True
    >>> len(instance['H'].points)
    12
    """
    # make a custom file name from the location e.g.
    # VariableFont-wghtXXX-wdthXXX.ttf
    instanceName = ""

    if isinstance(pathOrVarFont, Font):
        pathOrVarFont = pathOrVarFont.path

    varFont = Font(pathOrVarFont, lazy=lazy)
    ttFont = varFont.ttFont

    for k, v in sorted(location.items()):
        # TODO better way to normalize the location name to (0, 1000)
        v = min(v, 1000)
        v = max(v, 0)
        instanceName += "-%s%s" % (k, v)

    if dstPath is None:
        targetFileName = '.'.join(varFont.path.split('/')[-1].split('.')[:-1]) + instanceName + '.ttf'
        targetDirectory = getInstancePath()
        if not targetDirectory.endswith('/'):
            targetDirectory += '/'
        if not os.path.exists(targetDirectory):
            os.makedirs(targetDirectory)
        dstPath = targetDirectory + targetFileName

    # Instance does not exist as file. Create it.
    if not cached or not os.path.exists(dstPath):
        # Set the instance name IDs in the name table
        platforms=((1, 0, 0), (3, 1, 0x409)) # Macintosh and Windows

        for platformID, platEncID, langID in platforms:
            # 1 Font Family name
            familyName = ttFont['name'].getName(1, platformID, platEncID, langID)
            if not familyName:
                continue
            # NameRecord to unicode string
            familyName = familyName.toUnicode()
            # TODO make sure this works in any case
            styleName = instanceName
            fullFontName = " ".join([familyName, styleName])
            postscriptName = fullFontName.replace(" ", "-")
            # 2 Font Subfamily name
            ttFont['name'].setName(styleName, 2, platformID, platEncID, langID)
            # 4 Full font name
            ttFont['name'].setName(fullFontName, 4, platformID, platEncID, langID)
            # 6 Postscript name for the font
            ttFont['name'].setName(postscriptName, 6, platformID, platEncID, langID)
            # Other important name IDs
            # 3 Unique font identifier (e.g. Version 0.000;NONE;Promise Bold Regular)
            # 25 Variables PostScript Name Prefix

        fvar = ttFont['fvar']
        axes = {a.axisTag:(a.minValue,a.defaultValue,a.maxValue) for a in fvar.axes}
        # TODO Apply avar
        # TODO Round to F2Dot14?
        loc = normalizeLocation(location, axes)
        # Location is normalized now.

        gvar = ttFont['gvar']
        glyf = ttFont['glyf']

        # get list of glyph names in gvar sorted by component depth.
        glyphNames = sorted(
            gvar.variations.keys(),
            key=lambda name: (
                glyf[name].getCompositeMaxpValues(glyf).maxComponentDepth
                if glyf[name].isComposite() else 0,
                name))

        for glyphName in glyphNames:
            variations = gvar.variations[glyphName]
            coordinates, _ = glyf.getCoordinatesAndControls(glyphName, ttFont)
            origCoords, endPts = None, None

            for var in variations:
                scalar = supportScalar(loc, var.axes)#, ot=True)
                if not scalar:
                    continue
                delta = var.coordinates
                if None in delta:
                    if origCoords is None:
                        origCoords, control = glyf.getCoordinatesAndControls(glyphName, ttFont)
                        endPts = control[1] if control[0] >= 1 else list(range(len(control[1])))
                    delta = iup_delta(delta, origCoords, endPts)
                coordinates += GlyphCoordinates(delta) * scalar

            glyf.setCoordinates(glyphName, coordinates, ttFont)

        # Interpolate cvt.

        if 'cvar' in ttFont:
            cvar = ttFont['cvar']
            cvt = ttFont['cvt ']
            deltas = {}
            for var in cvar.variations:
                scalar = supportScalar(loc, var.axes)
                if not scalar:
                    continue
                for i, c in enumerate(var.coordinates):
                    if c is not None:
                        deltas[i] = deltas.get(i, 0) + scalar * c
            for i, delta in deltas.items():
                cvt[i] += int(round(delta))

        for tag in ('avar', 'cvar', 'fvar', 'gvar', 'HVAR', 'MVAR', 'VVAR', 'STAT'):
            if tag in ttFont:
                del ttFont[tag]

        if kerning is not None:
            for pair, value in kerning.items():
                varFont.kerning[pair] = value

        varFont.save(dstPath)

    # Answer instance.
    return Font(dstPath, lazy=lazy)

class Font:
    """Storage of font information while composing the pages.

    >>> from pagebot.fonttoolbox.objects.font import findFont
    >>> f = findFont('RobotoDelta-VF')
    >>> sorted(f.axes.keys())
    ['GRAD', 'POPS', 'PWDT', 'PWGT', 'UDLN', 'XOPQ', 'XTRA', 'YOPQ', 'YTAD', 'YTAS', 'YTDD', 'YTDE', 'YTLC', 'YTRA', 'YTUC', 'opsz', 'wdth', 'wght']
    >>> f.info.familyName
    'RobotoDelta'
    >>> len(f)
    188
    >>> f.axes['opsz']
    (8.0, 12.0, 144.0)
    >>> variables = f.variables
    >>> features = f.features
    >>> f.groups
    >>> f.designSpace
    {}
    """
    GLYPH_CLASS = Glyph
    FONTANALYZER_CLASS = FontAnalyzer

    def __init__(self, path=None, ttFont=None, name=None, opticalSize=None,
            location=None, styleName=None, lazy=True):
        """Initialize the TTFont, for which Font is a wrapper. self.name is
        supported, in case the calling function wants to use a different

        >>> f = Font()
        >>> f
        <Font Untitled Untitled>
        """

        if path is None and ttFont is None:
            self.ttFont = TTFont()
            self.path = '%d' % id(ttFont) # In case no path, use unique id instead.
        elif ttFont is None and path is not None:
            self.ttFont = TTFont(path, lazy=lazy)
            self.path = path # File path of the existing font file.
        elif path is None:
            self.ttFont = ttFont
            self.path = '%d' % id(ttFont) # In case no path, use unique id instead.
        else: # ttFont is not None: There is ttFont data
            self.ttFont = ttFont
            self.path = path

        # Store location, in case this was a created VF instance
        self.location = location
        # TTFont is available as lazy style.info.font
        self.info = FontInfo(self.ttFont)
        self.info.opticalSize = opticalSize # Optional optical size, to indicate where this Variable Font is rendered for.
        self.info.location = location # Store origina location of this instance of the font is derived from a Variable Font.
        # Stores optional custom name, otherwise use original DrawBot name.
        # Otherwise use from FontInfo.fullName
        self.name = name or self.info.fullName
        if styleName is not None:
            self.info.styleName = styleName # Overwrite default style name in the ttFont or Variable Font location
        self._kerning = None # Lazy reading.
        self._groups = None # Lazy reading.
        self._glyphs = {} # Lazy creation of self[glyphName]
        self._analyzer = None # Lazy creation.
        self._variables = None # Lazy creations of delta's dictionary per glyph per axis

    def __repr__(self):
        """
        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> path = getTestFontsPath() + '/google/roboto/Roboto-Black.ttf'
        >>> font = getFont(path)
        >>> str(font)
        '<Font Roboto-Black>'
        """
        return '<Font %s>' % (path2FontName(self.path) or self.name or 'Untitled').strip()

    def __getitem__(self, glyphName):
        """Answers the glyph with glyphName.

        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> path = getTestFontsPath() + '/google/roboto/Roboto-Black.ttf'
        >>> font = getFont(path)
        >>> g = font['A']
        >>> g.name, g.width
        ('A', 1395)
        """
        if not glyphName in self._glyphs:
            self._glyphs[glyphName] = self.GLYPH_CLASS(self, glyphName)
        return self._glyphs[glyphName]

    def __len__(self):
        """Answers the number of glyphs in the font.

        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> path = getTestFontsPath() + '/google/roboto/Roboto-Black.ttf'
        >>> font = getFont(path)
        >>> len(font)
        3387
        """
        if 'glyf' in self.ttFont:
            return len(self.ttFont['glyf'])
        return 0

    def __eq__(self, font):
        if isinstance(font, self.__class__):
            return self.info.familyName == font.info.familyName and self.info.styleName == font.info.styleName
        return False

    def __ne__(self, font):
        if not isinstance(font, self.__class__):
            return False
        return self.info.familyName != font.info.familyName or self.info.styleName != font.info.styleName

    def nameMatch(self, pattern):
        """Answers level of matching between pattern and the font file name or
        font.info.fullName. Pattern can be a single string or a list of
        string.

        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> path = getTestFontsPath() + '/google/roboto/Roboto-Black.ttf'
        >>> font = getFont(path)
        >>> font.nameMatch('Black')
        1.0
        >>> font.nameMatch('Blackish')
        0
        >>> font.nameMatch(('Roboto', 'Black'))
        1.0
        """
        fontName = path2FontName(self.path)
        if not isinstance(pattern, (list, tuple)):
            pattern = [pattern]
        for part in pattern:
            if not part in fontName:# or part in self.info.fullName):
                return 0
        return 1.0

    def weightMatch(self, weight):
        """Answers level of matching for the (abbreviated) weight name or
        number with font, in a value between 0 and 1. Currently there is only
        no-match (0) and full-match (1). Future implementations may give a
        float indicator for the level of matching, so the calling function can decide on
        the level of threshold.

        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> # We know this exists in the PageBot repository
        >>> path = getTestFontsPath() + '/google/roboto/Roboto-Black.ttf'
        >>> font = getFont(path)
        >>> font.info.weightClass
        900
        >>> # Bad match
        >>> font.weightMatch(0)
        0
        >>> # Bad match
        >>> font.weightMatch(800)
        0
        >>> # Exact match
        >>> font.weightMatch(900)
        0
        >>> # Bad match -
        >>> font.weightMatch(0)
        0
        >>> # Black --> Exact match on 900
        >>> font.weightMatch('Black')
        1.0
        >>> # Light --> No match on 900
        >>> font.weightMatch('Light')
        0
        >>> path = getTestFontsPath() + '/google/roboto/Roboto-Regular.ttf'
        >>> font = getFont(path)
        >>> font.info.weightClass
        400
        """

        """
        TODO: Fix these tests

        >>> # Match
        >>> font.weightMatch(400)
        1.0
        >>> # Match
        >>> font.weightMatch('Regular')
        1.0
        >>> # Matching with width name has no match.
        >>> font.weightMatch('Condensed')
        0
        """
        if isinstance(weight, (float, int)): # Comparing by numbers
            # Compare the weight as number as max difference to what we already have.
            w = self.info.weightClass
            if w in FONT_WEIGHT_MATCHES.get(weight, []):
                return 1.0 # Exact match
        else: # Comparing by string
            fileName = path2FontName(self.path)
            for w in FONT_WEIGHT_MATCHES.get(weight, []):
                if not isinstance(w, (float, int)) and (w in fileName or w in self.info.styleName):
                    return 1.0 # Exacly match
        return 0 # No match

    def widthMatch(self, width):
        """Answers level of matching for the (abbreviated) width name or number
        with font. Currently there is only no-match (0) and full-match (1).
        Future implementations may give a float indicator for the level of
        matching, so the calling function can decide on the level of threshold.

        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> path = getTestFontsPath() + '/google/roboto/Roboto-Black.ttf' # We know this exists in the PageBot repository
        >>> font = getFont(path)
        >>> font.info.widthClass
        5
        >>> font.widthMatch(0) # Bad match
        0
        >>> font.widthMatch(4) # Close match fails
        0
        >>> font.widthMatch(5) # Exact match
        1.0
        >>> font.widthMatch(6) # Close match fails
        0
        >>> font.widthMatch(10) # Bad match
        0
        >>> path = getTestFontsPath() + '/google/roboto/Roboto-Bold.ttf' # We know this exists in the PageBot repository
        >>> font = Font(path)
        >>> font.info.widthClass
        5
        >>> font.widthMatch(5) # Wrong exact match --> 1000 due to wrong font.info.widthClass
        1.0
        >>> font.widthMatch('Wide') # No match on "Wide"
        0
        >>> #font.widthMatch('Cond') # Exact match on "Cond"
        1.0
        """
        if isinstance(width, (float, int)):
            # Compare the width as number as max difference to what we already have.
            w = self.info.widthClass
            if w <= 100: # Normalize to 1000
                w *= 100
            if w in FONT_WIDTH_MATCHES.get(width, []):
                return 1.0
        else: # Comparing by string
            fileName = path2FontName(self.path)
            for w in FONT_WIDTH_MATCHES.get(width, []):
                if not isinstance(w, (float, int)) and (w in fileName or w in self.info.styleName):
                    return 1.0
        return 0

    def isItalic(self):
        """Answers if this font should be considered to be italic. Currently
        there is only no-match (0) and full-match (1). Future implementations
        may give a float indicator for the level of matching, so the calling
        function can decide on the level of threshold.

        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> fontPath = getTestFontsPath()
        >>> path = getTestFontsPath() + '/google/roboto/Roboto-BlackItalic.ttf'
        >>> font = getFont(path)
        >>> font.isItalic()
        1
        >>> path = getTestFontsPath() + '/google/roboto/Roboto-Bold.ttf'
        >>> font = Font(path)
        >>> font.isItalic()
        0
        """
        if self.info.italicAngle:
            return 1
        for altName in FONT_ITALIC_MATCHES:
            if altName in path2FontName(self.path) or altName in self.info.styleName:
                return 1.0
        return 0

    def match(self, name=None, weight=None, width=None, italic=None):
        """Answers a value between 0 and 1 to the amount that self matches the
        defined parameters. Only defined values count in the matching.

        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> path = getTestFontsPath() + '/google/roboto/Roboto-Black.ttf'
        >>> font = getFont(path)
        >>> font.info.widthClass, font.info.weightClass
        (5, 900)
        >>> font.match(name='Roboto')
        1.0
        >>> font.match(name='Robo', weight='Black')
        1.0
        >>> # Only match on the name.
        >>> font.match(name='Robo', weight='Light')
        0.5
        >>> font.match(name='Robo', width=5)
        1.0
        """

        """
        TODO: Fix these tests

        >>> font.match(name='Robo', weight=900, width=5)
        1.0
        >>> font.match(name='Robo', weight=900, width=5, italic=True)
        0.75
        >>> font.match(name='Robo', weight='Black', width=5, italic=False)
        1.0
        >>> font.match(name='Robo', weight='Blackish', width=5, italic=False)
        0.75
        """
        matches = []
        fontName = path2FontName(self.path)
        if name is not None:
            matches.append(self.nameMatch(name))
        # Currently the matches only answer 0 or 1. In future implementations this value may vary
        # as float between 0 and 1.
        if weight is not None:
            matches.append(self.weightMatch(weight))
        if width is not None:
            matches.append(self.widthMatch(width))
        if italic is not None:
            matches.append(italic == self.isItalic())
        if not matches:
            return 0  # Avoif division by zero
        return sum(matches)/len(matches) # Normalize to value between 0..1

    def keys(self):
        """Answers the glyph names of the font.

        >>> from pagebot.fonttoolbox.objects.font import Font
        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> fontPath = getTestFontsPath()
        >>> path = fontPath + '/fontbureau/Amstelvar-Roman-VF.ttf'
        >>> f = getFont(path, lazy=False)
        >>> 'A' in f.keys()
        True
        """
        if 'glyf' in self.ttFont:
            return self.ttFont['glyf'].keys()
        return []

    def _get_cmap(self):
        """Answers the dictionary of sorted {unicode: glyphName, ...} in the
        font.

        >>> from pagebot.fonttoolbox.objects.font import Font
        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> fontPath = getTestFontsPath()
        >>> path = fontPath + '/fontbureau/Amstelvar-Roman-VF.ttf'
        >>> f = getFont(path, lazy=False)
        >>> f.cmap[65]
        'A'
        """
        if 'cmap' in self.ttFont:
            return self.ttFont['cmap'].getBestCmap()
        return {}

    cmap = property(_get_cmap)

    def __contains__(self, glyphName):
        """Allow direct testing.

        >>> from pagebot.toolbox.transformer import *
        >>> from pagebot.fonttoolbox.objects.font import Font
        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> fontPath = getTestFontsPath()
        >>> path = fontPath + '/fontbureau/Amstelvar-Roman-VF.ttf'
        >>> f = getFont(path, lazy=False)
        >>> 'A' in f
        True
        """
        return glyphName in self.keys()

    def _get_analyzer(self):
        """Answers the style / font analyzer if it exists. Otherwise create
        one.

        >>> from pagebot.toolbox.transformer import *
        >>> from pagebot.fonttoolbox.objects.font import Font
        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> fontPath = getTestFontsPath()
        >>> path = fontPath + '/fontbureau/Amstelvar-Roman-VF.ttf'
        >>> f = getFont(path, lazy=False)
        >>> #f.analyzer.stems # TODO: Needs bezier path for pixel test.

        """
        if self._analyzer is None:
            self._analyzer = self.FONTANALYZER_CLASS(self)
        return self._analyzer
    analyzer = property(_get_analyzer)

    def _get_axes(self):
        """Answers dictionary of axes if self.ttFont is a Variable Font.
        Otherwise answer an empty dictioary.

        >>> from pagebot.toolbox.transformer import *
        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> f = findFont('Amstelvar-Roman-VF')
        >>> f.axes['opsz']
        (0.0, 0.0, 1.0)
         """
        try:
            # TODO: Change value to Axis dictionary instead of list
            axes = {a.axisTag: (a.minValue, a.defaultValue, a.maxValue) for a in self.ttFont['fvar'].axes}
        except KeyError:
            axes = {} # This is not a variable font.
        return axes
    axes = property(_get_axes)

    def getDefaultVarLocation(self):
        """Answers the location dictionary with the default axes values.

        >>> from pagebot.toolbox.transformer import *
        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> font = findFont('Amstelvar-Roman-VF')
        >>> len(font.getDefaultVarLocation().keys())
        1
        """
        defaultVarLocation = {}
        for axisName, axis in self.axes.items():
            defaultVarLocation[axisName] = axis[1]
        return defaultVarLocation

    def _get_rawDeltas(self):
        """Answers the list of axis dictionaries with deltas for all glyphs and
        axes. Answer an empty dictionary if the [gvar] table does not exist.

        >>> from pagebot.fonttoolbox.objects.font import Font
        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> fontPath = getTestFontsPath()
        >>> path = fontPath + '/fontbureau/Amstelvar-Roman-VF.ttf'
        >>> font = Font(path)
        >>> len(font.rawDeltas['A'])
        0
        """
        try:
            return self.ttFont['gvar'].variations
        except:
            return {}
    rawDeltas = property(_get_rawDeltas)

    def _get_designSpace(self):
        """Answers the design space in case this is a variable font.

        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> fontPath = getTestFontsPath()
        >>> path = fontPath + '/fontbureau/Amstelvar-Roman-VF.ttf'
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
        """Answers the gvar-table (if it exists) translated into plain Python
        dictionaries of deltas per glyph and per axis if this is a Var-fonts.
        Otherwise answer an empty dictionary

        """
        """
        TODO We need a "stable" var-font to test on.

        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> font = findFont('Amstelvar-Roman-VF')
        >>> len(font.variables)
        592
        >>> variables = font.variables['H']
        >>> sorted(variables.keys())
        []
        >>> #['GRAD', 'XOPQ', 'XTRA', 'YOPQ', 'YTRA', 'YTSE', 'YTUC', 'opsz', 'wdth', 'wght']
        >>> axis, deltas = variables['GRAD']
        >>> axis
        {'GRAD': (0.0, 1.0, 1.0)}
        >>> deltas[:6]
        [(0, 0), None, (52, 0), None, None, (89, 0)]
        >>> font.variables.get('wrongglyphName') is None
        True
        """
        if self._variables is None:
            try:
                # Get the raw fonttools gvar table if it exists.
                gvar = self.ttFont['gvar']
                self._variables = {}
                for glyphName, tupleVariations in gvar.variations.items():
                    self._variables[glyphName] = axisDeltas = {}
                    for tupleVariation in tupleVariations:
                        #{'GRAD': (0.0, 1.0, 1.0)} Make unique key, in case multiple
                        axisKey = '_'.join(tupleVariation.axes.keys())
                        # ({'GRAD': (0.0, 1.0, 1.0)}, [(0, 0), None, (52, 0), None, None, (89, 0), ...])
                        axisDeltas[axisKey] = tupleVariation.axes, tupleVariation.coordinates
            except KeyError:
                pass # No gvar table, just answer the current self._variables as None.
        return self._variables
    variables = property(_get_variables)

    def getInstance(self, location=None, dstPath=None, opticalSize=None,
            styleName=None, cached=True, lazy=True, kerning=None):
        """Answers the instance of self at location. If the cache file already
        exists, then just answer a Font instance to that font file.

        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> f = findFont('RobotoDelta-VF')
        >>> sorted(f.axes.keys())
        ['GRAD', 'POPS', 'PWDT', 'PWGT', 'UDLN', 'XOPQ', 'XTRA', 'YOPQ', 'YTAD', 'YTAS', 'YTDD', 'YTDE', 'YTLC', 'YTRA', 'YTUC', 'opsz', 'wdth', 'wght']
        >>> f.name
        'RobotoDelta VF'
        >>> len(f)
        188
        >>> f.axes['wght']
        (100.0, 400.0, 900.0)
        >>> g = f['H']
        >>> g
        <Glyph 'H' (Pts:12, Cnt:1, Cmp:0)>
        >>> g.points[6], g.width
        (APoint(1288,1456,On), 1458)
        >>> instance = f.getInstance(location=dict(wght=500))
        >>> instance
        <Font RobotoDelta-VF-wght500>
        >>> ig = instance['H']
        >>> ig
        <Glyph 'H' (Pts:12, Cnt:1, Cmp:0)>
        >>> ig.points[6], ig.width
        (APoint(1307,1456,On), 1477)
        """
        if location is None:
            location = self.getDefaultVarLocation()
        return getInstance(self.path, location=location, dstPath=dstPath, opticalSize=opticalSize,
            styleName=styleName, cached=cached, lazy=lazy, kerning=kerning)

    def _get_cmap(self):
        """Answer the best cmap for this font

        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> fontPath = getTestFontsPath()
        >>> path = fontPath + '/djr/bungee/Bungee-Regular.ttf'
        >>> f = getFont(path, lazy=False)
        >>> cmap = f.cmap
        >>> sorted(cmap.items())[0]
        (32, 'space')
        >>> len(cmap)
        1060
        """
        if self.ttFont is not None:
            return self.ttFont.getBestCmap()
        return None
    cmap = property(_get_cmap)

    def _get_features(self):
        # TODO: Use TTFont for this instead.
        #return context.listOpenTypeFeatures(self.path)
        return {}
    features = property(_get_features)

    def _get_kerning(self):
        """Answers the (expanded) kerning table of the font.

        >>> from pagebot.toolbox.transformer import *
        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> fontPath = getTestFontsPath()
        >>> path = fontPath + '/djr/bungee/Bungee-Regular.ttf'
        >>> f = getFont(path, lazy=False)
        >>> len(f.kerning)
        22827
        >>> f.kerning[('V','a')]
        -10
        """
        if self._kerning is None: # Lazy read.
            self._kerning = OTFKernReader(self.path).kerningPairs
        return self._kerning
    kerning = property(_get_kerning)

    def _get_groups(self):
        """Answers the groups dictionary of the font.

        >>> from pagebot.toolbox.transformer import *
        >>> from pagebot.fonttoolbox.objects.font import Font
        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> fontPath = getTestFontsPath()
        >>> path = fontPath + '/djr/bungee/Bungee-Regular.ttf'
        >>> f = getFont(path, lazy=False)
        >>> g = f['A']
        >>> f.groups is None
        True
        """
        return self._groups
    groups = property(_get_groups)

    def save(self, path=None):
        """Save the font to optional path or to self.path."""
        self.ttFont.save(path or self.path)

    def getAscender(self): # DrawBot compatible
        """Answer the ascender value in em-units from [hhea] table, as use by browser.

        >>> from pagebot.toolbox.transformer import *
        >>> from pagebot.fonttoolbox.objects.font import Font
        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> fontPath = getTestFontsPath()
        >>> path = fontPath + '/djr/bungee/Bungee-Regular.ttf'
        >>> f = getFont(path, lazy=False)
        >>> f.getAscender()
        860
        """
        return self.info.ascender # From self.ttFont['hhea'] table

    ascender = property(getAscender)

    def getDescender(self): # DrawBot compatible
        return self.info.descender # From self.ttFont['hhea'] table

    descender = property(getDescender)

    def getUpem(self): # DrawBot compatible
        return self.info.unitsPerEm

    upem = property(getUpem)

    def getXHeight(self):
        table = self.ttFont['OS/2']
        return getattr(table, 'sxHeight', None)

    xHeight = property(getXHeight)

    def getCapHeight(self):
        table = self.ttFont['OS/2']
        return getattr(table, 'sCapHeight', None)

    capHeight = property(getCapHeight)

    def getItalicAngle(self):
        table = self.ttFont['post']
        return getattr(table, 'italicAngle', None)

    italicAngle = property(getItalicAngle)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
