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
#     varfamily.py
#
#     Implements a VarFamily class Font instances.
#
import os, shutil, sys

from pagebot.fonttoolbox.objects.family import Family
from pagebot.fonttoolbox.objects.font import Font
from pagebot.toolbox.transformer import path2Name, path2ParentPath

def checkInterpolation(fonts):
    u"""This method will test if there are problems for the current set of fonts to be interpolated,
    regarding the special specs of VarFonts.
    Answer resulting dictionary with format dict(A=dict(ok=[path1,...], error=[path2,...], report=[]), ...)"""
    glyphs = {} # Total collection of (font.glyphName) that do or do not interpolate.
    glyphNames = set()
    # Collect all unique glyph names to look at, as the total set of all fonts.
    pathFonts = {}
    for font in fonts:
        glyphNames = glyphNames.union(set(font.keys()))
        pathFonts[font.path] = font # So we can make a sorted list.
        
    for glyphName in glyphNames:
        ok = []
        error = []
        report = []
        # Check for interpolation compatibility for this glyph in all fonts.
        for path, font in sorted(pathFonts.items()):
            if not glyphName in font:
                error.append(font.path)
                report.append('Glyph "%s" does not exist in font "%s"' % (glyphName, font))
                continue
            g = font[glyphName]
        # TODO: Needs checking of outline and component compatibility here.
        if ok or error or report: # Error with this glyph?
            glyphs[glyphName] = dict(ok=ok, error=error, report=report)
            
    return glyphs

class VarFamily(Family):
    u"""A VarFamily is a special kind of family that contains a set of font that potentially form 
    the masters to create a VariableFont export. But the collection may not be up for creation yet, 
    that is why it is not a "VarFont". There can be a design space file included to define the relation 
    between the fontfiles and axes.

    >>> from pagebot.contexts.platform import getRootFontPath
    >>> p = getRootFontPath() + '/google/roboto/'
    >>> paths = p+'Roboto-Black.ttf', p+'Roboto-Bold.ttf', p+'Roboto-Italic.ttf', p+'Roboto-Light.ttf', p+'Roboto-Medium.ttf', p+'Roboto-Regular.ttf', p+'Roboto-Thin.ttf'
    >>> vf = VarFamily('Test-Var', paths)
    >>> len(vf)
    7
    >>> checkInterpolation(vf.fonts.values()) # For now only glyph name compatibility check
    {}
    >>> fontPath = sorted(vf.metrics.keys())[0]
    >>> vf.metrics[fontPath]['path'] == fontPath
    True
    >>> vf.metrics[fontPath]['stems'].keys()
    [350]
    >>> vf.metrics[fontPath]['bars'].keys()
    [270]

    """
    BASE_GLYPH_NAME = 'H' # Use for base metrics analysis
    
    ORIGIN_OS2_WEIGHT_CLASS = 400
    # The quality of automatic parametric axis creation depends on the type of design and if
    # there are interpolating sources (e.g. for compensation of stem width in 'xtra' and 'xopq'.
    # Currently supporting these (automatic) parametric axes, if they can be derived from the 
    # available source fonts.
    XTRA = 'XTRA' # Fixed H-stems, variable H-counter, variable margins
    XOPQ = 'XOPQ' # Variable H-stems, fixed H-counter, variable margins
    YTRA = 'YTRA' # Fixed bar heights, variable 
    #YOPQ = 'yopq' 
    YTLC = 'YTLC' # Varialbe lower case
    YTUC = 'YTUC' # Variable capHeight
    YTDE = 'YTDE' # Variable descenders
    YTAS = 'YTAS' # Variable ascenders
    GRAD = 'GRAD' # Grades
    RNDS = 'RNDS' # Rounded corners and terminals
    STNC = 'STNC' # Stencil
    PARAMETRIC_AXES = [XTRA, XOPQ, YTRA, YTLC, YTUC, YTDE, YTAS, GRAD, RNDS, STNC]

    # Composite (registered) axes
    wght, wdth, opsz, ital, slnt = COMPOSITE_AXES = ['wght', 'wdth', 'opsz', 'ital', 'slnt']

    def __init__(self, name, pathsOrFonts=None):
        self.name = name
        self._fonts = {} # Key is font.path
        self._parametricAxisFonts = {} # Key is parametric axis name
        self._parametricAxisMetrics = {} # Collection of font metrics and calculated parameters.
        self._metrics = None # Initialized on property call
        # Add the fonts. Also initialize self._originFont
        for pathOrFont in pathsOrFonts or []:
            self.addFont(pathOrFont)
        self.baseGlyphName = self.BASE_GLYPH_NAME

    def __len__(self):
        return len(self._fonts)
        
    def __getitem__(self, path):
        return self._fonts[path]
 
    def keys(self):
        return self._fonts.keys()

    def _get_fonts(self):
        return self._fonts
    fonts = property(_get_fonts)
    
    def _get_originFont(self):
        u"""Answer the cashed font that is defined as origin. Try to guess if not defined."""
        if not self._originFont:
            originFonts = self.getClosestOS2Weight(self.ORIGIN_OS2_WEIGHT_CLASS)
            if originFonts:
                self._originFont = originFonts[0] # Should be sorted by name or parameteric XOPQ
                self._originFont.info.widthClass = 5
                self._originFont.info.weightClass = 400
        return self._originFont
    originFont = property(_get_originFont)
    
    def _get_parametricAxisFonts(self):
        u"""Generate the dictionary with parametric axis fonts. Key is the parametric axis name,
        value is the font instance (there can only be one font per axis). If the fonts don't
        exist as cached files, they are created. The font currently under self.originFont is 
        used a neutral, for which all delta's are 0."""
        origin = self.originFont
        
        # Create directory for the parametric axis fonts, if it does not exist.
        paFontDir = path2ParentPath(origin.path) + '/@axes'
        if not os.path.exists(paFontDir):
            os.makedirs(paFontPath)
        for axisName in self.PARAMETRIC_AXES:
            self._parametricAxisFonts[axisName] = []
            for extreme in ('_min', '_max'):
                fileNameParts = path2Name(origin.path).split('.')
                paFontPath = paFontDir + '/' + '.'.join(fileNameParts[:-1]) + '@' + axisName + extreme + '.' + fileNameParts[-1]
                if os.path.exists(paFontPath):
                    os.remove(paFontPath)
                shutil.copy(origin.path, paFontPath)
                self._parametricAxisFonts[axisName].append(Font(paFontPath))
            self._parametricAxisMetrics[axisName] = origin.analyzer.stems
        return self._parametricAxisFonts
    parametricAxisFonts = property(_get_parametricAxisFonts)
    
    def _get_parametricAxisMetrics(self):
        u"""The parametric axis metrcs is a compilation of all measures and calculation of
        values, required to generate the parameteric axis fonts."""
        if self._parametricAxisMetrics is None:
            self._parametricAxisMetrics = {}
        return self._parametricAxisMetrics
    parametricAxisMetrics = property(_get_parametricAxisMetrics)
           
    def addFont(self, pathOrFont):
        self._originFont = None # Reset to force new initialization of the property.
        if isinstance(pathOrFont, basestring): # If it is a path, then open a new Font instance.
            self._fonts[pathOrFont] = Font(pathOrFont)
        else: # Otherwise we assume it is a font, just add it to the dictionary.
            self._fonts[pathOrFont.path] = pathOrFont

    def _get_metrics(self):
        self._metrics = {}
        for path, font in self._fonts.items():
            fa = font.analyzer
            self._metrics[path] = dict(path=path, stems=fa.stems, bars=fa.bars)
        return self._metrics
    metrics = property(_get_metrics)
    
    def getClosestOS2Weight(self, weightClass=ORIGIN_OS2_WEIGHT_CLASS):
        u"""Answer the list of fonts (there can be more that one, accidentally located at that position.
        Default is the origin at weightClass == ORIGIN_OS2_WEIGHT_CLASS (400)."""
        os2Weights = {}
        for font in self._fonts.values():
            diff = abs(weightClass - font.info.weightClass)
            if not diff in os2Weights:
                os2Weights[diff] = []
            os2Weights[diff].append(font)
        return os2Weights[min(os2Weights.keys())] # Answer the set of fonts with the smallest difference.
        
    def getOS2WeightWidthClasses(self):
        u"""Answer the (x, y) dictionary, with (OS/2 weight class, OS/2 width class) as key and fonts list as value
        (as often there are be multiple fonts on the same (x, y) if not filled with the right OS/2 value."""
        weightWidthClasses = {}
        for font in self._fonts.values():
            weightWidth = font.info.weightClass, font.info.widthClass
            if weightWidth not in weightWidthClasses:
                weightWidthClasses[weightWidth] = []
            weightWidthClasses[weightWidth].append(font)
        return weightWidthClasses

    def getWeightWidthLocations(self):
        u"""Answer the (x, y) dictionary, with (H-stem width, H-width) as key and fonts list as value
        (theoretically there can be multiple fonts on the same (x, y)."""
        weightWidthLocations = {}
        for font in self._fonts.values():
            stemValues = font.analyzer.stems.keys()
            if not stemValues:
                continue
            stem = min(stemValues)
            width = font[self.baseGlyphName].width
            location = stem, width
            if location not in weightWidthLocations:
                weightWidthLocations[location] = []
            weightWidthLocations[location].append(font)
        return weightWidthLocations
            
    def getMinMaxWidth(self):
        u"""Answer the minimal/max widths of H."""
        minWidth = sys.maxint
        maxWidth = -minWidth
        for font in self._fonts.values():
            g = font[self.baseGlyphName].width or 0
            minWidth = min(g.width, minWidth)
            maxWidth = max(g.width, maxWidth)
        return minWidth, maxWidth    

    def getMinMaxStem(self):
        u"""Answer the minimal/max stems of H."""
        minStem = sys.maxint
        maxStem = -minStem
        for metrics in self.metrics.values():
            minStem = min(min(metrics['stems'].keys()), minStem)
            maxStem = max(max(metrics['stems'].keys()), maxStem)
        return minStem, maxStem    

    #   C O N S T R U C T  P A R A M E T R I C  F O N T S
    
    def makeParametricFonts(self, axisName):
        u"""Answer the two Font instances for calculated parametric Min and Max."""
        axisFontMin, axisFontMax = self.parametricAxisFonts[axisName]
        hook = 'makeParametricFont_'+axisName
        assert hasattr(self, hook)
        return getattr(self, hook)(axisFontMin, axisFontMax)

    def makeParametricFont_xtra(self, axisFontMin, axisFontMax):
        u"""Adjust the font outlines and other metrics to the guesse min/max, starting with self.originFont."""
        Hg = self.originFont[self.baseGlyphName]
        counters = Hg.analyzer.horizontalCounters
        stems = Hg.analyzer.stems
        axisFontMin.info.widthClass = 1
        axisFontMax.info.widthClass = 9
        return axisFontMin, axisFontMax

if __name__ == '__main__':
    import doctest
    doctest.testmod()


