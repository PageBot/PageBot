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
from pagebot.contexts.basecontext import BaseContext
from pagebot.contexts.builders.htmlbuilder import HtmlBuilder
from pagebot.contexts.strings.htmlstring import HtmlString

class HtmlContext(BaseContext):
    """A HtmlContext instance builds all necessary for a website, taking the element.
    Most of the building is done by the HtmlBuilder instance, stored as self.b.
    Still we need this HtmlContext layer, as not all drawing can be done in html, so 
    this context can decide to include SVG or pixel images for certain types of elements.
    """
    
    # Used by the generic BaseContext.newString( )
    STRING_CLASS = HtmlString
    EXPORT_TYPES = ('html', 'css', 'js')

    def __init__(self):
           self.b = HtmlBuilder()

    #   T E X T

    def newBulletString(self, bullet, e=None, style=None):
        """Answer the string with a bullet. As HTML does bullets automatic. Ignore answered None"""
        return None 

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
        """Answer the (w, h) image size of the image file at path."""
        return (0, 0)
        #return cls.b.imageSize(path)

    #   C O L O R

    def setFillColor(self, c, b=None):
        pass

    fill = setFillColor # DrawBot compatible API
      
    def setStrokeColor(self, c, w=None, b=None):
        pass

    stroke = setStrokeColor # DrawBot compatible API
       

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
