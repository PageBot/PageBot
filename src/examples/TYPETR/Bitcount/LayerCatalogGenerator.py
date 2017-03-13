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
    myglobals.layerFonts = {0: None, 1:None, 2:None, 3:None, 4:None, 5:None} # 
 
# Kinda hack, storing in empty module, to prevent globals to re-initialized, if variables are changed.
import myglobals

if not hasattr(myglobals, 'initialized'):
    myglobals.initialized = True
    # Store Italics flag, so we can test if it changed.
    myglobals.italics = Italics
    # Store Use_BitPath flag, so we can test if it changed.
    myglobals.use_BitPath = Use_BitPath
    # Currently (random) selected fonts per layer
    clearFonts() # Initialize font choice, so new random fonts will be selected.
    myglobals.layerColors = {0:NSColor.grayColor(), 1:NSColor.grayColor(), 2:NSColor.grayColor(), 
        3:NSColor.grayColor(), 4:NSColor.grayColor(), 5:NSColor.grayColor()} # 
    # Collections of avaiable fonts, filtered by weight and stem-pixel 
    myglobals.fontNamePaths = {}
    myglobals.lightPaths = {} # Not Bold or Black
    myglobals.boldPaths = {}
    myglobals.singleLightPaths = {} # Not Bold or Black
    myglobals.singleBoldPaths = {}
    myglobals.doubleLightPaths = {} # Not Bold or Black
    myglobals.doubleBoldPaths = {}

typetrStoreUrl = 'https://store.typenetwork.com/foundry/typetr'
EXPORT_DIR = '_export/BitcountLayerCatalog/'
EXPORT_IMAGES = EXPORT_DIR + 'images'
# Make sure the export directory exists
if not os.path.exists(EXPORT_IMAGES):
    os.makedirs(EXPORT_IMAGES)


if Italics != myglobals.italics: # Did it change?
    myglobals.italics = Italics
    # Force new random selection of fonts.
    clearFonts()

if Use_BitPath != myglobals.use_BitPath: # Did it changed?
    myglobals.use_BitPath = Use_BitPath
    # Force new random selection of fonts.
    clearFonts()

# Compare stored colors
for layerIndex in range(Layers):
    if globals()['Layer_Color_%d' % layerIndex] is None:
        globals()['Layer_Color_%d' % layerIndex] = myglobals.layerColors[layerIndex]
    elif myglobals.layerColors[layerIndex] != globals()['Layer_Color_%d' % layerIndex]:
        myglobals.layerColors[layerIndex] = globals()['Layer_Color_%d' % layerIndex]
          
def collectFonts():
    # Bitcount is made from 3 spacing sets: 
    #    - Monospaced (Grid, Mono)
    #    - Proportional (Prop)
    # Define the family name of fonts that we want to use, 
    # including the type of spacing.
    if myglobals.fontNamePaths: # Already installed, skip.
        return
        
    if monoSpaced:
        familyName = 'BitcountMono'
    else:
        familyName = 'BitcountProp' # Only works in layers, if also Single/Double is selected.
    
    # Just get paths of the fonts, not the Font objects. 
    # We want quick interactive response.
    # Call imported method, to find all installed Bitcount fonts.
    myglobals.fontNamePaths = getFamilyFontPaths(familyName) 
        
    for fontName in myglobals.fontNamePaths:
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
            myglobals.fontNamePaths[fontName] = fontPath

    # Remove all italic or roman, depending on setting of [x] Italics checkbox.
    if not Italics:
        for fontName in myglobals.fontNamePaths.keys():
            if 'Italic' in fontName:
                del myglobals.fontNamePaths[fontName]
    elif Italics:
        for fontName in myglobals.fontNamePaths.keys():
            if not 'Italic' in fontName:
                del myglobals.fontNamePaths[fontName] # Remove non-italics

    # Filter types of usage
    for fontName, fontPath in myglobals.fontNamePaths.items():
        if 'Bold' in fontName or 'Black' in fontName:
            myglobals.boldPaths[fontName] = fontPath
            if 'Single' in fontName:
                myglobals.singleBoldPaths[fontName] = fontPath
            else:
                myglobals.doubleBoldPaths[fontName] = fontPath
        else:
            myglobals.lightPaths[fontName] = fontPath
            if 'Single' in fontName:
                myglobals.singleLightPaths[fontName] = fontPath
            else:
                myglobals.doubleLightPaths[fontName] = fontPath

def getColor(index):
    g = globals()
    label = 'Layer_Color_%d' %  index
    #if g[label] is None:
    #    g[label] = (random(), random(), random())
    return g[label]
    
def getFontName(index):
    if myglobals.layerFonts.get(index) is None:
        if index < Layers/2: # First half of layers, use bold/black/shadow as background.
            fontName = choice(myglobals.boldPaths.keys())
        else:
            fontName = choice(myglobals.lightPaths.keys())
        myglobals.layerFonts[index] = fontName
    else:
        fontName = myglobals.layerFonts[index]   
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
        
    if layerColor is not None:
        r, g, b, opacity = layerColor.getRed_green_blue_alpha_(None, None, None, None)
    else:
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
        fs = getFormattedString(Sample_Text, style=dict(font=fontName, 
            fontSize=initialFontSize))
        fsWidth, fsHeight = fs.size()
        fontSize = initialFontSize * (W-2*M) / fsWidth
    # Make new formatted string in fitting fontSize
    fs = getFormattedString(t, style=dict(font=fontName, 
        fontSize=fontSize, textFill=(r, g, b, opacity)))
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
if not myglobals.fontNamePaths:
    os.system('open %s/fonts/%s' % (typetrStoreUrl, 'productus')) #familyName.lower())
else:
    drawSample()
    #saveImage(EXPORT_PATH) # Save the sample as file or animated gif.