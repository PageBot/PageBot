#!/usr/bin/env python
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
#     This script generates creates a Typetr logo as animated gif.
#     (takes around 10 minutes to run).
#
from pagebot import getFontPath
from pagebot.contexts import defaultContext as context
from pagebot.fonttoolbox.objects.font import Font
from pagebot.fonttoolbox.variablefontbuilder import getVariableFont, drawGlyphPath
    
EXPORT_PATH = '_export/DecovarAnimated_skeletons_terminals.gif'
  
FONT_DIR = getFontPath()
FONT_PATH = FONT_DIR + 'fontbureau/Decovar-VF_2017-02-06.ttf'

TEXT = 'DE' #DECOVAR' 

F = 1 # Animation speed
S = 7 #5
W = S*6*10*len(TEXT)-S*10
H = S*90
AXIS_FACTOR = 1000
FRAMES = 8 # Number of frames per sequence.
MOVE = FRAMES/80.0
STEP = 1 # 20

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

class AxisState(object):
    pass

def getProofSequences():
#   Answer sequences for proofing.
   
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

TerminalValue = 0
TerminalShape = 0
SkeletonValue = 0
SkeletonShape = 0
BlendValue = 0
BlendShape = 0
WeightValue = 0

TERMINAL_VALUES = (500, 750, 1000)
TERMINAL_VALUES_S = ['None']
for v in TERMINAL_VALUES:
    TERMINAL_VALUES_S.append(str(v))
TERMINALS = ('trmA', 'trmB', 'trmC', 'trmD', 'trmE', 'trmF', 'trmG', 'trmK', 'trmL')
SKELETON_VALUES = (250, 500, 750, 1000)
SKELETON_VALUES_S = ['None']
for v in SKELETON_VALUES:
    SKELETON_VALUES_S.append(str(v))
SKELETONS = ('sklA', 'sklB', 'sklD')
BLEND_VALUES = (125, 250, 375, 500, 625, 750, 875, 1000)
BLEND_VALUES_S = ['None']
for v in BLEND_VALUES:
    BLEND_VALUES_S.append(str(v))
BLENDS = ('bldA', 'bldB')
WEIGHT_VALUES = (125, 250, 375, 500, 625, 750, 875, 1000)
WEIGHT_VALUES_S = []
for v in WEIGHT_VALUES:
    WEIGHT_VALUES_S.append(str(v))


vMasterFont = Font(FONT_PATH)
    
# -----------------------------------------------------------------         
def makeAnimation():
    axes = vMasterFont.axes

    print 'Variable A X E S'
    for axisName, (minValue, defaultValue, maxValue) in vMasterFont.axes.items():
        print axisName, 'minValue', minValue, 'defaultValue', defaultValue, 'maxValue', maxValue

    location = getDefaultLocation(axes)

    if TERMINAL_VALUES_S[TerminalValue] != 'None':
        location[TERMINALS[TerminalShape]] = TERMINAL_VALUES[TerminalValue]
    if SKELETON_VALUES[SkeletonValue] != 'None':
        location[SKELETONS[SkeletonShape]] = SKELETON_VALUES[SkeletonValue]
    if BLEND_VALUES[BlendValue] != 'None':    
        location[BLENDS[BlendShape]] = BLEND_VALUES[BlendValue]
    location['wmx2'] = WEIGHT_VALUES[WeightValue-2]

    #for sequence in getProofSequences():   
    #    for location in getLocations(axes, sequence): # Expand into a sequence of locations. 
    #        newPage(W, H)
    context.fill(1)
    context.rect(0, 0, W, H)
    context.save()
    textColor = 0
    for gIndex, glyph in enumerate(TEXT):
        # Only works by glyph name.
        drawGlyphPath(vMasterFont.ttFont, glyph, S*40 + S*gIndex*6*9, S*22, location=location, s=S*0.04, fillColor=textColor)
        drawGlyphPath(vMasterFont.ttFont, glyph, S*40 + S*gIndex*6*9, S*22, location=location, s=S*0.04, fillColor=textColor)
    # TODO To be extended PageBot
    #drawGlyphPaths(vMasterFont, TEXT, x=S*40 + S*gIndex*6*9, y=S*22, location=location, fontSize=S*0.04, fillColor=textColor)
    context.restore()
    context.fill(0)
    context.fontSize(24)
    #text('%s %s' % (location['changed1'][0], location['changed2'][0]), (100, 20))


context.Variable([
    dict(name='TerminalValue', ui='PopUpButton', args=dict(items=TERMINAL_VALUES_S)),
    dict(name='TerminalShape', ui='PopUpButton', args=dict(items=(
        'Rounded [trmA]', 
        'Pointed [trmB]', 
        'Rounded slab [trmC]', 
        'Angled [trmD]', 
        'Cleaved [trmE]', 
        'Plussed [trmF]', 
        'Slabbed [trmG]', 
        'Rectangled [trmK]', 
        'Starred [trmL]'))),
    dict(name='SkeletonValue', ui='PopUpButton', args=dict(items=SKELETON_VALUES_S)),
    dict(name='SkeletonShape', ui='PopUpButton', args=dict(items=(
        'Neon [sklA]', 
        'Cleaved [sklB]', 
        'Zebra [sklD]'))),
    dict(name='BlendValue', ui='PopUpButton', args=dict(items=BLEND_VALUES_S)),
    dict(name='BlendShape', ui='PopUpButton', args=dict(items=(
        'Straight [bldA]', 
        'Leaved [bldB]'))),
    dict(name='WeightValue', ui='PopUpButton', args=dict(items=WEIGHT_VALUES_S)),
        
    
    # create a variable called 'useColor'
    # and the related ui is a CheckBox.
    #dict(name="useColor", ui="CheckBox"),
    # create a variable called 'c'
    # and the related ui is a ColorWell.
    #dict(name="c", ui="ColorWell")
    ], globals())

makeAnimation()
#saveImage(EXPORT_PATH)
print TerminalValue
