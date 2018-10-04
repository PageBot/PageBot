# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
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
#

import os, sys, shutil

from pagebot.toolbox.color import whiteColor, blackColor
from pagebot import getContext
from pagebot.fonttoolbox.objects.font import Font
from pagebot.fonttoolbox.objects.varfamily import VarFamily
from pagebot.fonttoolbox.analyzers.glyphanalyzer import GlyphAnalyzer
from pagebot.fonttoolbox.analyzers.stems import Stem, Bar, BlueBar, Counter, VerticalCounter, Width, DiagonalStem
from pagebot.toolbox.transformer import asInt, path2FontName, path2ParentPath

context = getContext()

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
#BASE_PATH = '/FontDevelopment/WebType-Raw/WT-TTF/'

def findFontPaths(basePath, paths=None):
    """Answer the recursive list of TTF non-Italic font paths that are in directory basePath."""
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
    """This method will test if there are problems for the current set of fonts to be interpolated,
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
    """Initialize by guessing the self._font axis locations.
    """
    paths = findFontPaths(basePath)
    name = name or path2FontName(basePath)
    return VarFamily(name, paths)

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
        print(f.info.styleName, f.info.weightClass, f.info.widthClass)

        glyphH = f[GLYPH]
        if not glyphH.width:
            print(glyphH, 'No width')
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
        pathLabel = '-'.join(path2FontName(f.path).split('-')[1:])
        #label = path2FontName(f.path)
        if fAxis is not None:
            label = '@'+fAxis
        elif fIndex is None:
            label = ''
        else:
            label = '#%d ' % fIndex
        label += '%s\n(%s)\n%d' % (pathLabel.replace('.ttf', '').replace('_','\n').replace('-','\n'), f.info.styleName, f.info.weightClass)
        bs = context.newString(label, style=dict(fontSize=10, align='center'))
        tw, th = bs.size
        c.text(bs, (x-tw/2, y-14))
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
            bs = c.newString(label + ('S:%d\nW:%d\n%d' % (weightLoc, widthLoc, f.info.weightClass)), style=dict(fontSize=10, xTextAlign='center', textFill=blackColor))
            tw, th = bs.size
            c.text(bs, (weightLoc-tw/2, widthLoc-24))

            if varFamily.originFont is f:
                # If one of these is the guessed origin font, then draw marker
                c.fill(None)
                c.stroke((0, 0.5, 0), 2) # Stroke color and width
                R = 23
                c.oval(weightLoc-R/2, widthLoc-R/2, R, R)

        else:
            pass
            #print('No stem for', glyphH.font)

def drawFamilyOverview(path):
    varFamily = guessVarFamilyFromPaths(path)
    if not varFamily: # No TTF fonts there?
        #print('No TTF fonts found in', path)
        return None


    # As we can guess the origin font, there is a reference for the other
    # masters to test against.
    #print('=== Guessed origin font:', path2FontName(varFamily.originFont.path))
    #print(checkInterpolation(varFamily.fonts))
    #print('=== Parametric axis fonts:', varFamily.parametricAxisFonts)
    #print('=== Parametric axis metrics:', varFamily.parametricAxisMetrics)

    context.newPage(1200, 1200)
    # Draw design space for width/weight
    context.translate(100,100)
    context.stroke(grayColor)
    context.strokeWidth(1)
    context.fill(color(0.9))
    context.rect(0, 0, 1000, 1000)
    for x in range(0, 1100, 100):
        if 0 < x < 1000:
            context.line((x, 0), (x, 1000))
        bs = context.newString(`x`, fontSize=12)
        tw, th = bs.size
        context.text(bs, (x-tw/2, -20))

    for y in range(11):
        if 0 < y < 11:
            line((0, 1000/10*y), (1000, 1000/10*y))
        if y > 0:
            bs = context.newString(`y`, fontSize=12, fill=color(1, 0, 0))
            bs += context.newString(' %s' % (y*100), fontSize=12, fill=color(0, 0.5, 0))
            tw, th = bs.size
        else:
            bs = context.newString(`y`, fontSize=12, fill=blackColor)
            tw, th = bs.size
        text(fs, (-10-tw, 1000/10*y-th/2))

    # Draw axis labels
    bs = context.newString('OS/2 weight class ', fontSize=12, fill=color(1, 0, 0))
    bs += context.newString('&', fontSize=12, fill=blackColor)
    bs += context.newString(' XTRA Axis (H-stem width)', fontSize=12, fill=color(0, 0.5, 0))
    tw, th = bs.size
    context.text(bs, (0, -50-th/2))

    context.save()
    context.rotate(90)
    bs = context.newString('OS/2 width class ', fontSize=12, fill=color(1, 0, 0))
    bs += context.newString('&', fontSize=12, fill=blackColor)
    bs += context.newString(' XOPQ Axis + stem (H.width - H.stem - H.lsb - H.rsb)', fontSize=12, fill=color(0, 0.5, 0))
    tw, th = bs.size
    context.text(fs, (0, 60))
    context.restore()

    # Draw family name title
    bs = context.newString(varFamily.name, fontSize=24)
    context.text(bs, (0, 1000+30))

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
        print(xtraMinFont, xtraMaxFont )
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

context.saveImage(EXPORT_PATH)
#context.saveImage(EXPORT_GIF)

