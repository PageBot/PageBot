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
from pagebot.toolbox.transformer import path2FontName

#   P A T H S 

def getRootPath():
    u"""Answer the root path of the pagebot module."""
    return '/'.join(__file__.split('/')[:-4])

def getRootFontPath():
    u"""Answer the standard font path of the pagebot module."""
    root = getRootPath()
    if root == "":
        return 'Fonts'
    else:
        return root + '/Fonts'

def _recursivelyCollectFontPaths(path, fontPaths):
    u"""Recursive helper function for getFontPaths. If the fileName already existsin the fontPaths, then ignore."""
    for fileName in os.listdir(path):
        filePath = path + '/' + fileName
        if os.path.isdir(filePath):
            _recursivelyCollectFontPaths(filePath, fontPaths)
        else:
            fontName = path2FontName(fileName) # File name without extension used as key, works for Flat and DrawBot.
            # If fontName is None, it does not have the right extension.
            # Note that files with the same file name will be overwritten, we expect them to be unique in the OS.
            if fontName is not None:
                fontPaths[fontName] = filePath

FONT_PATHS = {} # Cached dictionary

def getFontPaths(extraPaths=None): 
    u"""Answer a dictionary with all available font paths on the platform, key is the single file name.
    A typical example return for MaxOS the font paths available in directories (e.g. for user Petr): 
        ('/Library/Fonts', '/Users/petr/Library/Fonts', '/Users/petr/git/PageBot/Fonts')
    In this order, "local" defined fonts with the same file name, will overwrite the "deeper" located font files.

    >>> len(getFontPaths()) >= 1
    True

    """

    """
    >>> path = '/Users/petr/Desktop/TYPETR-git/TYPETR-Upgrade-Var/ufo-RNDS/variable_ttf/'
    >>> paths = getFontPaths(path)
    >>> for path in paths.values():
    ...     if '/TYPETR-git' in path:
    ...         print path
    /Users/petr/Desktop/TYPETR-git/TYPETR-Upgrade-Var/ufo-RNDS/variable_ttf//UpgradeRomanDS-Regular-VF.ttf
    """
    global FONT_PATHS
    if extraPaths is not None:
        FONT_PATHS = {}
    if not FONT_PATHS:

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
        _recursivelyCollectFontPaths(getRootFontPath(), FONT_PATHS)

        if extraPaths is not None:
            if not isinstance(extraPaths, (list, tuple)):
                extraPath = [extraPaths]
            _recursivelyCollectFontPaths(extraPaths, FONT_PATHS)

    return FONT_PATHS

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
