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
#  Eqivalent classes on PageBot <--> SketchApp2Py
#  Publication       Sketch file
#  Document          SketchApi
#  Page              SketchPage
#  Page.elements     SketchPage.layers = ArtBoards
#  Page.elements     SketchArtBoard.layers
#
#  The SketchContext is, together with the 
from pagebot.constants import FILETYPE_SKETCH, A4
from pagebot.contexts.basecontext.basecontext import BaseContext
from pagebot.contexts.sketchcontext.sketchbuilder import SketchBuilder
#from pagebot.toolbox.color import color
#from pagebot.toolbox.units import asNumber, pt
#from pagebot.toolbox.transformer import path2Dir, path2Extension
from pagebot.elements import *
from sketchapp2py.sketchapi import *

class SketchContext(BaseContext):

    W, H = A4 # Default size of a document, as SketchApp has infinite canvas.

    def __init__(self, path=None):
        """Constructor of Sketch context.

        >>> import sketchapp2py
        >>> from pagebot.toolbox.transformer import path2Dir
        >>> path = path2Dir(sketchapp2py.__file__) + '/Resources/TemplateSquare.sketch'
        >>> context = SketchContext(path)
        >>> doc = context.getDocument()
        >>> doc.w, doc.h
        (300pt, 400pt)
        """
        super().__init__()
        self.name = self.__class__.__name__
        self.b = SketchBuilder(path)
        self.shape = None # Current open shape
        self.fileType = FILETYPE_SKETCH

    def read(self, path):
        """
        >>>
        """
        self.b = SketchBuilder(path)
        return self.b

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
        Sketch Artboards as pages.

        >>>
        """
        doc = Document(w=300, h=400, contect=self)
        self.b
        """
        sketchPages = self.b.getArtBoards()
        doc = None
        page = None
        for artboard in self.b.getArtBoards():
            if page is None:
                doc = Document(w=artboard.width, h=artboard.height)
                page = doc[1]
            else:
                page = page.next
            # Create the element, and copy data from the artboard layers where necessary.
            self._createElements(page, artboard)
        """
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
