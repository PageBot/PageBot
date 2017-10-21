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
import os

#import imageio
#Could be used for animated gifs and other export. Gives currently an error
#File "/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/numpy/lib/npyio.py", line 32, in <module>
#ImportError: No module named future_builtins

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

    # In case of specific builder addressing, callers can check here.
    isFlat = True

    # Used by the generic BaseContext.newString( )
    STRING_CLASS = FlatString
    NEW_STRING = newFlatString

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
            if len(self.pages) == 1 or not multiPage:
                self.pages[0].image(kind='rgb').png(path)
            else:
                for n, p in enumerate(self.pages):
                    pagePath = path.replace('.png', '%03d.png' % n)
                    p.image(kind='rgb').png(pagePath)
        elif path.endswith('.jpg'):
            if len(self.pages) == 1 or not multiPage:
                self.pages[0].image(kind='rgb').jpeg(path)
            else:
                for n, p in enumerate(self.pages):
                    pagePath = path.replace('.png', '%03d.png' % n)
                    p.image(kind='rgb').jpeg(pagePath)
        elif path.endswith('.svg'):
            if len(self.pages) == 1 or not multiPage:
                self.pages[0].svg(path)
            else:
                for n, p in enumerate(self.pages):
                    pagePath = path.replace('.png', '%03d.png' % n)
                    p.svg(pagePath)
        elif path.endswith('.pdf'):
            self.doc.pdf(path)

    def newPage(self, w, h):
        u"""Other page sizes than default in self.doc, are ignored in Flat."""
        self.page = self.doc.addpage()
        self.page.size(w, h, units='pt')
        self.pages.append(self.page)

    #   C A N V A S

    def saveGraphicState(self):
        pass # Not implemented?

    def restoreGraphicState(self):
        pass # Not implemented?

    #   T E X T

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
        if shape is not None:
            print '234423423234', x, y, w, h, shape
            self.page.place(shape.rectangle(x, y, w, h))

    def oval(self, x, y, w, h):
        shape = self._getShape()
        if shape is not None:
            self.page.place(shape.ellipse(x, y, w, h)) 

    def circle(self, x, y, r):
        shape = self._getShape()
        if shape is not None:
            self.page.place(shape.circle(x, y, w, r)) 

    def line(self, (x1, y1), (x2, y2)):
        print self.fillColor, self.strokeColor, self.strokeWidth
        shape = self._getShape()
        if shape is not None:
            self.page.place(shape.line(x1, y1, x2, y2))

    #   S H A D O W  &  G R A D I E N T

    def setShadow(self, eShadow):
        u"""Set the DrawBot graphics state for shadow if all parameters are set. Pair the call of this
        method with self._resetShadow()"""
        pass # Not implemented?

    def resetShadow(self):
        pass # Not implemented?

    def setGradient(self, gradient, e, origin):
        pass # Not implemented?

    def lineDash(self, *lineDash):
        pass # Not implemented?

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
            # Not supported in PDF, leave out for general compatibility?
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
            # Not supported in PDF, leave out for general compatibility?
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
            self.strokeWidth = 20#w

    #   E X P O R T

    def create_gif(self, filenames, duration):
        images = []
        for filename in filenames:
            images.append(imageio.imread(filename))
        output_file = 'Gif-%s.gif' % datetime.datetime.now().strftime('%Y-%M-%d-%H-%M-%S')
        imageio.mimsave(output_file, images, duration=duration)

