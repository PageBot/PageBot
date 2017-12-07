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
#     DecovarNameAnimation.py
#
#     This script generates creates a the DECOVAR name as animated gif.
#     Note that there is no limitation in design space boundaries, showing
#     the whole spectrum of locations. This means that most of the generated
#     instances are "wrong".
#
from fontTools.ttLib import TTFont
from pagebot import getFontPath

from pagebot.fonttoolbox.objects.font import Font
import pagebot.fonttoolbox.variablebuilder
reload(pagebot.fonttoolbox.variablebuilder)
from pagebot.fonttoolbox.variablebuilder import getVariableFont, drawGlyphPath
    
EXPORT_PATH = '_export/DecovarNameAnimatedAllAxes.pdf'
  
FONT_DIR = getFontPath()
FONT_PATH = FONT_DIR + 'fontbureau/Decovar-VF_2017-02-06.ttf'

TEXT = 'DECOVAR' 

F = 1 # Animation speed
S = 5 #5
W = S*6*10*len(TEXT)-S*10
H = S*90
AXIS_FACTOR = 1000
FRAMES = 20
MOVE = FRAMES/80.0
STEP = 1 # 20

class AxisState(object):
    pass

def getProofSequences():
    #   Answer sequences for proofing.
    
    """
        Decovar test proof algorithm

        ['sklA', 'wmx2', 'bldB', 'bldA', 'sklD', 'trmA', 'sklB', 'trmC', 'trmB', 'trmE', 'trmD', 'trmG', 'trmF', 'trmK', 'trmL']

        Define axis granularities, per 0-1 axis value
        Terminal .5 (I.E. proof .5 and 1)
        Skeleton .25 (4 stops on axis)
        Paraweight .125 (8)
        Blend .125 (8)

        Set size 60

        Print glyphs A-Z

        Loop for each:
        A. Terminal axes
        B. Skeleton axes
        C. Parametric axis
        D. Blend axes

        Loop for each*:
        A + B
        A + C
        B + C
        A + B + C
        C + D
        * each not all, I.e there are never more than 3 axis proofed in this algorithm.

        Change text to something else.

        Let me know I'll work on Amstelvar's.
    """
    
def setValue(list, step, index):
    list[index] += step[index]*F
    if list[index] < 0 or list[index] > 1000:
        step[index] = -step[index]
        list[index] += step[index]*F

def newAxisState(axisName, minValue, defaultValue, maxValue):
    # Value, Start angle   Step cycles in FRAMES
    axisState = AxisState()
    axisState.value = minValue + random() * (maxValue - minValue)
    axisState.angle = random()*2-1 # Random start angle
    axisState.stepCycle = 1.0*int(MOVE+random()*MOVE)/FRAMES
    return axisState
         
def nextValue(axisState, padding1=500, padding2=500):
    # Calculate new angle and put back into array for next iteration.
    newAngle = sin(axisState.angle*2*pi)
    axisState.angle += axisState.stepCycle
    
    if axisState.angle > 1:
        axisState.angle -= 1
    elif axisState.angle < -1:
        axisState.angle += 1
    return newAngle 

def getNextLocation(axisStates):
    location = {}
    for axisName, axisState in axisStates.items():
        location[axisName] = nextValue(axisState) * AXIS_FACTOR
    return location
   

# -----------------------------------------------------------------         
def makeAnimatiom():
    vMasterFont = Font(FONT_PATH)
    axes = vMasterFont.axes
    print axes.keys()
    
    axisStates = {}
    for axisName, (minValue, defaultValue, maxValue) in axes.items():
        axisStates[axisName] = newAxisState(axisName, minValue, defaultValue, maxValue)
    
    c1, c2, c3 = [1, 0.1, 0, 0.7], [0, 1, 0, 0.7], [0, 0, 1, 0.7]
    
    for n in range(0, FRAMES, STEP):
        newPage(W, H)
        fill(1)
        rect(0, 0, W, H)
        textColor = 0
        """
        for cIndex, c in enumerate((c1, c2, c3)):
            if cIndex == 0:
                c[0] = (1.5+openV[cIndex][0]/2)/2
                #c[1] = (1+lineV[cIndex][0]/16)/2
                #c[2] = (1+wghtV[cIndex][0]/16)/2
            elif cIndex == 1:
                #c[0] = (1+rndoV[cIndex][0]/8)/2
                c[1] = (1.2+rndiV[cIndex][0]/2)/2
                #c[2] = (1+sqroV[cIndex][0]/8)/2
            else:
                #c[0] = (1+rndoV[cIndex][0]/16)/2
                #c[1] = (1+wghtV[cIndex][0]/16)/2
                c[2] = (1.5+wghtV[cIndex][0]/2)/2
        """
        location = getNextLocation(axisStates)
        for gIndex, glyph in enumerate(TEXT):
            # Only works by glyph name.
            drawGlyphPath(vMasterFont.ttFont, glyph, S*40 + S*gIndex*6*9, S*22, location=location, s=S*0.04, fillColor=textColor)
        # TODO To be extended PageBot
        #drawGlyphPaths(vMasterFont, TEXT, x=S*40 + S*gIndex*6*9, y=S*22, location=location, fontSize=S*0.04, fillColor=textColor)

makeAnimatiom()
saveImage(EXPORT_PATH) 

