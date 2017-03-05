# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     family.py
#
#     Implements a family collestion of Style instances.
#
from drawBot import installedFonts
from pagebot.fonttoolbox.objects.font import Font, getFontPathOfFont

def getFamilies(familyPaths):
    u"""Construct a dictionary of Family instances from dictionary familyPaths. It is assumed that all paths
    are valied to font files. Force key in family from dictionary familyPaths, instead of font.info.styleName.
    What is best practice? Keep as option?
    
    Example format of familyPaths dictionary:
    LIB_PATH = '/Library/Fonts/'
    SOME_SYSTEM_FONTS = {
    # Let's try some plain OSX system fonts, while they are still there (not variation yet).
    'Georgia': dict(regular=LIB_PATH+'Georgia.ttf', bold=LIB_PATH+'Georgia Bold.ttf', 
                    italic=LIB_PATH+'Georgia Italic.ttf', boldItalic=LIB_PATH+'Georgia Bold Italic.ttf'),
    'Verdana': dict(regular=LIB_PATH+'Verdana.ttf', bold=LIB_PATH+'Verdana Bold.ttf', 
                    italic=LIB_PATH+'Verdana Italic.ttf', boldItalic=LIB_PATH+'Verdana Bold Italic.ttf'),
    }
    """
    families = {} 
    for familyName, fontPaths in familyPaths.items():
        if not familyName in families:
            families[familyName] = Family(familyName)
        for styleName, fontPath in fontPaths.items():
            print '@@@@', styleName, fontPath
            font = Font(fontPath, styleName)
            families[familyName].addFont(font, styleName) # Force style name from dict, instead of font.info.styleName 
    return families

def getSystemFontPaths():
    u"""Answer the cleaned list of installed font names."""
    fontPaths = []
    for fontName in installedFonts():
        if not fontName.startswith('.'):
            fontPaths.append(getFontPathOfFont(fontName))
    return fontPaths

def guessFamilies(styleNames):
    u"""Find the family relation of all fonts in the list. Note that this cannot be a 100% safe guess.
    Answer a dictionary with Family instances. Key is family name."""
    families = {} # Keys is guessed family name.

    for styleName in styleNames:
        if styleName.startswith('.'): # Filter the system fonts that has a name with initial "."
            continue
        path = getFontPathOfFont(styleName)
        # Could have an extension like .ttf or .otf, by OSX system font don't have an extension.
        # o we just try to open the plain file and see how that goes.
        # Try to open the font in font tools, so we have access to a lot of information for our proof.
        # Create Style instance, as storage within our page composition passes.
        font = Font(path, styleName)
        if font.info is None:
            continue # Could not open the font file.            
        # Skip if there is not a clear family name and style name derived from FontInfo    
        if  font.info.familyName and font.info.styleName:
            # Make a family collection of style names, if not already there.
            if not font.info.familyName in families: 
                families[font.info.familyName] = Family(font.info.familyName)
            # Store the style name and path in the family collection.
            families[font.info.familyName].addFont(font) 

    return families 

class Family(object):
    def __init__(self, name):
        self.name = name
        self.fonts = {} # Key is font name. Value is Font instances.
        self.installedFonts = {} # DrawBot name as key. Value is same Font instance.

    def __len__(self):
        return len(self.fonts)
    
    def __getitem__(self, fontName):
        return self.fonts[fontName]
    
    def install(self, fontKeys=None):
        u"""Install all fonts of the family in DrawBot, if not alreadythere."""
        if fontKeys is None:
            fontKeys = self.fonts.keys()

        for fontKey in fontKeys:
            font = self.fonts[fontKey]
            if not fontKey in self.installedFonts: # Only if not already installed.
                fontName = font.install()
            self.installedFonts[fontName] = fontKey

    def addFont(self, font, key=None):
        if key is None:
            key = font.info.styleName
        assert not key in self.fonts, ('Font "%s" already in family "%s"' % (key, self.fonts.keys()))
        self.fonts[key] = font
        
    def getRegularFont(self):
        # Answer the style that has width/weight closest to 500 and angle is closest to 0
        targetWeight = targetWidth = 500
        targetAngle = 0
        regularFont = None
        for font in self.fonts.values(): # Scan through all, no particular oder.
            if font is None: # Take the first to compare with.
                regularFont = font
                continue
            # Find style that has width/weight/angle that is closest to the middle 500 value 
            # and closest to angle == 0
            if (abs(targetWeight - font.info.weightClass) < abs(targetWeight - font.info.weightClass) or
               abs(targetWidth - font.info.widthClass) < abs(targetWidth - font.info.widthClass) or
               abs(targetAngle - font.info.italicAngle) < abs(targetAngle - font.info.italicAngle)):
               regularFont = font
        return regularFont 
            
  