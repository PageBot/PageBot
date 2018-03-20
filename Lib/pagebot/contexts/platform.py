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
#     pagebot/contexts/platform.py
#
import os
import pagebot

from pagebot.toolbox.transformer import path2FontName, path2ParentPath

#   C O N T E X T S

DEFAULT_CONTEXT = None

def getContext():
    global DEFAULT_CONTEXT
    if DEFAULT_CONTEXT is None:
        try:
            #import ForceImportError # Uncomment for simulate testing of other contexts/platforms
            import AppKit # Force exception on non-OSX platforms
            from pagebot.contexts.drawbotcontext import DrawBotContext
            DEFAULT_CONTEXT = DrawBotContext() # Test if platform is supporing DrawBot:

        except (ImportError, AttributeError, ModuleNotFoundError):
            #import ForceOtherError # Uncomment for simulate testing of other contexts/platforms
            from pagebot.contexts.flatcontext import FlatContext
            DEFAULT_CONTEXT = FlatContext()
        except:
            raise NotImplementedError('Cannot decide on the platform context.')
    return DEFAULT_CONTEXT

#   P A T H S

ROOT_PATH = path2ParentPath(pagebot.__file__)
RESOURCES_PATH = ROOT_PATH + '/resources'
TEST_FONTS_PATH = RESOURCES_PATH + '/testfonts'

# Dictionary with all available font paths on the platform, key is the single file name.
FONT_PATHS = {}

def getRootPath():
    u"""Answer the root path on the platform for the PageBot module."""
    return ROOT_PATH

def getResourcesPath():
    u"""Answer the root path on the platform for the PageBot module."""
    return RESOURCES_PATH

def getTestFontsPath():
    u"""Answer the path of the PageBot test fonts."""
    return TEST_FONTS_PATH

def getFontPathOfFont(fontName):
    u"""Answer the path that is source of the given font name.
    If the path is already a valid font path, then aswer it unchanged.
    Answer None if the font cannot be found.

    >>> path = getFontPathOfFont('Skia')
    >>> path.endswith('Skia.ttf')
    True
    >>> path = getFontPathOfFont('Verdana')
    >>> path.endswith('Verdana.ttf')
    True

    """
    if fontName is not None and not os.path.exists(fontName):
        fontName = getFontPaths().get(fontName)
    return fontName

def _recursivelyCollectFontPaths(path, collectedFontPaths):
    u"""Recursive helper function for getFontPaths. If the fileName already exists in the fontPaths, then ignore."""
    if os.path.exists(path):
        if os.path.isdir(path):
            for fileName in os.listdir(path):
                dirPath = path + '/' + fileName
                _recursivelyCollectFontPaths(dirPath, collectedFontPaths)
        else:
            fontName = path2FontName(path) # File name without extension used as key, works for Flat and DrawBot.
            # If fontName is None, it does not have the right extension.
            # Note that files with the same file name will be overwritten, we expect them to be unique in the OS.
            if fontName is not None:
                collectedFontPaths[fontName] = path

def getFontPaths(extraPaths=None):
    u"""Answer a dictionary with all available font paths on the platform, key is the single file name.
    A typical example return for MaxOS the font paths available in directories (e.g. for user Petr):
        ('/Library/Fonts', '/Users/petr/Library/Fonts', '/Users/petr/git/PageBot/Fonts')
    In this order, "local" defined fonts with the same file name, will overwrite the "deeper" located font files.

    >>> import os
    >>> os.path.exists(TEST_FONTS_PATH + '/fontbureau/AmstelvarAlpha-VF.ttf')
    True
    >>> fontPaths = getFontPaths() # Only default paths on the platform
    >>> 'AmstelvarAlpha-VF' in fontPaths
    True
    >>> fontPaths = getFontPaths(TEST_FONTS_PATH + '/fontbureau/AmstelvarAlpha-VF.ttf') # As single extra path
    >>> 'AmstelvarAlpha-VF' in fontPaths
    True
    >>> fontPaths = getFontPaths([TEST_FONTS_PATH + '/fontbureau/AmstelvarAlpha-VF.ttf']) # As list of extra paths
    >>> 'AmstelvarAlpha-VF' in fontPaths
    True
    >>> fontPaths = getFontPaths(TEST_FONTS_PATH + '/OtherFont.ttf')
    >>> 'OtherFont' in fontPaths # Ignore if extra paths don't exists.
    False
    """
    global FONT_PATHS
    if extraPaths is not None:
        FONT_PATHS = {}  # Force (new) initialization

    if not FONT_PATHS:

        # If forced or initial call, get collect the font paths on this platform
        if os.name == 'posix':
            # Try typical OSX font folders:
            paths = ['/Library/Fonts', os.path.expanduser('~/Library/Fonts')]

            # Add other typical GNU+Linux font folders here to look at:
            paths += ['/usr/share/fonts']

            for path in paths:
                if os.path.exists(path):
                    _recursivelyCollectFontPaths(path, FONT_PATHS)
        elif os.name in ('nt', 'os2', 'ce', 'java', 'riscos'):
            # Add other typical Windows font folders here to look at.
            pass
        else:
            raise NotImplementedError('Unknown platform type "%s"' % os.name)

        # Add PageBot repository fonts, they always exist in this context.
        # But they can be overwritten by fonts with the same (file) name in the extraPaths.
        _recursivelyCollectFontPaths(TEST_FONTS_PATH, FONT_PATHS)

        if extraPaths is not None:
            if not isinstance(extraPaths, (list, tuple)):
                extraPaths = [extraPaths]
            for extraPath in extraPaths:
                _recursivelyCollectFontPaths(extraPath, FONT_PATHS)

    return FONT_PATHS

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
