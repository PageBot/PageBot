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

from pagebot.fonttoolbox.objects.family import Family, getFamily
from pagebot.fonttoolbox.objects.font import Font
from pagebot.toolbox.transformer import path2Name, path2ParentPath

def getVarFamily(name):
    family = getFamily(name)
    if family is not None:
        return VarFamily(name, family.fonts.values)
    return None

class VarFamily(Family):
    u"""A VarFamily is a special kind of family that contains a set of font that potentially form
    the masters to create a VariableFont export. But the collection may not be up for creation yet,
    that is why it is not a "VarFont". There can be a design space file included to define the relation
    between the fontfiles and axes.

    >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
    >>> p = getTestFontsPath() + '/google/roboto/'
    >>> paths = p+'Roboto-Black.ttf', p+'Roboto-Bold.ttf', p+'Roboto-Italic.ttf', p+'Roboto-Light.ttf', p+'Roboto-Medium.ttf', p+'Roboto-Regular.ttf', p+'Roboto-Thin.ttf'
    >>> vf = VarFamily('Test-Var', paths)
    >>> #len(vf)
    7
    >>> #vf.checkInterpolation() # For now only glyph name compatibility check
    {}
    >>> #fontPath = sorted(vf.metrics.keys())[0]
    >>> #vf.metrics[fontPath]['path'] == fontPath
    True
    >>> #vf.metrics[fontPath]['stems'].keys()
    [350]
    >>> #vf.metrics[fontPath]['bars'].keys()
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
    XGRD = 'XGRD' # Grade in x-direction
    YGRD = 'YGRD' # Grade in y-direction
    RNDS = 'RNDS' # Rounded corners and terminals
    STNC = 'STNC' # Stencil
    PARAMETRIC_AXES = [XTRA, XOPQ, YTRA, YTLC, YTUC, YTDE, YTAS, GRAD, RNDS, STNC]

    # Composite (registered) axes
    wght, wdth, opsz, ital, slnt = COMPOSITE_AXES = ['wght', 'wdth', 'opsz', 'ital', 'slnt']

    def __init__(self, name=None, fonts=None):
        u"""Answer a VarFamily instance in the defined list of font paths or fonts list.  """
        Family.__init__(self, name=None, fonts=None)
        self._parametricAxisFonts = {} # Key is parametric axis name
        self._parametricAxisMetrics = {} # Collection of font metrics and calculated parameters.
        self._metrics = None # Initialized on property call
        self._originFont = None
        # Add the fonts. Also initialize self.originFont
        self.baseGlyphName = self.BASE_GLYPH_NAME

    def _get_originFont(self):
        u"""Answer the cashed font that is defined as origin. Try to guess if not defined."""
        if not self._originFont:
            originFonts = self.getClosestOS2Weight(self.ORIGIN_OS2_WEIGHT_CLASS)
            if originFonts:
                self._originFont = originFonts[0] # Should be sorted by name or parameteric XOPQ
                self._originFont.info.widthClass = 5
                self._originFont.info.weightClass = 400
        return self._originFont
    def _set_originFont(self, font):
        self._originFont = font
    originFont = property(_get_originFont, _set_originFont)

    def _get_parametricAxisFonts(self):
        u"""Generate the dictionary with parametric axis fonts. Key is the parametric axis name,
        value is the font instance (there can only be one font per axis). If the fonts don't
        exist as cached files, they are created. The font currently under self.originFont is
        used a neutral, for which all delta's are 0."""
        origin = self.originFont
        if origin is None:
            return None

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

    def addFont(self, pathOrFont, install=True):
        self._originFont = None # Reset to force new initialization of the property.
        Family.addFont(self, pathOrFont)

    def _get_metrics(self):
        u"""Answer the metrics dictionary for the current included fonts.

        """
        self._metrics = {}
        for path, font in self.fonts.items():
            fa = font.analyzer
            self._metrics[path] = dict(path=path, stems=fa.stems, bars=fa.bars)
        return self._metrics
    metrics = property(_get_metrics)

    def getClosestOS2Weight(self, weightClass=ORIGIN_OS2_WEIGHT_CLASS):
        u"""Answer the list of fonts (there can be more that one, accidentally located at that position.
        Default is the origin at weightClass == ORIGIN_OS2_WEIGHT_CLASS (400).
        Answer None if no matching font could be found."""
        os2Weights = {}
        for font in self.fonts.values():
            diff = abs(weightClass - font.info.weightClass)
            if not diff in os2Weights:
                os2Weights[diff] = []
            os2Weights[diff].append(font)
        if not os2Weights:
            return None # Could not find one.
        return os2Weights[min(os2Weights.keys())] # Answer the set of fonts with the smallest difference.

    def getOS2WeightWidthClasses(self):
        u"""Answer the (x, y) dictionary, with (OS/2 weight class, OS/2 width class) as key and fonts list as value
        (as often there are be multiple fonts on the same (x, y) if not filled with the right OS/2 value."""
        weightWidthClasses = {}
        for font in self.fonts.values():
            weightWidth = font.info.weightClass, font.info.widthClass
            if weightWidth not in weightWidthClasses:
                weightWidthClasses[weightWidth] = []
            weightWidthClasses[weightWidth].append(font)
        return weightWidthClasses

    def getWeightWidthLocations(self):
        u"""Answer the (x, y) dictionary, with (H-stem width, H-width) as key and fonts list as value
        (theoretically there can be multiple fonts on the same (x, y)."""
        weightWidthLocations = {}
        for font in self.fonts.values():
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
        minWidth = sys.maxsize
        maxWidth = -minWidth
        for font in self._fonts.values():
            g = font[self.baseGlyphName].width or 0
            minWidth = min(g.width, minWidth)
            maxWidth = max(g.width, maxWidth)
        return minWidth, maxWidth

    def getMinMaxStem(self):
        u"""Answer the minimal/max stems of H."""
        minStem = sys.maxsize
        maxStem = -minStem
        for metrics in self.metrics.values():
            minStem = min(min(metrics['stems'].keys()), minStem)
            maxStem = max(max(metrics['stems'].keys()), maxStem)
        return minStem, maxStem

    #   C O N S T R U C T  P A R A M E T R I C  F O N T S

    def makeParametricFonts(self, axisName):
        u"""Answer the two Font instances for calculated parametric Min and Max."""
        parametricAxisFonts = self.parametricAxisFonts
        if parametricAxisFonts is None:
            return None
        axisFontMin, axisFontMax = parametricAxisFonts[axisName]
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

    #   I N T E R P O L A T I O N

    def checkInterpolation(self, fontFilter=None):
        u"""This method will test if there are problems for the current set of fonts to be interpolated,
        regarding the special specs of VarFonts.
        Answer resulting dictionary with format dict(A=dict(ok=[path1,...], error=[path2,...], report=[]), ...)
        """

        """
        TODO: Get some interpolating examples in the test fonts folder.
        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> path = '/Users/petr/Desktop/TYPETR-git/TYPETR-Proforma/master_ttf_interpolatable'
        >>> vf = VarFamily('Test-Var')
        >>> vf.addFonts(path)
        >>> vf.checkInterpolation() # For now only glyph name compatibility check
        The font has no kern feature.
        The fun ends here.
        {}
        """
        if fontFilter is None:
            fontFilter = []
        elif isinstance(fontFilter, str):
            fontFilter = [fontFilter]
        errors = {} # Total collection of (font.path-->glyphName) that do not interpolate.

        # Get reference regular to compare with.
        refFont = self.findRegularFont()

        # Collect all unique glyph names to look at, as the total set of all fonts.
        glyphNames = set()
        path2Fonts = {}
        for font in self.fonts.values():
            fontName = path2Name(font.path)
            match = True
            for filterPart in fontFilter:
                if not filterPart in fontName:
                    match = False
                    break
            if match:
                glyphNames = glyphNames.union(set(font.keys()))
                path2Fonts[font.path] = font # So we can make a sorted list of paths

        # Now we have the total set of all glyph names in all fonts.
        '''
        for glyphName in glyphNames:
            # Check compatibility of outlines
            report = self.checkOutlineCompatibility(refFont, font, glyphName)
            if report: # Error with this glyph?
                errors[(font.path, glyphName)] = report
        '''
        # Check group compatibility
        '''
        report = self.checkKerningCompatibility(font)
        if report:
            errors[(font.path, 'KERNING')] = report
        '''
        return errors

    def checkOutlineCompatibility(self, refFont, font, glyphName):

        report = []

        if refFont is None or not glyphName in refFont:
            report.append('Glyph "%s" not in reference master "%s"' % (glyphName, path2Name(refFont.path)))

        if font is None or not glyphName in font:
            report.append('Glyph "%s" not in master "%s"' % (glyphName, path2Name(font.path)))

        if report: # Errors here already, then they are fatal. No need for firther checking.
            return report

        rg = refFont[glyphName]
        g = font[glyphName]

        # Compare number of contours
        if len(g) > len(rg):
            report.append(u'Glyph "%s" has more contours (%d) in "%s" than in "%s" (%d).' % (glyphName, len(g), refFont.info.styleName, font.info.styleName, len(rg)))
        elif len(g) < len(rg):
            report.append(u'Glyph "%s" has fewer contours (%d) in "%s" than in "%s" (%d).' % (glyphName, len(g), refFont.info.styleName, font.info.styleName, len(rg)))
        else: # Same amount of contours, we can compare them.
            for cIndex, contour in enumerate(g.contours):
                rContour = rg.contours[cIndex]
                if len(contour) > len(rContour):
                    report.append(u'Glyph "%s" contour #%d has more points (%d) than “%s” (%d).' % (glyphName, cIndex, len(contour), refFont.info.styleName, len(rContour)))
                elif len(contour) < len(rContour):
                    report.append(u'Glyph "%s" contour #%d has fewer points (%d) than “%s” (%d).' % (glyphName, cIndex, len(contour), refFont.info.styleName, len(rContour)))
                else: # Contour lengths are equal, now we can test on point types.
                    # Test on contour clockwise directions.
                    if g.isClockwise(contour) != rg.isClockwise(rContour):
                        report.append(u'Glyph "%s" contour #%d has reversed direction of “%s”.' % (glyphName, cIndex, refFont.info.styleName))
                    else: # Now the length and directions are the same, we can test on the type of points.
                        pIndex = 0
                        for p in contour:
                            if p.onCurve != rContour[pIndex].onCurve:
                                report.append(u'"%s" Glyph "%s" point #%d (%d,%d,%s) is not same type as point #%d (%d,%d,%s) in “%s”.' % (font.info.styleName, glyphName, pIndex,
                                    p.x, p.y, p.onCurve, pIndex, rContour[pIndex].x, rContour[pIndex].y, rContour[pIndex].onCurve,
                                    refFont.info.styleName))
                            pIndex += 1

        components = g.components
        rComponents = rg.components

        if len(components) > len(rComponents):
            baseGlyphs = []
            for component in components:
                baseName = component.baseGlyph
                if not baseName in font:
                    baseName += self.DOES_NOT_EXIST
                baseGlyphs.append(baseName)
            rBaseGlyphs = []
            for component in rComponents:
                baseName = component.baseGlyph
                if not baseName in refFont:
                    baseName += self.DOES_NOT_EXIST
                rBaseGlyphs.append(baseName)
            report.append(u'Glyph "%s" has %d more components (%s) than %s (%s) in "%s".' % (glyphName, len(baseGlyphs) - len(rBaseGlyphs), ','.join(baseGlyphs), refFont.info.styleName, ','.join(rBaseGlyphs), refFont.info.styleName))
        elif len(components) < len(rComponents):
            baseGlyphs = []
            for component in components:
                baseName = component.baseGlyph
                if not baseName in font:
                    baseName += self.DOES_NOT_EXIST
                baseGlyphs.append(baseName)
            rBaseGlyphs = []
            for component in rComponents:
                baseName = component.baseGlyph
                if not baseName in refFont:
                    baseName += self.DOES_NOT_EXIST
                rBaseGlyphs.append(baseName)
            report.append(u'Glyph "%s" has %d fewer components (%d) than %s (%s) in "%s".' % (glyphName, len(rBaseGlyphs) - len(baseGlyphs), len(components), refFont.info.styleName, len(rComponents), refFont.info.styleName))
        return report

    def checkKerningCompatibility(self, font):
        u"""Check if all kerning glyphs exist in the font."""
        report = []
        glyphNames = set(font.keys())
        for c1, c2 in font.kerning.keys():
            if not c1 in font:
                report.append(u'Left kerning glyph "%s" does not exist in font "%s".' % (c1, font.info.styleName))
            if not c2 in font:
                report.append(u'Right kerning glyph "%s" does not exist in font "%s".' % (c2, font.info.styleName))
        return report

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
