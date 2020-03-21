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
#     htmlcontext.py
#
import os

from pagebot.contexts.basecontext.basecontext import BaseContext
from pagebot.contexts.markup.htmlbuilder import HtmlBuilder
from pagebot.contexts.markup.htmlstring import HtmlString
from pagebot.constants import BITMAP_TYPES
from pagebot.toolbox.color import noColor
from pagebot.toolbox.units import pt, upt
from pagebot.toolbox.transformer import path2Extension, path2ScaledImagePath, path2Dir

class HtmlContext(BaseContext):
    """The HtmlContext builds all parts necessary for a website. Most of the
    building is done by the HtmlBuilder instance, stored as self.b.

    HtmlContext is needed, because not all drawing can be done in HTML.
    Htmlcontext will decide to include SVG or pixel images for the
    HTML-representation depending on the type of element.

    TODO: Add all methods compatible with DrawBotContext, even if empty
    functionality for HTML/CSS.
    """
    # Indication to Typesetter that by default tags should be included in
    # output.
    useTags = True

    # Used by the generic BaseContext.newString( )
    STRING_CLASS = HtmlString
    EXPORT_TYPES = ('html', 'css', 'js')

    def __init__(self):
        super().__init__()
        self.b = HtmlBuilder()
        self.name = self.__class__.__name__
        self._fill = noColor

    # Drawing.

    def newDrawing(self, w=None, h=None, doc=None):
        """PageBot function. Ignore for now in HTMLContext.

        Clear output canvas, start new export file.
        The @doc is the optional Document instance of the caller.
        """

    def endDrawing(self):
        pass

    def saveDrawing(self, path):
        pass

    def getDrawing(self):
        pass

    def newPage(self, w=None, h=None, doc=None, page=None, **kwargs):
        pass

    def newPath(self):
        return None

    def frameDuration(self, value):
        pass

    #   T E X T

    def text(self, sOrBs, p):
        pass

    def textBox(self, sOrBs, r=None, clipPath=None, align=None):
        pass

    def textOverflow(self, sOrBs, box, align=None):
        pass

    def textBoxBaselines(self, txt, box, align=None):
        pass

    def textSize(self, bs, w=None, h=None, align=None):
        pass

    # String.

    def newBulletString(self, bullet, e=None, style=None):
        """Ignore by answering None, HTML creates bullets by default."""
        return None

    #   D R A W I N G

    def rect(self, x, y, w, h):
        # TODO: Implement as SVG.
        pass

    def oval(self, x, y, w, h):
        # TODO: Implement as SVG.
        pass

    def circle(self, x, y, r):
        # TODO: Implement as SVG.
        pass

    def line(self, p1, p2):
        # TODO: Implement as SVG.
        pass

    #   I M A G E

    def imagePixelColor(self, path, p):
        return 0
        #return cls.b.imagePixelColor(path, p)

    def imageSize(self, path):
        """Answers the pt(w, h) image size of the image file at path. As we cannot assume
        that we have DrawBotContext available, we are using PIL for size and scaling.
        
        Usage:
        from pagebot import getContext
        return getContext().imageSize(path)

        >>> from pagebot import getResourcesPath
        >>> imagePath = getResourcesPath() + '/images/peppertom_lowres_398x530.png'
        >>> context = HtmlContext()
        >>> context.imageSize(imagePath)
        (398pt, 530pt)
        """
        if not os.path.exists(path):
            return None
        if path.split('.')[-1] in BITMAP_TYPES:
            import PIL
            im = PIL.Image.open(path)
            return pt(im.size)
        return pt(100, 100) # PIL cannot find file size of SVG, At least return a default.

    def scaleImage(self, path, w, h, index=None, showImageLoresMarker=False,
            exportExtension=None, force=False):
        """
        >>> from pagebot import getResourcesPath
        >>> srcPath = getResourcesPath() + '/images/peppertom_lowres_398x530.png'
        >>> path2ScaledImagePath(srcPath, 100, 200, 0, 'png')
        'scaled/peppertom_lowres_398x530-w100-h200-i0.png'
        >>> context = HtmlContext()
        >>> imagePath = context.scaleImage(srcPath, 100, 200)
        >>> imagePath
        'scaled/peppertom_lowres_398x530-w100-h200.png'
        >>> context.imageSize(imagePath)
        (100pt, 133pt)
        """
        if exportExtension is None:
            exportExtension = path2Extension(path)
        exportExtension = exportExtension.lower()
        # FIXME, for now hard-converted to png, as JPG does not for for PIL now.
        exportExtension = 'png'
        # If default ./scaled directory does not exist, then create it.
        cachedFilePath = path2ScaledImagePath(path, w, h, index, exportExtension)
        cacheDirPath = path2Dir(cachedFilePath) #

        if not os.path.exists(cacheDirPath):
            os.makedirs(cacheDirPath)

        if exportExtension in BITMAP_TYPES and path != cachedFilePath:
            try:
                if force or not os.path.exists(cachedFilePath):
                    import PIL
                    im = PIL.Image.open(path)
                    im.thumbnail(upt(w, h), PIL.Image.ANTIALIAS)
                    im.save(cachedFilePath, exportExtension)
                    print('Scaling %s to (%d, %d)' % (path, w, h))
            except IOError:
                print("Cannot create resize image '%s'" % path)
        return cachedFilePath

    def image(self, path, p=None, alpha=1, pageNumber=None, w=None, h=None):
        """Make an HTML image tag by calling the builder"""
        self.b.img(path=path) # TODO: add other attributes here, width=w, height=h)

    def saveImage(self, path):
        """Ignore for now in this context."""

    #   C O L O R

    def fill(self, c):
        self._fill = c

    setFillColor = fill # DrawBot compatible API
    cmykFill = fill

    def stroke(self, c, w=None):
        self._stroke = c
        if w is not None:
            self.strokeWidth(w)

    setStrokeColor = stroke # DrawBot compatible API
    cmykStroke = stroke

    def strokeWidth(self, w):
        self._strokeWidth = w

    def drawGlyphPath(self, glyph):
        pass

    def getFlattenedContours(self, glyph):
        return None

    def getFlattenedPath(self, glyph):
        return None

    def getGlyphPath(self, glyph):
        return None

    def numberOfImages(self):
        return 0

    def shadow(self, eShadow, e=None):
        pass

    def linearGradient(self, startPoint=None, endPoint=None, colors=None,
            locations=None):
        pass

    cmykShadow = shadow
    cmykLinearGradient = linearGradient
    cmykRadialGradient = linearGradient

    def setStyles(self, styles):
        pass

    # System fonts listing, installation, font properties.

    def installedFonts(self, patterns=None):
        """Should Answer the list of all fonts (name or path) that are
        installed on the OS."""

    def installFont(self, fontOrName):
        """Should install the font in the context. fontOrName can be a Font
        instance (in which case the path is used) or a full font path."""

    def uninstallFont(self, fontOrName):
        pass

    def fontContainsCharacters(self, characters):
        pass

    def fontContainsGlyph(self, glyphName):
        pass

    def fontFilePath(self):
        pass

    def listFontGlyphNames(self):
        pass

    def fontAscender(self):
        pass

    def fontDescender(self):
        pass

    def fontXHeight(self):
        pass

    def fontCapHeight(self):
        pass

    def fontLeading(self):
        pass

    def fontLineHeight(self):
        pass

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
