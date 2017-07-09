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
#     DecovarNameAnimation.py
#
#     This script generates creates a Typetr logo as animated gif.
#     (takes around 10 minutes to run).
#
from pagebot import getFontPath

from pagebot.fonttoolbox.objects.font import Font
from pagebot.fonttoolbox.variablebuilder import getVariableFont, drawGlyphPath
    
EXPORT_PATH = '_export/DecovarAnimated_skeletons_terminals.gif'
  
FONT_DIR = getFontPath()
FONT_PATH = FONT_DIR + 'fontbureau/Decovar-VF_2017-02-06.ttf'

TEXT = 'DECOVAR' 

F = 1 # Animation speed
S = 3 #5
W = S*6*10*len(TEXT)-S*10
H = S*90
AXIS_FACTOR = 1000
FRAMES = 8 # Number of frames per sequence.
MOVE = FRAMES/80.0
STEP = 1 # 20

class AxisState(object):
    pass

def getProofSequences():
    #   Answer sequences for proofing.
    """
        Decovar test proof algorithm

        ['sklA', 'wmx2', 'bldB', '', '', '', '', '', '', '', '', '', '', '', '']

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
    # Dimension
    terminals = ((0.5, 1), ('trmA', 'trmB', 'trmC', 'trmD', 'trmE', 'trmF', 'trmG', 'trmK', 'trmL'))
    skeletons = ((0.25, 0.5, 0.75, 1), ('sklA', 'sklB', 'sklD'))
    blends = ((0.125, 0.250, 0.375, 0.5, 0.625, 0.750, 0.875, 1), ('bldA', 'bldB'))
    weights = ((0.125, 0.250, 0.375, 0.5, 0.625, 0.750, 0.875, 1), ('wmx2',))
    
    sequences = [
         (skeletons, terminals),
         #(weights, terminals),
         #(skeletons, weights),
         #(terminals, weights),
         #(terminals, skeletons, weights),
         #(blends, weights),
    ]
    return sequences
           
def getDefaultLocation(axes):
    # Copy into default location
    location = {}
    for name, (_, defaultValue, _) in axes.items():
        defaultValue = 0.5
        location[name] = defaultValue
    return location
    
def getLocations(axes, sequence):
    u"""Answer the list of locations for this sequence."""
    changed = []
    locations = []
    # Permutate the axes to cycle to
    cycleAxes = []
    dimension1 = sequence[0]
    dimension2 = sequence[1]

    values1, axisNames1 = dimension1
    minValue1 = values1[0]
    maxValue1 = values1[1]
    valueRange1 = maxValue1 - minValue1

    values2, axisNames2 = dimension2
    minValue2 = values2[0]
    maxValue2 = values2[1]
    valueRange2 = maxValue2 - minValue2

    location = getDefaultLocation(axes)

    for axisName1 in axisNames1:  
        for axisName2 in axisNames2:  
            angle = 0.5
            angleStep = 1.0/FRAMES
            while angle <= 2.5:
                a = sin(angle*2*pi)
                location = getDefaultLocation(axes)
                v1 = (minValue1 + a * valueRange1) * AXIS_FACTOR
                v2 = (minValue2 + a * 0.5 * valueRange2) * AXIS_FACTOR
                location[axisName1] = v1
                location[axisName2] = v2
                locations.append(location) 
                location['changed1'] = axisName1, int(round(v1))
                location['changed2'] = axisName2, int(round(v2))
                angle += angleStep
    return locations
    
# -----------------------------------------------------------------         
def makeAnimatiom():
    vMasterFont = Font(FONT_PATH)
    axes = vMasterFont.axes


    for sequence in getProofSequences():   
        for location in getLocations(axes, sequence): # Expand into a sequence of locations. 
            newPage(W, H)
            fill(1)
            rect(0, 0, W, H)
            save()
            textColor = 0
            for gIndex, glyph in enumerate(TEXT):
                # Only works by glyph name.
                drawGlyphPath(vMasterFont.ttFont, glyph, S*40 + S*gIndex*6*9, S*22, location=location, s=S*0.04, fillColor=textColor)
            # TODO To be extended PageBot
            #drawGlyphPaths(vMasterFont, TEXT, x=S*40 + S*gIndex*6*9, y=S*22, location=location, fontSize=S*0.04, fillColor=textColor)
            restore()
            fill(0)
            fontSize(24)
            text('%s %s' % (location['changed1'][0], location['changed2'][0]), (100, 20))

makeAnimatiom()
saveImage(EXPORT_PATH)
