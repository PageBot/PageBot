# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     LayerCatalogAnimation.py
#
#     The script assumes one or multiple Bitcount fonts to be installed in the system.
#     Otherwise the script will stop, opening the browser on the TypeNetwork store.
#     Purchase Bitcount fonts at https://store.typenetwork.com/foundry/typetr/fonts/bitcount
#     A single user license of Bitcount is $10.10 per font or $101 for the complete package of 300 styles).
#
#     TODO: Add Variation selection (color selector, checkbox, color wheel)
#
import os

import pagebot
from pagebot.fonttoolbox.objects.family import getFamilyFontPaths
from pagebot import getFormattedString, textBoxBaseLines

typetrStoreUrl = 'https://store.typenetwork.com/foundry/typetr'
EXPORT_PATH = '_export/BitcountLayerCatalogAnimation.gif'

USE_BITPATH = False

# Initial sample text. Can be altered in the text box of the popup window.
W = 500 # Width of the sample image
H = 200 # Height of the sample image
M = 16 # Margin between text and image side.
t = u'π-day' #Typetr' # Initial sample string
monoSpaced = True
backgroundColor = (0, 0, 0)#(1, 1, 1) #0.1, 0.2, 0.5
italics = False
layers = 4
color = True
frameLength = 4 # Number of 
frames = 8

# Bitcount is made from 3 spacing sets: 
#    - Monospaced (Grid, Mono)
#    - Proportional (Prop)
# Define the family name of fonts that we want to use, 
# including the type of spacing.
if monoSpaced:
    familyName = 'BitcountMono'
else:
    familyName = 'BitcountProp'
# Just get paths of the fonts, not the Font objects. 
# We want quick interactive response.
# Call imported method, to find all installed Bitcount fonts.
fontNamePaths = getFamilyFontPaths(familyName) 
if not italics:
    for fontName in fontNamePaths.keys():
        if 'Italic' in fontName:
            del fontNamePaths[fontName]

if USE_BITPATH:
    # Add Bitpath to selection pool of fonts
    if monoSpaced:
        familyName = 'BitpathMono'
    else:
        familyName = 'BitpathProp'

    bitpathPaths = getFamilyFontPaths(familyName)
    for fontName, fontPath in bitpathPaths.items(): # Merge the dictionaries
        if not italics and 'Italic' in fontName:
            continue
        fontNamePaths[fontName] = fontPath

# Define method to show a random sample
def drawSample():
    fss = []
    for frame in range(frames):
        fontName = choice(fontNamePaths.keys())
        fss.append(getFittingString(t, fontName))
        if len(fss) == layers: 
            drawLayers(fss) # Draw layers on several identical frames
            # Remove first layer
            fss = fss[1:]
            
def getFittingString(t, fontName):
    # Make formatted string of large type. 
    # Then see if it fits and calculate the fitting size.
    # First guess, to see if constructed formatted string fits.
    initialFontSize = 500 
    if color:
        r = 0.5+random()*0.5
        g = 0.5+random()*0.5
        b = 0.5+0.5*random()
    else:
        r = g = b = random()*0.8
    opacity = 0.4+0.6*random() # Not totally opaque.
    
    # Calculate the size for the given string for the selected font/spacing.
    # Then use the resulting with as source to calculate the fitting fontSize.
    fs = getFormattedString(t, None, dict(font=fontName, 
        fontSize=initialFontSize))
    fsWidth, fsHeight = fs.size()
    fontSize =  initialFontSize * (W-3*M) / fsWidth
    # Make new formatted string in fitting fontSize
    fs = getFormattedString(t, None, dict(font=fontName, 
        fontSize=fontSize, textFill=(r, g, b, opacity)))
    return fs
        
def drawLayers(fss):
    # Draw this layer in a couple of frame
    _, h = fss[0].size()
    h += M
    for n in range(frameLength):
        newPage(W, h)
        fill(backgroundColor[0],backgroundColor[1],backgroundColor[2])
        rect(0, 0, W, h)
        for fs in fss:
            text(fs, (2*M, 3*M))
     
# If no Bitcount fonts could be found, open the browser on the TypeNetwork shop page and stop this script.
if not fontNamePaths:
    os.system('open %s/fonts/%s' % (typetrStoreUrl, 'productus')) #familyName.lower())
else:
    for frame in range(frames):                
        drawSample()
    saveImage(EXPORT_PATH) # Save the sample as file or animated gif.