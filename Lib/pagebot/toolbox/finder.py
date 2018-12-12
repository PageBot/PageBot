#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     finder.py
#
import os
from pagebot.elements import elementFromPath

class Finder:
    """Answers a Finder instance that can find resources (images, texts)
    starting at a give root path. The Finder().find( ) allows optional
    searches, such as matching name, name pattern, extension, etc.

    >>> from pagebot.paths import RESOURCES_PATH
    >>> finder = Finder(RESOURCES_PATH)
    >>> imagePaths = finder.findPaths(extension='png')
    >>> imagePaths[0].endswith('png') # PageBot resources contain at least one .png
    True
    >>> textPaths = finder.findPaths(pattern='Roboto', extension='txt')
    >>> textPaths[0].endswith('txt') # Page resources contain Roboto OFL txt file.
    True
    >>> images = finder.find(pattern='pepper', extension='png') # Answer a list of unplaced Image elements
    >>> image = images[0]
    >>> image.path.split('/')[-1], image.w, image.h
    ('peppertom_lowres_398x530.png', 398pt, 530pt)
    """
    DEFAULT_IGNORE_PATTERNS = ('_scaled', '_export', '_local')

    def __init__(self, rootPath=None):
        """Create a new Finder instance for rootPath. If omitted, then used the current directory."""
        self.rootPath = rootPath or '.'

    def findPaths(self, name=None, pattern=None, extension=None, ignorePatterns=None,
            path=None, paths=None):
        """Answer the list of full file paths, that match the parameters. Matching both
        name.lower() and pattern.lower() 
        """
        if paths is None:
            paths = []
        if path is None:
            path = self.rootPath
        if ignorePatterns is None:
            ignorePatterns = self.DEFAULT_IGNORE_PATTERNS
        for fileName in os.listdir(path):
            if fileName.startswith('.'):
                continue
            # Test if this file or direction should be ignored.
            doIgnore = False
            for ignorePattern in ignorePatterns:
                if ignorePattern in fileName:
                    doIgnore = True
                    break
            if not doIgnore:
                filePath = path + '/' + fileName
                if os.path.isdir(filePath):
                    self.findPaths(name=name, pattern=pattern, extension=extension,
                        path=filePath, paths=paths)
                    continue
                fileNameLower = fileName.lower()
                if name is not None and name.lower() != fileNameLower:
                    continue
                if pattern is not None and not pattern.lower() in fileNameLower:
                    continue
                if extension is not None and not fileNameLower.endswith('.'+extension.lower()):
                    continue
                # Now we have a matching path, add it to the list
                paths.append(filePath)
        return paths

    def findPath(self, name=None, pattern=None, extension=None, ignorePatterns=None,
            path=None, paths=None):
        """Answer the first of the list of full file paths, that match the parameters.
        Answer None if nothing can be found.   
        """
        paths = self.findPaths(name, pattern, extension, ignorePatterns, path, paths)
        if paths: # If anything found, then answer the first one.
            return paths[0]
        return None

    def find(self, name=None, pattern=None, extension=None, **kwargs):
        """Answer the elements that hold the data of matching path extensions.
        """
        elements = []
        for path in self.findPaths(name=name, pattern=pattern, extension=extension):
            e = elementFromPath(path, name=name, **kwargs)
            if e is not None:
                elements.append(e)
        return elements

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

    