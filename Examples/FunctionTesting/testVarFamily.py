# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     testVarFamily6.py
#
#     TODO: Started using context for drawing.
#     TODO: Not done for all drawing functions yet.
#
#     https://www.typenetwork.com/brochure/opentype-font-variations/
#     https://variationsguide.typenetwork.com/#xopq
#    "wght" 134, "wdth" 369, "opsz" 36, “GRAD” 88 , ”XOPQ" 88, "XTRA" 402, "YOPQ" 50, "YTLC" 500, "YTSE" 18;
#
#     STAT table
#     https://www.microsoft.com/typography/otspec/stat.htm

import os, sys, shutil

from pagebot.contexts import defaultContext as c
from pagebot.fonttoolbox.objects.font import Font
from pagebot.fonttoolbox.objects.family import Family
from pagebot.fonttoolbox.analyzers.glyphanalyzer import GlyphAnalyzer
from pagebot.fonttoolbox.analyzers.stems import Stem, Bar, BlueBar, Counter, VerticalCounter, Width, DiagonalStem
from pagebot.toolbox.transformer import asInt, path2Name, path2ParentPath

SHOW_COORDINATES = True

ORIGIN_OS2_WEIGHT_CLASS = 400

GLYPH = 'H'

#EXPORT_PATH = '_export/FontBureauFamilies.pdf'
#BASE_PATH = u"/FontDevelopment/Fontbureau/TN-admin-2017-10-10T05_34_28.861995/"

EXPORT_PATH = '_export/TYPETR-Upgrade.pdf'
BASE_PATH = u"/Users/petr/Desktop/TYPETR-git/TYPETR-Upgrade/scripts/export/"
    
#EXPORT_PATH = '_export/GoogleFontFamilies.pdf'
#BASE_PATH = u"/Users/petr/Desktop/git/fonts/ofl/"

#EXPORT_PATH = '_export/WindowsFamilies.pdf'
#BASE_PATH = u"/FontDevelopment/Microsoft/MSFonts/"

# Old data
#EXPORT_GIF = '_export/FontBureauFamilies.gif'
#BASE_PATH = '/FontDevelopment/TypeNetwork/WebType-Raw/WT-TTF/'

def findFontPaths(basePath, paths=None):
    u"""Answer the recursive list of TTF non-Italic font paths that are in directory basePath."""
    if paths is None:
        paths = []
    for fileName in os.listdir(basePath):
        if fileName.startswith('.'):
            continue
        if 'Ital' in fileName or 'Oblique' in fileName:
            continue
        if fileName.split('.')[-1] != 'ttf': # PageBot only does TTF so far.
            continue
        filePath = basePath + '/' + fileName
        if os.path.isdir(filePath):
            findFontPaths(filePath, paths)
            continue
        paths.append(filePath)
    return paths

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
        glyphs[glyphName] = dict(ok=ok, error=error, report=report)
        # Check for interpolation compatibility for this glyph in all fonts.
        for path, font in sorted(pathFonts.items()):
            if not glyphName in font:
                error.append(font.path)
                report.append('Glyph "%s" does not exist in font "%s"' % (glyphName, font))
                continue
            g = font[glyphName]
            
    return glyphs
 
def guessVarFamilyFromPaths(basePath, name=None):
    u"""Initialize by guessing the self._font axis locations. 
    """
    paths = findFontPaths(basePath)    
    name = name or path2Name(basePath)
    return VarFamily(name, paths)

class VarFamily(Family):
    u"""A VarFamily contains a set of font paths that potentially form that masters to create a 
    VariableFont export. But the collection may not be up for creation yet, that is why it is not
    a "VarFont".
    """
    # The quality of automatic parametric axis creation depends on the type of design and if
    # there are interpolating sources (e.g. for compensation of stem width in 'xtra' and 'xopq'.
    # Currently supporting these (automatic) parametric axes, if they can be derived from the 
    # available source fonts.
    XTRA = 'xtra' # Fixed H-stems, variable H-counter, variable margins
    XOPQ = 'xopq' # Variable H-stems, fixed H-counter, variable margins
    XTRK = 'xtrk' # Variable H-stems, variable H-counter, fixed margins
    YTRA = 'ytra' # 
    YOPQ = 'yopq'
    YLTC = 'yltc'
    YTUC = 'ytuc'
    YTDE = 'ytde'
    YTAS = 'ytas'
    PARAMETRIC_AXES = [XTRA, XOPQ, YTRA, YOPQ, YLTC, YTUC, YTDE, YTAS]
    
    def __init__(self, name, pathsOrFonts=None):
        self.name = name
        self._fonts = {} # Key is font.path
        self._parametricAxisFonts = {} # Key is parametric axis name
        self._parametricAxisMetrics = {} # Collection of font metrics and calculated parameters.
        self._metrics = None # Initialized on property call
        # Add the fonts. Also initialize self._originFont
        for pathOrFont in pathsOrFonts or []:
            self.addFont(pathOrFont)
            
    def __len__(self):
        return len(self._fonts)
        
    def __getitem__(self, path):
        return self._fonts[path]
 
    def _get_fonts(self):
        return self._fonts.values()
    fonts = property(_get_fonts)
    
    def _get_originFont(self):
        u"""Answer the cashed font that is defined as origin. Try to guess if not defined."""
        if not self._originFont:
            originFonts = self.getClosestOS2Weight(ORIGIN_OS2_WEIGHT_CLASS)
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
            if not weightWidth in weightWidthClasses:
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
            width = font[GLYPH].width
            location = stem, width
            if not location in weightWidthLocations:
                weightWidthLocations[location] = []
            weightWidthLocations[location].append(font)
        return weightWidthLocations
            
    def getMinMaxWidth(self):
        u"""Answer the minimal/max widths of H."""
        minWidth = sys.maxint
        maxWidth = -minWidth
        for font in self._fonts.values():
            minWidth = min(font[GLYPH].width, minWidth)
            maxWidth = max(font[GLYPH].width, maxWidth)
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
        Hg = self.originFont[GLYPH]
        counters = Hg.analyzer.horizontalCounters
        stems = Hg.analyzer.stems
        axisFontMin.info.widthClass = 1
        axisFontMax.info.widthClass = 9
        return axisFontMin, axisFontMax

def drawOS2Label(varFamily, fonts, weight, width):
    fill(1, 0, 0)
    stroke(None)
    R = 20
    x, y = weight, width * 100 # Scale OS/2 width to 1000
    oval(x-R/2, y-R/2, R, R)
    if varFamily.originFont in fonts: 
        # If one of these is the guessed origin font, then draw marker
        fill(None)
        stroke(1, 0, 0)
        strokeWidth(2)
        R = 27
        oval(x-R/2, y-R/2, R, R)
    return x, y    

def drawFontLabel(p, varFamily, f, fIndex=None, fAxis=None):
        x, y = p
        print f.info.styleName, f.info.weightClass, f.info.widthClass
        
        glyphH = f[GLYPH]
        if not glyphH.width:
            print glyphH, 'No width'
            return
            
        s = 0.05 * 1000/f.info.unitsPerEm
        leading = 2048/f.info.unitsPerEm
        stroke(None)
        fill(0)
        save()
        translate(x-glyphH.width/2*s, y-leading-50)
        scale(s)
        drawPath(glyphH.path)
        restore()
        y -= leading+50
        
        save()
        pathLabel = '-'.join(path2Name(f.path).split('-')[1:])
        #label = path2Name(f.path)
        if fAxis is not None:
            label = '@'+fAxis 
        elif fIndex is None:
            label = ''
        else:
            label = '#%d ' % fIndex 
        label += '%s\n(%s)\n%d' % (pathLabel.replace('.ttf', '').replace('_','\n').replace('-','\n'), f.info.styleName, f.info.weightClass)
        fs = FormattedString(label, fontSize=10, align='center')
        tw, th = textSize(fs)
        text(fs, (x-tw/2, y-14))
        restore()
        y -= leading + th-22

        # Draw marker on actual position of H.stem and H.weight as green dot
        stemValues = f.analyzer.stems.keys()
        if stemValues: # Cannot find H-stem, skip this marker
            stem = min(stemValues)
            # XOPQ (counter) + H.stem == H.width - H.stem - H.lsb - H.rsb
            width = glyphH.width - stem - glyphH.leftMargin - glyphH.rightMargin 
    
            c.fill((0, 0.5, 0))
            c.stroke(None)
            R = 16
            weightLoc, widthLoc = stem, width/2
            c.oval(weightLoc-R/2, widthLoc-R/2, R, R)
            if fAxis is not None:
                label = '@'+fAxis 
            elif fIndex is None:
                label = ''               
            else:
                label = '#%d\n' % fIndex
            bs = c.newString(label + ('S:%d\nW:%d\n%d' % (weightLoc, widthLoc, f.info.weightClass)), style=dict(fontSize=10, xTextAlign='center', textFill=0))
            tw, th = c.textSize(bs)
            c.text(bs, (weightLoc-tw/2, widthLoc-24))

            if varFamily.originFont is f: 
                # If one of these is the guessed origin font, then draw marker
                c.fill(None)
                c.stroke((0, 0.5, 0), 2) # Stroke color and width
                R = 23
                c.oval(weightLoc-R/2, widthLoc-R/2, R, R)

        else:
            pass
            #print 'No stem for', glyphH.font
        
def drawFamilyOverview(path):
    varFamily = guessVarFamilyFromPaths(path)
    if not varFamily: # No TTF fonts there?
        #print 'No TTF fonts found in', path
        return None


    # As we can guess the origin font, there is a reference for the other
    # masters to test against.
    #print '=== Guessed origin font:', path2Name(varFamily.originFont.path)
    #print checkInterpolation(varFamily.fonts)
    #print '=== Parametric axis fonts:', varFamily.parametricAxisFonts
    #print '=== Parametric axis metrics:', varFamily.parametricAxisMetrics
    
    newPage(1200, 1200)
    # Draw design space for width/weight
    translate(100,100)
    stroke(0.5)
    strokeWidth(1)
    fill(0.9)
    rect(0, 0, 1000, 1000)
    for x in range(0, 1100, 100):
        if 0 < x < 1000:
            line((x, 0), (x, 1000))
        fs = FormattedString(`x`, fontSize=12)
        tw, th = textSize(fs)
        text(fs, (x-tw/2, -20))

    for y in range(11):
        if 0 < y < 11:
            line((0, 1000/10*y), (1000, 1000/10*y))
        if y > 0:
            fs = FormattedString(`y`, fontSize=12, fill=(1, 0, 0))
            fs += FormattedString(' %s' % (y*100), fontSize=12, fill=(0, 0.5, 0))
            tw, th = textSize(fs)
        else:
            fs = FormattedString(`y`, fontSize=12, fill=0)
            tw, th = textSize(fs)
        text(fs, (-10-tw, 1000/10*y-th/2))
    
    # Draw axis labels
    fs = FormattedString('OS/2 weight class ', fontSize=12, fill=(1, 0, 0))
    fs += FormattedString('&', fontSize=12, fill=0)
    fs += FormattedString(' XTRA Axis (H-stem width)', fontSize=12, fill=(0, 0.5, 0))
    tw, th = textSize(fs)
    text(fs, (0, -50-th/2))

    save()
    rotate(90)
    fs = FormattedString('OS/2 width class ', fontSize=12, fill=(1, 0, 0))
    fs += FormattedString('&', fontSize=12, fill=0)
    fs += FormattedString(' XOPQ Axis + stem (H.width - H.stem - H.lsb - H.rsb)', fontSize=12, fill=(0, 0.5, 0))
    tw, th = textSize(fs)
    text(fs, (0, 60))
    restore()
    
    # Draw family name title    
    fs = FormattedString(varFamily.name, fontSize=24)
    text(fs, (0, 1000+30))

    fIndex = 1
    # Find widths and weights as defined by OS/2 and plot them as dots + names
    for (weight, width), fonts in varFamily.getOS2WeightWidthClasses().items():
    
        # Draw positions according to OS/2 values
        x, y = drawOS2Label(varFamily, fonts, weight, width)

        # Draw H and labels, stacked under the dot.
        for f in fonts:
            drawFontLabel((x, y), varFamily, f, fIndex)
            fIndex += 1

    if varFamily is not None:
        xtraMinFont, xtraMaxFont = varFamily.makeParametricFonts(varFamily.XTRA)
        print xtraMinFont, xtraMaxFont 
        x, y = drawOS2Label(varFamily, [xtraMinFont], xtraMinFont.info.weightClass, xtraMinFont.info.widthClass)
        drawFontLabel((x, y), varFamily, xtraMinFont, fAxis=varFamily.XTRA+'_min')

        x, y = drawOS2Label(varFamily, [xtraMaxFont], xtraMaxFont.info.weightClass, xtraMaxFont.info.widthClass)
        drawFontLabel((x, y), varFamily, xtraMaxFont, fAxis=varFamily.XTRA+'_max')
            
    return varFamily
    
    
#for path in PATHS:
for path in os.listdir(BASE_PATH):#[:20]:
    if path.startswith('.'):
        continue
    dirPath = BASE_PATH + path
    if not os.path.isdir(dirPath):
        continue
    drawFamilyOverview(dirPath)
    
saveImage(EXPORT_PATH)
#saveImage(EXPORT_GIF)
     