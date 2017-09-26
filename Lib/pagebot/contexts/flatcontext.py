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
#     flatcontext.py
#
from basecontext import BaseContext
from pagebot.contexts.builders.flatbuilder import flatBuilder
from pagebot.contexts.strings. flatstring import FlatString, newFlatString

class FlatContext(BaseContext):
    u"""A FlatContext instance combines the specific functions of the Flat library, 
    and offers a PageBot “standard” API, so it can be swapped with the DrawBotContext.
    This way it way it also hides e.g. the type of BabelString
    instance needed, and the type of HTML/CSS file structure to be created."""

 
    def __init__(self):
        # Keep status of last color, to make difference between fill and stroke colors.
        self.fillColor = None
        self.strokeColor = None

        self.b = flatBuilder # Builder for this canvas.
        
        self.doc = None
        self.pages = []
        self.style = None # Current open style
        self.image = None # Current open image
        self.shape = None # Current open shape
        self.flatString = None

    def newDocument(self, w, h, units='pt'):
        self.doc = self.b.document(w, h, units)

    def saveDocument(self, doc, path, multiPages=True):
        if path.endswidth('png'):
            for p in self.pages:
                #p.png(path)
                pass
        elif path.endswith('svg'):
            for p in self.pages:
                #p.svg(path)
                pass
        elif page.endswith('pdf'):
            self.doc.pdf(path)

    #   T E X T

    def newString(self, s, e=None, style=None, w=None, h=None, fontSize=None, 
            styleName=None, tagName=None):
        u"""Create a new styles BabelString(FlatString) instance from s, using e or style.
        Ignore and answer s if it is already a FlatString."""
        if isinstance(s, basestring):
            s = newFlatString(s, self, e=e, style=style, w=w, h=h, 
                fontSize=fontSize, styleName=styleName, tagName=tagName)
        assert isinstance(s, FlatString)
        return s

    def newBulletString(self, bullet, e=None, style=None):
        return cls.newString(bullet, e=e, style=style)

    #   D R A W I N G

    def rect(self, x, y, w, h):
        self.b.rect(x, y, w, h)
        
    #   C O L O R

    def setFillColor(self, c, cmyk=False, spot=False, overprint=False):
        u"""Set the color for global or the color of the formatted string.
        See: http://xxyxyz.org/flat, color.py."""
        b = self.b
        if c is NO_COLOR:
            self.fillColor = None
            return # Color is undefined, do nothing.
        if c is None:
            self.fillColor = b.ga(0, 0) # Ignore by total transparant
            return
        if isinstance(c, (float, long, int)): # Grayscale
            self.fillColor = b.gray(c * 255, )
            return
        if isinstance(c, (list, tuple)):
            if len(c) == 2 and isinstance(c[0], basestring) and isinstance(c[1], (list,tuple)):
                name, cmyk = c
                self.fillColor = b.spot(name, cmyk)
                return
            if len(c) == 2:
                gray, opacity = c
                self.fillColor = b.ga(gray, opacity)
                return
            if cmyk:
                c_, m, y, k = c
                self.fillColor = b.cmyk(c_, m, y, k)
                return
            if len(c) == 4: # rgb and opaque
                r, g, b, a = c
                self.fillColor = b.rgba(r, g, b, a)
                return
            if len(c) == 3:
                r, g, b = c
                self.fillColor = b.rgb(r, g, b)
                return

        raise ValueError('FlatContext.setFillColor: Error in color format "%s"' % repr(c))

    @classmethod
    def setStrokeColor(cls, c, w=1, cmyk=False, b=None):
        u"""Set global stroke color or the color of the formatted string."""
        # TODO: Make this work in Flat
        b = self.b
        success = False
        if c is NO_COLOR:
            self.strokeColor = None
            success = True # Color is undefined, do nothing.
        elif c is None:
            self.strokeColor = b.ga(0, 0) # Ignore by total transparant
            success = True
        elif isinstance(c, (float, long, int)): # Grayscale
            self.strokeColor = b.gray(c * 255, )
            success = True
        elif isinstance(c, (list, tuple)):
            if len(c) == 2 and isinstance(c[0], basestring) and isinstance(c[1], (list,tuple)):
                name, cmyk = c
                self.strokeColor = b.spot(name, cmyk)
                success = True
            elif len(c) == 2:
                gray, opacity = c
                self.fillColor = b.ga(gray, opacity)
                success = True
            elif cmyk:
                c_, m, y, k = c
                self.strokeColor = b.cmyk(c_, m, y, k)
                success = True
            elif len(c) == 4: # rgb and opaque
                r, g, b, a = c
                self.strokeColor = b.rgba(r, g, b, a)
                success = True
            elif len(c) == 3:
                r, g, b = c
                self.strokeColor = b.rgb(r, g, b)
                success = True
        if not success:
            raise ValueError('FlatContext.setStrokeColor: Error in color format "%s"' % c)
        if w is not None:
            self.style.width = w


