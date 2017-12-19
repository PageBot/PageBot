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
#     http://xxyxyz.org/flat
#
import os

'''
FIXME
import imageio
Could be used for animated gifs and other export. Currently gives an error:

File "/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/numpy/lib/npyio.py", line 32, in <module>
ImportError: No module named future_builtins
'''

from pagebot import getFontPath
from basecontext import BaseContext
from pagebot.style import NO_COLOR
from pagebot.contexts.builders.flatbuilder import flatBuilder
from pagebot.contexts.strings.flatstring import FlatString
from pagebot.toolbox.transformer import path2Name

def iround(value):
    return min(255, max(0, int(round(value*255.0))))

class FlatContext(BaseContext):
    u"""A FlatContext instance combines the specific functions of the Flat
    library, and offers a PageBot “standard” API, so it can be swapped with the
    DrawBotContext. This way it way it also hides e.g. the type of BabelString
    instance needed, and the type of HTML/CSS file structure to be created.

    * https://github.com/xxyxyz/flat
    * http://xxyxyz.org/flat
    """

    # In case of specific builder addressing, callers can check here.
    isFlat = True

    # Used by the generic BaseContext.newString( )
    STRING_CLASS = FlatString

    def __init__(self):
        # Keep status of last color, to make difference between fill and stroke colors.
        self.fillColor = None
        self.strokeColor = None
        self.strokeWidth = 0

        self.b = flatBuilder # Builder for this canvas, e.g. equivalent of bare drawbot.fill( )

        # Dictionary of fontName-fontPath relations. Initialize with default PageBot fonts.
        self.fontPaths = self._findFontPaths()

        self.doc = None
        self.pages = []
        self.page = None # Current open page
        self.style = None # Current open style
        self.image = None # Current open image
        self.shape = None # Current open shape
        self.flatString = None

        self._pathCommands = None # Collect path commnands here before drawing the path.

    def newDocument(self, w, h, units='pt'):
        self.doc = self.b.document(w, h, units)

    def saveDocument(self, path, multiPage=True):
        u"""Save the document to file(s)."""
        if path.endswith('.png'):
            if len(self.pages) == 1 or not multiPage:
                self.pages[0].image(kind='rgba').png(path)
            else:
                for n, p in enumerate(self.pages):
                    pagePath = path.replace('.png', '%03d.png' % n)
                    p.image(kind='rgba').png(pagePath)
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

    saveImage = saveDocument # Compatible API with DrawBot

    def newPage(self, w, h, units='pt'):
        u"""Other page sizes than default in self.doc, are ignored in Flat."""
        if self.doc is None:
            self.newDocument(w, h, units)
        self.page = self.doc.addpage()
        self.page.size(w, h, units='pt')
        self.pages.append(self.page)

    #   C A N V A S

    def saveGraphicState(self):
        pass # Not implemented?

    def restoreGraphicState(self):
        pass # Not implemented?

    #   F O N T S

    def _findFontPaths(self, path=None, fontPaths=None):
        u"""Recursively find the default PageBot font paths. Answer the dictioanary of name-path relations."""
        if fontPaths is None:
            fontPaths = {}
        if path is None:
            path = getFontPath()
        for fileName in os.listdir(path):
            if fileName.startswith('.'):
                continue
            if not path.endswith('/'):
                path += '/'
            filePath = path + fileName
            if os.path.isdir(filePath):
                self._findFontPaths(filePath, fontPaths) # Recursively search in folder.
            elif fileName.lower().endswith('.ttf') or fileName.lower().endswith('.otf'):
                fontPaths[fileName] = filePath
        return fontPaths

    def installedFonts(self):
        u"""Answer the list with names of all installed fonts in the system, as available
        for cls.newString( ) style."""
        return self.fontPaths.keys()

    def installFont(self, fontPath):
        u"""Install the font in the context and answer the font (file)name."""
        # TODO: To be implemented later, if there is a real need for cached fonts.
        return path2Name(fontPath)

    def getFontPathOfFont(self, fontName):
        u"""Answer the path that is source of the given font name. Answer None if the font cannot be found."""
        return self.fontPaths.get(fontName)

    #   T E X T

    def newBulletString(self, bullet, e=None, style=None):
        return cls.newString(bullet, e=e, style=style)

    def text(self, bs, p):
        u"""Place the babelstring instance at position p. The position can be any 2D or 3D points tuple.
        Currently the z-axis is ignored. The FlatContext version of the BabelString is supposed to contain
        Flat.text. Note that in the Flat model, the positions is an attribute of the string, so
        strings cannot be reused to show on multiple positions."""
        placedText = self.page.place(bs.s)
        placedText.position(p[0], p[1])

    def textBox(self, bs, rect):
        x, y, w, h = rect
        placedText = self.page.place(bs.s)
        placedText.position(x, y)

    def textSize(self, bs, w=None, h=None):
        u"""Answer the size tuple (w, h) of the current text. Answer (0, 0) if there is no text defined.
        Answer the height of the string if the width w is given."""
        return self.b.textSize(self.s, w=w, h=h)

    def textOverflow(self, bs, bounds, align=LEFT):
        u"""Answer the overflowing of from the box (0, 0, w, h) as new FsString in 
        the current context."""
        return FlatString(self.b.textOverflow(bs.s, bounds, align), self)

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
            self.page.place(shape.rectangle(x, y, w, h))

    def oval(self, x, y, w, h):
        u"""Draw an oval in rectangle, where (x,y) is the bottom left origin and (w,h) is the size.
        This default DrawBot behavior, different from default Flat, where the (x,y) is the middle
        if the oval. Compensate for the difference."""
        shape = self._getShape()
        if shape is not None:
            self.page.place(shape.ellipse(x-w/2, y-h/2, w, h))

    def circle(self, x, y, r):
        u"""Draw an circle in square, with radius r and (x,y) as middle."""
        shape = self._getShape()
        if shape is not None:
            self.page.place(shape.circle(x, y, r))

    def line(self, p0, p1):
        shape = self._getShape()
        if shape is not None:
            self.page.place(shape.line(p0[0], p0[1], p1[0], p1[1]))

    def newPath(self):
        u"""Create a new path list, o collect the path commands."""
        self._pathCommands = [] # Collect path commands here.

    def drawPath(self, path=None, p=(0,0), sx=1, sy=None):
        shape = self._getShape()
        if shape is not None:
            self.page.place(shape.path(self._pathCommands))

    def moveTo(self, p):
        assert self._pathCommands is not None
        self._pathCommands.append(self.b.moveto(p[0], p[1]))

    def lineTo(self, p):
        assert self._pathCommands is not None
        self._pathCommands.append(self.b.lineto(p[0], p[1]))

    def quadTo(bcp, p):
        assert self._pathCommands is not None
        self._pathCommands.append(self.b.quadto(bcp[0], bcp[1], p[0], p[1]))

    def curveTo(self, bcp1, bcp2, p):
        assert self._pathCommands is not None
        self._pathCommands.append(self.b.curveto(bcp1[0], bcp1[1], bcp2[0], bcp2[1], p[0], p[1]))

    def closePath(self):
        assert self._pathCommands is not None
        self._pathCommands.append(self.b.closePath())

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
            self.fillColor = b.gray(iround(c))
            success = True
        elif isinstance(c, (list, tuple)):
            if len(c) == 2 and isinstance(c[0], basestring) and isinstance(c[1], (list,tuple)) and len(c[1]) == 4:
                name, (cyan, magenta, yellow, k) = c
                self.fillColor = b.spot(name, (iround(cyan), iround(magenta), iround(yellow)))
                success = True
            # Not supported in PDF, leave out for general compatibility?
            #elif len(c) == 2:
            #    gray, a = c
            #    self.fillColor = b.ga(gray, a)
            #    success = True
            elif cmyk:
                cyan, magenta, yellow, k = c
                self.fillColor = b.cmyk(iround(cyan), iround(magenta), iround(yellow), iround(k))
                success = True
            elif len(c) == 4: # rgb and opaque
                red, green, blue, a = c
                self.fillColor = b.rgba(iround(red), iround(green), iround(blue), iround(a))
                success = True
            elif len(c) == 3:
                red, green, blue = c
                self.fillColor = b.rgb(iround(red), iround(green), iround(blue))
                success = True
        if not success:
            raise ValueError('FlatContext.setFillColor: Error in color format "%s"' % repr(c))

    fill = setFillColor # DrawBot compatible API

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
            self.strokeColor = b.gray(iround(c))
            success = True
        elif isinstance(c, (list, tuple)):
            if len(c) == 2 and isinstance(c[0], basestring) and isinstance(c[1], (list,tuple)) and len(c[1]) == 4:
                name, (cyan, magenta, yellow, k) = c
                self.strokeColor = b.spot(name, (iround(cyan), iround(magenta), iround(yellow)))
                success = True
            # Not supported in PDF, leave out for general compatibility?
            #elif len(c) == 2:
            #    gray, a = c
            #    self.strokeColor = b.ga(gray, a)
            #    success = True
            elif cmyk:
                cyan, magenta, yellow, k = c
                self.strokeColor = b.cmyk(iround(cyan), iround(magenta), iround(yellow), iround(k))
                success = True
            elif len(c) == 4: # rgb and opaque
                red, green, blue, a = c
                self.strokeColor = b.rgba(iround(red), iround(green), iround(blue), iround(a))
                success = True
            elif len(c) == 3:
                red, green, blue = c
                self.strokeColor = b.rgb(iround(red), iround(green), iround(blue))
                success = True
        if not success:
            raise ValueError('FlatContext.setStrokeColor: Error in color format "%s"' % c)
        if w is not None:
            self.strokeWidth = w

    stroke = setStrokeColor # DrawBot compatible API

    #   E X P O R T

    def create_gif(self, filenames, duration):
        images = []
        for filename in filenames:
            images.append(imageio.imread(filename))
        output_file = 'Gif-%s.gif' % datetime.datetime.now().strftime('%Y-%M-%d-%H-%M-%S')
        imageio.mimsave(output_file, images, duration=duration)

