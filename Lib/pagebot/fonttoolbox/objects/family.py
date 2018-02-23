# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     family.py
#
#     Implements a family collection of Font instances.
#
from pagebot.contexts import defaultContext as context
from pagebot.contexts.platform import getFontPaths
from pagebot.fonttoolbox.objects.font import Font
from pagebot.toolbox.transformer import path2Name
from pagebot.style import FONT_WEIGHT_MATCHES, FONT_WIDTH_MATCHES, FONT_ITALIC_MATCHES


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
    for fontName in context.installedFonts(): # Answers complete list of all installed fonts.
        if familyName in fontName: # If this is a with with the familyName that we are looking for...
            fontPaths[fontName] = context.getFontPathOfFont(fontName) # Store the name and find the font path name.
    return fontPaths #  Answer the dictionary. This is empty, if no Bitcount fonts are installed now.

def getFamilyFonts(familyName):
    # Collect the DrawBot names of all available fonts for the named family, that are installed in the system.
    fonts = {} # Dictionary, where key is the DrawBot font name, value is the OS path of the font file.
    for fontName in context.installedFonts(): # Answers complete list of all installed fonts.
        if familyName in fontName: # If this is a with with the familyName that we are looking for...
            fontPath = context.getFontPathOfFont(fontName)
            if fontPath is not None:
                fonts[fontName] = Font(fontPath) # Store the name and find the font path name.
    return fonts #  Answer the dictionary. This is empty, if no Bitcount fonts are installed now.

def getSystemFontPaths():
    u"""Answer the cleaned list of installed font names."""
    fontPaths = []
    for fontName in context.installedFonts():
        if not fontName.startswith('.'):
            fontPaths.append(context.getFontPathOfFont(fontName))
    return fontPaths

def findFamilyByName(familyName):
    u"""Answer the family (from guessed families by pattern) that exactly matches the familyName.
    Answer None if there is not an excact match in the system."""
    return guessFamiliesByPatterns(familyName).get(familyName)

def guessFamiliesByPatterns(patterns):
    u"""Answer a dictionary family instances, where the fonts are selected to have the exclusive 
    patterns in their file names. Note that this is not a guearantees safe method to combine font files
    into families, but it is useful of exemple purpose, in caes the available set of fonts
    on the platform is not known. 
    After the fonts are selected by the pattern, the family name is taken from font.info.familyName.

    >>> familyName = 'Roboto' # We know this exists in the PageBot repository
    >>> # For now we assume that this testing works in all contexts on all platforms.
    >>> families = guessFamiliesByPatterns(familyName)
    >>> familyName in families.keys()
    True
    >>> family = families[familyName]
    >>> family.name
    u'Roboto'
    >>> len(family.fonts)
    18
    >>> sorted(family.fonts.keys())[0]
    'Roboto-Black.ttf'
    """
    families = {}
    for fontFileName, fontPath in getFontPaths().items():
        found = True
        for pattern in patterns:
            if not pattern in fontFileName:
                found = False
                break
        if found:
            font = Font(fontPath)
            familyName = font.info.familyName.split(' ')[0].split('-')[0]
            if not familyName in families:
                families[familyName] = Family(familyName, fonts=[font])
            else:
                families[familyName].addFont(font)
    return families

def guessFamilies(styleNames):
    u"""Find the family relation of all fonts in the list. Note that this cannot be a 100% safe guess.
    Answer a dictionary with Family instances. Key is family name."""
    families = {} # Keys is guessed family name.

    for styleName in styleNames:
        if styleName.startswith('.'): # Filter the system fonts that has a name with initial "."
            continue
        path = context.getFontPathOfFont(styleName)
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
    def __init__(self, name, fonts=None, fontPaths=None, fontStyles=None):
        u"""The Family instance is a container of related Font instances. There are 3 levels of access: file name, style name
        (either from font.info.styleName or defined in fontStyles attributes) and by DrawBot name if the font is installed.
        The optional fonts is a list of Font() instances.
        The optional fontPaths is a list of file paths. The optional fontStyles is a dictionary with format 
        dict(Regular=<fontPath>, Italic=<fontPath>, ...)
        One or multiple can be defined: fonts=None, fontPaths=None, fontStyles=None

        >>> familyName = 'Roboto' # We know this exists in the PageBot repository
        >>> families = guessFamiliesByPatterns(familyName)
        >>> family = families[familyName]
        >>> familyName in families.keys()
        True
        >>> family = families[familyName]
        >>> family.name
        u'Roboto'
        >>> font = family.findFont(weight='Regular')
        >>> font.info.styleName
        u'Regular'
        """
        self.name = name
        self.fonts = {} # Key is font name. Value is Font instances.
        self.fontStyles = {} # Key is font.info.styleName. Value is list of fonts (there can be overlapping style names).
        self.installedFonts = {} # DrawBot name as key. Value is same Font instance.
        # If any font or font paths given, open the fonts.
        if fonts is not None:
            for font in fonts:
                self.addFont(font)
        if fontPaths is not None:
            for fontPath in fontPaths:
                self.addFont(Font(fontPath)) # Use file name as key
        if fontStyles is not None:
            for fontStyle, fontPath in fontStyles.items():
                self.addFont(Font(fontPath), fontStyle=fontStyle)

    def __repr__(self):
        return '<PageBot Family %s>' % self.name

    def __len__(self):
        return len(self.fonts)
    
    def __getitem__(self, fontName):
        return self.fonts[fontName]
    
    def keys(self):
        return self.fonts.keys()

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
        assert fontKey not in self.fonts, ('Font "%s" already in family "%s"' % (fontKey, self.fonts.keys()))
        if fontStyle is None:
            fontStyle = font.info.styleName # It is allowed to have multiple fonts with the same style name.
        # Store the font under unique fontKey.
        self.fonts[fontKey] = font
        # Create list entry for fontStyle, if it does not exist.
        if not fontStyle in self.fontStyles:
            self.fontStyles[fontStyle] = [] # Keep list, there may be fonts with the same style name.
        self.fontStyles[fontStyle].append(font)
    
    def findRegularFont(self):
        u"""Try to find a font that is closest to style "Normal" or "Regular".
        Otherwise answer the font that has weight/width closest to (400, 5) and angle is closest to 0.

        >>> familyName = 'Roboto' # We know this exists in the PageBot repository
        >>> families = guessFamiliesByPatterns(familyName)
        >>> family = families[familyName]
        >>> font = family.findRegularFont()
        >>> font.info.styleName # We got the most "default" font of the family
        u'Regular'
        """
        return self.findFont(weight=400, width=500, italic=0)

    def _matchWeights(self, weight, font):
        u"""Answer level of matching for the (abbreviated) weight name or number with font."""
        match = 0
        if isinstance(weight, (float, int)): # Comparing by numbers
            # Compare the weight as number as max difference to what we already have.
            wf = font.info.weightClass
            for w in FONT_WEIGHT_MATCHES.get(weight, [weight]):
                if isinstance(w, (float, int)): # Then compare by numbers
                    match = max(match, 1000 - abs(w - wf)*10) # Remember best normalized match
        else: # Comparing by string
            for w in FONT_WEIGHT_MATCHES.get(weight, [weight]):
                if not isinstance(w, (float, int)) and w in font.info.styleName:
                    match = max(match, len(w)*10) # Longer weight name is better match
        return match

    def _matchWidths(self, width, font):
        u"""Answer level of matchting for the (abbreviated) width name or number with font."""
        match = 0
        if isinstance(width, (float, int)):
            # Compare the width as number as max difference to what we already have.
            wf = font.info.widthClass 
            if wf <= 10: # Normalize to 1000
                wf *= 10
            for w in FONT_WIDTH_MATCHES.get(width, [width]):
                if isinstance(w, (float, int)): 
                    if w <= 10: # Normalize to 1000
                        w *= 10
                    match = max(match, 1000 - abs(w - wf)*10) # Remember best normalized match
        else: # Comparing by string
            for w in FONT_WIDTH_MATCHES.get(width, [width]):
                if not isinstance(w, (float, int)) and w in font.info.styleName:
                    match = max(match, len(w)*10) # Longer width name is better match
        return match

    def _matchItalics(self, italic, font):
        u"""Answer the boolean to match the (abbreviated) italic name or number with font, and
        also decide if that would be a better match than the reference fonts."""
        match = 0
        if isinstance(italic, (float, int)):
            # Compare the width as number as max difference to what we already have.
            for i in FONT_ITALIC_MATCHES.get(italic, [italic]):
                if isinstance(i, (float, int)):
                    match = max(match, abs(i - font.info.italicAngle)*100)
        else:
            for i in FONT_ITALIC_MATCHES.get(italic, [italic]):
                if not isinstance(i, (float, int)) and (i in font.info.styleName or font.info.italicAngle != 0):
                    match = max(match, font.info.italicAngle*10)
        return match

    def findFont(self, name=None, weight=None, width=None, italic=None):
        u"""Answer the font that is the closest match on name, weight as name or weight as number,
        width as name or width as number and italic angle as name or number, if any of these are defined.
        In case there is one or more fonts in the family then there always is a closest match.
        If the family is empty, None is anwere.

        >>> familyName = 'Roboto' # We know this exists in the PageBot repository
        >>> families = guessFamiliesByPatterns(familyName)
        >>> familyName in families.keys()
        True
        >>> family = families[familyName]
        >>> len(family)
        18
        >>> sorted(family.keys())[1]
        'Roboto-BlackItalic.ttf'
        >>> family._matchWeights('Regular', family['Roboto-Regular.ttf']) # Match on name
        70
        >>> family._matchWeights('Normal', family['Roboto-Regular.ttf']) # Match on alternative name
        70
        >>> family._matchWeights('Normal', family['Roboto-Bold.ttf']) # No match on alternative name with Bold
        0
        >>> family._matchWeights('Bold', family['Roboto-Regular.ttf']) # No match on full name
        0
        >>> family._matchWeights('Bold', family['Roboto-Bold.ttf']) # Match on full style name
        40
        >>> family._matchWeights('Bd', family['Roboto-Bold.ttf']) # Match on partial style name
        40
        >>> family._matchWidths(5, family['Roboto-Regular.ttf']) # Full match in width 5
        1000
        >>> family._matchWidths('Normal', family['Roboto-Regular.ttf']) # Full match in normal width
        1000
        >>> family._matchWidths(5, family['Roboto-Regular.ttf']) # Full match in width 5
        1000
        >>> family._matchWidths(500, family['Roboto-Regular.ttf']) # Full match in width 500
        1000
        >>> font1 = family.findFont(weight='Regular')
        >>> font2 = family.findFont(weight='Normal')
        >>> font1 is font2, font1.info.styleName # Found by different style  names.
        (True, u'Regular')
        >>> font3 = family.findFont(weight=400, italic=True)
        >>> font3.info.styleName
        u'Italic'
        """
        matchingFont = None
        match = 0 # Matching value for the current matchingFont
        for font in self.fonts.values():
            thisMatch = 0
            if name is not None and name in path2Name(font.path):
                thisMatch += name*100 # Longer names have better matching
            thisMatch += self._matchWeights(weight or 'Regular', font)
            thisMatch += self._matchWidths(width or 500, font)
            thisMatch += self._matchItalics(italic or 0, font)
            if thisMatch > match or matchingFont is None:
                matchingFont = font
                match = thisMatch
        return matchingFont


if __name__ == '__main__':
    import doctest
    doctest.testmod()


  
