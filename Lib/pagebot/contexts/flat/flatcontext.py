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
# -----------------------------------------------------------------------------
#
#     flatcontext.py
#

from pagebot.constants import (FILETYPE_PDF, FILETYPE_JPG, FILETYPE_SVG,
        FILETYPE_PNG, FILETYPE_GIF, LEFT, DEFAULT_FILETYPE, RGB)
from pagebot.contexts.base.basecontext import BaseContext
from pagebot.contexts.flat.flatbuilder import flatBuilder
from pagebot.contexts.flat.flatbezierpath import BezierPath
from pagebot.contexts.flat.flatstring import FlatString
from pagebot.toolbox.color import color, Color, noColor
from pagebot.toolbox.mathematics import *
from pagebot.toolbox.units import pt, upt, point2D

class FlatContext(BaseContext):
    """The FlatContext implements the Flat functionality within the PageBot
    framework.

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

    # Used by the generic BaseContext.newString( )
    STRING_CLASS = FlatString
    EXPORT_TYPES = (FILETYPE_PDF, FILETYPE_SVG, FILETYPE_PNG, FILETYPE_JPG)

    # Default is point document, should not be changed. Units render to points.
    UNITS = 'pt'

    def __init__(self):
        """Constructor of Flat context.

        >>> context = FlatContext()
        >>> context.newDocument(100, 100)
        >>> context.doc.__class__.__name__
        'document'
        """
        super().__init__()
        self.name = self.__class__.__name__
        self.b = flatBuilder
        self.save() # Save current set of values on gState stack.
        self.shape = None # Current open shape
        self.flatString = None
        self.fileType = DEFAULT_FILETYPE
        self._pages = []
        self.flipped = True

    #   D O C U M E N T

    def newDocument(self, w, h, size=None, doc=None, flipped=True):
        """Create a new self.doc Flat canvas to draw on. Flipped `y`-axis by
        default to conform to DrawBot's drawing methods.

        >>> context = FlatContext()
        >>> context.newDocument(100, 100)
        >>> int(context.doc.width), int(context.doc.height)
        (100, 100)
        >>> context.newDocument(100, 100)
        >>> int(context.doc.width), int(context.doc.height)
        (100, 100)
        """
        if size is not None:
            w, h = size
        self.flipped = flipped

        # Convert units to point values.
        wpt, hpt = upt(w, h)
        self.doc = self.b.document(wpt, hpt, units=self.UNITS)

    def getX(self, x):
        """Calculates `x`-coordinate based translation."""
        return self._ox + x

    def getY(self, y):
        """Calculates `y`-coordinate based on origin and translation."""
        y = self._oy + y

        if not self.flipped:
            return y
        else:
            y = self.doc.height - y
            return y

    def saveDocument(self, path, multiPage=True):
        """Save the current document to file(s)

        >>> import os
        >>> from pagebot import getRootPath
        >>> from pagebot.toolbox.color import blackColor
        >>> exportPath = getRootPath() + '/_export' # _export/* Files are ignored in git
        >>> if not os.path.exists(exportPath): os.makedirs(exportPath)
        >>> context = FlatContext()
        >>> w = h = pt(100)
        >>> x = y = pt(0)
        >>> c = blackColor
        """

        """
        FIX
        >>> context.fileType = FILETYPE_JPG
        >>> context.newDocument(w, h)
        >>> context.newPage(w, h)
        >>> context.fill(c)
        >>> context.rect(x, y, w-20, h-20)
        # Flat is too strict with color-format match?
        >>> context.saveDocument(exportPath + '/MyTextDocument_F.%s' % FILETYPE_JPG)
        >>> context.fileType = FILETYPE_PDF
        >>> context.newDocument(w, h)
        >>> context.newPage(w, h)
        >>> context.fill(c)
        >>> context.rect(x, y, w-20, h-20)
        # Flat is too strict with color-format match?
        >>> context.saveDocument(exportPath + '/MyTextDocument_F.%s' % FILETYPE_PDF)
        >>> context.fileType = FILETYPE_PNG
        >>> context.newDocument(w, h)
        >>> context.newPage(w, h)
        >>> context.fill(c)
        >>> context.rect(x, y, w-20, h-20)
        >>> context.saveDocument(exportPath + '/MyTextDocument_F.%s' % FILETYPE_PNG)
        >>> context.saveDocument(exportPath + '/MyTextDocument_F.gif')
        [FlatContext] Gif not yet implemented for "MyTextDocument_F.gif"
        """
        # In case path starts with "_export", make sure that the directory
        # exists.
        self.checkExportPath(path)
        self.fileType = path.split('.')[-1].lower()

        if self.fileType == FILETYPE_PNG:
            if len(self.pages) == 1 or not multiPage:
                im = self.pages[0].image(kind=RGB)
                im.png(path)
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

    def getDocument(self):
        pass

    def newPage(self, w=None, h=None, doc=None):
        """Other page sizes than default in self.doc, are ignored in Flat.
        # FIXME: test units, page auto-sizes to parent doc.

        >>> context = FlatContext()
        >>> w = h = pt(100)
        >>> context.newDocument(w, h)
        >>> context.newPage()
        """
        if doc is not None:
            w = w or doc.w
            h = h or doc.h
        if self.doc is None:
            self.newDocument(w, h)

        self.page = self.doc.addpage()
        self.pages.append(self.page)

    def newDrawing(self, doc=None):
        """Clear output canvas, start new export file.

        >>> context = FlatContext()
        >>> w = h = pt(100)
        >>> context.newDocument(w, h)
        """
        # FIXME: needs a width and height, so different from DrawBot?
        #context = FlatContext()
        #context.newDrawing(w, h)
        pass

    #   S T A T E

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
            rotationCenter=self._rotationCenter,
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
        self._rotationCenter = gState['rotationCenter']

    restore = restoreGraphicState

    #   F O N T S

    def listOpenTypeFeatures(self, fontName=None):
        """Answers the list of opentype features available in the named font.
        TODO: To be implemented."""
        #return self.b.listOpenTypeFeatures(fontName)
        return []

    '''
    def drawGlyph(self, glyph, x, y, fill=None, stroke=None, strokeWidth=0,
            fontSize=None, xAlign=CENTER):
        """Draw the font[glyphName] at the defined position with the defined
        fontSize."""
        path = self.getGlyphPath(glyph)
        self.drawPath(path)
    '''

    def getGlyphPath(self, glyph, p=None, path=None):
        """Converts the cubic commands to a drawable path."""
        if path is None:
            path = self.newPath()

        if p is None:
            px = py = 0
            px = self.getX(px)
            py = self.getY(py)
        else:
            px = p[0]
            py = p[1]
            px = self.getX(px)
            py = self.getY(py)

        for command, t in glyph.cubic:
            if command == 'moveTo':
                x, y = t
                if self.flipped:
                    y = -y
                path.moveTo((px+x, py+y))

            elif command == 'lineTo':
                x, y = t
                if self.flipped:
                    y = -y
                path.lineTo((px+x, py+y))
            elif command == 'closePath':
                path.closePath()
            elif command == 'curveTo':
                p0, p1, p = t
                x0, y0 = p0
                x0 = px + x0
                if self.flipped:
                    y0 = -y0
                y0 = py + y0

                x1, y1 = p1
                x1 = px + x1
                if self.flipped:
                    y1 = -y1
                y1 = py + y1

                x, y = p
                x = px + x
                if self.flipped:
                    y = -y
                y = py + y
                path.curveTo((x0, y0), (x1, y1), (x, y))
            elif command == 'component':
                (x, y), componentGlyph = t
                if self.flipped:
                    y = -y
                self.getGlyphPath(componentGlyph, (px+x, py+y), path)
        return path

    #   A N I M A T I O N

    def frameDuration(self, secondsPerFrame, **kwargs):
        """Set the frame duretion for animated gifs to a number of seconds per
        frame."""
        self._frameDuration = secondsPerFrame

    #   T E X T

    def newBulletString(self, bullet, e=None, style=None):
        return self.newString(bullet, e=e, style=style)

    def text(self, bs, p):
        """Place the babelstring instance at position p. The position can be
        any 2D or 3D points tuple. Currently the z-axis is ignored. The
        FlatContext version of the BabelString should contain
        Flat.text.

        NOTE:in the Flat model the position is an attribute of the string,
        therefore strings cannot be reused to be displayed on multiple
        positions.

        >>> context = FlatContext()
        >>> style = dict(font='Roboto-Regular', fontSize=pt(12))
        >>> bs = context.newString('ABC', style=style)
        >>> bs.__class__.__name__
        'FlatString'
        >>> context.newDocument(1000, 1000)
        >>> context.newPage()
        >>> context.text(bs, (100, 100))

        """
        if not isinstance(bs, FlatString):
            if isinstance(bs, str):
                bs = self.newString(bs)
            else:
                print('wrong type %s' % type(bs))
                # TODO: raise error.

        assert self.page is not None, 'FlatString.text: self.page is not set.'
        placedText = self.page.place(bs.s)
        xpt, ypt = point2D(upt(p))
        xpt = self.getX(xpt)
        ypt = self.getY(ypt)
        placedText.position(xpt, ypt) # Render unit tuple to value tuple

    def font(self, font, fontSize=None):
        """Set the current font, in case it is not defined in a formatted
        string. Font can be a Font instance, or a full font file path, or an
        abbreveation that can be found by family or by findFont.

        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> from pagebot.fonttoolbox.fontpaths import *
        >>> from pagebot.paths import DEFAULT_FONT_PATH
        >>> pbFonts = getPageBotFontPaths()
        >>> print(len(pbFonts))
        59
        >>> font = findFont('Roboto-Regular')
        >>> print(font)
        <Font Roboto-Regular>
        >>> context = FlatContext()
        >>> print(context)
        <FlatContext>
        >>> context.font(font.path)
        >>> context._font.endswith('/Roboto-Regular.ttf')
        True
        >>> context.font('OtherFont', 12) # If doesn't exists, path is set to default.
        >>> context._font == DEFAULT_FONT_PATH
        True
        >>> context._fontSize # Renders to pt-unit
        12
        """
        from pagebot.fonttoolbox.fontpaths import getFontPathOfFont

        self._font = getFontPathOfFont(font) # Convert name or path to font path.
        if fontSize is not None:
            self._fontSize = upt(fontSize)

    def fontSize(self, fontSize):
        """Sets the current fontSize in case it is not defined in a formatted
        string.

        >>> from pagebot.toolbox.units import p
        >>> context = FlatContext()
        >>> context.fontSize(p(1)) # Set a unit
        >>> context._fontSize # Defaults to pt-unit
        12
        >>> context.fontSize(14) # Set a number
        >>> context._fontSize # Defaults to pt-unit
        14
        """
        self._fontSize = upt(fontSize)

    def textBox(self, sOrBs, r=None, clipPath=None, align=None):
        """

        FIXME: Not using width and height here?
        TODO: clipPath
        TODO: align

        """
        if hasattr(sOrBs, 's'):
            # Assume here is's a BabelString with a FormattedString inside.
            sOrBs = sOrBs.s
        else:
            # Otherwise convert to string if it isn't already.
            sOrBs = str(sOrBs)

        xpt, ypt, _, _ = upt(r)
        placedText = self.page.place(sOrBs)

        placedText.position(xpt, ypt)

    def textSize(self, bs, w=None, h=None):
        """Answers the size tuple (w, h) of the current text. Answer (0, 0) if
        there is no text defined.  Answer the height of the string if the width
        w is given.

        >>> w = h = 500 # Default to pt-units
        >>> x = y = 0
        >>> context = FlatContext()
        >>> print(context)
        <FlatContext>
        >>> context.newDocument(w, h)
        >>> context.newPage(w, h)
        >>> style = dict(font='Roboto-Regular', fontSize=12) # Number defaults to pt-unit
        >>> print(style)
        {'font': 'Roboto-Regular', 'fontSize': 12}
        >>> bs = context.newString('ABC ' * 100, style=style)
        >>> print(type(bs))
        <class 'pagebot.contexts.flat.flatstring.FlatString'>
        >>> t = context.page.place(bs.s)
        >>> t = t.frame(x, y, w, h) # Numbers default to pt-units
        >>> t.overflow()
        False
        >>> bs = context.newString('ABC ' * 100000, style=style)
        >>> t = context.page.place(bs.s)
        >>> t = t.frame(x, y, w, h)
        >>> t.overflow()
        True
        >>> lines = t.lines()
        >>> #len(lines)
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

    def textOverflow(self, bs, w, h, align=LEFT):
        """Answers the the box (0, 0, w, h) overflow as a new FlatString in the
        current context."""
        wpt, hpt = upt(w, h)
        return FlatString(self.b.textOverflow(bs.s, (0, 0, wpt, hpt), align), self)

    def textBoxBaseLines(self, txt, box):
        raise NotImplementedError

    def language(self, language):
        self._language = language

    def hyphenation(self, onOff):
        # TODO: Implementation in Flat should use PageBot hyphenation?
        self._hyphenation = onOff

    #   I M A G E

    def imagePixelColor(self, path, p):
        return self.b.imagePixelColor(path, p)

    def imageSize(self, path):
        """Answers the (w, h) image size of the image file at path.

        >>> from pagebot import getResourcesPath
        >>> imagePath = getResourcesPath() + '/images/peppertom_lowres_398x530.png'
        >>> context = FlatContext()
        >>> context.imageSize(imagePath)
        (398pt, 530pt)
        """
        img = self.b.image.open(path)
        # Answer units of the same time as the document.w was defined.
        return pt(img.width), pt(img.height)

    def image(self, path, p=None, alpha=1, pageNumber=None, w=None, h=None, scaleType=None):
        """Draws the image. If position is none, sets x and y to the origin. If
        w or h is defined, then scale the image to fit."""
        if p is None:
            p = 0, 0


        xpt, ypt = point2D(upt(p))
        self.save()

        img = self.b.image.open(path)

        # TODO: calculate other if one is None.
        if not w is None and not h is None:
            img.resize(width=w.pt, height=h.pt)

        placed = self.page.place(img)
        placed.position(xpt, ypt)
        self.restore()

    #   D R A W I N G

    def getFlatRGB(self, c):
        """Answers the color tuple that is valid for self.fileType, otherwise
        Flat gives an error.

        TODO: Make better match for all file types, transparency and spot
        color."""
        from flat import rgb
        return rgb(*to255(c.rgb))


    def _getShape(self):
        """Renders Pagebot FlatBuilder shape to a Flat shape."""
        if self._fill is noColor and self._stroke is noColor:
            return None

        shape = self.b.shape()

        # TODO: revert to PageBot Color globally, convert to Flat RGB here.
        if self._fill is None:
            shape.nofill()
        elif self._fill != noColor:
            shape.fill(self.getFlatRGB(self._fill))

        if self._stroke is None:
            shape.nostroke()
        elif self._stroke != noColor:
            shape.stroke(self.getFlatRGB(self._stroke)).width(self._strokeWidth)

        return shape

    def ensure_page(self):
        """
        Flat function?
        """
        if not self.doc:
            self.newDocument(pt(100), pt(100)) # Standardize FlatContext document on pt.

        if not self.pages:
            self.newPage(self.doc.width, self.doc.height)

    def rect(self, x, y, w, h):
        y = self.getY(y) - h
        shape = self._getShape()

        if shape is not None:
            self.ensure_page()
            r = shape.rectangle(x, y, w, h)
            self.page.place(r)

    def oval(self, x, y, w, h):
        """Draws an oval in a rectangle, where (x, y) is the bottom left origin
        and (w, h) is the size. This default DrawBot behavior, different from
        default Flat, where the (x, y) is the middle of the oval. Compensate
        for the difference."""
        #xpt, ypt, wpt, hpt = upt(x, y, w, h)
        shape = self._getShape()

        if shape is not None:
            self.ensure_page()
            x0 = x + w / 2
            y0 = self.getY(y+ h / 2)
            w0 = w
            h0 = h
            self.page.place(shape.ellipse(x0, y0, w0, h0))

    def circle(self, x, y, r):
        """Draws a circle in a square with radius r and (x, y) as center."""
        xpt, ypt, rpt = upt(x, y, r)
        ypt = self.getY(ypt)

        shape = self._getShape()

        if shape is not None:
            self.ensure_page()
            self.page.place(shape.circle(xpt, ypt, rpt))

    def line(self, p0, p1):
        """Draws a line from point p0 to point p1."""

        x0pt, y0pt = point2D(upt(p0))
        x1pt, y1pt = point2D(upt(p1))
        y0pt = self.getY(y0pt)
        y1pt = self.getY(y1pt)
        shape = self._getShape()

        if shape is not None:
            self.ensure_page()
            self.page.place(shape.line(x0pt, y0pt, x1pt, y1pt))

    #   P A T H

    def newPath(self):
        """Creates a new Bézier path object to store subsequent path commands."""
        self._path = BezierPath(self.b)
        return self._path

    def drawPath(self, path=None, p=None, sx=1, sy=None):
        """Renders the path object as a Flat vector graphic."""
        if p is None:
            xpt = ypt = 0
        else:
            xpt, ypt = point2D(upt(p))

        # TODO: xpt, ypt?
        shape = self._getShape()

        if shape is not None:
            self.ensure_page()
            self.page.place(shape.path(self._path.commands))

    def moveTo(self, p):
        ppt = point2D(upt(p))
        assert self._path is not None
        self._path.moveTo(ppt)

    def lineTo(self, p):
        ppt = point2D(upt(p))
        assert self._path is not None
        self._path.lineTo(ppt)

    def quadTo(self, bcp, p):
        bpt = point2D(upt(bcp))
        ppt = point2D(upt(p))
        assert self._path is not None
        self._path.quadTo(bpt, ppt)

    def curveTo(self, bcp1, bcp2, p):
        b1pt = point2D(upt(bcp1))
        b2pt = point2D(upt(bcp2))
        ppt = point2D(upt(p))
        assert self._path is not None
        self._path.curveTo(b1pt, b2pt, ppt)

    def closePath(self):
        assert self._path is not None
        self._path.closePath()

    def bezierPathByFlatteningPath(self, path):
        """TODO: Make Flat version of the NSBezier flatten path function."""
        return None #path.getNSBezierPath().bezierPathByFlatteningPath()

    #   S H A D O W  &  G R A D I E N T

    def setShadow(self, eShadow):
        """Sets the DrawBot graphics state for shadow if all parameters are
        set."""
        pass # Not implemented?

    def setGradient(self, gradient, origin, w, h):
        wpt, hpt = upt(w, h)
        pass # Not implemented?

    def lineDash(self, *lineDash):
        pass # Not implemented?

    #   C O L O R

    def textFill(self, c):
        self.fill(c)

    setTextFillColor = textFill

    def fill(self, c):
        """Set the color for global or the color of the formatted string.
        See: http://xxyxyz.org/flat, color.py.

        """
        if c is None:
            c = noColor
        elif isinstance(c, (tuple, list)):
            c = color(*c)
        elif isinstance(c, (int, float)):
            c = color(c)

        msg = 'FlatContext.fill: Color "%s" is not Color instance'
        assert isinstance(c, Color), (msg % str(c))
        self._fill = c

    def stroke(self, c, w=None):
        """Set global stroke color or the color of the formatted string."""
        if c is None:
            c = noColor
        elif isinstance(c, (tuple, list)):
            c = color(*c)
        elif isinstance(c, (int, float)):
            c = color(c)

        msg = 'FlatContext.stroke: Color "%s" is not Color instance'
        assert isinstance(c, Color), (msg % c)
        self._stroke = c

        self.strokeWidth(w)

    def textStroke(self, c, w=None):
        """
        Flat function?
        """
        msg = 'FlatContext.textStroke: Color "%s" is not Color instance'
        assert isinstance(c, Color), (msg % c)
        self.stroke(c, w)

    setTextStrokeColor = textStroke

    def strokeWidth(self, w):
        self._strokeWidth = upt(w)

    # Transform.

    def transform(self, matrix, center=(0, 0)):
        raise NotImplementedError

    def translate(self, dx, dy):
        """Translates the origin by (dx, dy).
        TODO: use transform matrix.
        """
        dxpt, dypt = point2D(upt(dx, dy))
        self._ox += dxpt
        self._oy += dypt

    def rotate(self, angle, center=None):
        """Rotates by angle.
        TODO: use transform matrix.
        """
        self._rotationCenter = center
        self._rotate = angle

    def scale(self, sx=1, sy=None, center=(0, 0)):
        """
        TODO: use transform matrix.
        """
        pass

    def skew(self, angle1, angle2=0, center=(0, 0)):
        """
        TODO: use transform matrix.
        """
        pass

    #   E X P O R T

    def create_gif(self, filenames, duration):
        """
        Flat function?

        TODO: Not implement yet.
        ::

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
