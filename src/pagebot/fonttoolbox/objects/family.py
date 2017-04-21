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
from pagebot.toolbox.transformer import path2Name

def getFamilies(familyPaths):
    u"""Construct a dictionary of Family instances from dictionary familyPaths. It is assumed that all paths
    are valied to font files. Force key in family from dictionary familyPaths, instead of font.info.styleName.
    What is best practice? Keep as option?
    
    Example format of familyPaths dictionary:
    LIB_PATH = '/Library/Fonts/'
    SOME_SYSTEM_FONTS = {
    # Let's try some plain OSX system fonts, while they are still there (not variable yet).
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
            font = Font(fontPath, styleName)
            families[familyName].addFont(font, styleName) # Force style name from dict, instead of font.info.styleName 
    return families

def getFamilyFontPaths(familyName):
    # Collect the DrawBot names of all available fonts for the named family, that are installed in the system.
    fontPaths = {} # Dictionary, where key is the DrawBot font name, value is the OS path of the font file.
    for fontName in installedFonts(): # Answers complete list of all installed fonts.
        if familyName in fontName: # If this is a with with the familyName that we are looking for...
            fontPaths[fontName] = getFontPathOfFont(fontName) # Store the name and find the font path name.
    return fontPaths #  Answer the dictionary. This is empty, if no Bitcount fonts are installed now.

def getFamilyFonts(familyName):
    # Collect the DrawBot names of all available fonts for the named family, that are installed in the system.
    fonts = {} # Dictionary, where key is the DrawBot font name, value is the OS path of the font file.
    for fontName in installedFonts(): # Answers complete list of all installed fonts.
        if familyName in fontName: # If this is a with with the familyName that we are looking for...
            fontPath = getFontPathOfFont(fontName)
            if fontPath is not None:
                fonts[fontName] = Font(fontPath) # Store the name and find the font path name.
    return fonts #  Answer the dictionary. This is empty, if no Bitcount fonts are installed now.

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
    def __init__(self, name, fontPaths=None, fontStyles=None):
        u"""The Family instance is a container of related Font instances. There are 3 levels of access: file name, style name
        (either from font.info.styleName or defined in fontStyles attributes) and by DrawBot name if the font is installed.
        The optional fontPaths is a list of file paths. The optional fontStyles is a dictionary with format 
        dict(Regular=<fontPath>, Italic=<fontPath>, ...)
        """
        assert fontPaths is None or fontStyles is None # If defined, cannot be defined both.
        self.name = name
        self.fonts = {} # Key is font name. Value is Font instances.
        self.fontStyles = {} # Key is font.info.styleName. Value is list of fonts (there can be overlapping style names).
        self.installedFonts = {} # DrawBot name as key. Value is same Font instance.
        # If any font paths given, open the fonts.
        if fontPaths is not None:
            for fontPath in fontPaths:
                self.addFont(Font(fontPath)) # Use file name as key
        elif fontStyles is not None:
            for fontStyle, fontPath in fontStyles.items():
                self.addFont(Font(fontPath), fontStyle=fontStyle)

    def __repr__(self):
        return '<PageBot Family %s>' % self.name

    def __len__(self):
        return len(self.fonts)
    
    def __getitem__(self, fontName):
        return self.fonts[fontName]
    
    def install(self, fontKeys=None):
        u"""Install all fonts of the family in DrawBot, if not alreadythere."""
        if fontKeys is None: # fontKey is the font file name.
            fontKeys = self.fonts.keys()

        for fontKey in fontKeys:
            font = self.fonts[fontKey]
            if not fontKey in self.installedFonts: # Only if not already installed.
                fontName = font.install()
            self.installedFonts[fontName] = fontKey

    def addFont(self, font, fontKey=None, fontStyle=None):
        if fontKey is None:
            fontKey = path2Name(font.path) # This must be unique in the family, used as key in self.fonts.
        assert not fontKey in self.fonts, ('Font "%s" already in family "%s"' % (fontKey, self.fonts.keys()))
        if fontStyle is None:
            fontStyle = font.info.styleName # It is allowed to have multiple fonts with the same style name.
        # Store the font under unique fontKey.
        self.fonts[fontKey] = font
        # Create list entry for fontStyle, if it does not exist.
        if not fontStyle in self.fontStyles:
            self.fontStyles[fontStyle] = [] # Keep list, there may be fonts with the same style name.
        self.fontStyles[fontStyle].append(font)
        
    def getRegularFont(self):
        u"""Try to find a font that is closest to style "Normal" or "Regular".
        Otherwise answer the font that has weight/width closest to (400, 5) and angle is closest to 0."""
        targetWeight = 400
        targetWidth = 5
        targetAngle = 0
        regularFont = None
        for font in self.fonts.values(): # Scan through all fonts, no particular order.
            if regularFont is None: # Take the first to compare with, best guess
                regularFont = font
                continue
            # Find style that has weight/width/angle that is closer to the target values.
            if (abs(targetWeight - font.info.weightClass) < abs(targetWeight - regularFont.info.weightClass) or
               abs(targetWidth - font.info.widthClass) < abs(targetWidth - regularFont.info.widthClass) or
               abs(targetAngle - font.info.italicAngle) < abs(targetAngle - regularFont.info.italicAngle)):
               regularFont = font
        return regularFont 
            
  