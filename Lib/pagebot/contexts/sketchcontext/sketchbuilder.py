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
#     sketchbuilder.py
#
from pagebot.contexts.basecontext.basebuilder import BaseBuilder
from pagebot.toolbox.units import upt
from pysketch.sketchapi import SketchApi

class SketchBuilder(BaseBuilder):
    PB_ID = 'Sketch'

    def __init__(self, path=None, **kwargs):
        """
        >>> import pysketch
        >>> from pagebot.filepaths import getResourcesPath
        >>> path = getResourcesPath() + '/sketch/TemplateSquare.sketch'
        >>> b = SketchBuilder(path)
        >>> b
        <SketchBuilder path=TemplateSquare.sketch>
        >>> b.sketchApi
        <SketchApi path=TemplateSquare.sketch>
        >>> sketchPage = b.sketchApi.selectPage(0)
        >>> sketchPage, sketchPage.frame
        (<SketchPage name=Page 1>, <SketchRect x=0 y=0 w=0 h=0>)
        """
        super().__init__(**kwargs)
        self.sketchApi = SketchApi(path)

    def __repr__(self):
        return '<%s path=%s>' % (self.__class__.__name__, self.sketchApi.sketchFile.path.split('/')[-1])

    def frameDuration(self, frameDuration):
        pass

    def save(self):
        pass

    def fill(self, e, g, b, alpha=None):
        pass


    def rect(self, x, y, w=None, h=None, **kwargs):
        self.sketchApi.rect(x=x, y=y, w=w, h=h, **kwargs)

    def _get_pages(self):
        """Answer the list of all SketchPage instances.

        >>> import pysketch
        >>> from pagebot.filepaths import getResourcesPath
        >>> path = getResourcesPath() + '/sketch/TemplateSquare.sketch'
        >>> b = SketchBuilder(path)
        >>> b.pages
        [<SketchPage name=Page 1>]
        """
        return self.sketchApi.getPages()
    pages = property(_get_pages)

    def _get_artboards(self):
        """Answer a list with all artboards on the current selected page.

        >>> import pysketch
        >>> from pagebot.filepaths import getResourcesPath
        >>> path = getResourcesPath() + '/sketch/TemplateSquare.sketch'
        >>> b = SketchBuilder(path)
        >>> b.artboards
        [<SketchArtboard name=Artboard 1 w=576 h=783>]
        """
        return self.sketchApi.getArtboards()
    artboards = property(_get_artboards)

    def _get_idLayers(self):
        """Answer the dictionary with {layer.do_objectID: layer, ...}

        """
        return self.sketchApi.getIdLayers()
    idLayers = property(_get_idLayers)

    def _get_size(self):
        return upt(self.sketchApi.getSize())
    size = property(_get_size)

    def restore(self):
        pass


if __name__ == '__main__':
  import doctest
  import sys
  sys.exit(doctest.testmod()[0])
