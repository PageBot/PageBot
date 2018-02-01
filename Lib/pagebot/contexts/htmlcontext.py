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
#     htmlcontext.py
#
from basecontext import BaseContext
from pagebot.contexts.builders.webbuilder import WebBuilder
from pagebot.contexts.strings.htmlstring import HtmlString

class HtmlContext(BaseContext):
    u"""A HtmlContext instance combines the specific functions of the Flat library
    This way it way it hides e.g. the type of BabelString
    instance needed, and the type of HTML/CSS file structure to be created."""

    # Used by the generic BaseContext.newString( )
    STRING_CLASS = HtmlString

    def __init__(self):
        self.b = WebBuilder()

    #   T E X T

    def newBulletString(self, bullet, e=None, style=None):
        return None # HTML does bullets automatic. Ignore answered None.

    #   D R A W I N G

    def rect(self, x, y, w, h):
        pass
    
    def oval(self, x, y, w, h):
        pass
    
    def circle(self, x, y, r):
        pass
    
    def line(self, p1, p2):
        pass

    #   I M A G E

    def imagePixelColor(self, path, p):
        return 0
        #return cls.b.imagePixelColor(path, p)

    def imageSize(self, path):
        u"""Answer the (w, h) image size of the image file at path."""
        return (0, 0)
        #return cls.b.imageSize(path)

    #   C O L O R

    def setFillColor(self, c, cmyk=False, b=None):
        pass

    fill = setFillColor # DrawBot compatible API
      
    def setStrokeColor(self, c, w=1, cmyk=False, b=None):
        pass

    stroke = setStrokeColor # DrawBot compatible API
       
