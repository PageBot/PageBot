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
#     abstractcontext.py
#
from pagebot.constants import PAGE_SIZES

class AbstractContext:
    """All contexts should at least contain the same (public) functions DrawBot
    does.  That API is the standard. Additionally there is an optional doc=None
    or e=None, that contains the calling Document or Element instance.  This
    way contexts can derive their own information if needed.

    * https://github.com/typemytype/drawbot/blob/master/drawBot/drawBotDrawingTools.py
    """

    # Drawing.

    def newDrawing(self, w=None, h=None, doc=None):
        """Resets to a clean and empty drawing stack."""
        raise NotImplementedError

    def endDrawing(self, doc=None):
        """Explicitly tells the context that drawing is done. This is advised
        when using DrawBot as a standalone module.  The `doc` attribute is the
        optional Document instance of the caller."""
        raise NotImplementedError

    def saveDrawing(self, path, multiPage=None):
        """PageBot function."""
        raise NotImplementedError

    def getDrawing(self):
        raise NotImplementedError

    # Styles

    def setStyles(self, styles):
        """Set the dictionary of style dictionaries. E.g. to be transformed
        into paragraph styles in InDesignContext or to be used as styles
        for context strings."""
        raise NotImplementedError

    # Magic variables.

    def width(self):
        """Answers the width of the current page."""
        raise NotImplementedError

    def height(self):
        """Answers the height of the current page."""
        raise NotImplementedError

    def sizes(self, paperSize=None):
        """Returns the (w, h) of a specified canvas size. If no canvas size is
        given it will return the dictionary containing all possible page sizes.
        Note that the sizes are in PageBot units, different from what DrawBot
        returns.

        >>> ac = AbstractContext()
        >>> ac.sizes('A4')
        (210mm, 297mm)
        >>> ac.sizes('IllegalSize') is None
        True
        >>> 'Tabloid' in ac.sizes()
        True
        >>> ac.sizes() is PAGE_SIZES
        True
        """
        if paperSize is None:
            return PAGE_SIZES
        return PAGE_SIZES.get(paperSize)

    def pageCount(self):
        """Answer the current page count."""
        raise NotImplementedError

    # Public callbacks.

    def size(self, w, h=None):
        """Sets the width and height of the current page. Standardize on
        PageBot `(w, h)` for consistent naming, instead of DrawBot (width,
        height)."""
        raise NotImplementedError

    def newPage(self, w=None, h=None, page=None, **kwargs):
        """Optional width and height if defined. Standardize on PageBot `(w,
        h)` for consistent naming, instead of DrawBot (width, height).
        Otherwise the optional PageBot `page` instance can be used by the
        context to extract page size."""
        raise NotImplementedError

    def _get_pages(self):
        """To be implemented as property for get. Not to be implemented
        (pages are stored in the Document instance, not in the context),
        other than for the DrawBot context to make it compatible."""
        raise NotImplementedError
    pages = property(_get_pages)

    def saveImage(self, path, *args, **options):
        """Save or export the canvas to a specified format. The `path`
        argument is a single destination path to save the current drawing
        actions. The `file` extension is important because it will determine
        the format in which the image will be exported. All supported file
        extensions: %(supporttedExtensions)s. (`*` will print out all
        actions.)

        When exporting an animation or movie, each page represents a frame and
        the framerate is set by page.frameDuration."""
        raise NotImplementedError

    def scaleImage(self, path, w, h, index=None, showImageLoresMarker=False,
            exportExtension=None, force=False):
        raise NotImplementedError

    def printImage(self, pdf=None):
        """Export the canvas to a printing dialog, ready to print. Optionally
        a `pdf` object can be provided."""
        raise NotImplementedError

    def pdfImage(self):
        """Return the image as a pdf document object."""
        raise NotImplementedError

    # Graphics state.

    def save(self):
        """DrawBot strongly recommends to use self.savedState() in a `with`
        statement instead. Save the current graphics state. This will save the
        state of the canvas (with all the transformations) but also the state
        of the colors, strokes."""
        raise NotImplementedError

    def restore(self):
        """DrawBot strongly recommends to use self.savedState() in a `with`
        statement instead. Restore from a previously saved graphics state.
        This will restore the state of the canvas (with all the
        transformations) but also the state of colors, strokes."""
        raise NotImplementedError

    def savedState(self):
        """Save and restore the current graphics state in a `with` statement."""
        raise NotImplementedError

    # Basic shapes.

    def rect(self, x, y, w=None, h=None, e=None):
        """Draw a rectangle at position `(x, y)`, with the optional given `w`
        width and `h` height. Otherwise the optional PageBot Element instance
        `e` can be used by the context to extract width and height."""
        raise NotImplementedError

    def oval(self, x, y, w=None, h=None, e=None):
        """Draw an oval at position `(x, y)`, with the optional given `w` width
        and `h` height. Otherwise the optional PageBot Element instance `e` can
        be used by the context to extract width and height."""
        raise NotImplementedError

    # Path.

    def newPath(self):
        """Create a new path."""
        raise NotImplementedError

    def moveTo(self, p):
        """Move to a point `p` (x, y)."""
        raise NotImplementedError

    def lineTo(self, p):
        """Line to a point `p` (x, y)."""
        raise NotImplementedError

    def curveTo(self, bcp1, bcp2, p):
        """Curve to a point `p` (x3, y3).
        With given bezier handles `bxp1` (x1, y1) and `bcp1` (x2, y2)."""
        raise NotImplementedError

    def qCurveTo(self, *points):
        """Quadratic curve with a given set of off curves `points` to a on
        curve."""
        raise NotImplementedError

    def arc(self, center, radius, startAngle, endAngle, clockwise):
        """Arc with `center` (x, y) and a given `radius``, from `startAngle` to
        `endAngle`, going clockwise if `clockwise` is True and counter
        clockwise if `clockwise` is False."""
        raise NotImplementedError

    def arcTo(self, xy1, xy2, radius):
        """Arc from one point `xy1` (x1, y1) to an other point `xy2` (x2, y2)
        with a given `radius`."""
        raise NotImplementedError

    def closePath(self):
        """Close the open path."""
        raise NotImplementedError

    def drawPath(self, path=None, p=None, sx=1, sy=None, fill=None,
            stroke=None, strokeWidth=None):
        """Draw `path` or the current path at `p` (x, y), scaled by
        `(sx, sy)` using `fill`, `stroke` and `strokeWidth` as colors."""
        raise NotImplementedError

    def clipPath(self, clipPath=None):
        """Use the given `clipPath` as a clipping path, or the current path if
        no path was given. Everything drawn after a `clipPath()` call will be
        clipped by the clipping path. To "undo" the clipping later, make sure
        you do the clipping inside a `with savedState():` block, as shown in
        the example."""
        raise NotImplementedError

    def line(self, p1=None, p2=None, e=None):
        """Draws a line between two given points `p1` and `p`. Use optional
        calling Element `e` for points and additional drawing settings of the
        line."""
        raise NotImplementedError

    def polygon(self, *points, **kwargs):
        """Draws a polygon with n-amount of points. Optionally a `close`
        argument can be provided to open or close the path. As default a
        `polygon` is a closed path."""
        raise NotImplementedError

    # Color.

    def colorSpace(self, colorSpace):
        """Set the color space. Options are `genericRGB`, `adobeRGB1998`,
        `sRGB`, `genericGray`, `genericGamma22Gray`. The default is
        `genericRGB`. `None` will reset it back to the default."""
        raise NotImplementedError

    def listColorSpaces(self):
        """Return a list of all available color spaces."""
        raise NotImplementedError

    def blendMode(self, operation):
        """Set a blend mode.

        Available operations are::

            `normal`, `multiply`, `screen`, `overlay`, `darken`, `lighten`,
            `colorDodge`, `colorBurn`, `softLight`, `hardLight`, `difference`,
            `exclusion`, `hue`, `saturation`, `color`, `luminosity`, `clear`,
            `copy`, `sourceIn`, `sourceOut`, `sourceAtop`, `destinationOver`,
            `destinationIn`, `destinationOut`, `destinationAtop`, `xOR`,
            `plusDarker` and `plusLighter`

        """
        raise NotImplementedError

    def fill(self, c):
        """
        Note: signature differs from DrawBot.

            def fill(self, r, g=None, b=None, a=None, alpha=None):

        Implementing context needs to check on RGB or CMYK nature of the color."""
        raise NotImplementedError

    cmykFill = fill

    def stroke(self, c, w=None):
        """
        Note: signature differs from DrawBot.

            def stroke(self, r, g=None, b=None, a=None, alpha=None):

        Implementing method needs to check on RGB or CMYK nature of the
        color."""
        raise NotImplementedError

    cmykStroke = stroke

    def shadow(self, shadow):
        """Adds a Shadow `shadow` instance with an shadow.offset (x, y), `
        shadow.blur and a shadow.color. This is different from DrawBot API::

            shadow(offset, blur=None, color=None).

        Implementing context needs to check on RGB or CMYK nature of the
        color."""
        raise NotImplementedError

    cmykShadow = shadow

    def linearGradient(self, gradient, origin, w, h, e=None):
        """A linear Gradient `gradient` instance fill with:

        * `startPoint` as (x, y)
        * `endPoint` as (x, y)
        * `colors` as a list of colors, described similary as `fill`
        * `locations` of each color as a list of floats. (optionally)

        Setting a gradient will ignore the `fill`.
        This is different from the DrawBot API

        startPoint=None, endPoint=None, colors=None, locations=None

        Implementing context needs to check on RGB or CMYK nature of the
        color."""
        raise NotImplementedError

    cmykLinearGradient = linearGradient

    #def radialGradient(self, startPoint=None, endPoint=None, colors=None,
    #        locations=None, startRadius=0, endRadius=100):
    # A radial gradient fill with:
    #    * `startPoint` as (x, y)
    #    * `endPoint` as (x, y)
    #    * `colors` as a list of colors, described similary as `fill`
    #    * `locations` of each color as a list of floats. (optionally)
    #    * `startRadius` radius around the startPoint in degrees (optionally)
    #    * `endRadius` radius around the endPoint in degrees (optionally)
    #    Setting a gradient will ignore the `fill`.
    #    raise NotImplementedError

    radialGradient = linearGradient
    cmykRadialGradient = radialGradient

    # Path drawing behavior.

    def strokeWidth(self, w):
        """Sets stroke width."""
        raise NotImplementedError

    def miterLimit(self, value):
        """Set a miter limit. Used on corner points."""
        raise NotImplementedError

    def lineJoin(self, value):
        raise NotImplementedError

    def lineCap(self, value):
        raise NotImplementedError

    def lineDash(self, value):
        raise NotImplementedError

    # Transform.

    def transform(self, matrix, center=(0, 0)):
        raise NotImplementedError

    def translate(self, x=0, y=0):
        raise NotImplementedError

    def rotate(self, angle, center=None):
        raise NotImplementedError

    def scale(self, x=1, y=None, center=(0, 0)):
        raise NotImplementedError

    def skew(self, angle1, angle2=0, center=(0, 0)):
        raise NotImplementedError

    # Text.

    def font(self, fontName, fontSize=None):
        raise NotImplementedError

    def fallbackFont(self, fontName):
        raise NotImplementedError

    def fontSize(self, fontSize):
        raise NotImplementedError

    def lineHeight(self, value):
        raise NotImplementedError

    def tracking(self, value):
        raise NotImplementedError

    def baselineShift(self, value):
        raise NotImplementedError

    def underline(self, value):
        raise NotImplementedError

    def hyphenation(self, onOff):
        raise NotImplementedError

    def tabs(self, *tabs):
        raise NotImplementedError

    def language(self, language):
        raise NotImplementedError

    def listLanguages(self):
        raise NotImplementedError

    def openTypeFeatures(self, features):
        raise NotImplementedError

    def listOpenTypeFeatures(self, fontName=None):
        raise NotImplementedError

    def fontVariations(self, *args, **axes):
        raise NotImplementedError

    def listFontVariations(self, fontName=None):
        raise NotImplementedError

    # Drawing text.

    def text(self, sOrBs, p):
        raise NotImplementedError

    def textOverflow(self, txt, box, align=None):
        raise NotImplementedError

    def textBox(self, sOrBs, r=None, clipPath=None):
        raise NotImplementedError

    def textBoxBaselines(self, txt, box, align=None):
        raise NotImplementedError

    def FormattedString(self, *args, **kwargs):
        raise NotImplementedError

    # Images

    def image(self, path, p, alpha=1, pageNumber=None,
            w=None, h=None, scaleType=None, e=None):
        raise NotImplementedError

    def imageSize(self, path):
        raise NotImplementedError

    def imagePixelColor(self, path, p):
        raise NotImplementedError

    def numberOfPages(self, path):
        raise NotImplementedError

    # Mov.

    def frameDuration(self, secondsPerFrame):
        raise NotImplementedError

    # PDF links.

    def linkDestination(self, name, x=None, y=None):
        raise NotImplementedError

    def linkRect(self, name, xywh):
        raise NotImplementedError

    # Helpers.

    def textSize(self, bs, w=None, h=None, align=None):
        raise NotImplementedError

    def installedFonts(self, patterns=None):
        raise NotImplementedError

    def installFont(self, fontOrName):
        raise NotImplementedError

    def uninstallFont(self, fontOrName):
        raise NotImplementedError

    def fontContainsCharacters(self, characters):
        raise NotImplementedError

    def fontContainsGlyph(self, glyphName):
        raise NotImplementedError

    def fontFilePath(self):
        raise NotImplementedError

    def listFontGlyphNames(self):
        raise NotImplementedError

    def fontAscender(self):
        raise NotImplementedError

    def fontDescender(self):
        raise NotImplementedError

    def fontXHeight(self):
        raise NotImplementedError

    def fontCapHeight(self):
        raise NotImplementedError

    def fontLeading(self):
        raise NotImplementedError

    def fontLineHeight(self):
        raise NotImplementedError

    def BezierPath(self, path=None, glyphSet=None):
        raise NotImplementedError

    def ImageObject(self, path=None):
        raise NotImplementedError

    def Variable(self, variables, workSpace):
        raise NotImplementedError

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
