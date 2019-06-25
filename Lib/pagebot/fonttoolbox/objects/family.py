# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     family.py
#
#     Implements a family collection of Font instances.
#
import os
from pagebot.fonttoolbox.fontpaths import getFontPaths
from pagebot.fonttoolbox.objects.font import Font, getFont
from pagebot.toolbox.transformer import path2FamilyName

FAMILY_PATHS = {} # Cached family name --> [fontPath, fontPath, ...]
FAMILIES = {} # Cached family name --> Family instance

def getFamilyPaths(useFontInfo=True, useFileName=True, force=False):
    """Construct a dictionary of familyName-->[fontPath, fontPath, ...]. If
    omitted, then create the families from all avaible font paths found by the
    context.

    The flag useFontInfo defines if the familyName, styleName) should be taken
    from the font.info or just guessed from the font file name.

    >>> familyPaths = getFamilyPaths()
    >>> len(familyPaths['Roboto'])
    38
    >>> len(familyPaths['Bungee'])
    5
    """
    global FAMILY_PATHS
    if force:
        FAMILY_PATHS = {}
    if not FAMILY_PATHS: # If forced or not initialized yet
        for fontPath in getFontPaths().values():
            familyName = None
            if useFontInfo:
                font = getFont(fontPath)
                if font is not None:
                    familyName = font.info.familyName

            if not familyName and useFileName:
                familyName = path2FamilyName(fontPath)

            if familyName is not None:
                if familyName not in FAMILY_PATHS:
                    FAMILY_PATHS[familyName] = []
                FAMILY_PATHS[familyName].append(fontPath)
    return FAMILY_PATHS

def getFamily(familyName, useFontInfo=True, useFileName=True):
    """Create a new Family instance and fill it with available fonts that fit the name.

    >>> getFamily('Roboto')
    <PageBot Family Roboto (38 fonts)>
    >>> getFamily('Bungee')
    <PageBot Family Bungee (5 fonts)>
    """
    if familyName in FAMILIES:
        return FAMILIES[familyName] # Answer family is there is a cached on with this name.
    familyPaths = getFamilyPaths(useFontInfo=useFontInfo, useFileName=useFileName)
    if familyName in familyPaths:
        family = Family(familyName, paths=familyPaths[familyName])
        FAMILIES[familyName] = family # Cache the family
        return family
    return None

def findFamily(pattern, defaultName=None, useFontInfo=True, useFileName=True):
    """Answers the family that best matches the pattern.

    >>> findFamily('Bungee')

    """
    familyPaths = getFamilyPaths()
    foundFamilyName = None
    for familyName in familyPaths:
        if pattern in familyName:
            foundFmailyName = familyName
            break
    if foundFamilyName is None:
        foundFamilyName = defaultName
    if foundFamilyName in familyPaths:
        return getFamily(foundFamilyName, useFontInfo=useFontInfo, useFileName=useFileName)
    return None

def newFamily(familyName, fonts=None):
    """Create a new family with this name. If the family already exists, then raise an error.

    >>> familyPaths = getFamilyPaths()
    >>> family = newFamily('MyFamily')
    >>> family.name in familyPaths
    True
    >>> del familyPaths[family.name] # Delete cache family, so it disappear.
    >>> family.name in familyPaths
    False
    """
    familyPaths = getFamilyPaths()
    assert familyName not in familyPaths
    family = Family(familyName, fonts=fonts)
    familyPaths[familyName] = family
    return family

class Family:

    FONT_CLASS = Font

    def __init__(self, name=None, fonts=None, paths=None):
        """The Family instance is a container of related Font instances. There are various levels of access: file name, style name,
        width and weight OS/values by DrawBot name if the font is installed.
        The fonts attribute can be a list of Font instances, a list of font file paths or directories.

        Test with a limited set of patsj:
        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> familyName = 'Roboto' # We know this exists in the PageBot repository
        >>> fontPath = getTestFontsPath() + '/google/roboto'
        >>> family = Family(familyName, fontPath)
        """
        self.name = name or 'Untitled'
        self.fonts = {} # Key is unique font file path. Value is Font instances.
        if paths is not None:
            for path in paths:
                if os.path.exists(path):
                    self.addFont(path)
        if fonts is not None:
            self.addFonts(fonts) # Try to figure out what these are, and add them

    def __repr__(self):
        """Answers the representation stirng of the family."""
        return '<PageBot Family %s (%d fonts)>' % (self.name, len(self))

    def __len__(self):
        """Answers the length of the family, as the amount of fonts."""
        return len(self.fonts)

    def __contains__(self, fontPath):
        """Answers if there is a Font instance with path fontPath.

        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> fontPath = getTestFontsPath()
        >>> path = fontPath + '/fontbureau/Amstelvar-Roman-VF.ttf'
        >>> family = Family('MyFamily')
        >>> font = family.addFont(path)
        >>> path in family
        True
        """
        return fontPath in self.fonts

    def __getitem__(self, fontPath):
        """Answers the Font instance by this fontPath.

        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> fontPath = getTestFontsPath()
        >>> path = fontPath + '/fontbureau/Amstelvar-Roman-VF.ttf'
        >>> family = Family('MyFamily')
        >>> family.addFonts(path)
        >>> len(family)
        1
        >>> family.fonts[path].path == path
        True
        """
        return self.fonts[fontPath]

    def keys(self):
        """Answers the paths of fonts, which are the keys in self.fonts.

        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> fontPath = getTestFontsPath()
        >>> path = fontPath + '/fontbureau/Amstelvar-Roman-VF.ttf'
        >>> family = Family('MyFamily')
        >>> family.addFonts(path)
        >>> sorted(family.keys())[0] == path
        True
        """
        return self.fonts.keys()

    def addFonts(self, fontsOrPaths):
        """And the fonts to the family. This can be a list of Font instances, a
        list of font names or a list of font paths.
        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> fontPath = getTestFontsPath()
        >>> path = fontPath + '/fontbureau/Amstelvar-Roman-VF.ttf'
        >>> familyPaths = getFamilyPaths()
        >>> family = newFamily('MyOtherFamily')
        >>> family.addFonts(path)
        >>> len(family)
        1
        """
        if isinstance(fontsOrPaths, dict):
            fontsOrPaths = fontsOrPaths.values()
        elif not isinstance(fontsOrPaths, (tuple, list)): # Only if not None and not empty.
            fontsOrPaths = [fontsOrPaths]
        for fontOrPath in fontsOrPaths:
            self.addFont(fontOrPath)

    def addFont(self, fontOrPath):
        """Add the fonts to the family. This can be a list of Font instances, a
        list of font names or a list of font paths."""
        """
        FIXME: restore doctests.
        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> font = findFont('Roboto-Regular')
        >>> path = font.path
        >>> families = getFamilies()
        >>> family = newFamily('MyOtherFamily')
        >>> font = family.addFont(path)
        >>> font.path == path
        True
        >>> len(family)
        1
        """
        font = None
        if isinstance(fontOrPath, self.FONT_CLASS):
            self.fonts[fontOrPath.path] = font = fontOrPath
        elif os.path.isdir(fontOrPath):
            for fileName in os.listdir(fontOrPath):
                if not fontOrPath.endswith('/'):
                    fontOrPath += '/'
                filePath = fontOrPath + fileName
                if not filePath in self.fonts: # Only create if not already there.
                    font = getFont(filePath)
                    if font is not None:
                        self.fonts[filePath] = font # Not recursive, this just folder.
                else: # Font exists, just return it
                    font = self.fonts[filePath]
        else:
            font = getFont(fontOrPath)
            if font is not None:
                self.fonts[fontOrPath] = font
        return font

    def getFonts(self):
        """Answers the unsorted list of Font instances in the family.

        """
        """
        >>> family = getFamily('Roboto') # We know this exists in the PageBot repository
        >>> len(family.getFonts())
        38
        """
        return self.fonts.values()

    def getStyles(self):
        """Answers the dictionary {fontStyle: [font, font, ...], ...}

        >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
        >>> fontPath = getTestFontsPath()
        >>> path = fontPath + '/fontbureau/Amstelvar-Roman-VF.ttf'
        >>> family = Family('MyFamily')
        >>> family.addFonts(path)
        >>> family.getStyles()
        {'Regular': [<Font Amstelvar-Roman-VF>]}
        """
        """
        >>> family = getFamily('Bungee')
        >>> family.name
        'Bungee'
        >>> sorted(family.getStyles())
        ['Regular']
        """
        fontStyles = {}
        for font in self.fonts.values():
            styleName = font.info.styleName
            if not styleName in fontStyles:
                fontStyles[styleName] = [font]
            else:
                fontStyles[styleName].append(font)
        return fontStyles

    def getWeights(self):
        """Answers the dictionary {weightClass: [font, font, ...], ...]}

        """
        """
        >>> family = getFamily('Bungee')
        >>> sorted(family.getWeights())
        [400]
        >>> family = getFamily('Roboto') # We know this exists in the PageBot repository
        >>> sorted(family.getWeights())
        [250, 300, 400, 500, 700, 900]
        """
        weightClasses = {}
        for font in self.fonts.values():
            weightClass = font.info.weightClass
            if not weightClass in weightClasses:
                weightClasses[weightClass] = [font]
            else:
                weightClasses[weightClass].append(font)
        return weightClasses

    def getWidths(self):
        """Answers the dictionary {widthClass: [font, font, ...], ...]}

        """
        """
        >>> family = getFamily('Bungee')
        >>> sorted(family.getWidths())
        [5]
        >>> family = getFamily('Roboto')
        >>> sorted(family.getWidths())
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

    def getRomanFonts(self):
        """Answers the dictionary {romanFontPath: font, ...]}

        """
        """
        >>> family = getFamily('Bungee')
        >>> len(family.getRomanFonts())
        5
        >>> family = getFamily('Roboto')
        >>> len(family.getRomanFonts())
        29
        """
        romanFonts = {}
        for fontPath, font in self.fonts.items():
            if not font.isItalic():
                romanFonts[fontPath] = font
        return romanFonts

    def getItalicFonts(self):
        """Answers the dictionary {italicFontPath: font, ...]}

        """
        """
        >>> family = getFamily('Bungee')
        >>> len(family.getItalicFonts())
        0
        >>> family = getFamily('Roboto')
        >>> len(family.getItalicFonts())
        9
        """
        italicFonts = {}
        for fontPath, font in self.fonts.items():
            if font.isItalic():
                italicFonts[fontPath] = font
        return italicFonts

    def findRegularFont(self, italic=False):
        """Try to find a font that is closest to style "Normal" or "Regular".
        Otherwise answer the font that has weight/width closest to (400, 5) and angle is closest to 0.
        Default is to find the roman. The italic is optional to find the regular italic, if it exists.


        """

        """
        >>> from pagebot.toolbox.transformer import path2FontName
        >>> family = getFamily('Roboto') # We know this exists in the PageBot repository
        >>> font = family.findRegularFont()
        >>> font.info.styleName # We got the most "default" font of the family
        'Regular'
        TODO: Get more docTest like these to work
        >>> path2FontName(font.path)
        'Roboto-Regular'
        >>> family.findRegularFont(italic=True)
        <Font Roboto-Italic>
        """
        return self._findFont(weight=400, width=5, italic=italic)

    def _findFont(self, name=None, weight=None, width=None, italic=False):
        """Private method to find the font closest to the defined parameters."""
        match = 0
        matchingFont = None
        for font in self.fonts.values():
            thisMatch = font.match(name=name, weight=weight, width=width, italic=italic)
            if thisMatch > match:
                matchingFont = font
                match = thisMatch
        return matchingFont

    def findFont(self, name=None, weight=None, width=None, italic=False):
        """Answers the font that is the closest match on name, weight as name or weight as number,
        width as name or width as number and italic angle as name or number, if any of these are defined.
        In case there is one or more fonts in the family then there always is a closest match.
        If the family is empty, None is anwere.


        """
        """
        >>> family = getFamily('Roboto') # We know this exists in the PageBot repository
        >>> family
        >>> len(family)
        38
        >>> family.findFont(weight='Medium')
        <Font Roboto-Medium>

        TODO: Better finding by family parameters
        >>> family.findFont(weight='Medium', italic=True)
        <Font Roboto-MediumItalic>
        >>> family.findFont(weight=400, width=5)
        <Font Roboto-Regular>
        >>> family.findFont(weight='Bold')
        <Font Roboto-Bold>
        >>> family.findFont(weight='Bold', italic=True)
        <Font Roboto-BoldItalic>
        >>> family.findFont(weight='Boldish', width='NotWide')
        <Font Roboto-Regular>
        """
        matchingFont = self._findFont(name=name, weight=weight, width=width, italic=italic)
        if matchingFont is None: # No match, answer regular if it can be found.
            matchingFont = self._findFont(weight=400, width=5, italic=italic)
        return matchingFont

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
