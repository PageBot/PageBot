# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
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
FRAMES = 200
MOVE = FRAMES/80.0
STEP = 1 # 20

def setValue(list, step, index):
    list[index] += step[index]*F
    if list[index] < 0 or list[index] > 1000:
        step[index] = -step[index]
        list[index] += step[index]*F

def rnd():
    return [
        # Start angle   Step cycles in FRAMES
        [random()*2-1, 1.0*int(MOVE+random()*MOVE)/FRAMES], 
        [random()*2-1, 1.0*int(MOVE+random()*MOVE)/FRAMES], 
        [random()*2-1, 1.0*int(MOVE+random()*MOVE)/FRAMES], 
    ]        
         
def aValue(index, values, margin1=500, margin2=500):
    # Calculate new angle and put back into array for next iteration.
    angle, step = values[index]    
    newAngle = sin(angle*2*pi)
    values[index][0] += step
    if values[index][0] > 1:
        values[index][0] -= 1
    elif values[index][0] < -1:
        values[index][0] += 1
    return newAngle * margin1 + margin2
    
# -----------------------------------------------------------------         
def makeAnimatiom():
    lineV = rnd() # ((angle, speed), (angle, speed), (angle, speed))
    openV = rnd() 
    rndiV = rnd() 
    rndoV = rnd() 
    sqriV = rnd() 
    sqroV = rnd() 
    wghtV = rnd() 
    
    c1, c2, c3 = [1, 0, 0], [1, 0, 0.5], [0.5, 0.1, 0.5]

    vMasterFont = TTFont(FONT_PATH)
    for n in range(0, FRAMES, STEP):
        newPage(W, H)
        fill(0)
        rect(0, 0, W, H)
        for cIndex, c in enumerate((c1, c2, c3)):
            if cIndex == 0:
                c[0] = (1+lineV[cIndex][0])/2
                c[1] = (1+openV[cIndex][0])/2
                c[2] = (1+wghtV[cIndex][0])/2
            elif cIndex == 1:
                c[0] = (1+rndoV[cIndex][0])/2
                c[1] = (1+wghtV[cIndex][0])/2
                c[2] = (1+sqriV[cIndex][0])/2
            else:
                c[0] = (1+wghtV[cIndex][0])/2
                c[1] = (1+sqroV[cIndex][0])/2
                c[2] = (1+rndiV[cIndex][0])/2
            location = {
                'line': aValue(cIndex, lineV), 
                'open': aValue(cIndex, openV), 
                'rndi': aValue(cIndex, rndiV), 
                'rndo': aValue(cIndex, rndoV), 
                'sqri': aValue(cIndex, sqriV), 
                'sqro': aValue(cIndex, sqroV), 
                'wght': aValue(cIndex, wghtV)
            }
            drawGlyphPath(vMasterFont, 'a', S*45, S*25, location=location, s=S*0.09, fillColor=c)
makeAnimatiom()
saveImage(EXPORT_PATH) 

