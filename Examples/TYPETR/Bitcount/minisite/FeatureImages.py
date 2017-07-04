# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     FeatureImages.py
#
#    Images for mini-site
#
from AppKit import NSColor
import os

import pagebot
from pagebot.fonttoolbox.objects.family import getFamilyFontPaths
from pagebot import newFS, textBoxBaseLines
from pagebot.toolbox.transformer import path2ScriptId


fontNames = []
for fontName in installedFonts():
    if 'BitcountProp' in fontName:
        fontNames.append(fontName)
        
def collectFonts():
    # Bitcount is made from 3 spacing sets: 
    #    - Monospaced (Grid, Mono)
    #    - Proportional (Prop)
    # Define the family name of fonts that we want to use, 
    # including the type of spacing.
    pass

def drawFigures():
    W, H = 860, 451
    newPage(W, H)
    LEADING = 0.9
    fs = newFS('ABC0123456789\n', style=dict(textFill=0, rLeading=1, font='BitcountPropSingle-RegularCircle', fontSize=90))
    fs += newFS('abc0123456789\n', style=dict(textFill=0, font='BitcountPropSingle-RegularCircle', rLeading=LEADING, fontSize=90, openTypeFeatures=dict(smcp=True)))
    fs += newFS('ABCabc0123456789\n', style=dict(textFill=0, font='BitcountPropSingle-RegularCircle', rLeading=LEADING, fontSize=90, openTypeFeatures=dict(onum=True, ss07=True)))
    fs += newFS('ABCabc0123456789\n', style=dict(textFill=0, font='BitcountPropSingle-RegularCircle', rLeading=LEADING, fontSize=90, openTypeFeatures=dict(ss07=True)))
    fs += newFS('Fraction 1/2 12345/67890\n', style=dict(textFill=0, font='BitcountPropSingle-RegularCircle', rLeading=LEADING, fontSize=90, openTypeFeatures=dict(frac=True)))
    M = 30
    textBox(fs, (M+10, -10, W-2*M, H))
    saveImage('_export/figures.png') # Save the sample as file or animated gif.
     
def drawSamples():
    print fontNames
    drawFigures()
     
# If no Bitcount fonts could be found, open the browser on the TypeNetwork shop page and stop this script.
collectFonts() # Collect available fonts, filter into characteristics, as weight, italic, etc.
if not fontNames:
    os.system('open %s/fonts/%s' % (typetrStoreUrl, 'productus')) #familyName.lower())
else:
    drawSamples()

