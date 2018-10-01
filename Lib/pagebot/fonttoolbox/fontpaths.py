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
#     fontpaths.py
#
import os

from pagebot.toolbox.transformer import path2FontName
from pagebot.paths import RESOURCES_PATH, DEFAULT_FONT_PATH

#   P A T H S

TEST_FONTS_PATH = RESOURCES_PATH + '/testfonts'

# Dictionary with all available font paths on the platform, key is the single file name.
FONT_PATHS = {}

def getTestFontsPath():
    """Answers the path of the PageBot test fonts."""
    return TEST_FONTS_PATH

def getFontPathOfFont(font, default=None):
    """Answers the path that is source of the given font name.
    If the path is already a valid font path, then aswer it unchanged.
    Answer None if the font cannot be found.

    >>> from pagebot.fonttoolbox.objects.font import findFont
    >>> font = findFont('Roboto-Regular')
    >>> path = getFontPathOfFont(font.path) # Set as font path
    >>> path.endswith('/Roboto-Regular.ttf')
    True
    >>> font.path == path
    True
    >>> path = getFontPathOfFont(font) # Set as Font instance
    >>> path.endswith('/Roboto-Regular.ttf')
    True
    >>> font.path == path
    True
    >>> path = getFontPathOfFont('Roboto-Regular') # Set as font name
    >>> path.endswith('/Roboto-Regular.ttf')
    True
    >>> path = getFontPathOfFont('UnknowFont.ttf') # Unknown font is set to DEFAULT_FONT_PATH
    >>> path == DEFAULT_FONT_PATH
    True
    """
    if hasattr(font, 'path'): # In case it is a Font instance, get its path.
        font = font.path
    if font is not None and not os.path.exists(font):
        font = getFontPaths().get(font)
    if font is None:
        font = default or DEFAULT_FONT_PATH
    return font

def _recursivelyCollectFontPaths(path, collectedFontPaths):
    """Recursive helper function for getFontPaths. If the fileName already
    exists in the fontPaths, then ignore."""
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

def getPageBotFontPaths():
    paths = {}
    _recursivelyCollectFontPaths(TEST_FONTS_PATH, paths)
    return paths

def getFontPaths(extraPaths=None):
    """Answers a dictionary with all available font paths on the platform, key
    is the single file name. Typically on Mac OS Xthe font paths
    available in these respective directories are returned:

        ('/Library/Fonts', '/Users/<username>/Library/Fonts', '/Users/<username>/<path-to>/PageBot/Fonts')

    Locally defined fonts with the same file name will overwrite the font files
    that  are located deeper.

    >>> import os
    >>> os.path.exists(TEST_FONTS_PATH + '/fontbureau/Amstelvar-Roman-VF.ttf')
    True
    >>> fontPaths = getFontPaths() # Only default paths on the platform
    >>> 'Amstelvar-Roman-VF' in fontPaths
    True
    >>> fontPaths = getFontPaths(TEST_FONTS_PATH + '/fontbureau/Amstelvar-Roman-VF.ttf') # As single extra path
    >>> 'Amstelvar-Roman-VF' in fontPaths
    True
    >>> fontPaths = getFontPaths([TEST_FONTS_PATH + '/fontbureau/Amstelvar-Roman-VF.ttf']) # As list of extra paths
    >>> 'Amstelvar-Roman-VF' in fontPaths
    True
    >>> fontPaths = getFontPaths(TEST_FONTS_PATH + '/OtherFont.ttf')
    >>> 'OtherFont' in fontPaths # Ignore if extra paths don't exists.
    False
    """
    global FONT_PATHS
    if extraPaths is not None:
        FONT_PATHS = {}  # Force (new) initialization

    if not FONT_PATHS:

        # If forced or initial call, collect the font paths on this
        # platform.
        if os.name == 'posix':
            paths = []

            # TODO: only for darwin platform.
            # Try typical OSX font folders:
            paths += ['/Library/Fonts', os.path.expanduser('~/Library/Fonts')]

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

        # Add PageBot repository fonts, they always exist in this context. But
        # they can be overwritten by fonts with the same (file) name in the
        # extraPaths.
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
