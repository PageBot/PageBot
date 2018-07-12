# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     flatcontext.py
#
#     http://xxyxyz.org/flat
#
#import imageio
from pagebot.contexts.basecontext import BaseContext
from pagebot.contexts.builders.flatbuilder import flatBuilder, BezierPath
from pagebot.contexts.strings.flatstring import FlatString
from pagebot.style import NO_COLOR, LEFT, DEFAULT_FONT_PATH, DEFAULT_FONT_SIZE

def iround(value):
    return min(255, max(0, int(round(value*255.0))))

class FlatContext(BaseContext):
    """A FlatContext instance combines the specific functions of the Flat
    library, and offers a PageBot “standard” API, so it can be swapped with the
    DrawBotContext. This way it also hides e.g. the type of BabelString
    instance needed, and the type of HTML/CSS file structure to be created.

    * https://github.com/xxyxyz/flat
    * http://xxyxyz.org/flat

    Text behavior:
    st = strike(font)
        st.size(size, leading=0.0, units='pt')
        st.color(color)
        st.width(string)

        sp = st.span(string)
        par = st.paragraph(string)
        tx = st.text(string)

    placed = page.place()
    outl = outlines(string)

    par = paragraph(spans)

    placed = placetext()
        placed.position(x, y)
        placed.frame(x, y, w, h)
        placed.overflow()
        placed.lines()

    """

    # In case of specific builder addressing, callers can check here.
    isFlat = True

    # Used by the generic BaseContext.newString( )
    STRING_CLASS = FlatString
    EXPORT_TYPES = ('pdf', 'svg', 'png', 'jpg')

    def __init__(self):
        """Constructor of Flat context.

        >>> context = FlatContext()
        >>> context.isFlat
        True
        >>> context.newDocument(100, 100)
        >>> context.doc.__class__.__name__
        'document'
        """
        # Keep status of last color, to make difference between fill and stroke colors.
        self.name = self.__class__.__name__
        self._fill = None
        self._stroke = None
        self._strokeWidth = 0
        self._font = DEFAULT_FONT_PATH # Optional setting of the current font and fontSize
        self._fontSize = DEFAULT_FONT_SIZE
        self._frameDuration = 0
        self._ox = 0 # Origin set by self.translate()
        self._oy = 0
        self._rotate = 0

        self._gState = [] # Stack of graphic states.
        self.save() # Save current set of values on gState stack.

        self.b = flatBuilder # Builder for this canvas, e.g. equivalent of bare drawbot.fill( )

        self.doc = None
        self.pages = []
        self.page = None # Current open page
        self.style = None # Current open style
        self.shape = None # Current open shape
        self.flatString = None

        self._path = None # Collect path commnands here before drawing the path.

    #   V A R I A B L E

    def Variable(self, variableUI, globalVariables):
        # TODO: Make this work in Flat-way. Getting parameters from command line?
        pass

    #   D O C U M E N T

    def newDocument(self, w, h, title=None, pageCount=None, units='pt'):
        """Create a new self.doc Flat canvas to draw on.

        >>> context = FlatContext()
        >>> context.isFlat
        True
        >>> context.newDocument(100, 100)
        >>> int(context.doc.width), int(context.doc.height)
        (100, 100)
        """
        self.title = title
        self.pageCount = pageCount
        self.doc = self.b.document(w, h, units)

    def saveDocument(self, path, multiPage=True):
        """Save the current document to file(s)

        >>> import os
        >>> from pagebot import getRootPath
        >>> exportPath = getRootPath() + '/_export' # _export/* Files are ignored in git
        >>> if not os.path.exists(exportPath): os.makedirs(exportPath)
        >>> context = FlatContext()
        >>> w, h = 100, 100
        >>> context.newDocument(w, h)
        >>> context.newPage(w, h)
        >>> context.fill((0, 0, 0))
        >>> context.rect(10, 10, w-20, h-20)
        >>> context.saveDocument(exportPath + '/MyTextDocument_F.jpg') # Flat is too scrict with color-format match
        >>> context.saveDocument(exportPath + '/MyTextDocument_F.pdf') # Flat is too scrict with color-format match
        >>> context.saveDocument(exportPath + '/MyTextDocument_F.png')
        >>> context.saveDocument(exportPath + '/MyTextDocument_F.gif')
        [FlatContext] Gif not yet implemented for "MyTextDocument_F.gif"
        """
        self.checkExportPath(path) # In case path starts with "_export", make sure that the directories exist.
        extension = path.split('.')[-1]
        if extension == 'png':
            if len(self.pages) == 1 or not multiPage:
                self.pages[0].image(kind='rgba').png(path)
            else:
                for n, p in enumerate(self.pages):
                    pagePath = path.replace('.png', '%03d.png' % n)
                    p.image(kind='rgb').png(pagePath)
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
        """Other page sizes than default in self.doc, are ignored in Flat.

        >>> context = FlatContext()
        >>> w, h = 100, 100
        >>> context.newDocument(w, h)
        >>> context.newPage(w, h)
        """
        if self.doc is None:
            self.newDocument(w, h, units)
        self.page = self.doc.addpage()
        self.page.size(w, h, units='pt')
        self.pages.append(self.page)

    def newDrawing(self):
        """Clear output canvas, start new export file.

        >>> context = FlatContext()
        >>> context.newDocument(100, 100)
        """
        # FIXME: needs a width and height, so different from DrawBot?
        #context = FlatContext()
        #context.newDrawing(w, h)
        pass

    #   C A N V A S

    def saveGraphicState(self):
        """Save the current graphic state.

        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> context = FlatContext()
        >>> context._font.endswith('Roboto-Regular.ttf')
        True
        >>> context.save()
        >>> boldFont = findFont('Roboto-Bold')
        >>> context.font(boldFont) # Set by Font instance
        >>> context._font.endswith('Roboto-Bold.ttf')
        True
        >>> context.restore() # Restore to original graphic state values
        >>> context._font.endswith('Roboto-Regular.ttf')
        True
        """
        gState = dict(
            font=self._font,
            fontSize=self._fontSize,
            fill=self._fill,
            stroke=self._stroke,
            strokeWidth=self._strokeWidth,
            ox=self._ox,
            oy=self._oy,
            rotate=self._rotate,
        )
        self._gState.append(gState)

    save = saveGraphicState

    def restoreGraphicState(self):
        gState = self._gState.pop()
        self._font = gState['font']
        self._fontSize = gState['fontSize']
        self._fill = gState['fill']
        self._stroke = gState['stroke']
        self._strokeWidth = gState['strokeWidth']
        self._ox = gState['ox']
        self._oy = gState['oy']
        self._rotate = gState['rotate']

    restore = restoreGraphicState

    def translate(self, ox, soy):
        """Shift the origin of the canvas by (ox, oy).
        TODO: To be implenented."""
        pass

    #   F O N T S

    def listOpenTypeFeatures(self, fontName):
        """Answer the list of opentype features available in the named font.
        TODO: To be implemented."""
        #return self.b.listOpenTypeFeatures(fontName)
        return []

    #   F R A M E S
    def frameDuration(self, secondsPerFrame):
        """Set the frame duretion for animated gifs to a number of seconds per frame."""
        self._frameDuration = secondsPerFrame

    #   T E X T

    def newBulletString(self, bullet, e=None, style=None):
        return self.newString(bullet, e=e, style=style)

    def text(self, bs, p):
        """Place the babelstring instance at position p. The position can be any 2D or 3D points tuple.
        Currently the z-axis is ignored. The FlatContext version of the BabelString is supposed to contain
        Flat.text. Note that in the Flat model, the positions is an attribute of the string, so
        strings cannot be reused to show on multiple positions.

        >>> context = FlatContext()
        >>> style = dict(font='Roboto-Regular', fontSize=12)
        >>> bs = context.newString('ABC', style=style)
        >>> bs.__class__.__name__
        'FlatString'
        >>> #context.text(bs, (100, 100))

        """
        assert isinstance(bs, FlatString)
        placedText = self.page.place(bs.s)
        placedText.position(p[0], p[1])

    def font(self, font, fontSize=None):
        """Set the current font, in case it is not defined in a formatted string.
        font can be a Font instance, or a full font file path, or an abbreveation that can be found
        by family or by findFont.

        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> font = findFont('Roboto-Regular')
        >>> context = FlatContext()
        >>> context.font(font.path)
        >>> context._font.endswith('/Roboto-Regular.ttf')
        True
        >>> context.font('OtherFont', 12) # Font does not exists, font path is set to DEFAULT_FONT_PATH
        >>> context._font == DEFAULT_FONT_PATH
        True
        >>> context._fontSize
        12
        """
        from pagebot.fonttoolbox.fontpaths import getFontPathOfFont

        self._font = getFontPathOfFont(font) # Convert name or path to font path.
        if fontSize is not None:
            self._fontSize = fontSize

    def fontSize(self, fontSize):
        """Set the current fontSize, in case it is not defined in a formatted string

        >>> context = FlatContext()
        >>> context.fontSize(12)
        >>> context._fontSize
        12
        """
        self._fontSize = fontSize

    def textBox(self, bs, rect):
        x, y, w, h = rect
        placedText = self.page.place(bs.s)
        placedText.position(x, y)

    def textSize(self, bs, w=None, h=None):
        """Answer the size tuple (w, h) of the current text. Answer (0, 0) if there is no text defined.
        Answer the height of the string if the width w is given.

        >>> w = h = 500
        >>> context = FlatContext()
        >>> context.newDocument(w, h)
        >>> context.newPage(w, h)
        >>> style = dict(font='Roboto-Regular', fontSize=12)
        >>> bs = context.newString('ABC ' * 100, style=style)
        >>> t = context.page.place(bs.s)
        >>> t = t.frame(0, 0, w, h)
        >>> t.overflow()
        False
        >>> bs = context.newString('ABC ' * 100000, style=style)
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
        """Answer the overflowing of from the box (0, 0, w, h) as new FlatString
        in the current context."""
        return FlatString(self.b.textOverflow(bs.s, bounds, align), self)

    def textBoxBaseLines(self, txt, box):
        raise NotImplementedError()

    #   I M A G E

    def imagePixelColor(self, path, p):
        return self.b.imagePixelColor(path, p)

    def imageSize(self, path):
        """Answer the (w, h) image size of the image file at path.

        >>> from pagebot import getResourcesPath
        >>> imagePath = getResourcesPath() + '/images/peppertom_lowres_398x530.png'
        >>> context = FlatContext()
        >>> context.imageSize(imagePath)
        (398, 530)
        """
        img = self.b.image.open(path)
        return img.width, img.height

    def image(self, path, p, alpha=1, pageNumber=None, w=None, h=None):
        """Draw the image. If w or h is defined, then scale the image to fit."""
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
        if self._fill == NO_COLOR and self._stroke == NO_COLOR:
            return None
        shape = self.b.shape()
        if self._fill is None:
            shape.nofill()
        elif self._fill != NO_COLOR:
            shape.fill(self._fill)
        if self._stroke is None:
            shape.nostroke()
        elif self._stroke != NO_COLOR:
            shape.stroke(self._stroke).width(self._strokeWidth)
        return shape

    def ensure_page(self):
        if not self.doc:
            self.newDocument(0, 0)
        if not self.pages:
            self.newPage(self.doc.w, self.doc.h)

    def rect(self, x, y, w, h):
        shape = self._getShape()
        if shape is not None:
            self.ensure_page()
            self.page.place(shape.rectangle(x, y, w, h))

    def oval(self, x, y, w, h):
        """Draw an oval in rectangle, where (x,y) is the bottom left origin and (w,h) is the size.
        This default DrawBot behavior, different from default Flat, where the (x,y) is the middle
        if the oval. Compensate for the difference."""
        shape = self._getShape()
        if shape is not None:
            self.ensure_page()
            self.page.place(shape.ellipse(x-w/2, y-h/2, w, h))

    def circle(self, x, y, r):
        """Draw an circle in square, with radius r and (x,y) as middle."""
        shape = self._getShape()
        if shape is not None:
            self.ensure_page()
            self.page.place(shape.circle(x, y, r))

    def line(self, p0, p1):
        shape = self._getShape()
        if shape is not None:
            self.ensure_page()
            self.page.place(shape.line(p0[0], p0[1], p1[0], p1[1]))

    def newPath(self):
        """Create a new path list, o collect the path commands."""
        self._path = BezierPath(self.b) # Collect path commands here.
        return self._path

    def drawPath(self, path=None, p=(0,0), sx=1, sy=None):
        shape = self._getShape()
        if shape is not None:
            self.ensure_page()
            self.page.place(shape.path(self._path.commands))

    def moveTo(self, p):
        assert self._path is not None
        self._path.moveTo(p)

    def lineTo(self, p):
        assert self._path is not None
        self._path.lineTo(p)

    def quadTo(self, bcp, p):
        assert self._path is not None
        self._path.quadTo(bcp, p)

    def curveTo(self, bcp1, bcp2, p):
        assert self._path is not None
        self._path.curveTo(bcp1, bcp1, bcp2, p)

    def closePath(self):
        assert self._path is not None
        self._path.closePath()

    def bezierPathByFlatteningPath(self, path):
        """TODO: Make Flat version of the NSBezier flatten path function."""
        return None #path.getNSBezierPath().bezierPathByFlatteningPath()

    #   S H A D O W  &  G R A D I E N T

    def setShadow(self, eShadow):
        """Set the DrawBot graphics state for shadow if all parameters are set."""
        pass # Not implemented?

    def setGradient(self, gradient, origin, w, h):
        pass # Not implemented?

    def lineDash(self, *lineDash):
        pass # Not implemented?

    #   C O L O R

    def setFillColor(self, c, cmyk=False, spot=False, overprint=False):
        """Set the color for global or the color of the formatted string.
        See: http://xxyxyz.org/flat, color.py."""
        b = self.b
        success = False
        if c is NO_COLOR:
            self._fill = NO_COLOR # Ignore drawing
            success = True # Color is undefined, do nothing.
        elif c is None:
            self._fill = None # No fill
            success = True
        elif isinstance(c, (float, int)): # Grayscale
            self._fill = b.gray(iround(c))
            success = True
        elif isinstance(c, (list, tuple)):
            if len(c) == 2 and isinstance(c[0], str) and isinstance(c[1], (list,tuple)) and len(c[1]) == 4:
                name, (cyan, magenta, yellow, k) = c
                self._fill = b.spot(name, (iround(cyan), iround(magenta), iround(yellow)))
                success = True
            # Not supported in PDF, leave out for general compatibility?
            #elif len(c) == 2:
            #    gray, a = c
            #    self._fill = b.ga(gray, a)
            #    success = True
            elif cmyk:
                cyan, magenta, yellow, k = c
                self._fill = b.cmyk(iround(cyan), iround(magenta), iround(yellow), iround(k))
                success = True
            elif len(c) == 4: # rgb and opaque
                red, green, blue, a = c
                self._fill = b.rgba(iround(red), iround(green), iround(blue), iround(a))
                success = True
            elif len(c) == 3:
                red, green, blue = c
                self._fill = b.rgb(iround(red), iround(green), iround(blue))
                success = True
        if not success:
            raise ValueError('FlatContext.setFillColor: Error in color format "%s"' % repr(c))

    fill = setFillColor # DrawBot compatible API

    def setStrokeColor(self, c, w=1, cmyk=False, b=None):
        """Set global stroke color or the color of the formatted string."""
        # TODO: Make this work in Flat
        b = self.b
        success = False
        if c is NO_COLOR:
            self._stroke = NO_COLOR # Ignore drawing
            success = True # Color is undefined, do nothing.
        elif c is None:
            self._stroke = None # no stroke
            success = True
        elif isinstance(c, (float, int)): # Grayscale
            self._stroke = b.gray(iround(c))
            success = True
        elif isinstance(c, (list, tuple)):
            if len(c) == 2 and isinstance(c[0], str) and isinstance(c[1], (list,tuple)) and len(c[1]) == 4:
                name, (cyan, magenta, yellow, k) = c
                self._stroke = b.spot(name, (iround(cyan), iround(magenta), iround(yellow)))
                success = True
            # Not supported in PDF, leave out for general compatibility?
            #elif len(c) == 2:
            #    gray, a = c
            #    self._stroke = b.ga(gray, a)
            #    success = True
            elif cmyk:
                cyan, magenta, yellow, k = c
                self._stroke = b.cmyk(iround(cyan), iround(magenta), iround(yellow), iround(k))
                success = True
            elif len(c) == 4: # rgb and opaque
                red, green, blue, a = c
                self._stroke = b.rgba(iround(red), iround(green), iround(blue), iround(a))
                success = True
            elif len(c) == 3:
                red, green, blue = c
                self._stroke = b.rgb(iround(red), iround(green), iround(blue))
                success = True
        if not success:
            raise ValueError('FlatContext.setStrokeColor: Error in color format "%s"' % c)
        if w is not None:
            self._strokeWidth = w

    stroke = setStrokeColor # DrawBot compatible API

    def translate(self, dx, dy):
        """Translate the origin by (dx, dy)."""
        self._ox += dx
        self._oy += dy

    def rotate(self, angle):
        """Rotate by angle."""
        self._rotate = angle

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
    import sys
    sys.exit(doctest.testmod()[0])
