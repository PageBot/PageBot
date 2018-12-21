#!/usr/bin/env python3
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
#     Supporting Sketch, https://github.com/Zahlii/python_sketch_api
# -----------------------------------------------------------------------------
#
#     sketchcontext.py
#
import os
from pagebot.constants import FILETYPE_SKETCH
from pagebot.contexts.basecontext import BaseContext
from pagebot.contexts.builders.sketchbuilder import sketchBuilder

class SketchContext(BaseContext):
 
    def __init__(self):
        """Constructor of Sketch context.

        >>> context = SketchContext()
        >>> context.newDocument(100, 100)
        """
        super().__init__()
        self.name = self.__class__.__name__
        self.b = sketchBuilder
        self.save() # Save current set of values on gState stack.
        self.shape = None # Current open shape
        self.flatString = None
        self.fileType = FILETYPE_SKETCH

    def save(self):
        pass

    def newDocument(self, w, h):
        pass

    def readDocument(self, path):
        """Read a sketch file and answer a Document that contains the interpreted data.

        >>> context = SketchContext()
        >>> finder = Finder()
        >>> filePath = finder.findPath('')
        """
        filePath = finder.findPath(path)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
