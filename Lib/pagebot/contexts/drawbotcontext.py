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
#     drawbotcontext.py
#

import os
import traceback
from pagebot.contexts.basecontext import BaseContext
from pagebot.toolbox.color import color, Color, noColor, inheritColor
from pagebot.toolbox.units import pt, upt, point2D, Angle
from pagebot.toolbox.transformer import path2Name, path2Dir
from pagebot.constants import (CENTER, RIGHT, DEFAULT_FRAME_DURATION, ORIGIN,
        FILETYPE_PDF, FILETYPE_SVG, FILETYPE_JPG, FILETYPE_PNG, FILETYPE_GIF,
        FILETYPE_MOV, DEFAULT_FILETYPE, DEFAULT_FALLBACK_FONT_PATH)

try:
    import drawBot
    from drawBot import Variable

    from pagebot.contexts.strings.drawbotstring import DrawBotString as stringClass
    drawBotBuilder = drawBot
    # Id to make builder hook name. Views will try to call e.build_html()
    drawBotBuilder.PB_ID = 'drawBot'
except (AttributeError, ImportError):
    print(traceback.format_exc())
    NSFont = None
    CTFontDescriptorCreateWithNameAndSize = None
    CTFontDescriptorCopyAttribute = None
    kCTFontURLAttribute = None
    Variable = None
    from pagebot.contexts.builders.nonebuilder import NoneDrawBotBuilder
    from pagebot.contexts.strings.drawbotstring import NoneDrawBotString as stringClass

    # If DrawBot is not available on the platform, the noneDrawBotBuilder
    # instance is used to run DrawBot related docTests.
    drawBotBuilder = NoneDrawBotBuilder()

class DrawBotContext(BaseContext):
    """The DrawBotContext implements the DrawBot functionality within the
    PageBot framework."""

    # In case of specific builder addressing, callers can check here.
    isDrawBot = True

    # Used by the generic BaseContext.newString()
    STRING_CLASS = stringClass
    EXPORT_TYPES = (FILETYPE_PDF, FILETYPE_SVG, FILETYPE_PNG, FILETYPE_JPG,
            FILETYPE_GIF, FILETYPE_MOV)

    def __init__(self):
        """Constructor of DrawBotContext if drawBot import exists.

        >>> drawBotBuilder is not None
        True
        >>> drawBotBuilder is not None and drawBotBuilder.PB_ID == 'drawBot'
        True
        >>> context = DrawBotContext()
        >>> context.isDrawBot
        True
        >>> context.name
        'DrawBotContext'
        """
        # The context builder "cls.b" is drawBot which executes actual drawing
        # calls, similar to function calls in DrawBot scripts.
        self.b = drawBotBuilder #  Builder for this canvas.
        self.name = self.__class__.__name__
        # Holds the extension as soon as the export file path is defined.
        self.fileType = DEFAULT_FILETYPE
        super().__init__()

    #   D O C U M E N T

    def newDocument(self, w, h):
        """Ignore for DrawBot; document opens automatically if first page
        is created."""
        pass

    def saveDocument(self, path, multiPage=None):
        """Select non-standard DrawBot export builders here. Save the current
        image as path, rendering depending on the extension of the path file.
        In case the path starts with "_export", create its directories.

        >>> context = DrawBotContext()
        >>> context.saveImage('_export/MyFile.pdf')

        """
        self.checkExportPath(path)
        self.b.saveImage(path, multipage=multiPage)

    saveImage = saveDocument # Compatible API with DrawBot

    def getDocument(self):
        """Returns a PDF document of the current state."""
        return self.b.pdfImage()

    #   V A R I A B L E

    def Variable(self, variableUI , globalVariables):
        """Offers interactive global value manipulation in DrawBot. Probably to
        be ignored in other contexts."""
        # Variable is a DrawBot context global, used to make simple UI with
        # controls on input parameters.
        try:
            Variable(variableUI, globalVariables)
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

        >>> context = DrawBotContext()
        >>> context.bluntCornerRect(pt(0), pt(0), pt(100), pt(100))
        >>> context.bluntCornerRect(0, 0, 100, 100)
        """

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

        >>> context = DrawBotContext()
        >>> context.roundedRect(pt(0), pt(0), pt(100), pt(100))
        >>> context.roundedRect(0, 0, 100, 100)
        """
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

    def quadTo(bcp, p):
        # TODO: Convert to Bezier with 0.6 rule
        pass

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

    #   G R A D I E N T  &  S H A D O W

    def setShadow(self, eShadow):
        """Set the DrawBot graphics state for shadow if all parameters are
        set."""
        if eShadow is not None and eShadow.offset is not None:
            if eShadow.color.isCmyk:
                self.b.shadow(upt(eShadow.offset), # Convert units to values
                              blur=upt(eShadow.blur),
                              color=color(eShadow.color).cmyk)
            else:
                self.b.shadow(upt(eShadow.offset),
                              blur=upt(eShadow.blur),
                              color=color(eShadow.color).rgb)

    def setGradient(self, gradient, origin, w, h):
        """Define the gradient call to match the size of element e., Gradient
        position is from the origin of the page, so we need the current origin
        of e."""
        b = self.b
        start = origin[0] + gradient.start[0] * w, origin[1] + gradient.start[1] * h
        end = origin[0] + gradient.end[0] * w, origin[1] + gradient.end[1] * h

        if gradient.linear:
            if (gradient.colors[0]).isCmyk:
                colors = [color(c).cmyk for c in gradient.colors]
                b.cmykLinearGradient(startPoint=upt(start), endPoint=upt(end),
                    colors=colors, locations=gradient.locations)
            else:
                colors = [color(c).rgb for c in gradient.colors]
                b.linearGradient(startPoint=upt(start), endPoint=upt(end),
                    colors=colors, locations=gradient.locations)
        else: # Gradient must be radial.
            if color(gradient.colors[0]).isCmyk:
                colors = [color(c).cmyk for c in gradient.colors]
                b.cmykRadialGradient(startPoint=upt(start), endPoint=upt(end),
                    colors=colors, locations=gradient.locations,
                    startRadius=gradient.startRadius, endRadius=gradient.endRadius)
            else:
                colors = [color(c).rgb for c in gradient.colors]
                b.radialGradient(startPoint=upt(start), endPoint=upt(end),
                    colors=colors, locations=gradient.locations,
                    startRadius=gradient.startRadius, endRadius=gradient.endRadius)

    def lineDash(self, lineDash):
        """Linesash is None or a list of dash lengths."""
        if lineDash is None:
            self.b.lineDash(None)
        else:
            self.b.lineDash(*lineDash)

    def miterLimit(self, value):
        self.b.miterLimit(value)

    def lineJoin(self, value):
        """option value"""
        self.b.lineJoin(value)

    def lineCap(self, value):
        """Possible values are butt, square and round."""
        assert value in ('butt', 'square', 'round')
        self.b.lineCap(value)

    #   C A N V A S

    def save(self):
        self.b.save()

    saveGraphicState = save # Compatible with DrawBot API

    def restore(self):
        self.b.restore()

    restoreGraphicState = restore # Compatible with DrawBot API

    #   F O N T S

    def fontPath2FontName(self, fontPath):
        """Answers the font name of the font related to fontPath. This is done
        by installing it (again). Answers None if the font cannot be installed
        or if the path does not exists.

        >>> import os
        >>> from pagebot.fonttoolbox.fontpaths import TEST_FONTS_PATH
        >>> context = DrawBotContext()
        >>> context.fontPath2FontName('Aaa.ttf') is None # Does not exist
        True
        >>> path = TEST_FONTS_PATH + '/fontbureau/Amstelvar-Roman-VF.ttf'
        >>> os.path.exists(path)
        True
        >>> context.fontPath2FontName(path)
        'Amstelvar-Roman'
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
        nsFont = NSFont.fontWithName_size_(fontName, 25)
        if nsFont is not None:
            fontRef = CTFontDescriptorCreateWithNameAndSize(nsFont.fontName(), nsFont.pointSize())
            url = CTFontDescriptorCopyAttribute(fontRef, kCTFontURLAttribute)
            return url.path()
        return None

    def listOpenTypeFeatures(self, fontName):
        """Answers the list of opentype features available in the named font."""
        return self.b.listOpenTypeFeatures(fontName)

    def installedFonts(self, patterns=None):
        """Answers a list of all fonts (name or path) that are installed in the
        OS.

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> installed = context.installedFonts()
        >>> len(installed) > 0
        True
        """
        if isinstance(patterns, str): # In case it is a string, convert to a list
            patterns = [patterns]
        fontNames = []
        for fontName in self.b.installedFonts():
            if not patterns:
                fontNames.append(fontName) # If no pattern theun answer all.
            else:
                for pattern in patterns:
                    if pattern in fontName:
                        fontNames.append(fontName)
                        break
        return fontNames

    def installFont(self, fontOrName):
        """Install the font in the context. fontOrName can be a Font instance
        (in which case the path is used) or a full font path.

        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> from pagebot import getContext
        >>> context = getContext()
        >>> installed = context.installedFonts()
        >>> len(installed) > 0
        True
        >>> font = findFont('Roboto-Regular')
        >>> context.installFont(font)
        'Roboto-Regular'
        """
        if hasattr(fontOrName, 'path'):
            fontOrName.info.installedName = self.b.installFont(fontOrName.path)
            return fontOrName.info.installedName
        return self.b.installFont(fontOrName)

    def unInstallFont(self, fontOrName):
        if hasattr(fontOrName, 'path'):
            fontOrName = fontOrName.path
        return self.b.uninstallFont(fontOrName)

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

    #   T E X T

    def text(self, sOrBs, p):
        """Draw the sOrBs text string, can be a str or BabelString, including a
        DrawBot FormattedString at position p."""
        if not isinstance(sOrBs, str):
            sOrBs = sOrBs.s # Assume here is's a BabelString with a FormattedString inside.
        ppt = point2D(upt(p))
        self.b.text(sOrBs, ppt) # Render point units to value tuple

    def textBox(self, sOrBs, r=None, clipPath=None):
        """Draw the sOrBs text string, can be a str or BabelString, including a
        DrawBot FormattedString in rectangle r.

        >>> from pagebot.toolbox.units import pt
        >>> context = DrawBotContext()
        >>> context.textBox('ABC', (10, 10, 200, 200))
        """
        if not isinstance(sOrBs, str):
            sOrBs = sOrBs.s # Assume here is's a BabelString with a FormattedString inside.
        if clipPath is not None:
            self.b.textBox(sOrBs, clipPath) # Render rectangle units to value tuple
        elif r is not None:
            xpt, ypt, wpt, hpt = upt(r)
            self.b.textBox(sOrBs, (xpt, ypt, wpt, hpt)) # Render rectangle units to value tuple

    #   C O L O R

    def fill(self, c):
        """Set the color for global or the color of the formatted string.

        >>> from pagebot.toolbox.color import color
        >>> context = DrawBotContext()
        >>> context.fill(color(0.5)) # Same as setFillColor
        >>> context.fill(color('red'))
        >>> context.fill(inheritColor)
        >>> context.fill(noColor)
        >>> context.fill(0.5)
        """
        if c is None:
            c = noColor
        elif isinstance(c, (tuple, list, int, float)):
            c = color(c)

        msg = 'DrawBotContext.fill: %s should be of type Color'
        assert isinstance(c, Color), (msg % c)

        if c is inheritColor:
            # Keep color setting as it is.
            pass
        elif c is noColor:
            self.b.fill(None) # Set color to no-color
        elif c.isCmyk:
            # DrawBot.fill has slight API differences compared to
            # FormattedString fill().
            c, m, y, k = c.cmyk
            self.b.cmykFill(c, m, y, k, alpha=c.a)
        else:
            # DrawBot.fill has slight API differences compared to
            # FormattedString fill(). Convert to RGB, whatever the color type.
            r, g, b = c.rgb
            self.b.fill(r, g, b, alpha=c.a)

    def stroke(self, c, w=None):
        """Set the color for global or the color of the formatted string.

        >>> from pagebot.toolbox.color import color
        >>> context = DrawBotContext()
        >>> context.stroke(color(0.5)) # Same as setStrokeColor
        >>> context.stroke(color('red'))
        >>> context.stroke(inheritColor)
        >>> context.stroke(noColor)
        >>> context.stroke(0.5)
        """
        if c is None:
            c = noColor
        elif isinstance(c, (tuple, list, int, float)):
            c = color(c)

        msg = 'DrawBotContext.stroke: %s should be of type Color'
        assert isinstance(c, Color), (msg % c)

        if c is inheritColor:
            # Keep color setting as it is.
            pass
        if c is noColor:
            self.b.stroke(None) # Set color to no-color
        elif c.isCmyk:
            # DrawBot.stroke has slight API differences compared to
            # FormattedString stroke().
            cc, cm, cy, ck = c.cmyk
            self.b.cmykStroke(cc, cm, cy, ck, alpha=c.a)
        else:
            # DrawBot.stroke has slight API differences compared to
            # FormattedString stroke(). Convert to RGB, whatever the color type.
            r, g, b = c.rgb
            self.b.stroke(r, g, b, alpha=c.a)
        if w is not None:
            self.strokeWidth(w)

    # Transformation.

    def scale(self, sx, sy=None):
        """Set the drawing scale."""
        if isinstance(sx, (tuple, list)):
            assert len(sx) in (2, 3)
            sx, sy = sz[0], s[1]
        if sy is None:
            sy = sx

        msg = 'DrawBotContext.scale: Values (%s, %s) must all be of numbers'
        assert isinstance(sx, (int, float)) and isinstance(sy, (int, float)), (msg % (sx, sy))
        self.b.scale(sx, sy)

    def translate(self, dx, dy):
        """Translate the origin to this point."""
        dxpt, dypt = point2D(upt(dx, dy))
        self.b.translate(dxpt, dypt)

    def transform(self, t):
        """Transform canvas over matrix t, e.g. (1, 0, 0, 1, dx, dy) to shift
        over vector (dx, dy)"""
        self.b.transform(t)

    def rotate(self, angle, center=None):
        """Rotate the canvas by angle. If angle is not a units.Angle instance,
        then convert.

        >>> context = DrawBotContext()
        >>> context.rotate(40)
        """
        if center is None:
            center = (0, 0)
        else:
            center = point2D(upt(center))
        if isinstance(angle, Angle):
            angle = angle.degrees
        # Otherwise assume the value to be a degrees number.
        self.b.rotate(angle, center=center)

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

    def getImageObject(self, path):
        """Answers the ImageObject that knows about image filters. For names
        and parameters of filters see:

        * http://www.drawbot.com/content/image/imageObject.html

        >>> from pagebot import getResourcesPath
        >>> context = DrawBotContext()
        >>> path = getResourcesPath() + '/images/peppertom_lowres_398x530.png'
        >>> imo = context.getImageObject(path)

        """
        return self.b.ImageObject(path)

    def path2ScaledImagePath(self, path, w, h, index=None, exportExtension=None):
        """Answers the path to the scaled image.

        >>> context = DrawBotContext()
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
        >>> context = DrawBotContext()
        >>> path = getResourcesPath() + '/images/peppertom_lowres_398x530.png'
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

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
