
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
#     Supporting usage of InDesign API-scripting
# -----------------------------------------------------------------------------
#
#     idmlcontext.py

from pagebot.contexts.basecontext import BaseContext
from pagebot.contexts.builders.idmlbuilder import IdmlBuilder
from pagebot.contexts.strings.idmlstring import IdmlString

class IdmlContext(BaseContext):

    # Used by the generic BaseContext.newString( )
    STRING_CLASS = IdmlString
    EXPORT_TYPES = ('idml',)

    def __init__(self):
        """Constructor of InDesignContext.

        >>> context = IdmlContext()
        """
        super().__init__()
        self.b = IdmlBuilder() # cls.b builder for this context.
        self.name = self.__class__.__name__

    def newDrawing(self, path=None):
        pass

    def newPage(self, w, h):
        """Ignore for now in this context."""

    def frameDuration(self, frameDuration):
        """Ignore for now in this context."""

    def fill(self, c):
        """
        FIXME: signature differs from DrawBot.
        def fill(self, r, g=None, b=None, a=None, alpha=None):
        
        Ignore for now in this context."""

    def stroke(self, c, w=None):
        """Ignore for now in this context."""

    # Basic shapes.

    def rect(self, x, y, w, h):
        """Ignore for now in this context."""

    def oval(self, x, y, w, h):
        """Ignore for now in this context."""

    def newString(self, s, e=None, style=None, w=None, h=None, pixelFit=True):
        """Creates a new styles BabelString instance of self.STRING_CLASS from
        `s` (converted to plain unicode string), using e or style as
        typographic parameters. Ignore and just answer `s` if it is already a
        self.STRING_CLASS instance and no style is forced. PageBot function.
        
        Ignore for now in this context."""
        return ''

    def text(self, sOrBs, p):
        """Ignore for now in this context."""

    def image(self, path, p, alpha=1, pageNumber=None, w=None, h=None):
        """Ignore for now in this context."""

    def imageSize(self, path):
        """Answers the (w, h) image size of the image file at path. If the path is an SVG
        image, then determine by parsing the SVG-XML.

        if path.lower().endswith('.'+FILETYPE_SVG):
            import xml.etree.ElementTree as ET
            svgTree = ET.parse(path)
            print(svgTree)
            return pt(1000, 1000)

        return pt(self.b.imageSize(path))
        """
        return pt(1000, 1000)

    def saveImage(self, path):
        """Ignore for now in this context."""



