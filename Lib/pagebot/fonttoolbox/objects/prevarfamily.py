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
#     prevarfamily.py
#
#     Implements a VarFamily class Font instances.
#
import os, shutil, sys
from fontTools.designspaceLib import DesignSpaceDocument
from pagebot.fonttoolbox.objects.family import Family
from pagebot.fonttoolbox.objects.font import Font
from pagebot.toolbox.transformer import path2Name, path2ParentPath

ERROR_MISSING_GLYPH = 'MissingGlyph'

class PreVarFamily(Family):
    """A PreVarFamily is a special kind of family that contains a set of font
    that potentially form the masters to create a VariableFont export. But the
    collection may not be up for creation yet, that is why it is not a
    "VarFont". The PreVarFamily is created from an existing design space file
    the defines the relation between fontfiles and axes.

    >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
    >>> path = getTestFontsPath() + '/google/roboto/Roboto.ttf.designspace'
    >>> pvf = PreVarFamily('Roboto', path)
    >>> sorted(pvf.axes.keys())
    ['slnt', 'wdth', 'wght']
    >>> len(pvf.designSpace.sources) == len(pvf.fonts) == 18
    True
    """
    BASE_GLYPH_NAME = 'H' # Use for base metrics analysis

    ORIGIN_OS2_WEIGHT_CLASS = 400

    # The quality of automatic parametric axis creation depends on the type of
    # design and if there are interpolating sources (e.g. for compensation of
    # stem width in 'XTRA' and 'XOPQ'.  Currently supporting these (automatic)
    # parametric axes, if they can be derived from the available source fonts.
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
    CATL = 'CATL' # Catalog of compatubke designs

    PARAMETRIC_AXES = [CATL, XTRA, XOPQ, YTRA, YTLC, YTUC, YTDE, YTAS, GRAD, RNDS, STNC]

    # Composite (registered) axes
    wght, wdth, opsz, ital, slnt = COMPOSITE_AXES = ['wght', 'wdth', 'opsz', 'ital', 'slnt']

    def __init__(self, name, path):
        """Answers a PreVarFamily instance from the defined design space path."""
        self.designSpace = ds = DesignSpaceDocument()
        ds.read(path)
        self.axes = {}

        for axis in self.designSpace.axes:
            self.axes[axis.tag] = axis

        fonts = {}

        for source in ds.sources:
            fonts[source.path] = Font(source.path)

        #print(fonts)

        Family.__init__(self, name=name, fonts=fonts)
        self._parametricAxisFonts = {} # Key is parametric axis name
        self._parametricAxisMetrics = {} # Collection of font metrics and calculated parameters.
        self._metrics = None # Initialized on property call
        self._defaultFont = None # Initialized on property call
        self._glyphNames = None # Set of all unique glyph names in all design space fonts
        self.baseGlyphName = self.BASE_GLYPH_NAME

    def _get_glyphNames(self):
        """Answers the set of all unique glyph names in all design space fonts.
        Initialize if it does not exist yet.

        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> path = getTestFontsPath() + '/google/roboto/Roboto.ttf.designspace'
        >>> pvf = PreVarFamily('Roboto', path)
        >>> 'A' in pvf.glyphNames
        True
        >>> len(pvf.glyphNames)
        3387
        """
        if self._glyphNames is None:
        # Collect all unique glyph names to look at, as the total set of all fonts in the design space.
            self._glyphNames = set()
            for font in self.fonts.values():
                self._glyphNames = self._glyphNames.union(set(font.keys()))
        return self._glyphNames
    glyphNames = property(_get_glyphNames)

    def _get_defaultFont(self):
        """Answers the cached font that is defined as origin. Try to guess if
        not defined.

        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> path = getTestFontsPath() + '/google/roboto/Roboto.ttf.designspace' # On TTF files
        >>> pvf = PreVarFamily('Roboto', path)
        >>> pvf.defaultFont
        <Font Roboto-Regular>
        """
        if not self._defaultFont:
            self._defaultFont = self.getDefaultFont()
            if not self._defaultFont:
                defaultFonts = self.getClosestOS2Weight(self.ORIGIN_OS2_WEIGHT_CLASS)
                if defaultFonts:
                    self._defaultFont = defaultFonts[0] # Should be sorted by name or parameteric XOPQ
                    self._defaultFont.info.widthClass = 5
                    self._defaultFont.info.weightClass = 400
        return self._defaultFont
    def _set_defaultFont(self, font):
        self._defaultFont = font
    defaultFont = property(_get_defaultFont, _set_defaultFont)

    def _get_parametricAxisFonts(self):
        """Generate the dictionary with parametric axis fonts. Key is the
        parametric axis name, value is the font instance (there can only be one
        font per axis). If the fonts don't exist as cached files, they are
        created. The font currently under self.defaultFont is used a neutral,
        for which all delta's are 0."""
        origin = self.defaultFont
        if origin is None:
            return None

        # Create directory for the parametric axis fonts, if it does not exist.
        paFontDir = path2ParentPath(origin.path) + '/_export/@axes'
        if not os.path.exists(paFontDir):
            os.makedirs(paFontDir)
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
        """The parametric axis metrics is a compilation of all measures and
        calculation of values, required to generate the parameteric axis
        fonts."""
        if self._parametricAxisMetrics is None:
            self._parametricAxisMetrics = {}
        return self._parametricAxisMetrics
    parametricAxisMetrics = property(_get_parametricAxisMetrics)

    def addFont(self, pathOrFont, install=True):
        self._defaultFont = None # Reset to force new initialization of the property.
        Family.addFont(self, pathOrFont)

    def _get_metrics(self):
        """Answers the metrics dictionary for the current included fonts.

        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> path = getTestFontsPath() + '/google/roboto/Roboto.ttf.designspace'
        >>> pvf = PreVarFamily('Roboto', path)
        >>> #len(pvf.metrics) # TODO: Testing
        18
        >>> #metrics = pvf.metrics[pvf.defaultFont.path]
        >>> #metrics['stems'].keys()[0]
        193
        """
        self._metrics = {}
        for path, font in self.fonts.items():
            fa = font.analyzer
            self._metrics[path] = dict(path=path, stems=fa.stems, bars=fa.bars)
        return self._metrics
    metrics = property(_get_metrics)

    def getDefaultFont(self):
        """Answers the font that is on the design space location with all axes
        as default.

        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> path = getTestFontsPath() + '/google/roboto/Roboto.ttf.designspace'
        >>> pvf = PreVarFamily('Roboto', path)
        >>> pvf.getDefaultFont()
        <Font Roboto-Regular>
        """
        if self.designSpace.default is None: # Not yet initialized
            self.designSpace.checkDefault()
        path = self.designSpace.default.path
        return self.fonts.get(path)

    def getClosestOS2Weight(self, weightClass=ORIGIN_OS2_WEIGHT_CLASS):
        """Answers the list of fonts (there can be more that one, accidentally
        located at that position. Default is the origin at weightClass ==
        ORIGIN_OS2_WEIGHT_CLASS (400). Answer None if no matching font could
        be found."""
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
        """Answers the (x, y) dictionary, with (OS/2 weight class, OS/2 width
        class) as key and fonts list as value (as often there are be multiple
        fonts on the same (x, y) if not filled with the right OS/2 value."""
        weightWidthClasses = {}
        for font in self.fonts.values():
            weightWidth = font.info.weightClass, font.info.widthClass
            if weightWidth not in weightWidthClasses:
                weightWidthClasses[weightWidth] = []
            weightWidthClasses[weightWidth].append(font)
        return weightWidthClasses

    def getWeightWidthLocations(self):
        """Answers the (x, y) dictionary, with (H-stem width, H-width) as key
        and fonts list as value (theoretically there can be multiple fonts on
        the same (x, y)."""
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
        """Answers the minimal/maximal widths of H.

        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> path = getTestFontsPath() + '/google/roboto/Roboto.ttf.designspace'
        >>> pvf = PreVarFamily('Roboto', path)
        >>> pvf.getMinMaxWidth()
        (1219, 1461)
        """
        minWidth = sys.maxsize
        maxWidth = -minWidth
        for font in self.fonts.values():
            width = font[self.baseGlyphName].width or 0
            minWidth = min(width, minWidth)
            maxWidth = max(width, maxWidth)
        return minWidth, maxWidth

    def getMinMaxStem(self):
        """Answers the minimal/max stems of H.

        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> path = getTestFontsPath() + '/google/roboto/Roboto.ttf.designspace'
        >>> pvf = PreVarFamily('Roboto', path)
        >>> #pvf.getMinMaxStem()
        (54, 350)
        """
        minStem = sys.maxsize
        maxStem = -minStem
        for metrics in self.metrics.values():
            minStem = min(min(metrics['stems'].keys()), minStem)
            maxStem = max(max(metrics['stems'].keys()), maxStem)
        return minStem, maxStem

    #   C O N S T R U C T  P A R A M E T R I C  F O N T S

    def makeParametricFonts(self, axisName):
        """Answers the two Font instances for calculated parametric Min and Max.
        If one of the extreme is equal to the origin, then answer None for that
        instance."""
        parametricAxisFonts = self.parametricAxisFonts
        if parametricAxisFonts is None:
            return None, None
        axisFontMin, axisFontMax = parametricAxisFonts[axisName]
        hook = 'makeParametricFont_'+axisName
        assert hasattr(self, hook), ('VarFamily.makeParametricFonts "%s" not implemented' % hook)
        return getattr(self, hook)(axisFontMin, axisFontMax)

    def makeParametricFont_XTRA(self, axisFontMin, axisFontMax):
        """Adjust the font outlines and other metrics to the guess min/max,
        starting with self.defaultFont."""
        Hg = self.defaultFont[self.baseGlyphName]
        counters = Hg.analyzer.horizontalCounters
        stems = Hg.analyzer.stems
        axisFontMin.info.widthClass = 1
        axisFontMax.info.widthClass = 9
        return axisFontMin, axisFontMax

    #   I N T E R P O L A T I O N

    def checkInterpolation(self):
        """This method will test if there are interpolation problems for the
        fonts in the design space. The comparing is done against the default
        font (therefore not included in the error messages) Answer resulting
        dictionary with Error instances, showing the type of error.

        dict(
            A=dict(
                ok=[fontPath1, ...],
                error=[fontPath2, ...],
                report=[]
            ),
            ...
        )

        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> path = getTestFontsPath() + '/google/roboto/Roboto.ttf.designspace'
        >>> pvf = PreVarFamily('Roboto', path)
        >>> pvf.checkInterpolation() # For now only glyph name compatibility check
        {}
        >>> pvf.glyphNames.add('BadGlyph') # Insert error in total set of glyphNames
        >>> len(pvf.checkInterpolation()['BadGlyph'][ERROR_MISSING_GLYPH])
        18
        """
        errors = {} # Total collection of (font.path-->glyphName) that do not interpolate.

        # Test compatibility of the total set of all glyph names in the design space.
        for glyphName in self.glyphNames: # Get glyphs names of all fonts combined
            for font in self.fonts.values():
                if not glyphName in font:
                    if not glyphName in errors:
                        errors[glyphName] = {}
                    if not ERROR_MISSING_GLYPH in errors[glyphName]:
                        errors[glyphName][ERROR_MISSING_GLYPH] = []
                    errors[glyphName][ERROR_MISSING_GLYPH].append(font.path)

        # Get reference regular to compare with.
        refFont = self.defaultFont

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
        """Check if all kerning glyphs exist in the font."""
        report = []
        glyphNames = set(font.keys())
        for c1, c2 in font.kerning.keys():
            if not c1 in font:
                report.append(u'Left kerning glyph "%s" does not exist in font "%s".' % (c1, font.info.styleName))
            if not c2 in font:
                report.append(u'Right kerning glyph "%s" does not exist in font "%s".' % (c2, font.info.styleName))
        return report

if __name__ == '__main__':
    from pagebot.fonttoolbox.fontpaths import getTestFontsPath
    path = getTestFontsPath() + '/google/roboto/Roboto.ttf.designspace'
    pvf = PreVarFamily('Roboto', path)
    #import doctest
    #import sys
    #sys.exit(doctest.testmod()[0])
