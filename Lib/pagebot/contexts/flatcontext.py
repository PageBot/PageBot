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
from pagebot.style import NO_COLOR
from pagebot.contexts.builders.flatbuilder import flatBuilder
from pagebot.contexts.strings. flatstring import FlatString, newFlatString

class FlatContext(BaseContext):
    u"""A FlatContext instance combines the specific functions of the Flat library, 
    and offers a PageBot “standard” API, so it can be swapped with the DrawBotContext.
    This way it way it also hides e.g. the type of BabelString
    instance needed, and the type of HTML/CSS file structure to be created.
    https://github.com/xxyxyz/flat
    http://xxyxyz.org/flat
    """
 
    def __init__(self):
        # Keep status of last color, to make difference between fill and stroke colors.
        self.fillColor = None
        self.strokeColor = None
        self.strokeWidth = 0

        self.b = flatBuilder # Builder for this canvas.

        self.doc = None
        self.pages = []
        self.page = None # Current open page
        self.style = None # Current open style
        self.image = None # Current open image
        self.shape = None # Current open shape
        self.flatString = None

    def newDocument(self, w, h, units='pt'):
        self.doc = self.b.document(w, h, units)

    def saveDocument(self, path, multiPage=True):
        if path.endswith('.png'):
            for n, p in enumerate(self.pages):
                p.image(kind='rgb').png(path.replace('.png', '%03d.png' % n))
        elif path.endswith('.svg'):
            for p in self.pages:
                #p.svg(path)
                pass
        elif path.endswith('.pdf'):
            self.doc.pdf(path)

    def newPage(self, w, h):
        u"""Other page sizes than default in self.doc, are ignored in Flat."""
        self.page = self.doc.addpage()
        self.pages.append(self.page)

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

    def text(self, bs):
        self.b.text(bs.s, p)

    #   D R A W I N G

    def _getShape(self):
        if self.fillColor == NO_COLOR and self.strokeColor == NO_COLOR:
            return None
        shape = self.b.shape()
        if self.fillColor is None:
            shape.nofill()
        elif self.fillColor != NO_COLOR:
            shape.fill(self.fillColor)
        if self.strokeColor is None:
            shape.nostroke()
        elif self.strokeColor != NO_COLOR:
            shape.stroke(self.strokeColor).width(self.strokeWidth)
        return shape

    def rect(self, x, y, w, h):
        shape = self._getShape()
        print '@##@#@#', shape
        if shape is not None:
            self.page.place(shape.rectangle(x, y, w, h))

    #   C O L O R

    def setFillColor(self, c, cmyk=False, spot=False, overprint=False):
        u"""Set the color for global or the color of the formatted string.
        See: http://xxyxyz.org/flat, color.py."""
        b = self.b
        success = False
        if c is NO_COLOR:
            self.fillColor = NO_COLOR # Ignore drawing
            success = True # Color is undefined, do nothing.
        elif c is None:
            self.fillColor = None # No fill
            success = True
        elif isinstance(c, (float, long, int)): # Grayscale
            self.fillColor = b.gray(c * 255, )
            success = True
        elif isinstance(c, (list, tuple)):
            if len(c) == 2 and isinstance(c[0], basestring) and isinstance(c[1], (list,tuple)) and len(c[1]) == 4:
                name, cmyk = c
                self.fillColor = b.spot(name, cmyk)
                success = True
            # Not supported in PDF, leave out for compatibility?
            #elif len(c) == 2:
            #    gray, a = c
            #    self.fillColor = b.ga(gray, a)
            #    success = True
            elif cmyk:
                cyan, magenta, yellow, k = c
                self.fillColor = b.cmyk(cyan, magenta, yellow, k)
                success = True
            elif len(c) == 4: # rgb and opaque
                red, green, blue, a = c
                self.fillColor = b.rgba(red, green, blue, a)
                success = True
            elif len(c) == 3:
                red, green, blue = c
                self.fillColor = b.rgb(red, green, blue)
                success = True
        if not success:
            raise ValueError('FlatContext.setFillColor: Error in color format "%s"' % repr(c))

    def setStrokeColor(self, c, w=1, cmyk=False, b=None):
        u"""Set global stroke color or the color of the formatted string."""
        # TODO: Make this work in Flat
        b = self.b
        print 'ewrrewrrwe', c
        success = False
        if c is NO_COLOR:
            self.strokeColor = NO_COLOR # Ignore drawing
            success = True # Color is undefined, do nothing.
        elif c is None:
            self.strokeColor = None # no stroke
            success = True
        elif isinstance(c, (float, long, int)): # Grayscale
            self.strokeColor = b.gray(c * 255, )
            success = True
        elif isinstance(c, (list, tuple)):
            if len(c) == 2 and isinstance(c[0], basestring) and isinstance(c[1], (list,tuple)) and len(c[1]) == 4:
                name, cmyk = c
                self.strokeColor = b.spot(name, cmyk)
                success = True
            # Not supported in PDF, leave out for compatibility?
            #elif len(c) == 2:
            #    gray, a = c
            #    self.strokeColor = b.ga(gray, a)
            #    success = True
            elif cmyk:
                cyan, magenta, yellow, k = c
                self.strokeColor = b.cmyk(cyan, magenta, yellow, k)
                success = True
            elif len(c) == 4: # rgb and opaque
                red, green, blue, a = c
                self.strokeColor = b.rgba(red, green, blue, a)
                success = True
            elif len(c) == 3:
                red, green, blue = c
                self.strokeColor = b.rgb(red, green, blue)
                success = True
        if not success:
            raise ValueError('FlatContext.setStrokeColor: Error in color format "%s"' % c)
        if w is not None:
            self.strokeWidth = w


