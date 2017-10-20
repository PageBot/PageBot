# -*- coding: utf8 -*-
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
#     LayerEditor.py
#
#     The script assumes one or multiple Bitcount fonts to be installed in the system.
#     Otherwise the script will stop, opening the browser on the TypeNetwork store.
#     Purchase Bitcount fonts at https://store.typenetwork.com/foundry/typetr/fonts/bitcount
#     A single user license of Bitcount is $10.10 per font or $101 for the complete package of 300 styles).
#
from AppKit import NSColor
import os

import pagebot
from pagebot.contexts import defaultContext as context
from pagebot.fonttoolbox.objects.family import getFamilyFontPaths
from pagebot import textBoxBaseLines
from pagebot.toolbox.transformer import path2ScriptId

# Optional using Bitpath family, mixed with Bitcount
Use_BitPath = True
# Initial sample text. Can be altered in the text box of the popup window.
W = 500 # Width of the sample image. Heights is calculated from string.
 # Height of the sample image
M = 32 # Margin between text and image side.
Sample_Text = u'Typëtr' # Initial sample string
monoSpaced = True #random()<0.5
Background_Color = NSColor.blackColor()
Italics = False
Layers = 3
Actions = 'QQQ'
color = True
Layer_Offset_X = -2
Layer_Offset_Y = 2

Layer_Color_0 = None
Layer_Color_1 = None
Layer_Color_2 = None
Layer_Color_3 = None
Layer_Color_4 = None
Layer_Color_5 = None

def clearFonts():
    scriptGlobals.layerFonts = {0: None, 1:None, 2:None, 3:None, 4:None, 5:None} # 
 
# Kinda hack, storing in empty module, to prevent globals to re-initialized, if variables are changed.
scriptGlobals = pagebot.getGlobals(path2ScriptId(__file__))

if not hasattr(scriptGlobals, 'initializedLayerEditor'):
    scriptGlobals.initializedLayerEditor = True
    # Store Italics flag, so we can test if it changed.
    scriptGlobals.italics = Italics
    # Store Use_BitPath flag, so we can test if it changed.
    scriptGlobals.use_BitPath = Use_BitPath
    # Currently (random) selected fonts per layer
    clearFonts() # Initialize font choice, so new random fonts will be selected.
    scriptGlobals.layerColors = {0:NSColor.grayColor(), 1:NSColor.grayColor(), 2:NSColor.grayColor(), 
        3:NSColor.grayColor(), 4:NSColor.grayColor(), 5:NSColor.grayColor()} # 
    # Collections of avaiable fonts, filtered by weight and stem-pixel 
    scriptGlobals.fontNamePaths = {}
    scriptGlobals.lightPaths = {} # Not Bold or Black
    scriptGlobals.boldPaths = {}
    scriptGlobals.singleLightPaths = {} # Not Bold or Black
    scriptGlobals.singleBoldPaths = {}
    scriptGlobals.doubleLightPaths = {} # Not Bold or Black
    scriptGlobals.doubleBoldPaths = {}

typetrStoreUrl = 'https://store.typenetwork.com/foundry/typetr'
EXPORT_DIR = '_export/BitcountLayerCatalog/'
EXPORT_IMAGES = EXPORT_DIR + 'images'
# Make sure the export directory exists
if not os.path.exists(EXPORT_IMAGES):
    os.makedirs(EXPORT_IMAGES)

if Italics != scriptGlobals.italics: # Did it change?
    scriptGlobals.italics = Italics
    # Force new random selection of fonts.
    clearFonts()

if Use_BitPath != scriptGlobals.use_BitPath: # Did it changed?
    scriptGlobals.use_BitPath = Use_BitPath
    # Force new random selection of fonts.
    clearFonts()

# Compare stored colors
for layerIndex in range(Layers):
    if globals()['Layer_Color_%d' % layerIndex] is None:
        globals()['Layer_Color_%d' % layerIndex] = scriptGlobals.layerColors[layerIndex]
    elif scriptGlobals.layerColors[layerIndex] != globals()['Layer_Color_%d' % layerIndex]:
        scriptGlobals.layerColors[layerIndex] = globals()['Layer_Color_%d' % layerIndex]
          
def collectFonts():
    # Bitcount is made from 3 spacing sets: 
    #    - Monospaced (Grid, Mono)
    #    - Proportional (Prop)
    # Define the family name of fonts that we want to use, 
    # including the type of spacing.
    if scriptGlobals.fontNamePaths: # Already installed, skip.
        return
        
    if monoSpaced:
        familyName = 'BitcountMono'
    else:
        familyName = 'BitcountProp' # Only works in layers, if also Single/Double is selected.
    
    # Just get paths of the fonts, not the Font objects. 
    # We want quick interactive response.
    # Call imported method, to find all installed Bitcount fonts.
    scriptGlobals.fontNamePaths = getFamilyFontPaths(familyName) 
        
    for fontName in scriptGlobals.fontNamePaths:
        if 'Prop' in fontName:
            print fontName

    if Use_BitPath:
        # Add Bitpath to selection pool of fonts
        if monoSpaced:
            familyName = 'BitpathMono'
        else:
            familyName = 'BitpathProp'

        bitpathPaths = getFamilyFontPaths(familyName)
        for fontName, fontPath in bitpathPaths.items(): # Merge the dictionaries
            scriptGlobals.fontNamePaths[fontName] = fontPath

    # Remove all italic or roman, depending on setting of [x] Italics checkbox.
    if not Italics:
        for fontName in scriptGlobals.fontNamePaths.keys():
            if 'Italic' in fontName:
                del scriptGlobals.fontNamePaths[fontName]
    elif Italics:
        for fontName in scriptGlobals.fontNamePaths.keys():
            if not 'Italic' in fontName:
                del scriptGlobals.fontNamePaths[fontName] # Remove non-italics

    # Filter types of usage
    for fontName, fontPath in scriptGlobals.fontNamePaths.items():
        if 'Bold' in fontName or 'Black' in fontName:
            scriptGlobals.boldPaths[fontName] = fontPath
            if 'Single' in fontName:
                scriptGlobals.singleBoldPaths[fontName] = fontPath
            else:
                scriptGlobals.doubleBoldPaths[fontName] = fontPath
        else:
            scriptGlobals.lightPaths[fontName] = fontPath
            if 'Single' in fontName:
                scriptGlobals.singleLightPaths[fontName] = fontPath
            else:
                scriptGlobals.doubleLightPaths[fontName] = fontPath

def getColor(index):
    g = globals()
    label = 'Layer_Color_%d' %  index
    #if g[label] is None:
    #    g[label] = (random(), random(), random())
    return g[label]
    
def getFontName(index):
    if scriptGlobals.layerFonts.get(index) is None:
        if index < Layers/2: # First half of layers, use bold/black/shadow as background.
            fontName = choice(scriptGlobals.boldPaths.keys())
        else:
            fontName = choice(scriptGlobals.lightPaths.keys())
        scriptGlobals.layerFonts[index] = fontName
    else:
        fontName = scriptGlobals.layerFonts[index]   
    return fontName
       
# Define method to show a random sample
def drawSample():
    fss = []
    fontSize = None # Calculate from first formatted string size.
    for layerIndex in range(Layers):
        fontName = getFontName(layerIndex)
        fontSize, fs = getFittingString(Sample_Text, fontName, layerIndex, fontSize)
        fss.append(fs)
    drawLayers(fss, fontSize) # Draw layers on several identical frames
            
def getFittingString(t, fontName, layerIndex, fontSize=None):
    # Make formatted string of large type. 
    # Then see if it fits and calculate the fitting size.
    # First guess, to see if constructed formatted string fits.
    initialFontSize = 500 
    glb = globals()
    colorLabel = 'Layer_Color_%d' % layerIndex
    layerColor = getColor(layerIndex)
    if glb.get(colorLabel) is None:
        glb[colorLabel] = NSColor.whiteColor()
        
    try:
        r, g, b, opacity = layerColor.getRed_green_blue_alpha_(None, None, None, None)
    except ValueError:
        r = random()
        g = random()
        b = random()
        opacity = 0.4+0.6*random() # Not totally opaque.
        glb[colorLabel] = NSColor.colorWithCalibratedRed_green_blue_alpha_(r, g, b, opacity)

    if not color:
        r = g = b = random()*0.8
    
    if fontSize is None:
        # Calculate the size for the given string for the selected font/spacing.
        # Then use the resulting with as source to calculate the fitting fontSize.
        fs = context.newString(Sample_Text,
                               style=dict(font=fontName,
                                          fontSize=initialFontSize))
        fsWidth, fsHeight = fs.size()
        fontSize = initialFontSize * (W-2*M) / fsWidth
    # Make new formatted string in fitting fontSize
    fs = context.newString(t, style=dict(font=fontName,
                                         fontSize=fontSize,
                                         textFill=(r, g, b, opacity)))
    return fontSize, fs
               
def drawLayers(fss, fontSize):
    # Draw this layer in a couple of frame
    offsetX = 0
    offsetY = 0
    _, h = fss[0].size()
    h += M
    newPage(W, h)
    fill(Background_Color)
    rect(0, 0, W, h)
    for fs in fss:
        text(fs, (M+offsetX, M+offsetY))
        offsetX += Layer_Offset_X
        offsetY += Layer_Offset_Y

if __name__ == '__main__':

    UI = [
        dict(name='Sample_Text', ui='EditText', args=dict(text=u'Typetr')),
        dict(name='Italics', ui='CheckBox'),
        dict(name='Use_BitPath', ui='CheckBox'), # Optional usage mixture with Bitpath.
        dict(name='Background_Color', ui='ColorWell'),
        #dict(name='Layers', ui='PopUpButton', args=dict(items=('0','1','2','3','4','5','6'))),
        dict(name="Layer_Offset_X", ui="Slider", args=dict(value=0, minValue=-16, maxValue=16)),
        dict(name="Layer_Offset_Y", ui="Slider", args=dict(value=0, minValue=-16, maxValue=16)),
    ]
    for layerIndex in range(Layers):
        UI.append(dict(name='Layer_Color_%d' % layerIndex, ui='ColorWell'))
        
    UI.append(dict(name="Actions", ui="PopUpButton", args=dict(items=('New Random Fonts', 'New Random Color', 'Save'))))
        
    Variable(UI, globals())
           
            
    # If no Bitcount fonts could be found, open the browser on the TypeNetwork shop page and stop this script.
    collectFonts() # Collect available fonts, filter into characteristics, as weight, italic, etc.
    if not scriptGlobals.fontNamePaths:
        os.system('open %s/fonts/%s' % (typetrStoreUrl, 'productus')) #familyName.lower())
    else:
        drawSample()
        #saveImage(EXPORT_PATH) # Save the sample as file or animated gif.

