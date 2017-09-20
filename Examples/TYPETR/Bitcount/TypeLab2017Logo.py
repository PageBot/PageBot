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
#     TypeLab2017Logo.py
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
from pagebot import newFS, textBoxBaseLines
from pagebot.fonttoolbox.objects.font import Font
#from pagebot.toolbox.transformer import path2ScriptId

def path2ScriptId(path):
    u"""Answer the scriptId, derived from the __file__ of the main source."""
    return path.split('/src/')[-1]

# Kinda hack, storing in empty module, to prevent globals to re-initialized, if variables are changed.
scriptGlobals = pagebot.getGlobals(path2ScriptId(__file__))

Random_Features = False
# Optional using Bitpath family, mixed with Bitcount
Use_BitPath = False
# Initial sample text. Can be altered in the text box of the popup window.
W = 800 # Width of the sample image. Heights is calculated from string.
 # Height of the sample image
ML = 2 # Margin between text and image side in pixels.
MR = 1
MT = 0 # Above ascender, depending on extended ascender feature
MB = 1 # Below descender, depending on extended descender feature

LAYER_OPTIONS = ('1', '2', '3', '4', '5')
# Tracking in amount of pixels
TRACKING_OPTIONS = ('-2', '-1', '0', '1', '2', '3', '4', '5')

Save_PDF = True
Sample_Text = u'TypeLab' # Initial sample string
Spacing_Variant = True #random()<0.5
Tracking = 0
Background_Color = NSColor.blackColor()
Italic = False
Italic_Shapes = False # [ss08]
Condensed = False # [ss07] Excludes Double if selected
Smallcaps = False # [smcp]
Caps_As_Smallcaps = False # [c2cs]
Extended_Ascenders = False # [ss01]
Extended_Capitals = False # [ss02]
Extended_Descenders = False # [ss03]
Contrast_Pixel = False # [ss04] and [ss05]
Alternative_g = False # [ss09]
LC_Figures = False # [onum]
Layers = 2 # Popup list index. Default is 3
Gray_Scale = True
Slashed_Zero = True # [zero]
Layer_Offset_X = -3
Layer_Offset_Y = 3

familyName = 'Bitcount'
if Spacing_Variant:
    searchName = familyName + 'Mono'
else:
    # Only works in layers, if also Single/Double is selected.
    searchName = familyName + 'Prop'

lightPaths = {}
boldPaths = {}
singleLightPaths = {}
singleBoldPaths = {}
doubleLightPaths = {}
doubleBoldPaths = {}

typetrStoreUrl = 'https://store.typenetwork.com/foundry/typetr'
EXPORT_DIR = '_export/BitcountLayerCatalog/'
EXPORT_IMAGES = EXPORT_DIR + 'images/'

# Make sure the export directory exists
if not os.path.exists(EXPORT_IMAGES):
    os.makedirs(EXPORT_IMAGES)

def path2ScriptId(path):
    u"""Answer the scriptId, derived from the __file__ of the main source."""
    return path.split('/src/')[-1]

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
        if Spacing_Variant:
            familyName = 'BitpathMono'
        else:
            familyName = 'BitpathProp'

        bitpathPaths = getFamilyFontPaths(familyName)
        for fontName, fontPath in bitpathPaths.items(): # Merge the dictionaries
            fontNamePaths[fontName] = fontPath

    # Remove all italic or roman, depending on setting of [x] Italic checkbox.
    if not Italic:
        for fontName in fontNamePaths.keys():
            if 'Italic' in fontName:
                del fontNamePaths[fontName]
    elif Italic:
        for fontName in fontNamePaths.keys():
            if not 'Italic' in fontName:
                del fontNamePaths[fontName] # Remove non-italic

    # Excluse Double if Condensed feature is selected
    if Condensed:
        for fontName in fontNamePaths.keys():
            if 'Double' in fontName:
                del fontNamePaths[fontName]
                
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
    print fontName
    return Font(fontNamePaths[fontName])
       
def getFontName(index):
    u"""Intelligent random select of a font. Lower layers get Bold or Black.
    Higher layers get lighter weights. Anser the Font instance."""
    if index < (Layers+1)/2: # First half of layers, use bold/black/shadow as background.
        fontName = choice(boldPaths.keys())
    else:
        fontName = choice(lightPaths.keys())
    return fontName
       
# Define method to show a random sample
def drawSample():
    layers = {}
    fontSize = None
    for layerIndex in range(Layers+1):
        layers[layerIndex] = layer = dict(offsetX=Layer_Offset_X, offsetY=Layer_Offset_Y)
        layer['fontName'] = fontName = getFontName(layerIndex)
        layer['font'] = getFont(fontName)
        fontSize, fs = getFittingString(Sample_Text, fontName, layerIndex, fontSize)
        layer['fontSize'] = fontSize
        layer['pixel'] = fontSize/10
        layer['text'] = fs
    drawLayers(layers) # Draw layers on several identical frames
    # Explain from parameters
    explain(layers)
          
def getFittingString(t, fontName, layerIndex, fontSize):
    # Make formatted string of large type. 
    # Then see if it fits and calculate the fitting size.
    # First guess, to see if constructed formatted string fits.
    initialFontSize = 500   
    c1 = (0x30/256.0, 0xf1/256.0, 0xba/256.0)      
    c2 = (0xff/256.0, 0x00/256.0, 0x99/256.0)      
    if Gray_Scale:
        r = g = b = 0.5 + 0.5*random()
        opacity = 0.7+0.3*random() # Not totally opaque.
    else:
        if layerIndex == 0: # Never black as first or single layer
            c = choice((c1, c2, (1, 1, 1)))
        else:
            c = choice((c1, c2, (0, 0, 0), (1, 1, 1)))
        r, g, b = c
        opacity = 1
        #opacity = 0.4+0.6*random() # Not totally opaque.
    
    # Contrast pixel behavior depends on Single or Mono
    features = dict(zero=Slashed_Zero, smcp=Smallcaps, c2sc=Caps_As_Smallcaps, ss08=Italic_Shapes,
        ss07=Condensed, ss01=Extended_Ascenders, ss02=Extended_Capitals, ss03=Extended_Descenders,
        ss04=Contrast_Pixel, ss05=not Contrast_Pixel, ss09=Alternative_g, onum=LC_Figures)
    
    rTracking = int(Tracking-2) * 0.1
    if layerIndex == 0:
        # Calculate the size for the given string for the selected font/spacing.
        # Then use the resulting with as source to calculate the fitting fontSize.
        fs = newFS(Sample_Text, None, dict(font=fontName, rTracking=rTracking,
            fontSize=initialFontSize, openTypeFeatures=features))
        fsWidth, fsHeight = fs.size()
        fontSize = int(round(initialFontSize * (W-ML-MR) / fsWidth))
    # Make new formatted string in fitting fontSize
    fs = newFS(Sample_Text, None, dict(font=fontName, rTracking=rTracking,
        fontSize=fontSize, textFill=(r, g, b, opacity), openTypeFeatures=features))
    return fontSize, fs

S_HEADLINES = [
    u"""## %(familyName)s %(whatIsIt)s in %(layers)d %(color)s layers.""",   
    u"""## %(layers)d layers make %(color)s %(whatIsIt)s with %(familyName)s.""",   
]
S_WHAT_IS_IT = ['design', 'logo', 'symbol', 'name']

def explain(layers):
    # Try to compose a real readable MD-text, commenting about the current "design".
    if Gray_Scale:
        colorLabel = 'gray scale'
    elif Layers > 2:
        colorLabel = 'colorful'
    elif Layers == 1:
        colorLabel = 'single color'
    else:
        colorLabel = 'color'
    parms = dict(familyName=familyName, layers=len(layers), whatIsIt=choice(S_WHAT_IS_IT),
        color=colorLabel)
    print parms
    print choice(S_HEADLINES) % parms
    # More could go here
                 
def drawLayers(layers):
    # Draw this layer in a couple of frame
    # Calculate the pixel size. 100 units on 1000 Em. 
    #pixelSize = 
    w, h = layers[0]['text'].size()
    pixel = layers[0]['pixel']
    w += ML*pixel + MR*pixel
    h += MT*pixel + MB*pixel
    x = ML*pixel
    y = (2+MB)*pixel
    if Extended_Ascenders or Extended_Capitals:
        h += pixel
    if Extended_Descenders:
        h += pixel
    newPage(w, h)
    fill(Background_Color)
    rect(0, 0, w, h)
    for layerIndex, layer in sorted(layers.items()):
        text(layer['text'], (x, y))
        x += layer['offsetX']
        y += layer['offsetY']

def export():
    # Find non-existing name, starting from #0.
    for n in range(10000):
        if Save_PDF:
            EXTENSION = 'pdf'
        else:
            EXTENSION = 'png'
        EXPORT_PATH = EXPORT_IMAGES + 'TypeLabLogo%04d.'+EXTENSION
        filePath = EXPORT_PATH % n
        if not os.path.exists(filePath):
            print 'AAA', filePath
            saveImage(filePath) # Save the sample as png.
            break # Make sure to break, or else 10000 copies are created.

if __name__ == '__main__':
    UI = [
        dict(name='Save_PDF', ui='CheckBox'),
        dict(name='Sample_Text', ui='EditText', args=dict(text=Sample_Text)),
        dict(name='Spacing_Variant', ui='PopUpButton', args=dict(items=('Mono', 'Prop'))),
        dict(name='Tracking', ui='PopUpButton', args=dict(items=TRACKING_OPTIONS)),
        dict(name='Layers', ui='PopUpButton', args=dict(items=LAYER_OPTIONS)),
        dict(name='Italic', ui='CheckBox'),
        dict(name='Gray_Scale', ui='CheckBox'),
        dict(name='Use_BitPath', ui='CheckBox'), # Optional usage mixture with Bitpath if installed.
        dict(name='Random_Features', ui='CheckBox'), # If random features, omit rest of choices
    ]
    if not hasattr(scriptGlobals, 'randomFeatures'):
        scriptGlobals.random_Features = Random_Features

    if not scriptGlobals.random_Features:
        UI.append(dict(name='Italic_Shapes', ui='CheckBox')) # [ss08]
        UI.append(dict(name='Condensed', ui='CheckBox')) # Used Condensed feaure. Excludes "Double" Bitcount font selection.
        UI.append(dict(name='Slashed_Zero', ui='CheckBox')) # Used Condensed feaure. Excludes "Double" Bitcount font selection.
        UI.append(dict(name='Smallcaps', ui='CheckBox')) # [smcp]
        UI.append(dict(name='Caps_As_Smallcaps', ui='CheckBox')) # [c2sc].
        UI.append(dict(name='Extended_Ascenders', ui='CheckBox')) # [ss01].
        UI.append(dict(name='Extended_Capitals', ui='CheckBox')) # [ss02].
        UI.append(dict(name='Extended_Descenders', ui='CheckBox')) # [ss03].
        UI.append(dict(name='Contrast_Pixel', ui='CheckBox')) # [ss04].
        UI.append(dict(name='Alternative_g', ui='CheckBox')) # [ss09].
        UI.append(dict(name='LC_Figures', ui='CheckBox')) # [onum].
    else:
        Italic_Shapes = random() < 0.2 # [ss08]
        Condensed = random() < 0.2 # [ss07]
        Slashed_Zero = random() < 0.5 # [zero]
        Smallcaps = random() < 0.3 # [smcp]
        Caps_As_Smallcaps = random() < 0.1 # [c2sc]
        Extended_Ascenders = random() < 0.7 # [ss01]
        Extended_Capitals = random() < 0.5 # [ss02]
        Extended_Descenders = random() < 0.7 # [ss03]
        Contrast_Pixel = random() < 0.5 # [ss04]
        Alternative_g = random() < 0.3 # [ss09]
        LC_Figures = random() < 0.3 # [onum]      

    Variable(UI, globals())

    # Store Italics flag, so we can test if it changed.
    scriptGlobals.random_Features = Random_Features
        
                         
    # If no Bitcount fonts could be found, open the browser on the TypeNetwork shop page and stop this script.
    fontNamePaths = collectFonts(searchName) # Collect available fonts, filter into characteristics, as weight, italic, etc.
    if not fontNamePaths:
        print 'The %s family is not installed in your system. How about buying a license @typenetwork?' % familyName
        os.system('open %s/fonts/%s' % (typetrStoreUrl, familyName.lower()))
    else:
        drawSample()
        export()
        
