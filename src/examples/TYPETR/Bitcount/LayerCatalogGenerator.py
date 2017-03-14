# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     LayerCatalogGenerator.py
#
#     The script assumes one or multiple Bitcount fonts to be installed in the system.
#     Otherwise the script will stop, opening the browser on the TypeNetwork store.
#     Purchase Bitcount fonts at https://store.typenetwork.com/foundry/typetr/fonts/bitcount
#     A single user license of Bitcount is $10.10 per font or $101 for the complete package of 300 styles).
#
from AppKit import NSColor
import os

import pagebot
from pagebot.fonttoolbox.objects.family import getFamilyFontPaths
from pagebot import getFormattedString, textBoxBaseLines
from pagebot.fonttoolbox.objects.font import Font

# Optional using Bitpath family, mixed with Bitcount
Use_BitPath = True
# Initial sample text. Can be altered in the text box of the popup window.
W = 500 # Width of the sample image. Heights is calculated from string.
 # Height of the sample image
M = 32 # Margin between text and image side.
Sample_Text = u'Typetr' # Initial sample string
monoSpaced = True #random()<0.5
Background_Color = NSColor.blackColor()
Italics = False
Layers = 3
Color = True
Layer_Offset_X = -1
Layer_Offset_Y = 2

familyName = 'Bitcount'
if monoSpaced:
    searchName = familyName + 'Mono'
else:
    # Only works in layers, if also Single/Double is selected.
    searchName = familyName + 'Prep'

lightPaths = {}
boldPaths = {}
singleLightPaths = {}
singleBoldPaths = {}
doubleLightPaths = {}
doubleBoldPaths = {}

typetrStoreUrl = 'https://store.typenetwork.com/foundry/typetr'
EXPORT_DIR = '_export/BitcountLayerCatalog/'
EXPORT_IMAGES = EXPORT_DIR + 'images/'
EXPORT_PATH = EXPORT_IMAGES + 'LayerCatalogImage%04d.png'

# Make sure the export directory exists
if not os.path.exists(EXPORT_IMAGES):
    os.makedirs(EXPORT_IMAGES)

def collectFonts(searchName):
    # Bitcount is made from 3 spacing sets: 
    #    - Monospaced (Grid, Mono)
    #    - Proportional (Prop)
    # Define the family name of fonts that we want to use, 
    # including the type of spacing.
        
    
    # Just get paths of the fonts, not the Font objects. 
    # We want quick interactive response.
    # Call imported method, to find all installed Bitcount fonts.
    fontNamePaths = getFamilyFontPaths(searchName) 
        
    for fontName in fontNamePaths:
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
            fontNamePaths[fontName] = fontPath

    # Remove all italic or roman, depending on setting of [x] Italics checkbox.
    if not Italics:
        for fontName in fontNamePaths.keys():
            if 'Italic' in fontName:
                del fontNamePaths[fontName]
    elif Italics:
        for fontName in fontNamePaths.keys():
            if not 'Italic' in fontName:
                del fontNamePaths[fontName] # Remove non-italics

    # Filter types of usage
    for fontName, fontPath in fontNamePaths.items():
        if 'Bold' in fontName or 'Black' in fontName:
            boldPaths[fontName] = fontPath
            if 'Single' in fontName:
                singleBoldPaths[fontName] = fontPath
            else:
                doubleBoldPaths[fontName] = fontPath
        else:
            lightPaths[fontName] = fontPath
            if 'Single' in fontName:
                singleLightPaths[fontName] = fontPath
            else:
                doubleLightPaths[fontName] = fontPath
    return fontNamePaths
    
def getColor(index):
    g = globals()
    label = 'Layer_Color_%d' %  index
    #if g[label] is None:
    #    g[label] = (random(), random(), random())
    return g[label]

def getFont(fontName):
    u"""Answer the Font instance, so we can get more information about features, etc."""
    return Font(fontNamePaths[fontName])
       
def getFontName(index):
    u"""Intelligent random select of a font. Lower layers get Bold or Black.
    Higher layers get lighter weights. Anser the Font instance."""
    if index < Layers/2: # First half of layers, use bold/black/shadow as background.
        fontName = choice(boldPaths.keys())
    else:
        fontName = choice(lightPaths.keys())
    return fontName
       
# Define method to show a random sample
def drawSample():
    layers = {}
    fontSize = None # Calculate from first formatted string size.
    for layerIndex in range(Layers):
        layers[layerIndex] = layer = dict(offsetX=Layer_Offset_X, offsetY=Layer_Offset_Y)
        layer['fontName'] = fontName = getFontName(layerIndex)
        layer['font'] = getFont(fontName)
        fontSize, fs = getFittingString(Sample_Text, fontName, layerIndex, fontSize)
        layer['fontSize'] = fontSize
        layer['text'] = fs
    drawLayers(layers) # Draw layers on several identical frames
    # Explain from parameters
    explain(layers)
          
def getFittingString(t, fontName, layerIndex, fontSize=None):
    # Make formatted string of large type. 
    # Then see if it fits and calculate the fitting size.
    # First guess, to see if constructed formatted string fits.
    initialFontSize = 500         
    if Color:
        r = random()
        g = random()
        b = random()
    else:
        r = g = b = random()*0.8
    opacity = 0.4+0.6*random() # Not totally opaque.
    
    if fontSize is None:
        # Calculate the size for the given string for the selected font/spacing.
        # Then use the resulting with as source to calculate the fitting fontSize.
        fs = getFormattedString(Sample_Text, style=dict(font=fontName, 
            fontSize=initialFontSize))
        fsWidth, fsHeight = fs.size()
        fontSize = initialFontSize * (W-2*M) / fsWidth
    # Make new formatted string in fitting fontSize
    fs = getFormattedString(t, style=dict(font=fontName, 
        fontSize=fontSize, textFill=(r, g, b, opacity)))
    return fontSize, fs

def explain(layers):
    for layerIndex, layer in sorted(layers.items()):
        print layer
        print listOpenTypeFeatures(fontName=layer['fontName'])
        #oprint layer['font'].features
                 
def drawLayers(layers):
    # Draw this layer in a couple of frame
    x = M
    y = M
    _, h = layers[0]['text'].size()
    h += M/2
    newPage(W, h)
    fill(Background_Color)
    rect(0, 0, W, h)
    for layerIndex, layer in sorted(layers.items()):
        text(layer['text'], (x, y))
        x += layer['offsetX']
        y += layer['offsetY']

def export():
    # Find non-existing name
    for n in range(10000):
        filePath = EXPORT_PATH % n
        if not os.path.exists(filePath):
            saveImage(filePath) # Save the sample as png.
            break # Make sure to break, or else 10000 copies are created.
                    
# If no Bitcount fonts could be found, open the browser on the TypeNetwork shop page and stop this script.
fontNamePaths = collectFonts(searchName) # Collect available fonts, filter into characteristics, as weight, italic, etc.
if not fontNamePaths:
    os.system('open %s/fonts/%s' % (typetrStoreUrl, familyName.lower()))
else:
    drawSample()
    export()
