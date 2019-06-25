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
#     pdflibcontext.py
#
#     https://www.pdflib.com/buy/online-shop/pdflib-pdflib-pdi-pps/
#     https://www.pdflib.com/products/pdflib-family/pdflib/
#
import os
import PDFlib 
import traceback

from pagebot.toolbox.units import pt, upt, point2D
from pagebot.toolbox.color import noColor, color
from pagebot.contexts.basecontext import BaseContext
from pagebot.constants import *
from pagebot.contexts.strings.pdflibstring import PdfLibString as stringClass
from pagebot.toolbox.transformer import path2Name, path2Dir

class PdfLibContext(BaseContext):

    STRING_CLASS = stringClass
    EXPORT_TYPES = (FILETYPE_PDF, FILETYPE_SVG, FILETYPE_PNG, FILETYPE_JPG,
        FILETYPE_GIF, FILETYPE_MOV)

    def __init__(self):
        """Constructor of PdfLibContext if drawBot import exists.

        """
        super().__init__()
        # The context builder "cls.b" is drawBot which executes actual drawing
        # calls, similar to function calls in DrawBot scripts.
        self.b = PDFlib.PDFlib() #  PDFlib Builder for this canvas.
        self.name = self.__class__.__name__
        # Holds the extension as soon as the export file path is defined.
        self.fileType = DEFAULT_FILETYPE

    #   D O C U M E N T

    def newDocument(self, w, h):
        """Can be ignored for DrawBot; document opens automatically if first page
        is created."""
        #self.b.size(upt(w), upt(h))

    def saveDocument(self, path, multiPage=None):
        """Select non-standard DrawBot export builders here. Save the current
        image as path, rendering depending on the extension of the path file.
        In case the path starts with "_export", create its directories.

        >>> context = PdfLibContext()
        >>> #context.saveImage('_export/MyFile.pdf')

        """
        self.checkExportPath(path)
        self.b.saveImage(path, multipage=multiPage)

    saveImage = saveDocument

    def getDocument(self):
        """Returns a PDF document of the current state."""
        return self.b.pdfImage()

    #   V A R I A B L E

    def Variable(self, variables, workSpace):
        """Offers interactive global value manipulation in DrawBot. Probably to
        be ignored in other contexts."""
        # Variable is a DrawBot context global, used to make simple UI with
        # controls on input parameters.
        try:
            from drawBot import Variable
            Variable(variables, workSpace)
        except self.b.misc.DrawBotError:
            # Ignore if there is a DrawBot context, but not running inside
            # DrawBot.
            print(traceback.format_exc())

    #   D R A W I N G

    def bluntCornerRect(self, x, y, w, h, offset=5):
        """Draw a rectangle in the canvas. This method is using the core BezierPath
        as path to draw on. For a more rich environment use PageBotPath(context)
        instead.

        TODO: move to elements.

        >>> context = PdfLibContext()
        >>> context.bluntCornerRect(pt(0), pt(0), pt(100), pt(100))
        >>> context.bluntCornerRect(0, 0, 100, 100)
        """
        if 0:
            xPt, yPt, wPt, hPt, offsetPt = upt(x, y, w, h, offset)
            path = self.newPath() #
            path.moveTo((xPt+offsetPt, yPt))
            path.lineTo((xPt+wPt-offsetPt, yPt))
            path.lineTo((xPt+wPt, yPt+offsetPt))
            path.lineTo((xPt+wPt, yPt+hPt-offsetPt))
            path.lineTo((xPt+w-offsetPt, y+hPt))
            path.lineTo((xPt+offsetPt, y+hPt))
            path.lineTo((xPt, yPt+h-offsetPt))
            path.lineTo((xPt, yPt+offsetPt))
            self.closePath()
            self.drawPath(path)

    def roundedRect(self, x, y, w, h, offset=25):
        """Draw a rectangle in the canvas. This method is using the core BezierPath
        as path to draw on. For a more rich environment use PageBotPath(context)
        instead.

        TODO: move to elements.

        >>> context = PdfLibContext()
        >>> context.roundedRect(pt(0), pt(0), pt(100), pt(100))
        >>> context.roundedRect(0, 0, 100, 100)
        """
        if 0:
            xPt, yPt, wPt, hPt, offsetPt = upt(x, y, w, h, offset)
            path = self.newPath()
            path.moveTo((xPt+offsetPt, yPt))
            path.lineTo((xPt+wPt-offsetPt, yPt))
            path.curveTo((xPt+wPt, yPt), (xPt+wPt, yPt), (xPt+wPt, yPt+offsetPt))
            path.lineTo((xPt+wPt, yPt+hPt-offsetPt))
            path.curveTo((xPt+wPt, yPt+hPt), (xPt+wPt, yPt+hPt), (xPt+wPt-offsetPt, yPt+hPt))
            path.lineTo((xPt+offsetPt, yPt+hPt))
            path.curveTo((xPt, yPt+hPt), (xPt, yPt+hPt), (xPt, yPt+hPt-offsetPt))
            path.lineTo((xPt, yPt+offsetPt))
            path.curveTo((xPt, yPt), (xPt, yPt), (xPt+offsetPt, yPt))
            self.closePath()
            self.drawPath(path)

    #   P A T H
    #
    #   Function that work on the current running path stored in self._path
    #

    def drawGlyphPath(self, glyph):
        """Converts the cubic commands to a drawable path."""
        path = self.getGlyphPath(glyph)
        self.drawPath(path)

    def getGlyphPath(self, glyph, p=None, path=None):
        """Answers the DrawBot path. Allow optional position offset and path,
        in case we do recursive component drawing.

        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> f = findFont('Roboto-Regular')
        >>> print(f)
        <Font Roboto-Regular>
        >>> g = f['H']
        >>> path = context.getGlyphPath(g)
        """
        if path is None:
            path = self.newPath()
        if p is None:
            px = py = 0
        else:
            px = p[0]
            py = p[1]

        for command, t in glyph.cubic:
            if command == 'moveTo':
                path.moveTo((px+t[0], py+t[1]))
            elif command == 'lineTo':
                path.lineTo((px+t[0], py+t[1]))
            elif command == 'curveTo':
                path.curveTo((px+t[0][0], py+t[0][1]),
                        (px+t[1][0], py+t[1][1]), (px+t[2][0], py+t[2][1]))
            elif command == 'closePath':
                path.closePath()
            elif command == 'component':
                (x, y), componentGlyph = t
                self.getGlyphPath(componentGlyph, (px+x, py+y), path)
        return path

    def getFlattenedPath(self, path=None):
        """Use the NSBezier flatten path. Answers None if the flattened path
        could not be made."""
        if path is None:
            path = self.path
        #return path._path.getNSBezierPath().bezierPathByFlatteningPath()
        return path._path.bezierPathByFlatteningPath()

    def getFlattenedContours(self, path=None):
        """Answers the flattened Bézier path as  a contour list [contour,
        contour, ...] where contours are lists of point2D() points."""
        contour = []
        flattenedContours = [contour]
        flatPath = self.bezierPathByFlatteningPath(path) # Use/create self._path if path is None

        if flatPath is not None:
            for index in range(flatPath.elementCount()):
                # NSBezierPath size + index call.
                p = flatPath.elementAtIndex_associatedPoints_(index)[1]

                if p:
                    # Make point2D() tuples, no need to add point type, all
                    # onCurve.
                    contour.append((p[0].x, p[0].y))
                else:
                    contour = []
                    flattenedContours.append(contour)

        return flattenedContours

    #   F O N T S

    def fontPath2FontName(self, fontPath):
        """Answers the font name of the font related to fontPath. This is done
        by installing it (again). Answers None if the font cannot be installed
        or if the path does not exists.

        >>> import os
        >>> from pagebot.fonttoolbox.fontpaths import TEST_FONTS_PATH
        >>> context = PdfLibContext()
        >>> context.fontPath2FontName('Aaa.ttf') is None # Does not exist
        True
        >>> path = TEST_FONTS_PATH + '/fontbureau/Amstelvar-Roman-VF.ttf'
        >>> os.path.exists(path)
        True
        """
        if os.path.exists(fontPath):
            return self.b.font(fontPath)
        return None

    def fontName2FontPath(self, fontName):
        """Answers the unchanged path, if it exists as file. Answers the path
        that is source of the given font name. Answers None if the font cannot
        be found."""
        # If the font cannot be found by name, then test if the file exists as
        # path and answer it.
        if os.path.exists(fontName): #
            return fontName
        # Otherwise try OSX for the conversion.
        # FIXME
        # Change to PageBot font code.
        #nsFont = NSFont.fontWithName_size_(fontName, 25)
        #if nsFont is not None:
        #    fontRef = CTFontDescriptorCreateWithNameAndSize(nsFont.fontName(), nsFont.pointSize())
        #    url = CTFontDescriptorCopyAttribute(fontRef, kCTFontURLAttribute)
        #    return url.path()
        return None

    #   G L Y P H

    def drawGlyph(self, glyph, x, y, fill=noColor, stroke=noColor,
            strokeWidth=0, fontSize=None, xAlign=CENTER):
        """Draw the font[glyphName] at the defined position with the defined
        fontSize."""
        font = glyph.font
        if fontSize is None:
            fontSize = font.info.unitsPerEm
        s = fontSize/font.info.unitsPerEm
        if xAlign == CENTER:
            x -= (glyph.width or 0)/2*s
        elif xAlign == RIGHT:
            x -= glyph.width*s
        self.save()
        self.fill(fill)
        self.stroke(stroke, w=strokeWidth)
        self.translate(x, y)
        self.scale(s)
        self.drawGlyphPath(glyph)
        self.restore()

    #   I M A G E

    def imagePixelColor(self, path, p=None):
        if p is None:
            p = ORIGIN
        ppt = point2D(upt(p))
        return self.b.imagePixelColor(path, ppt)

    def numberOfImages(self, path):
        """Answers the number of images in the file referenced by path."""
        return self.b.numberOfPages(path)

    def image(self, path, p=None, alpha=1, pageNumber=None, w=None, h=None):
        """Draws the image. If w or h is defined, scale the image to fit."""
        if p is None:
            p = ORIGIN

        iw, ih = self.imageSize(path)

        if w and not h: # Scale proportional
            wpt = upt(w)
            hpt = ih * wpt/iw # iw : ih = w : h
        elif not w and h:
            hpt = upt(h)
            wpt = iw * hpt/ih
        elif not w and not h:
            wpt = iw
            hpt = ih
        else: # Both are defined, scale disproportional
            wpt = upt(w)
            hpt = upt(h)

        # Else both w and h are defined, scale disproportionally.
        xpt, ypt, = point2D(p)
        sx, sy = upt(wpt/iw, hpt/ih) # We need ratio values, not units

        self.save()
        self.translate(xpt, ypt)
        self.scale(sx, sy)
        #self.b.image(path, (x, y), alpha=alpha, pageNumber=pageNumber)
        self.b.image(path, (0, 0), alpha=alpha, pageNumber=pageNumber)
        self.restore()

    def path2ScaledImagePath(self, path, w, h, index=None, exportExtension=None):
        """Answers the path to the scaled image.

        >>> context = PdfLibContext()
        >>> context.path2ScaledImagePath('/xxx/yyy/zzz/This.Is.An.Image.jpg', 110, 120)
        ('/xxx/yyy/zzz/_scaled/', 'This.Is.An.Image.110x120.0.jpg')
        """
        cachePath = '%s/_scaled/' % path2Dir(path)
        fileNameParts = path2Name(path).split('.')
        if not exportExtension: # If undefined, take the original extension for exporting the cache.
            exportExtension = fileNameParts[-1].lower()
        cachedFileName = '%s.%dx%d.%d.%s' % ('.'.join(fileNameParts[:-1]), w, h, index or 0, exportExtension)
        return cachePath, cachedFileName

    def scaleImage(self, path, w, h, index=None, showImageLoresMarker=False,
            exportExtension=None, force=False):
        """Scales the image at the path into a new cached image file. Ignore if
        the cache file is already there.

        First create the new file name, depending on the resolution of the
        scaled image.  Note that in DrawBot this scaling and saving should be
        done before any real document/page drawing started, since this proces
        is using DrawBot canvas pages to execute.

        In case the source contains indexed pages, use index to select the
        page. If omitted, the default index is 0 (in DrawBot this also works on
        non-PDF files).

        >>> from pagebot import getResourcesPath
        >>> context = PdfLibContext()
        >>> path = getResourcesPath() + '/images/peppertom_lowres_398x530.png'
        """
        
        """
        >>> scaledImagePath = context.scaleImage(path, 300, 400)
        >>> os.path.exists(scaledImagePath)
        True
        >>> scaledImagePath = context.scaleImage(path, 3, 4) # Reall small
        >>> os.path.exists(scaledImagePath)
        True
        """
        # If default _scaled directory does not exist, then create it.
        cachePath, fileName = self.path2ScaledImagePath(path, w, h, index, exportExtension)
        if not os.path.exists(cachePath):
            os.makedirs(cachePath)
        cachedFilePath = cachePath + fileName

        if force or not os.path.exists(cachedFilePath):
            self.newDrawing() # Clean the drawing stack.
            self.newPage(w, h)
            self.image(path, (0, 0), w=w, h=h, pageNumber=index or 0)
            if showImageLoresMarker:
                bs = self.newString('LO-RES',
                        style=dict(font=DEFAULT_FALLBACK_FONT_PATH,
                            fontSize=pt(64), fill=color(0, 1, 1),
                            textFill=color(1, 0, 0)))
                tw, th = bs.size
                self.text(bs, (w/2-tw/2, h/2-th/4))
            self.saveImage(cachedFilePath)
            self.newDrawing() # Clean the drawing stack.
        return cachedFilePath

    def endDrawing(self):
        pass

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
