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

def rnd():
    return [
        int(round(random()*1000)), 
        int(round(random()*1000)), 
        int(round(random()*1000))
    ], [
        int(round(random()*200))-100, 
        int(round(random()*200))-100, 
        int(round(random()*200))-100
    ]
     
    
# -----------------------------------------------------------------         
def makeAnimatiom():
    lineV, lineS = rnd()
    openV, openS = rnd()
    rndiV, rndiS = rnd()
    rndoV, rndoS = rnd()
    sqriV, sqriS = rnd()
    sqroV, sqroS = rnd()
    wghtV, wghtS = rnd()
    
    c1 = (random(), random(), random())
    c2 = (random(), random(), random())
    c3 = (random(), random(), random())

    vMasterFont = TTFont(FONT_PATH)
    for n in range(20):
        newPage(W, H)
        for cIndex, c in enumerate((c1, c2, c3)):
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

