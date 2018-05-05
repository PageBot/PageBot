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
#     testPreVarFamily.py
##
#     https://www.typenetwork.com/brochure/opentype-font-variations/
#     https://variationsguide.typenetwork.com/#xopq
#     "wght" 134, "wdth" 369, "opsz" 36, “GRAD” 88 , ”XOPQ" 88, "XTRA" 402, "YOPQ" 50, "YTLC" 500, "YTSE" 18;
#
#     STAT table
#     https://www.microsoft.com/typography/otspec/stat.htm

import os, sys, shutil

if 1:
    from pagebot.contexts.platform import getContext
    context = getContext()
else:
    from pagebot.contexts.svgcontext import SvgContext
    context = SvgContext()
from pagebot.style import CENTER

from pagebot.fonttoolbox.fontpaths import getTestFontsPath
from pagebot.fonttoolbox.objects.prevarfamily import PreVarFamily
from pagebot.fonttoolbox.analyzers.glyphanalyzer import GlyphAnalyzer
from pagebot.fonttoolbox.analyzers.stems import Stem, Bar, BlueBar, Counter, VerticalCounter, Width, DiagonalStem
from pagebot.toolbox.transformer import asInt, path2Name, path2ParentPath

path = getTestFontsPath() + '/google/roboto/Roboto.designspace'
usedPositions = {}

SHOW_COORDINATES = True

ORIGIN_OS2_WEIGHT_CLASS = 400

GLYPH = 'H'

EXPORT_PATH = '_export/RobotoDelta-VF.pdf'

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

def drawOS2Label(varFamily, fonts, weight, width):
    context.fill((1, 0, 0))
    context.stroke(None)
    R = 20
    x, y = weight, width * 100 # Scale OS/2 width to 1000

    context.oval(x-R/2, y-R/2, R, R)
    
    if varFamily.defaultFont in fonts: 
        # If one of these is the guessed origin font, then draw marker
        context.fill(None)
        context.stroke(1, 0, 0)
        context.strokeWidth(2)
        R = 27
        context.oval(x-R/2, y-R/2, R, R)
    return x, y    

def drawFontLabel(p, prevarFamily, f, fIndex=None, fAxis=None):
        x, y = p
        #print f.info.styleName, f.info.weightClass, f.info.widthClass
        while (x, y) in usedPositions:
            y -= 80
        usedPositions[(x, y)] = f
        
        glyphH = f[GLYPH]
        if not glyphH.width:
            print glyphH, 'No width'
            return
            
        s = 0.05 * 1000/f.info.unitsPerEm
        leading = 2048/f.info.unitsPerEm
        context.stroke(None)
        context.fill(0)
        context.save()
        context.translate(x-glyphH.width/2*s, y-leading-50)
        context.scale(s)
        context.drawPath(glyphH.path)
        context.restore()
        y -= leading+50
        
        context.save()
        pathLabel = '-'.join(path2Name(f.path).split('-')[1:])
        #label = path2Name(f.path)
        if fAxis is not None:
            label = '@'+fAxis 
        elif fIndex is None:
            label = ''
        else:
            label = '#%d ' % fIndex 
        label += '%s\n(%s)\n%d' % (pathLabel.replace('.ttf', '').replace('_','\n').replace('-','\n'), f.info.styleName, f.info.weightClass)
        bs = context.newString(label, style=dict(fontSize=10, xTextAlign=CENTER))
        tw, th = context.textSize(bs)
        context.text(bs, (x-tw/2, y-14))
        context.restore()
        y -= leading + th-22

        # Draw marker on actual position of H.stem and H.weight as green dot
        stemValues = f.analyzer.stems.keys()
        if stemValues: # Cannot find H-stem, skip this marker
            stem = min(stemValues)
            # XOPQ (counter) + H.stem == H.width - H.stem - H.lsb - H.rsb
            width = glyphH.width - stem - glyphH.leftMargin - glyphH.rightMargin 
    
            context.fill((0, 0.5, 0))
            context.stroke(None)
            R = 16
            weightLoc, widthLoc = stem, width/2
            context.oval(weightLoc-R/2, widthLoc-R/2, R, R)
            if fAxis is not None:
                label = '@'+fAxis 
            elif fIndex is None:
                label = ''               
            else:
                label = '#%d\n' % fIndex
            bs = context.newString(label + ('S:%d\nW:%d\n%d' % (weightLoc, widthLoc, f.info.weightClass)), style=dict(fontSize=10, xTextAlign='center', textFill=0))
            tw, th = context.textSize(bs)
            context.text(bs, (weightLoc-tw/2, widthLoc-24))

            if prevarFamily.defaultFont is f: 
                # If one of these is the guessed origin font, then draw marker
                context.fill(None)
                context.stroke((0, 0.5, 0), 2) # Stroke color and width
                R = 23
                context.oval(weightLoc-R/2, widthLoc-R/2, R, R)

        else:
            pass
            #print 'No stem for', glyphH.font
        
def drawFamilyOverview(name):

    # As we can guess the origin font, there is a reference for the other
    # masters to test against.
    #print '=== Guessed origin font:', path2Name(prevarFamily.defaultFont.path)
    #print checkInterpolation(prevarFamily.fonts)
    #print '=== Parametric axis fonts:', prevarFamily.parametricAxisFonts
    #print '=== Parametric axis metrics:', prevarFamily.parametricAxisMetrics
    
    prevarFamily = PreVarFamily('Roboto', path)
    
    context.newPage(1200, 1200)
    # Draw design space for width/weight
    context.translate(100,100)
    context.stroke(0.5, 1)
    context.fill(0.9)
    context.rect(0, 0, 1000, 1000)
    for x in range(0, 1100, 100):
        if 0 < x < 1000:
            context.line((x, 0), (x, 1000))
        fs = context.newString(str(x), style=dict(fontSize=12))
        tw, th = context.textSize(fs)
        context.text(fs, (x-tw/2, -20))

    for y in range(11):
        if 0 < y < 11:
            context.line((0, 1000/10*y), (1000, 1000/10*y))
        if y > 0:
            bs = context.newString(str(y), style=dict(fontSize=12, textFill=(1, 0, 0)))
            bs += context.newString(' %s' % (y*100), style=dict(fontSize=12, textFill=(0, 0.5, 0)))
            tw, th = context.textSize(bs)
        else:
            bs = context.newString(str(y), style=dict(fontSize=12, textFill=0))
            tw, th = context.textSize(bs)
        context.text(bs, (-10-tw, 1000/10*y-th/2))
    
    # Draw axis labels
    bs = context.newString('OS/2 weight class ', style=dict(fontSize=12, textFill=(1, 0, 0)))
    bs += context.newString('&', style=dict(fontSize=12, textFill=0))
    bs += context.newString(' XTRA Axis (H-stem width)', style=dict(fontSize=12, textFill=(0, 0.5, 0)))
    tw, th = context.textSize(bs)
    context.text(bs, (0, -50-th/2))

    context.save()
    context.rotate(90)
    bs = context.newString('OS/2 width class ', style=dict(fontSize=12, textFill=(1, 0, 0)))
    bs += context.newString('&', style=dict(fontSize=12, textFill=0))
    bs += context.newString(' XOPQ Axis + stem (H.width - H.stem - H.lsb - H.rsb)', style=dict(fontSize=12, textFill=(0, 0.5, 0)))
    tw, th = context.textSize(bs)
    context.text(bs, (0, 60))
    context.restore()
    
    # Draw family name title    
    bs = context.newString(name, style=dict(fontSize=24))
    context.text(bs, (0, 1000+30))
    
    fIndex = 1
    # Find widths and weights as defined by OS/2 and plot them as dots + names
    for (weight, width), fonts in prevarFamily.getOS2WeightWidthClasses().items():
    
        # Draw positions according to OS/2 values
        x, y = drawOS2Label(prevarFamily, fonts, weight, width)

        # Draw H and labels, stacked under the dot in case there are fonts 
        # on the same position.
        for f in fonts:
            drawFontLabel((x, y), prevarFamily, f, fIndex)
            fIndex += 1

    if prevarFamily is not None:
        
        xtraFonts = prevarFamily.makeParametricFonts(prevarFamily.XTRA)
        xtraMinFont, xtraMaxFont = xtraFonts
        x, y = drawOS2Label(prevarFamily, [xtraMinFont], xtraMinFont.info.weightClass, xtraMinFont.info.widthClass)
            
        drawFontLabel((x, y), prevarFamily, xtraMinFont, fAxis=prevarFamily.XTRA+'_min')

        x, y = drawOS2Label(prevarFamily, [xtraMaxFont], xtraMaxFont.info.weightClass, xtraMaxFont.info.widthClass)
        drawFontLabel((x, y), prevarFamily, xtraMaxFont, fAxis=prevarFamily.XTRA+'_max')
            
    return prevarFamily
    
#'RobotoDelta-VF'
drawFamilyOverview('Roboto')
    
context.saveImage(EXPORT_PATH)
os.system('open %s' % EXPORT_PATH)
