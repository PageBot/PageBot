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
#     AutomaticPageComposition.py
#
#     This script generates an article (in Dutch) of 2009 about the approach to
#     generate automatic layouts, using Style, Galley, Typesetter and Composer classes.
#
from fontTools.ttLib import TTFont

import pagebot.fonttoolbox.variationbuilder
reload(pagebot.fonttoolbox.variationbuilder)
from pagebot.fonttoolbox.variationbuilder import getVariationFont, drawGlyphPath
    
EXPORT_PATH = 'export/animatedA-1.gif'
  
ROOT_DIR = '/'.join(pagebot.__file__.split('/')[:-2]) + '/'
FONT_DIR = ROOT_DIR + 'fonts/'
FONT_NAME = 'BitcountGrid-GX.ttf'
FONT_PATH = FONT_DIR + FONT_NAME

F = 1 # Animation speed
S = 5
W = H = S*90

def setValue(list, step, index):
    list[index] += step[index]*F
    if list[index] < 0 or list[index] > 1000:
        step[index] = -step[index]
        list[index] += step[index]*F
        
# -----------------------------------------------------------------         
def makeAnimatiom():
    lineV = [0, 100, 200]
    lineS = [100, -30, 60]
    openV = [500, 600, 700]
    openS = [50, -30, 140]
    rndiV = [200, 300, 100]
    rndiS = [120, -30, 120]
    rndoV = [700, 300, 400]
    rndoS = [-130, -40, -60]
    sqriV = [400, 300, 400]
    sqriS = [80, -30, -50]
    sqroV = [300, 500, 600]
    sqroS = [-40, -80, 60]
    wghtV = [500, 600, 400]
    wghtS = [-30, 50, 80]
    vMasterFont = TTFont(FONT_PATH)
    for n in range(100):
        newPage(W, H)
        for cIndex, c in enumerate(((0.2, 0, 0.5), (1, 0, 0), (0, 0.1, 0))):
            location = {'line': lineV[cIndex], 'open': openV[cIndex], 'rndi': rndiV[cIndex], 'rndo': rndoS[cIndex], 'sqri': sqriV[cIndex], 'sqro': sqroV[cIndex], 'wght': wghtV[cIndex]}
            drawGlyphPath(vMasterFont, 'a', S*45, S*25, location=location, s=S*0.09, fillColor=c)
            setValue(lineV, lineS, cIndex)
            setValue(openV, openS, cIndex)
            setValue(rndiV, rndiS, cIndex)
            setValue(rndoV, rndoS, cIndex)
            setValue(sqriV, sqriS, cIndex)
            setValue(sqroV, sqroS, cIndex)
            setValue(wghtV, wghtS, cIndex)
makeAnimatiom()
saveImage(EXPORT_PATH) 

