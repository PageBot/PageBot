#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#  P A G E B O T
#
#  Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#  www.pagebot.io
#  Licensed under MIT conditions
#
#  Supporting DrawBot, www.drawbot.com
#  Supporting Flat, xxyxyz.org/flat
#  Supporting Sketch, https://github.com/Zahlii/python_sketch_api
# -----------------------------------------------------------------------------
#
#  sketchcontext.py
#
#  Inspace sketch file:
#  https://xaviervia.github.io/sketch2json/
#
#  https://gist.github.com/xaviervia/edbea95d321feacaf0b5d8acd40614b2
#  This description is not complete.
#  Additions made where found in the Reading specification of this context.
#
from pagebot.document import Document
from pagebot.constants import FILETYPE_SKETCH, A4
from pagebot.contexts.basecontext import BaseContext
from pagebot.contexts.builders.sketchbuilder import SketchBuilder
#from pagebot.toolbox.color import color
#from pagebot.toolbox.units import asNumber, pt
#from pagebot.toolbox.transformer import path2Dir, path2Extension
from pagebot.elements import *

from sketchapi import *

class SketchContext(BaseContext):

    W, H = A4 # Default size of a document, as SketchApp has infinite canvas.

    DOCUMENT_CLASS = Document

    def __init__(self):
        """Constructor of Sketch context.

        >>> context = SketchContext()
        >>> doc = context.getDocument()
        >>> doc.w, doc.h
        (576pt, 783pt)
        """
        super().__init__()
        self.name = self.__class__.__name__
        self.b = SketchBuilder()
        self.shape = None # Current open shape
        self.fileType = FILETYPE_SKETCH

    def read(self, path):
        #self.b = SketchBuilder(path)
        pass

    def _createElements(self, sketchLayer, e):
        """Copy the attributes of the sketchLayer into the element where
        necessary.

        """
        pass
        '''
        if isinstance(sketchLayer, (SketchArtboard, SketchPage)):
            e.w = artboard.width
            e.h = artboard.height
        elif isinstance(sketchLayer, SketchFramed):
            e.x = artboard.x
            e.y = artboard.y
            e.w = artboard.width
            e.h = artboard.height

        if isinstance(sketchLayer, SketchLayer): # There are child layers
            for layer in sketchLayer.layers:
                if isinstance(SketchShapeGroup):
                    self._createElements(layer, newGroup(parent=e))
        '''

    def getDocument(self):
        """Create a new tree of Document/Page/Element instances, interpreting
        Artboards."""
        artboards = self.b.getArtboards()
        doc = None
        page = None
        for artboard in self.b.getArtboards():
            if page is None:
                doc = Document(w=artboard.width, h=artboard.height)
                page = doc[1]
            else:
                page = page.next
            # Create the element, and copy data from the artboard layers where necessary.
            self._createElements(page, artboard)

        return doc

    def save(self):
        pass

    def newDocument(self, w, h):
        pass

    def newDrawing(self):
        pass

    def newPage(self, w, h):
        pass

    def getFlattenedPath(self, path=None):
        pass

    def getFlattenedContours(self, path=None):
        pass

    def getGlyphPath(self, glyph, p=None, path=None):
        pass

if __name__ == '__main__':
  import doctest
  import sys
  sys.exit(doctest.testmod()[0])
