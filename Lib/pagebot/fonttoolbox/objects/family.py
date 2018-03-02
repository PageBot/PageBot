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
import os
from pagebot.contexts import defaultContext as context
from pagebot.contexts.platform import getFontPaths
from pagebot.fonttoolbox.objects.font import Font, isFontPath
from pagebot.toolbox.transformer import path2FontName


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
            font = Font.FONT_CLASS(fontPath, styleName)
            families[familyName].addFont(font, styleName) # Force style name from dict, instead of font.info.styleName 
    return families

def getFamilyFontPaths(familyName):
    # Collect the DrawBot names of all available fonts for the named family, that are installed in the system.
    fontPaths = {} # Dictionary, where key is the DrawBot font name, value is the OS path of the font file.
    for fontName in context.installedFonts(): # Answers complete list of all installed fonts.
        if familyName in fontName: # If this is a with with the familyName that we are looking for...
            fontPaths[fontName] = context.fontName2FontPath(fontName) # Store the name and find the font path name.
    return fontPaths #  Answer the dictionary. This is empty, if no Bitcount fonts are installed now.

def getFamilyFonts(familyName):
    # Collect the DrawBot names of all available fonts for the named family, that are installed in the system.
    fonts = {} # Dictionary, where key is the DrawBot font name, value is the OS path of the font file.
    for fontName in context.installedFonts(): # Answers complete list of all installed fonts.
        if familyName in fontName: # If this is a with with the familyName that we are looking for...
            fontPath = context.fontName2FontPath(fontName)
            if fontPath is not None:
                fonts[fontName] = Family.FONT_CLASS(fontPath) # Store the name and find the font path name.
    return fonts #  Answer the dictionary. This is empty, if no Bitcount fonts are installed now.

def getSystemFontPaths():
    u"""Answer the cleaned list of installed font names."""
    fontPaths = []
    for fontName in context.installedFonts():
        if not fontName.startswith('.'):
            fontPaths.append(context.fontName2FontPath(fontName))
    return fontPaths

def findFamilyByName(familyName):
    u"""Answer the family (from guessed families by pattern) that exactly matches the familyName.
    Answer None if there is not an excact match in the system."""
    return guessFamiliesByPatterns(familyName).get(familyName)

def guessFamiliesByPatterns(patterns, familyClass=None):
    u"""Answer a dictionary family instances, where the fonts are selected to have the exclusive 
    patterns in their file names. Note that this is not a guearantees safe method to combine font files
    into families, but it is useful of exemple purpose, in caes the available set of fonts
    on the platform is not known. 
    After the fonts are selected by the pattern, the family name is taken from font.info.familyName.
    If patterns is single string, it will be included as list.

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
    >>> path = sorted(family.fonts.keys())[0] # Key is the font.path
    >>> path2FontName(path) # Convert to standard readable name
    'Roboto-Black'
    >>> font = family.fonts[path]
    >>> g = font['A']
    >>> g.name
    'A'
    """
    if familyClass is None:
        familyClass = Family
    if not isinstance(patterns, (list, tuple)):
        patterns = [patterns]
    families = {}
    for fontFileName, fontPath in getFontPaths().items():
        found = True
        for pattern in patterns:
            if not pattern in fontFileName:
                found = False
                break
        if found:
            font = Family.FONT_CLASS(fontPath)
            familyName = font.info.familyName.split(' ')[0].split('-')[0]
            if not familyName in families:
                families[familyName] = familyClass(familyName, fonts=[font])
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
        path = context.fontName2FontPath(styleName)
        # Could have an extension like .ttf or .otf, by OSX system font don't have an extension.
        # o we just try to open the plain file and see how that goes.
        # Try to open the font in font tools, so we have access to a lot of information for our proof.
        # Create Style instance, as storage within our page composition passes.
        font = Family.FONT_CLASS(path, styleName)
        if font.info is None:
            continue # Could not open the font file.            
        # Skip if there is not a clear family name and style name derived from FontInfo    
        if font.info.familyName and font.info.styleName:
            # Make a family collection of style names, if not already there.
            if not font.info.familyName in families: 
                families[font.info.familyName] = Family(font.info.familyName)
            # Store the style name and path in the family collection.
            families[font.info.familyName].addFont(font) 

    return families 

class Family(object):

    FONT_CLASS = Font

    def __init__(self, name=None, fonts=None):
        u"""The Family instance is a container of related Font instances. There are various levels of access: file name, style name,
        width and weight OS/values by DrawBot name if the font is installed.
        The fonts attribute can be a list of Font instances, a list of font file paths or directories.

        Test with a limited set of patsj:
        >>> from pagebot.contexts.platform import getRootFontPath
        >>> familyName = 'Roboto' # We know this exists in the PageBot repository
        >>> fontPath = getRootFontPath() + '/google/roboto'
        >>> family = Family(familyName, fontPath)
        >>> #family.findRegularFont()
        >>> families = guessFamiliesByPatterns(familyName)
        >>> family = families[familyName]
        >>> familyName in families.keys()
        True
        >>> family = families[familyName]
        >>> family.name
        u'Roboto'
        """
        self.name = name or 'UntitledFamily'
        self.fonts = {} # Key is unique font file path. Value is Font instances.
        if fonts is not None:
            self.addFonts(fonts) # Try to figure out what these are, and add them

    def __repr__(self):
        return '<PageBot Family %s (%d fonts)>' % (self.name, len(self))

    def __len__(self):
        return len(self.fonts)
    
    def __contains__(self, fontPath):
        u"""Answer the boolean flag if there is a Font instance with path fontPath.

        >>> from pagebot.contexts.platform import getRootFontPath
        >>> fontPath = getRootFontPath()
        >>> path = fontPath + '/fontbureau/AmstelvarAlpha-VF.ttf'
        >>> family = Family('MyFamily')
        >>> font = family.addFont(path)
        >>> path in family
        True
        """
        return fontPath in self.fonts

    def __getitem__(self, fontPath):
        u"""Answer the Font instance by this fontPath.

        >>> from pagebot.contexts.platform import getRootFontPath
        >>> fontPath = getRootFontPath()
        >>> path = fontPath + '/fontbureau/AmstelvarAlpha-VF.ttf'
        >>> family = Family('MyFamily')
        >>> family.addFonts(path)
        >>> len(family)
        1
        >>> family.fonts[path].path == path
        True
        """
        return self.fonts[fontPath]
    
    def keys(self):
        u"""Answer the paths of fonts, which are the keys in self.fonts.

        >>> from pagebot.contexts.platform import getRootFontPath
        >>> fontPath = getRootFontPath()
        >>> path = fontPath + '/fontbureau/AmstelvarAlpha-VF.ttf'
        >>> family = Family('MyFamily')
        >>> family.addFonts(path)
        >>> family.keys()[0] == path
        True
        """
        return self.fonts.keys()

    def install(self, fontNames=None):
        u"""Install all fonts of the family in DrawBotContext, if not alreadythere. The context
        can ignore, if fonts are accessed by their file path only."""
        if fontNames is None: # fontKey is the font file name.
            fontNames = self.fonts.keys()

        for fontName in fontNames:
            font = self.fonts.get(fontName)
            if not font.path in self.installedFonts: # Only if not already installed.
                fontName = font.install()
            self.installedFonts[font.path] = font

    def addFonts(self, fontsOrPaths):
        u"""And the fonts to the family. This can be a list of Font instances, a list of font names or
        a list of font paths.

        >>> from pagebot.contexts.platform import getRootFontPath
        >>> fontPath = getRootFontPath()
        >>> path = fontPath + '/fontbureau/AmstelvarAlpha-VF.ttf'
        >>> family = Family('MyFamily')
        >>> family.addFonts(path)
        """
        if not isinstance(fontsOrPaths, (tuple, list)): # Only if not None and not empty.
            fontsOrPaths = [fontsOrPaths]
        for fontOrPath in fontsOrPaths:
            self.addFont(fontOrPath)

    def addFont(self, fontOrPath, install=True):
        font = None
        if isinstance(fontOrPath, self.FONT_CLASS):
            self.fonts[fontOrPath.path] = font = fontOrPath
        elif os.path.isdir(fontOrPath):
            for fileName in os.listdir(fontOrPath): 
                if not fontOrPath.endswith('/'):
                    fontOrPath += '/'
                filePath = fontOrPath + fileName
                if isFontPath(filePath):
                    self.fonts[fontOrPath] = self.FONT_CLASS(filePath, install=install) # Not recursive, this just folder.
        elif isFontPath(fontOrPath):
            self.fonts[fontOrPath] = self.FONT_CLASS(fontOrPath, install=install)

    def fontStyles(self):
        u"""Answer the dictionary {fontStyle: [font, font, ...], ...}

        >>> from pagebot.contexts.platform import getRootFontPath
        >>> fontPath = getRootFontPath()
        >>> path = fontPath + '/fontbureau/AmstelvarAlpha-VF.ttf'
        >>> family = Family('MyFamily')
        >>> family.addFonts(path)
        >>> family.fontStyles().keys()
        [u'Regular']
        """
        fontStyles = {}
        for font in self.fonts.values():
            styleName = font.info.styleName
            if not styleName in fontStyles:
                fontStyles[styleName] = [font]
            else:
                fontStyles[styleName].append(font)
        return fontStyles

    def fontsByName(self, fontName):
        u"""Answer the font(s) that fit the name.

        >>> from pagebot.toolbox.transformer import path2FontName
        >>> familyName = 'Roboto' # We know this exists in the PageBot repository
        >>> families = guessFamiliesByPatterns(familyName)
        >>> family = families[familyName]
        >>> fontName = 'Roboto-Regular'
        >>> font = family.fontsByName(fontName)[0]
        >>> path2FontName(font.path) == fontName
        True
        """
        namedFonts = []
        for font in self.fonts.values():
            if fontName == path2FontName(font.path):
                namedFonts.append(font)
        return namedFonts

    def fontWeights(self):
        u"""Answer the dictionary {weightClass: [font, font, ...], ...]}
        
        >>> from pagebot.contexts.platform import getRootFontPath
        >>> fontPath = getRootFontPath()
        >>> path = fontPath + '/fontbureau/AmstelvarAlpha-VF.ttf'
        >>> family = Family('MyFamily')
        >>> family.addFonts(path)
        >>> family.fontWeights().keys()
        [400]
        """
        weightClasses = {}
        for font in self.fonts.values():
            weightClass = font.info.weightClass
            if not weightClass in weightClasses:
                weightClasses[weightClass] = [font]
            else:
                weightClasses[weightClass].append(font)
        return weightClasses

    def fontWidths(self):
        u"""Answer the dictionary {widthClass: [font, font, ...], ...]}
        
        >>> from pagebot.contexts.platform import getRootFontPath
        >>> fontPath = getRootFontPath()
        >>> path = fontPath + '/fontbureau/AmstelvarAlpha-VF.ttf'
        >>> family = Family('MyFamily')
        >>> family.addFonts(path)
        >>> family.fontWidths().keys()
        [5]
        """
        widthClasses = {}
        for font in self.fonts.values():
            widthClass = font.info.widthClass
            if not widthClass in widthClasses:
                widthClasses[widthClass] = [font]
            else:
                widthClasses[widthClass].append(font)
        return widthClasses

    def romanFonts(self):
        u"""Answer the dictionary {romanFontPath: font, ...]}
        
        >>> from pagebot.contexts.platform import getRootFontPath
        >>> fontPath = getRootFontPath()
        >>> path = fontPath + '/fontbureau/AmstelvarAlpha-VF.ttf'
        >>> family = Family('MyFamily')
        >>> family.addFonts(path)
        >>> len(family.romanFonts())
        1
        """
        romanFonts = {}
        for fontPath, font in self.fonts.items():
            if not font.isItalic():
                romanFonts[fontPath] = font
        return romanFonts

    def italicFonts(self):
        u"""Answer the dictionary {italicFontPath: font, ...]}
        
        >>> from pagebot.contexts.platform import getRootFontPath
        >>> fontPath = getRootFontPath()
        >>> path = fontPath + '/fontbureau/AmstelvarAlpha-VF.ttf'
        >>> family = Family('MyFamily')
        >>> family.addFonts(path)
        >>> len(family.italicFonts())
        0
        """
        italicFonts = {}
        for fontPath, font in self.fonts.items():
            if font.isItalic():
                italicFonts[fontPath] = font
        return italicFonts

    
    def findRegularFont(self):
        u"""Try to find a font that is closest to style "Normal" or "Regular".
        Otherwise answer the font that has weight/width closest to (400, 5) and angle is closest to 0.

        >>> from pagebot.toolbox.transformer import path2FontName
        >>> familyName = 'Roboto' # We know this exists in the PageBot repository
        >>> families = guessFamiliesByPatterns(familyName)
        >>> family = families[familyName]
        >>> font = family.findRegularFont()
        >>> font.info.styleName # We got the most "default" font of the family
        u'Regular'
        >>> path2FontName(font.path)
        'Roboto-Regular'
        """
        return self.findFont(weight=400, width=5, italic=False)

    def findFont(self, name=None, weight=None, width=None, italic=None):
        u"""Answer the font that is the closest match on name, weight as name or weight as number,
        width as name or width as number and italic angle as name or number, if any of these are defined.
        In case there is one or more fonts in the family then there always is a closest match.
        If the family is empty, None is anwere.

        >>> from pagebot.toolbox.transformer import path2FontName
        >>> familyName = 'Roboto' # We know this exists in the PageBot repository
        >>> families = guessFamiliesByPatterns(familyName)
        >>> familyName in families.keys()
        True
        >>> family = families[familyName]
        >>> len(family)
        18
        >>> #family.findFont(weight=400, width=5)

        >>> family.findFont(weight=400, width=3)
        <Font RobotoCondensed-Regular>
        """
        matchingFont = None
        match = 0 # Matching value for the current matchingFont
        for font in self.fonts.values():
            thisMatch = 0
            if name is not None and name in path2FontName(font.path):
                thisMatch += len(name)**4 # Longer names have better matching
            thisMatch += font.weightMatch(weight or 'Regular')*1000
            thisMatch += font.widthMatch(width or 5)
            if matchingFont is None:
                matchingFont = font
                match = thisMatch
            elif thisMatch > match:
                matchingFont = font
                match = thisMatch
            elif thisMatch == match and italic == font.isItalic():
                matchingFont = font

        return matchingFont


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
