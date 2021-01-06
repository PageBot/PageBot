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

from pagebot.constants import BITMAP_TYPES
from pagebot.contexts.basecontext.babelstring import BabelString
from pagebot.contexts.basecontext.basecontext import BaseContext
from pagebot.contexts.htmlcontext.htmlbuilder import HtmlBuilder
from pagebot.toolbox.color import noColor
from pagebot.toolbox.units import upt
from pagebot.toolbox.transformer import path2Extension, path2ScaledImagePath, path2Dir

HAS_PIL = True

try:
    from PIL import Image
except:
    HAS_PIL = False

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
    STRING_CLASS = BabelString
    EXPORT_TYPES = ('html', 'css', 'js')

    def __init__(self):
        super().__init__()
        self.b = HtmlBuilder()
        self._fill = noColor
        self._numberOfPages = 1

    # Drawing.

    def newDrawing(self, w=None, h=None, doc=None):
        """PageBot function. Ignore for now in HTMLContext.

        Clear output canvas, start new export file.
        The @doc is the optional Document instance of the calling function.
        """

    def endDrawing(self):
        pass

    def saveDrawing(self, path, multiPage=None):
        pass

    def getDrawing(self):
        pass

    def newPage(self, w=None, h=None, doc=None, **kwargs):
        pass

    def pageCount(self):
        return self._numberOfPages

    def newPath(self):
        return None

    def frameDuration(self, value):
        pass

    def _get_width(self):
        """Answers the width of the current page."""
        raise NotImplementedError

    width = property(_get_width)

    def _get_height(self):
        """Answers the height of the current page."""
        raise NotImplementedError

    height = property(_get_height)

    #   T E X T

    def getTextLines(self, bs, w=None, h=None):
        pass

    def textSize(self, bs, w=None, h=None):
        pass

    # Babelstring

    def fromBabelString(self, bs):
        """For now, Typesetter put tagged text into bs.s, so it works for current
        website generators.
        FIXME: Use the bs.cs for rendered native HTML tagged text and the bs.runs
        for plain text + styles, so the BabelString can also be used to convert
        to other contexts."""
        return bs.s

    def asBabelString(self, bs):
        """FIXME: Needs to be better implemented using tags and styles."""
        if isinstance(bs, BabelString):
            return bs
        return self.newString(str(bs))

    def text(self, sOrBs, p):
        pass

    def textBox(self, sOrBs, r=None, clipPath=None, align=None):
        pass

    def textOverflow(self, sOrBs, box, align=None):
        pass

    def baselines(self, bs, box, align=None):
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

    def scaleImage(self, path, w, h, index=None, showImageLoresMarker=False,
            exportExtension=None, force=False):
        """
        >>> from pagebot.filepaths import getResourcesPath
        >>> srcPath = getResourcesPath() + '/images/peppertom.png'
        >>> path2ScaledImagePath(srcPath, 100, 200, 0, 'png')
        'scaled/peppertom-w100-h200-i0.png'
        >>> context = HtmlContext()
        >>> imagePath = context.scaleImage(srcPath, 100, 200)
        >>> imagePath
        'scaled/peppertom-w100-h200.png'
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
                    if HAS_PIL:
                        im = Image.open(path)
                        im.thumbnail(upt(w, h), Image.ANTIALIAS)
                        im.save(cachedFilePath, exportExtension)
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
