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
#     sketchbuilder.py
#
from pagebot.contexts.basecontext.basebuilder import BaseBuilder
from sketchapp2py.sketchapi import SketchApi

class SketchBuilder(BaseBuilder):
    PB_ID = 'Sketch'

    def __init__(self, path=None, **kwargs):
    	"""
        >>> import sketchapp2py
        >>> from pagebot.toolbox.transformer import path2Dir
        >>> path = path2Dir(sketchapp2py.__file__) + '/Resources/TemplateSquare.sketch'
		>>> b = SketchBuilder(path)
		>>> b.sketchApi
		<SketchApi path=TemplateSquare.sketch>
		>>> sketchPage = b.sketchApi.selectPage(0)
		>>> sketchPage, sketchPage.frame
		(<SketchPage name=Page 1>, <SketchRect x=0 y=0 w=0 h=0>)

    	"""
    	super().__init__(**kwargs)
    	self.sketchApi = SketchApi(path)

    def frameDuration(self, frameDuration):
        pass

    def save(self):
        pass

    def fill(self, e, g, b, alpha=None):
        pass


if __name__ == '__main__':
  import doctest
  import sys
  sys.exit(doctest.testmod()[0])


