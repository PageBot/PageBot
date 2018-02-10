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
#import imageio
from pagebot import getFontPath
from basecontext import BaseContext
from pagebot.style import NO_COLOR
from pagebot.contexts.builders.flatbuilder import flatBuilder
from pagebot.contexts.strings.flatstring import FlatString
from pagebot.toolbox.transformer import path2Name
from pagebot.style import NO_COLOR, LEFT

def iround(value):
    return min(255, max(0, int(round(value*255.0))))

class FlatContext(BaseContext):
    u"""A FlatContext instance combines the specific functions of the Flat
    library, and offers a PageBot “standard” API, so it can be swapped with the
    DrawBotContext. This way it also hides e.g. the type of BabelString
    instance needed, and the type of HTML/CSS file structure to be created.

    * https://github.com/xxyxyz/flat
    * http://xxyxyz.org/flat
    """

    # In case of specific builder addressing, callers can check here.
    isFlat = True

    # Used by the generic BaseContext.newString( )
    STRING_CLASS = FlatString

    def __init__(self):
        u"""Constructor of Flat context.

        >>> context = FlatContext()
        >>> context.isFlat
        True
        >>> context.newDocument(100, 100)
        >>> context.doc.__class__.__name__
        'document'
        """
        # Keep status of last color, to make difference between fill and stroke colors.
        self.name = self.__class__.__name__
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
        self.shape = None # Current open shape
        self.flatString = None

        self._pathCommands = None # Collect path commnands here before drawing the path.

    #   V A R I A B L E

    def Variable(self, variableUI, globalVariables):
        # TODO: Make this work in Flat-way. Getting parameters from command line?
        pass

    #   D O C U M E N T

    def newDocument(self, w, h, units='pt'):
        u"""Create a new self.doc Flat canvas to draw on.

        >>> context = FlatContext()
        >>> context.isFlat
        True
        >>> context.newDocument(100, 100)
        >>> int(context.doc.width), int(context.doc.height)
        (100, 100)
        """
        self.doc = self.b.document(w, h, units)

    def saveDocument(self, path, multiPage=True):
        u"""Save the current document to file(s)

        >>> import os
        >>> from pagebot import getRootPath
        >>> exportPath = getRootPath() + '/_export/' # _export/* Files are ignored in git
        >>> if not os.path.exists(exportPath): os.makedirs(exportPath)
        >>> context = FlatContext()
        >>> w, h = 100, 100
        >>> context.newDocument(w, h)
        >>> context.newPage(w, h)
        >>> context.fill((0, 0, 0, 0))
        >>> context.rect(10, 10, w-20, h-20)
        >>> #context.saveDocument(exportPath + 'MyTextDocument_F.jpg') # Flat is too scrict with color-format match
        >>> #context.saveDocument(exportPath + 'MyTextDocument_F.pdf') # Flat is too scrict with color-format match
        >>> context.saveDocument(exportPath + 'MyTextDocument_F.png')
        >>> context.saveDocument(exportPath + 'MyTextDocument_F.gif')
        [FlatContext] Gif not yet implemented for "MyTextDocument_F.gif"
        """
        extension = path.split('.')[-1]
        if extension == 'png':
            if len(self.pages) == 1 or not multiPage:
                self.pages[0].image(kind='rgba').png(path)
            else:
                for n, p in enumerate(self.pages):
                    pagePath = path.replace('.png', '%03d.png' % n)
                    p.image(kind='rgba').png(pagePath)
        elif extension == 'jpg':
            if len(self.pages) == 1 or not multiPage:
                self.pages[0].image(kind='rgb').jpeg(path)
            else:
                for n, p in enumerate(self.pages):
                    pagePath = path.replace('.png', '%03d.png' % n)
                    p.image(kind='rgb').jpeg(pagePath)
        elif extension == 'svg':
            if len(self.pages) == 1 or not multiPage:
                self.pages[0].svg(path)
            else:
                for n, p in enumerate(self.pages):
                    pagePath = path.replace('.png', '%03d.png' % n)
                    p.svg(pagePath)
        elif extension == 'pdf':
            self.doc.pdf(path)
        elif extension == 'gif':
            print('[FlatContext] Gif not yet implemented for "%s"' % path.split('/')[-1])
        else:
            raise NotImplementedError('[FlatContext] File format "%s" is not implemented' % path.split('/')[-1])

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
        for self.newString( ) style."""
        return self.fontPaths.keys()

    def installFont(self, fontPath):
        u"""Install the font in the context and answer the font (file)name."""
        # TODO: To be implemented later, if there is a real need for cached fonts.
        return path2Name(fontPath)

    def getFontPathOfFont(self, fontName):
        u"""Answer the path that is source of the given font name. Answer None if the font cannot be found."""
        return self.fontPaths.get(fontName)

    def listOpenTypeFeatures(self, fontName):
        u"""Answer the list of opentype features available in the named font.
        TODO: Tobe implemented"""
        #return self.b.listOpenTypeFeatures(fontName)
        return []

    #   T E X T

    def newBulletString(self, bullet, e=None, style=None):
        return self.newString(bullet, e=e, style=style)

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
        Answer the height of the string if the width w is given.

        >>> w = h = 500
        >>> context = FlatContext()
        >>> context.newDocument(w, h)
        >>> context.newPage(w, h)
        >>> bs = context.newString('ABC ' * 100)
        >>> t = context.page.place(bs.s)
        >>> t = t.frame(0, 0, w, h)
        >>> t.overflow()
        False
        >>> bs = context.newString('ABC ' * 100000)
        >>> t = context.page.place(bs.s)
        >>> t = t.frame(0, 0, w, h)
        >>> t.overflow()
        True
        >>> lines = t.lines()
        >>> len(lines)
        35
        """
        # FIXME! This is a totally wrong boilerplate for now!

        #t = placedtext(bs.s)
        if not bs.s:
            return (0, 0)
        elif w is None:
            return (100, 100)
        else:
            return (w, w/len(bs))

    def textOverflow(self, bs, bounds, align=LEFT):
        u"""Answer the overflowing of from the box (0, 0, w, h) as new FlatString
        in the current context."""
        return FlatString(self.b.textOverflow(bs.s, bounds, align), self)

    def textBoxBaseLines(self, txt, box):
        raise NotImplementedError()

    #   I M A G E

    def imagePixelColor(self, path, p):
        return self.b.imagePixelColor(path, p)

    def imageSize(self, path):
        u"""Answer the (w, h) image size of the image file at path.

        >>> from pagebot import getRootPath
        >>> rootPath = getRootPath()
        >>> imagePath = rootPath + '/Examples/Magazines/Fashion/images/IMG_8914.jpg'
        >>> context = FlatContext()
        >>> context.imageSize(imagePath)
        (3024, 4032)
        """ 
        img = self.b.image.open(path)
        return img.width, img.height

    def image(self, path, p, alpha=1, pageNumber=None, w=None, h=None):
        u"""Draw the image. If w or h is defined, then scale the image to fit."""
        if w is None or h is None:
            w, h = self.imageSize(path)

        x, y, = p[0], p[1]
        self.save()
        img = self.b.image(path)
        img.resize(width=w, height=h)
        placed = self.page.place(img)
        placed.position(x, y)
        self.restore()

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

    def quadTo(self, bcp, p):
        assert self._pathCommands is not None
        self._pathCommands.append(self.b.quadto(bcp[0], bcp[1], p[0], p[1]))

    def curveTo(self, bcp1, bcp2, p):
        assert self._pathCommands is not None
        self._pathCommands.append(self.b.curveto(bcp1[0], bcp1[1], bcp2[0], bcp2[1], p[0], p[1]))

    def closePath(self):
        assert self._pathCommands is not None
        self._pathCommands.append(self.b.closepath)

    #   S H A D O W  &  G R A D I E N T

    def setShadow(self, eShadow):
        u"""Set the DrawBot graphics state for shadow if all parameters are set. Pair the call of this
        method with self._resetShadow()"""
        pass # Not implemented?

    def resetShadow(self):
        pass # Not implemented?

    def setGradient(self, gradient, origin, w, h):
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
        """
        #TODO: Not implement yet. 
        images = []
        for filename in filenames:
            images.append(imageio.imread(filename))
        output_file = 'Gif-%s.gif' % datetime.now().strftime('%Y-%M-%d-%H-%M-%S')
        imageio.mimsave(output_file, images, duration=duration)
        """

if __name__ == '__main__':
    import doctest
    doctest.testmod()

  
