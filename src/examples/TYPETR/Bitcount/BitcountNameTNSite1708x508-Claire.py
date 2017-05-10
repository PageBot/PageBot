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
#     TODO: Add Variable selection (color selector, checkbox, color wheel)
#
import os
from random import choice

import pagebot
from pagebot.fonttoolbox.objects.family import getFamilyFontPaths
from pagebot import getFormattedString, textBoxBaseLines

typetrStoreUrl = 'https://store.typenetwork.com/foundry/typetr'
EXPORT_PATH = '_export/BitcountLayerCatalogAnimation1708x508-Claire-%d.gif'

USE_BITPATH = False

# Initial sample text. Can be altered in the text box of the popup window.
W = 1708 # Width of the sample image. TypeNetwork preference 2040 x 1020
H = 508 # Height of the sample image
padding = 16 # Padding between text and image side.
#t = u'π-day' #Typetr' # Initial sample string
t = 'Bitcount' # Initial sample string
monoSpaced = True
backgroundColor = (0, 0, 0)#(1, 1, 1) #0.1, 0.2, 0.5
italics = False
color = True
frames = 6
fd = 1 # Frame duration

if monoSpaced:
    familyName = 'BitcountMono'
else:
    familyName = 'BitcountProp'
fontNamePaths = getFamilyFontPaths(familyName) 
if not italics:
    for fontName in fontNamePaths.keys():
        if 'Italic' in fontName or 'Double' in fontName:
            del fontNamePaths[fontName]

animation = [
    (('BoldPlus', 'c4ef4d'),
    ('BoldLineCircle', '5581d9'),
    ('LightSquare', '2e4e8c')),
    
    (('BoldSquare', '5581d9'),
    ('BoldLineSquare', 'c4ef4d'),
    ('BoldPlus', 'fcfc9b'),
    ('BookLineCircle', '2e4e8c')),
    
    (('BoldCircle', '5581d9'),
    ('LightPlus', 'c4ef4d'),
    ('RegularLineCircle', 'c4ef4d')),
    
    (('MediumSquare', '2e4e8c'),
    ('LightSquare', 'c4ef4d'),
    ('BookPlus', 'fcfc9b'))
]
# Define method to show a random sample
def drawSample(name):
    for imageIndex, layers in enumerate(animation):
        newDrawing()
        for index in range(len(layers)):
            fss = []
            for fontName, color in layers[:index+1]:
                fontName = 'BitcountPropSingle-%s' % fontName
                c = (int(color[:2], 16)/256.0,int(color[2:4], 16)/256.0,int(color[4:], 16)/256.0)
                # First half of frames, add
                fss.append(getFittingString(name, fontName, c))
            drawLayers(fss) # Draw layers on several identical frames, using SIngle or Double.
        for index in range(len(layers)-2):
            fss = []
            for fontName, color in layers[:-index-1]:
                fontName = 'BitcountPropSingle-%s' % fontName
                c = (int(color[:2], 16)/256.0,int(color[2:4], 16)/256.0,int(color[4:], 16)/256.0)
                # First half of frames, add
                fss.append(getFittingString(name, fontName, c))
            drawLayers(fss) # Draw layers on several identical frames, using SIngle or Double.
        saveImage(EXPORT_PATH % imageIndex) # Save the sample as file or animated gif.
        print EXPORT_PATH % imageIndex
         
def getFittingString(t, fontName, c):
    # Make formatted string of large type. 
    # Then see if it fits and calculate the fitting size.
    # First guess, to see if constructed formatted string fits.
    
    # Calculate the size for the given string for the selected font/spacing.
    # Then use the resulting with as source to calculate the fitting fontSize.
    initialFontSize = 500 
    fs = getFormattedString(t, None, dict(font=fontName, 
        fontSize=initialFontSize))
    fsWidth, fsHeight = fs.size()
    fontSize =  initialFontSize * (W-3*padding) / fsWidth
    # Make new formatted string in fitting fontSize
    fs = getFormattedString(t, None, dict(font=fontName, 
        fontSize=fontSize, textFill=c))
    return fs
        
def drawLayers(fss):
    # Draw this layer in a couple of frame
    newPage(W, H)
    frameDuration(fd)
    #fill(backgroundColor[0],backgroundColor[1],backgroundColor[2])
    #rect(0, 0, W, H)
    y = 3*padding
    for fs in fss:
        text(fs, (2*padding, y+100))
 
if __name__ == '__main__':    
    # If no Bitcount fonts could be found, open the browser on the TypeNetwork shop page and stop this script.
    if not fontNamePaths:
        os.system('open %s/fonts/%s' % (typetrStoreUrl, 'productus')) #familyName.lower())
    else:
        drawSample(t)
    
    