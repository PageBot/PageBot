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

#   P A T H S 

def getRootPath():
    u"""Answer the root path of the pagebot module."""
    return '/'.join(__file__.split('/')[:-4]) # Path of this file with pagebot/__init__.py(c) removed.

def getRootFontPath():
    u"""Answer the standard font path of the pagebot module."""
    return getRootPath() + '/Fonts'

def _recursivelyCollectFontPaths(path, fontPaths):
    u"""Recursive helper function for getFontPaths."""
    for fileName in os.listdir(path):
        filePath = path + '/' + fileName
        if os.path.isdir(filePath):
            _recursivelyCollectFontPaths(filePath, fontPaths)
        else:
            extension = fileName.split('.')[-1].lower()
            if extension in ('ttf', 'otf', 'svg'):
                fontPaths[fileName] = filePath

FONT_PATHS = {} # Cached dictionary

def getFontPaths(): 
    u"""Answer a dictionary with all available font paths on the platform, key is the single file name.
    A typical example return for MaxOS the font paths available in directories (for user Petr): 
        ('/Library/Fonts', '/Users/petr/Library/Fonts', '/Users/petr/git/PageBot/Fonts')
    In this order, "local" defined fonts with the same file name, will overwrite the "deeper" located font files.

    >>> len(getFontPaths()) >= 1
    True
    """
    global FONT_PATHS
    if not FONT_PATHS:

        if os.name == 'posix':
            # Try typical OSX font folders

            paths = ('/Library/Fonts', os.path.expanduser('~/Library/Fonts')) 
            for path in paths:
                if os.path.exists(path):
                    _recursivelyCollectFontPaths(path, FONT_PATHS)
            # Add other typical Linux font folders here to look at.
        elif os.name in ('nt', 'os2', 'ce', 'java', 'riscos'):
            # Add other typical Windows font folders here to look at.
            pass
        else:
            raise NotImplementedError('Unknown platform type "%s"' % os.name)
        # Add PageBot repository fonts, they always exist in this context.
        _recursivelyCollectFontPaths(getRootFontPath(), FONT_PATHS)

    return FONT_PATHS

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
