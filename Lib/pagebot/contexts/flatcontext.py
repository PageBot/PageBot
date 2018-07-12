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
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     flatcontext.py
#
#     xxyxyz.org/flat
#
#import imageio
from pagebot.toolbox.units import pt, Pt, units, ru
from pagebot.toolbox.color import Color, noColor, color, blackColor
from pagebot.contexts.basecontext import BaseContext
from pagebot.contexts.builders.flatbuilder import flatBuilder, BezierPath
from pagebot.contexts.strings.flatstring import FlatString
from pagebot.constants import *

def iround(value):
    return min(255, max(0, int(round(value*255.0))))

class FlatContext(BaseContext):
    """A FlatContext instance combines the specific functions of the Flat
    library, and offers a PageBot “standard” API, so it can be swapped with the
    DrawBotContext. This way it also hides e.g. the type of BabelString
    instance needed, and the type of HTML/CSS file structure to be created.

    * xxyxyz.org/flat
    * xxyxyz.org/flat

    Text behavior:
    st = strike(font)
        st.size(size, leading=0.0, units=Pt.UNIT)
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
    EXPORT_TYPES = (FILETYPE_PDF, FILETYPE_SVG, FILETYPE_PNG, FILETYPE_JPG)

    def __init__(self):
        """Constructor of Flat context.

        >>> context = FlatContext()
        >>> context.isFlat
        True
        >>> context.newDocument(pt(100), pt(100))
        >>> context.doc.__class__.__name__
        'document'
        """
        # Keep status of last color, to make difference between fill and stroke colors.
        self.name = self.__class__.__name__
        self._fill = blackColor
        self._stroke = noColor
        self._strokeWidth = noColor
        self._textFill = blackColor
        self._textStroke = noColor
        self._textStrokeWidth = noColor
        self._font = DEFAULT_FONT_PATH # Optional setting of the current font and fontSize
        self._fontSize = DEFAULT_FONT_SIZE
        self._frameDuration = 0
        self._ox = pt(0) # Origin set by self.translate()
        self._oy = pt(0)
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
        self.unit = pt # Default is point document. Changed by w.
        self.fileType = DEFAULT_FILETYPE

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
        >>> context.newDocument(pt(100), pt(100))
        >>> int(context.doc.width), int(context.doc.height)
        (100, 100)
        """
        assert w.UNIT == h.UNIT
        self.unit = w.UNIT
        self.title = title
        self.pageCount = pageCount
        self.doc = self.b.document(w.r, h.r, w.UNIT)
        self.newPage(w, h)

    def saveDocument(self, path, multiPage=True):
        """Save the current document to file(s)

        >>> import os
        >>> from pagebot import getRootPath
        >>> from pagebot.toolbox.color import Color
        >>> exportPath = getRootPath() + '/_export' # _export/* Files are ignored in git
        >>> if not os.path.exists(exportPath): os.makedirs(exportPath)
        >>> context = FlatContext()
        >>> w = h = pt(100)
        >>> x = y = pt(0)
        >>> c = blackColor
        >>> context.fileType = FILETYPE_JPG
        >>> context.newDocument(w, h)
        >>> context.newPage(w, h)
        >>> context.fill(c)
        >>> context.rect(x, y, w-20, h-20)
        >>> context.saveDocument(exportPath + '/MyTextDocument_F.%s' % FILETYPE_JPG) # Flat is too scrict with color-format match
        >>> context.fileType = FILETYPE_PDF
        >>> context.newDocument(w, h)
        >>> context.newPage(w, h)
        >>> context.fill(c)
        >>> context.rect(x, y, w-20, h-20)
        >>> context.saveDocument(exportPath + '/MyTextDocument_F.%s' % FILETYPE_PDF) # Flat is too scrict with color-format match
        >>> context.fileType = FILETYPE_PNG
        >>> context.newDocument(w, h)
        >>> context.newPage(w, h)
        >>> context.fill(c)
        >>> context.rect(x, y, w-20, h-20)
        >>> context.saveDocument(exportPath + '/MyTextDocument_F.%s' % FILETYPE_PNG)
        >>> context.saveDocument(exportPath + '/MyTextDocument_F.gif')
        [FlatContext] Gif not yet implemented for "MyTextDocument_F.gif"
        """
        self.checkExportPath(path) # In case path starts with "_export", make sure that the directories exist.

        RGB = 'rgb'
        RGBA = 'rgba'

        if self.fileType == FILETYPE_PNG:
            if len(self.pages) == 1 or not multiPage:
                self.pages[0].image(kind='rgba').png(path)
            else:
                for n, p in enumerate(self.pages):
                    pagePath = path.replace('.'+FILETYPE_PNG, '%03d.%s' % (n, FILETYPE_PNG))
                    p.image(kind=RGB).png(pagePath)
        elif self.fileType == FILETYPE_JPG:
            if len(self.pages) == 1 or not multiPage:
                self.pages[0].image(kind=RGB).jpeg(path)
            else:
                for n, p in enumerate(self.pages):
                    pagePath = path.replace('.'+FILETYPE_PNG, '%03d.%s' % (n, FILETYPE_PNG))
                    p.image(kind=RGB).jpeg(pagePath)
        elif self.fileType == FILETYPE_SVG:
            if len(self.pages) == 1 or not multiPage:
                self.pages[0].svg(path)
            else:
                for n, p in enumerate(self.pages):
                    pagePath = path.replace('.'+FILETYPE_SVG, '%03d.%s' % (n, FILETYPE_SVG))
                    p.svg(pagePath)
        elif self.fileType == FILETYPE_PDF:
            self.doc.pdf(path)
        elif self.fileType == FILETYPE_GIF:
            print('[FlatContext] Gif not yet implemented for "%s"' % path.split('/')[-1])
        else:
            raise NotImplementedError('[FlatContext] File format "%s" is not implemented' % path.split('/')[-1])

    saveImage = saveDocument # Compatible API with DrawBot

    def newPage(self, w, h, units='pt'):
        """Other page sizes than default in self.doc, are ignored in Flat.

        >>> context = FlatContext()
        >>> w = h = pt(100)
        >>> context.newDocument(w, h)
        >>> context.newPage(w, h)
        """
        if self.doc is None:
            self.newDocument(w, h)
        self.page = self.doc.addpage()
        self.page.size(w.r, h.r)
        self.pages.append(self.page)

    def newDrawing(self):
        """Clear output canvas, start new export file.

        >>> context = FlatContext()
        >>> w = h = pt(100)
        >>> context.newDocument(w, h)
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
        >>> context.font('OtherFont', pt(12)) # Font does not exists, font path is set to DEFAULT_FONT_PATH
        >>> context._font == DEFAULT_FONT_PATH
        True
        >>> context._fontSize
        12pt
        """
        from pagebot.fonttoolbox.fontpaths import getFontPathOfFont

        self._font = getFontPathOfFont(font) # Convert name or path to font path.
        if fontSize is not None:
            self._fontSize = fontSize

    def fontSize(self, fontSize):
        """Set the current fontSize, in case it is not defined in a formatted string

        >>> fontSize = pt(12)
        >>> context = FlatContext()
        >>> context.fontSize(fontSize)
        >>> context._fontSize
        12pt
        """
        self._fontSize = fontSize

    def textBox(self, bs, rect):
        x, y, w, h = rect
        placedText = self.page.place(bs.s)
        placedText.position(x.r, y.r)

    def textSize(self, bs, w=None, h=None):
        """Answer the size tuple (w, h) of the current text. Answer (0, 0) if
        there is no text defined.  Answer the height of the string if the width
        w is given.

        >>> w = h = pt(500)
        >>> x = y = pt(0)
        >>> context = FlatContext()
        >>> context.newDocument(w, h)
        >>> context.newPage(w, h)
        >>> style = dict(font='Roboto-Regular', fontSize=pt(12))
        >>> bs = context.newString('ABC ' * 100, style=style)
        >>> t = context.page.place(bs.s)
        >>> t = t.frame(x.r, y.r, w.r, h.r)
        >>> t.overflow()
        False
        >>> bs = context.newString('ABC ' * 100000, style=style)
        >>> t = context.page.place(bs.s)
        >>> t = t.frame(x.r, y.r, w.r, h.r)
        >>> t.overflow()
        True
        >>> lines = t.lines()
        >>> len(lines)
        35
        """
        # FIXME! This is a totally wrong boilerplate for now!

        #t = placedtext(bs.s)
        if not bs.s:
            return (pt(0), pt(0))
        elif w is None:
            return (pt(100), pt(100))
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
        (398pt, 530pt)
        """
        img = self.b.image.open(path)
        # Answer units of the same time as the document.w was defined.
        return units(img.width, maker=self.unit), units(img.height, maker=self.unit)

    def image(self, path, p, alpha=1, pageNumber=None, w=None, h=None):
        """Draw the image. If w or h is defined, then scale the image to fit."""
        if w is None or h is None:
            w, h = self.imageSize(path)

        x, y, = p[0], p[1]
        self.save()
        img = self.b.image(path)
        img.resize(width=w.r, height=h.r)
        placed = self.page.place(img)
        placed.position(x.r, y.r)
        self.restore()

    #   D R A W I N G

    def _getValidColor(self, c):
        u"""Answer the color tuple that is valid for self.fileType, otherwise Flat gives an error."""
        # TODO: Make better match for all file types, transparance and spot color
        if self.fileType in (FILETYPE_JPG, FILETYPE_PNG):
            return c.rgb
        return c.rgb

    def _getShape(self):
        if self._fill is noColor and self._stroke is noColor:
            return None
        shape = self.b.shape()
        if self._fill is None:
            shape.nofill()
        elif self._fill != noColor:
            shape.fill(self._getValidColor(self._fill))
        if self._stroke is None:
            shape.nostroke()
        elif self._stroke != noColor:
            shape.stroke(self._getValidColor(self._stroke)).width(self._strokeWidth)
        return shape

    def ensure_page(self):
        if not self.doc:
            self.newDocument(pt(0), pt(0))
        if not self.pages:
            self.newPage(self.doc.w, self.doc.h)

    def rect(self, x, y, w, h):
        shape = self._getShape()
        if shape is not None:
            self.ensure_page()
            self.page.place(shape.rectangle(x.r, y.r, w.r, h.r))

    def oval(self, x, y, w, h):
        """Draw an oval in rectangle, where (x,y) is the bottom left origin and
        (w,h) is the size.  This default DrawBot behavior, different from
        default Flat, where the (x,y) is the middle if the oval. Compensate for
        the difference."""
        shape = self._getShape()
        if shape is not None:
            self.ensure_page()
            self.page.place(shape.ellipse((x-w/2).r, (y-h/2).r, w.r, h.r))

    def circle(self, x, y, r):
        """Draw an circle in square, with radius r and (x,y) as middle."""
        shape = self._getShape()
        if shape is not None:
            self.ensure_page()
            self.page.place(shape.circle(x.r, y.r, r.r))

    def line(self, p0, p1):
        shape = self._getShape()
        if shape is not None:
            self.ensure_page()
            self.page.place(shape.line(p0[0].r, p0[1].r, p1[0].r, p1[1].r))

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
        self._path.moveTo(ru(p))

    def lineTo(self, p):
        assert self._path is not None
        self._path.lineTo(ru(p))

    def quadTo(self, bcp, p):
        assert self._path is not None
        self._path.quadTo(ru(bcp), ru(p))

    def curveTo(self, bcp1, bcp2, p):
        assert self._path is not None
        self._path.curveTo(ru(bcp1), ru(bcp1), ru(bcp2), ru(p))

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

    def setTextFillColor(self, c):
        self.fill(c)

    #def setFillColor(self, c, builder=None):
    def setFillColor(self, c, cmyk=False, spot=False, overprint=False):
        u"""Set the color for global or the color of the formatted string.
        See: http://xxyxyz.org/flat, color.py."""
        assert isinstance(c, Color)
        self._fill = c

        '''
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
        '''

    fill = setFillColor # DrawBot compatible API

    def setTextStrokeColor(self, c, w=None):
        self.stroke(c, w)

    def setStrokeColor(self, c, w=None, b=None):
        u"""Set global stroke color or the color of the formatted string."""
        assert isinstance(c, Color)
        self._stroke = c

        '''
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
        '''

        if w is not None:
            self._strokeWidth = w

    stroke = setStrokeColor # DrawBot compatible API

    def strokeWidth(self, w):
        self._strokeWidth = w

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
