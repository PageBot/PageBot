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
from pagebot.fonttoolbox.objects.font import Font, getFont, isFontPath
from pagebot.toolbox.transformer import path2FontName, path2FamilyName

FAMILIES = {} # Cached build families

def getFamilies(familyPaths=None, useFontInfo=True, useFileName=True, force=False):
    u"""Construct a dictionary of Family instances from dictionary familyPaths. If omitted, then create
    the families from all aviable font paths found in the by the context.
    The flag useFontInfo defines if the familyName, styleName) should be taken from the font.info
    or guess from the font file name.
    
    >>> families = getFamilies()
    >>> 'Roboto' in families
    True
    >>> 'Bungee' in families
    True
    >>> families = getFamilies(useFontInfo=False, force=True) # Forced to look an fileName only, RobotoCondensed is a family
    >>> 'RobotoCondensed' in families
    True
    >>> families = getFamilies(useFileName=False, force=True) # Looking into font.info, Roboto is the family name.
    >>> 'RobotoCondensed' in families
    False
    >>> #families = getFamilies(useFontInfo=False, useFileName=False) finds nothing
    """
    global FAMILIES
    if force:
        FAMILIES = {}
    if not FAMILIES: # If forced or not initialized yet
        for fontPath in getFontPaths().values():
            font = getFont(fontPath)
            if font is not None:
                #print font.path.split('/')[-1], `font.info.familyName`, `font.info.styleName`
                familyName = None
                if useFontInfo:
                    familyName = font.info.familyName
                if not familyName and useFileName:
                    familyName = path2FamilyName(font.path)
                if familyName:
                    if familyName not in FAMILIES:
                        FAMILIES[familyName] = Family(familyName)
                    FAMILIES[familyName].addFont(font)
    return FAMILIES

def getFamily(familyName, useFontInfo=True, useFileName=True):
    u"""Create a new Family instance and fill it with available fonts that fit  the name.

    >>> families = getFamilies()
    >>> family = families.get('Bungee')
    >>> family.name
    u'Bungee'
    >>> len(family)
    5
    """
    return getFamilies(useFontInfo=useFontInfo, useFileName=useFileName).get(familyName)

def newFamily(familyName, fonts=None):
    u"""Create a new family with this name. If the family already exists, then raise an error.

    >>> families = getFamilies()
    >>> family = newFamily('MyFamily')
    >>> family.name in families
    True
    >>> del families[family.name]
    """
    families = getFamilies()
    assert familyName not in families
    family = Family(familyName, fonts=fonts)
    families[familyName] = family
    return family

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
        """
        self.name = name or 'Untitled'
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

    def addFonts(self, fontsOrPaths):
        u"""And the fonts to the family. This can be a list of Font instances, a list of font names or
        a list of font paths.

        >>> from pagebot.contexts.platform import getRootFontPath
        >>> fontPath = getRootFontPath()
        >>> path = fontPath + '/fontbureau/AmstelvarAlpha-VF.ttf'
        >>> families = getFamilies()
        >>> family = newFamily('MyOtherFamily')
        >>> family.addFonts(path)
        >>> len(family)
        1
        >>> del families[family.name]
        """
        if not isinstance(fontsOrPaths, (tuple, list)): # Only if not None and not empty.
            fontsOrPaths = [fontsOrPaths]
        for fontOrPath in fontsOrPaths:
            self.addFont(fontOrPath)

    def addFont(self, fontOrPath):
        u"""And the fonts to the family. This can be a list of Font instances, a list of font names or
        a list of font paths.

        >>> from pagebot.contexts.platform import getRootFontPath
        >>> fontPath = getRootFontPath()
        >>> path = fontPath + '/fontbureau/AmstelvarAlpha-VF.ttf'
        >>> families = getFamilies()
        >>> family = newFamily('MyOtherFamily')
        >>> font = family.addFont(path)
        >>> font.path == path
        True
        >>> len(family)
        1
        >>> del families[family.name]
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

    def getFontStyles(self):
        u"""Answer the dictionary {fontStyle: [font, font, ...], ...}

        >>> from pagebot.contexts.platform import getRootFontPath
        >>> fontPath = getRootFontPath()
        >>> path = fontPath + '/fontbureau/AmstelvarAlpha-VF.ttf'
        >>> family = Family('MyFamily')
        >>> family.addFonts(path)
        >>> family.getFontStyles().keys()
        [u'Regular']
        >>> family = getFamily('Bungee')
        >>> family.name
        u'Bungee'
        >>> sorted(family.getFontStyles().keys())
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

    def findFontsByName(self, pattern):
        u"""Answer the font(s) that fit the pattern.

        >>> family = getFamily('Bungee')
        >>> family.findFontsByName('BungeeOutline')
        [<Font BungeeOutline-Regular>]
        """
        namedFonts = []
        for font in self.fonts.values():
            if pattern in path2FontName(font.path):
                namedFonts.append(font)
        return namedFonts

    def getFontWeights(self):
        u"""Answer the dictionary {weightClass: [font, font, ...], ...]}
        
        >>> family = getFamily('Bungee')
        >>> family.getFontWeights().keys()
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

    def getFontWidths(self):
        u"""Answer the dictionary {widthClass: [font, font, ...], ...]}
        
        >>> family = getFamily('Bungee')
        >>> family.getFontWidths().keys()
        [5]
        >>> family = getFamily('Roboto')
        >>> family.getFontWidths().keys()
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
        
        >>> family = getFamily('Bungee')
        >>> len(family.romanFonts())
        5
        >>> family = getFamily('Roboto')
        >>> len(family.romanFonts())
        9
        """
        romanFonts = {}
        for fontPath, font in self.fonts.items():
            if not font.isItalic():
                romanFonts[fontPath] = font
        return romanFonts

    def italicFonts(self):
        u"""Answer the dictionary {italicFontPath: font, ...]}
        
        >>> family = getFamily('Bungee')
        >>> len(family.italicFonts())
        0
        >>> family = getFamily('Roboto')
        >>> len(family.italicFonts())
        9
        """
        italicFonts = {}
        for fontPath, font in self.fonts.items():
            if font.isItalic():
                italicFonts[fontPath] = font
        return italicFonts

    def findRegularFont(self):
        u"""Try to find a font that is closest to style "Normal" or "Regular".
        Otherwise answer the font that has weight/width closest to (400, 5) and angle is closest to 0.

        >>> family = getFamily('Roboto') # We know this exists in the PageBot repository
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

        >>> family = getFamily('Roboto') # We know this exists in the PageBot repository
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
