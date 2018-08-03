#!/usr/bin/env python
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
#     drawbotcontext.py
#
import os
from pagebot.contexts.basecontext import BaseContext
from pagebot.style import LEFT, CENTER, RIGHT, DEFAULT_FRAME_DURATION
from pagebot.toolbox.color import color, Color, noColor, inheritColor
from pagebot.toolbox.units import pt, upt, point2D # Render units to points
from pagebot.constants import *
from sys import platform

try:
#if platform == 'darwin':
    from CoreText import CTFontDescriptorCreateWithNameAndSize, \
        CTFontDescriptorCopyAttribute, kCTFontURLAttribute, \
        CTFramesetterCreateWithAttributedString, CTFramesetterCreateFrame, \
        CTFrameGetLines, CTFrameGetLineOrigins
    from Quartz import CGPathAddRect, CGPathCreateMutable, CGRectMake
    import drawBot
    from drawBot import Variable

    from pagebot.contexts.strings.drawbotstring import DrawBotString as stringClass
    drawBotBuilder = drawBot
    # Id to make builder hook name. Views will try to call e.build_html()
    drawBotBuilder.PB_ID = 'drawBot'
except AttributeError:
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
    """A DrawBotContext instance combines the specific functions of the DrawBot
    library This way it way it hides e.g. the type of BabelString instance
    needed, and the type of HTML/CSS file structure to be created."""

    # In case of specific builder addressing, callers can check here.
    isDrawBot = True

    # Used by the generic BaseContext.newString( )
    STRING_CLASS = stringClass
    EXPORT_TYPES = (FILETYPE_PDF, FILETYPE_SVG, FILETYPE_PNG, FILETYPE_JPG, FILETYPE_GIF, FILETYPE_MOV)

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
        # The context builder "cls.b" is the main drawBot library, that contains all
        # drawing calls in as used regular DrawBot scripts.
        self.b = drawBotBuilder # cls.b builder for this canvas.
        self.name = self.__class__.__name__
        self._path = None # Hold current open DrawBot path
        self.fileType = DEFAULT_FILETYPE # Holds the extension as soon as the export file path is defined.

    #   S C R E E N

    def screenSize(self):
        """Answer the current screen size in DrawBot. Otherwise default is to
        do nothing.

        >>> context = DrawBotContext()
        >>> size = context.screenSize()
        >>> size[0] > 100 and size[1] > 100
        True
        """
        return pt(self.b.sizes().get('screen', None))

    #   D O C U M E N T

    def newDocument(self, w, h):
        u"""Ignore for DrawBot, as document open automatic if first page is created."""
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

    def newPage(self, w, h):
        """Creates a new drawbot page.

        >>> from pagebot.toolbox.units import px
        >>> context = DrawBotContext()
        >>> context.newPage(pt(100), pt(100))
        >>> context.newPage(100, 100)
        """
        wpt, hpt = upt(w, h)
        self.b.newPage(wpt, hpt)

    def newDrawing(self):
        """Clear output canvas, start new export file.

        >>> context = DrawBotContext()
        >>> context.newDrawing()
        """
        self.b.newDrawing()

    #   V A R I A B L E

    def Variable(self, variableUI , globalVariables):
        """Offers interactive global value manipulation in DrawBot. Probably to be ignored in other contexts."""
        # Variable is a DrawBot context global, used to make simple UI with controls on input parameters.
        try:
            Variable(variableUI, globalVariables)
        except self.b.misc.DrawBotError:
            pass # Ingore if there is a DrawBot context, but not running inside DrawBot.

    #   D R A W I N G

    def rect(self, x, y, w, h):
        """Draw a rectangle in the canvas.

        >>> context = DrawBotContext()
        >>> context.rect(pt(0), pt(0), pt(100), pt(100))
        >>> context.rect(0, 0, 100, 100)
        """
        xpt, ypt, wpt, hpt = upt(x, y, w, h)
        self.b.rect(xpt, ypt, wpt, hpt) # Render units to points for DrawBot.

    def oval(self, x, y, w, h):
        """Draw an oval in rectangle, where (x,y) is the bottom-left and size
        (w,h).

        >>> context = DrawBotContext()
        >>> context.oval(pt(0), pt(0), pt(100), pt(100))
        >>> context.oval(0, 0, 100, 100)
        """
        xpt, ypt, wpt, hpt = upt(x, y, w, h)
        self.b.oval(xpt, ypt, wpt, hpt) # Render units to points for DrawBot.

    def circle(self, x, y, r):
        u"""Circle draws a DrawBot oval with (x,y) as middle point and radius r.
        >>> context = DrawBotContext()
        >>> context.circle(pt(100), pt(200), pt(50))
        >>> context.circle(100, 200, 50)
        """
        xpt, ypt, rpt = upt(x, y, r)
        self.b.oval(xpt-rpt, ypt-rpt, rpt*2, rpt*2) # Render the unit values

    def line(self, p1, p2):
        """Draw a line from p1 to p2.

        >>> context = DrawBotContext()
        >>> context.line(pt(100, 100), pt(200, 200))
        >>> context.line((100, 100), (200, 200))
        """
        p1pt  = point2D(upt(p1))
        p2pt  = point2D(upt(p2))
        self.b.line(p1pt, p2pt) # Render tuple of units point

    def newPath(self):
        """Make a new DrawBot Bezierpath() to draw in.

        >>> context = DrawBotContext()
        >>> context.path is not None
        True
        """
        self._path = self.b.BezierPath()
        return self._path


    def _get_path(self):
        """Answers the open drawing path. Create one if it does not exist.

        >>> context = DrawBotContext()
        >>> context.path is not None
        True
        """
        if self._path is None:
            self.newPath()
        return self._path
    path = property(_get_path)

    def drawPath(self, path=None, p=None, sx=1, sy=None):
        """Draw the NSBezierPath, or equivalent in other contexts. Scaled image is drawn on (x, y),
        in that order."""
        if path is None:
            path = self._path
        if path is not None:
            self.save()
            if sy is None:
                sy = sx
            if p is None:
                xpt = ypt = 0
            else:
                xpt, ypt = point2D(upt(p))
            self.scale(sx, sy)
            self.b.translate(xpt/sx, ypt/sy)
            self.b.drawPath(path)
            self.restore()

    def moveTo(self, p):
        """Move to point p. Create a new path if none is open.

        >>> from pagebot.toolbox.units import pt
        >>> context = DrawBotContext()
        >>> path = context.newPath()
        >>> path.moveTo(pt(100, 100))
        >>> path.moveTo((100, 100))
        """
        if self._path is None:
            self.newPath()
        ppt = point2D(upt(p))
        self._path.moveTo(ppt) # Render units point tuple to tuple of values

    def lineTo(self, p):
        """Line to point p. Create a new path if none is open.

        >>> context = DrawBotContext()
        >>> # Draw directly on th epath
        >>> # Draw on the context cached path
        >>> _ = context.newPath()
        >>> context.moveTo(pt(100, 100))
        >>> context.curveTo(pt(100, 200), pt(200, 200), pt(200, 100))
        >>> context.closePath()
        >>> path = context.newPath()
        >>> path.moveTo(pt(100, 100))
        >>> path.curveTo(pt(100, 200), pt(200, 200), pt(200, 100))
        >>> path.closePath()
        >>> context.drawPath(path)
        """
        if self._path is None:
            self.newPath()
        ppt = point2D(upt(p))
        self._path.lineTo(ppt) # Render units point tuple to tuple of values

    def quadTo(bcp, p):
        # TODO: Convert to Bezier with 0.6 rule
        pass

    def curveTo(self, bcp1, bcp2, p):
        """Curve to point p. Create a new path if none is open.

        >>> context = DrawBotContext()
        >>> # Draw directly on th epath
        >>> # Draw on the context cached path
        >>> _ = context.newPath()
        >>> context.moveTo(pt(100, 100))
        >>> context.curveTo(pt(100, 200), pt(200, 200), pt(200, 100))
        >>> context.closePath()
        >>> path = context.newPath()
        >>> path.moveTo(pt(100, 100))
        >>> path.curveTo(pt(100, 200), pt(200, 200), pt(200, 100))
        >>> path.closePath()
        """
        if self._path is None:
            self.newPath()
        b1pt = point2D(upt(bcp1))
        b2pt = point2D(upt(bcp2))
        ppt = point2D(upt(p))
        self._path.curveTo(b1pt, b2pt, ppt) # Render units tuples to value tuples

    def closePath(self):
        """Curve to point p. Create a new path if none is open.

        >>> context = DrawBotContext()
        >>> # Draw directly on th epath
        >>> # Draw on the context cached path
        >>> _ = context.newPath()
        >>> context.moveTo(pt(100, 100))
        >>> context.curveTo(pt(100, 200), pt(200, 200), pt(200, 100))
        >>> context.closePath()
        >>> path = context.newPath()
        >>> path.moveTo(pt(100, 100))
        >>> path.curveTo(pt(100, 200), pt(200, 200), pt(200, 100))
        >>> path.closePath()
        """
        if self._path is not None:
            self._path.closePath()

    def bezierPathByFlatteningPath(self, path):
        """Use the NSBezier flatten path."""
        return path.getNSBezierPath().bezierPathByFlatteningPath()

    def scale(self, sx, sy=None):
        """Set the drawing scale."""
        if sy is None:
            sy = sx
        assert isinstance(sx, (int, float)) and isinstance(sy, (int, float)), ('DrawBotContext.scale: Values (%s, %s) must all be of numbers' % (sx, sy))
        self.b.scale(sx, sy)

    def translate(self, dx, dy):
        """Translate the origin to this point."""
        dxpt, dypt = point2D(upt(dx, dy))
        self.b.translate(dxpt, dypt)

    def transform(self, t):
        """Transform canvas over matrix t, e.g. (1, 0, 0, 1, dx, dy) to shift over vector (dx, dy)"""
        self.b.transform(t)

    #   G R A D I E N T  &  S H A D O W

    def setShadow(self, eShadow):
        """Set the DrawBot graphics state for shadow if all parameters are set."""
        if eShadow is not None and eShadow.offset is not None:
            if eShadow.color.isCmyk:
                self.b.shadow(eShadow.offset,
                              blur=eShadow.blur,
                              color=eShadow.color.cmyk)
            else:
                self.b.shadow(eShadow.offset,
                              blur=eShadow.blur,
                              color=eShadow.color.rgb)

    def setGradient(self, gradient, origin, w, h):
        """Define the gradient call to match the size of element e., Gradient position
        is from the origin of the page, so we need the current origin of e."""
        b = self.b
        start = origin[0] + gradient.start[0] * w, origin[1] + gradient.start[1] * h
        end = origin[0] + gradient.end[0] * w, origin[1] + gradient.end[1] * h

        if gradient.linear:
            if gradient.colors[0].isCmyk:
                colors = [color.cmyk for color in gradient.colors]
                b.cmykLinearGradient(startPoint=start, endPoint=end,
                    colors=colors, locations=gradient.locations)
            else:
                colors = [color.rgb for color in gradient.colors]
                b.linearGradient(startPoint=start, endPoint=end,
                    colors=colors, locations=gradient.locations)
        else: # Gradient must be radial.
            if gradient.colors[0].isCmyk:
                colors = [color.cmyk for color in gradient.colors]
                b.cmykRadialGradient(startPoint=start, endPoint=end,
                    colors=colors, locations=gradient.locations,
                    startRadius=gradient.startRadius, endRadius=gradient.endRadius)
            else:
                colors = [color.rgb for color in gradient.colors]
                b.radialGradient(startPoint=start, endPoint=end,
                    colors=colors, locations=gradient.locations,
                    startRadius=gradient.startRadius, endRadius=gradient.endRadius)

    def lineDash(self, *lineDash):
        self.b.lineDash(*lineDash)

    def miterLimit(self, value):
        self.b.miterLimit(value)

    def lineJoin(self, value):
        """option value"""
        self.b.lineJoin(value)

    def lineCap(self, value):
        """Possible values are butt, square and round."""
        self.b.lineCap(value)

    #   C A N V A S

    def saveGraphicState(self):
        self.b.save()

    save = saveGraphicState # Compatible with DrawBot API

    def restoreGraphicState(self):
        self.b.restore()

    restore = restoreGraphicState # Compatible with DrawBot API

    #   F O N T S

    def fontPath2FontName(self, fontPath):
        """Answers the font name of the font related to fontPath. This is done
        by installing it (again). Answers None if the font cannot be installed
        or if the path does not exists.

        >>> from pagebot.fonttoolbox.fontpaths import TEST_FONTS_PATH
        >>> context = DrawBotContext()
        >>> context.fontPath2FontName('Aaa.ttf') is None # Dow not exist
        True
        >>> path = TEST_FONTS_PATH + '/fontbureau/Amstelvar-Roman-VF.ttf'
        >>> context.fontPath2FontName(path)
        'Amstelvar-Roman-VF.ttf'
        """
        if os.path.exists(fontPath):
            return self.b.installFont(fontPath)
        return None

    def fontName2FontPath(self, fontName):
        """Answers the unchanged path, if it exists as file. Answers the path
        that is source of the given font name. Answers None if the font cannot
        be found."""
        # If the font cannot be found by name, then test if the file exists as path and answer it.
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
        """Answer the list of opentype features available in the named font."""
        return self.b.listOpenTypeFeatures(fontName)

    #   G L Y P H

    def drawGlyphPath(self, font, glyphName, x, y, fill=noColor, stroke=noColor, strokeWidth=0, fontSize=None, xAlign=CENTER):
        u"""Draw the font[glyphName] at the defined position with the defined fontSize.

        """
        s = fontSize/font.info.unitsPerEm
        glyph = font[glyphName]
        if xAlign == CENTER:
            x -= (glyph.width or 0)/2*s
        elif xAlign == RIGHT:
            x -= glyph.width*s
        self.save()
        self.setFillColor(fill)
        self.setStrokeColor(stroke, w=strokeWidth)
        self.transform((1, 0, 0, 1, x, y))
        self.scale(s)
        self.drawPath(glyph.path)
        self.restore()

    #   T E X T

    def fontSize(self, fontSize):
        """Set the font size in the context.

        >>> from pagebot.toolbox.units import pt
        >>> context = DrawBotContext()
        >>> context.fontSize(pt(12))
        """
        fspt = upt(fontSize)
        self.b.fontSize(fspt) # Render fontSize unit to value

    def font(self, font, fontSize=None):
        self.b.font(font)
        if fontSize is not None:
            fspt = upt(fontSize)
            self.b.fontSize(fspt) # Render fontSize unit to value

    def newBulletString(self, bullet, e=None, style=None):
        return self.newString(bullet, e=e, style=style)

    def text(self, sOrBs, p):
        """Draw the sOrBs text string, can be a str or BabelString, including a
        DrawBot FormattedString at position p."""
        if not isinstance(sOrBs, str):
            sOrBs = sOrBs.s # Assume here is's a BabelString with a FormattedString inside.
        ppt = point2D(upt(p)) 
        self.b.text(sOrBs, ppt) # Render point units to value tuple

    def textBox(self, sOrBs, r):
        """Draw the sOrBs text string, can be a str or BabelString, including a
        DrawBot FormattedString in rectangle r.

        >>> from pagebot.toolbox.units import pt
        >>> context = DrawBotContext()
        >>> context.textBox('ABC', (10, 10, 200, 200))
        """
        if not isinstance(sOrBs, str):
            sOrBs = sOrBs.s # Assume here is's a BabelString with a FormattedString inside.
        xpt, ypt, wpt, hpt = upt(r) 
        self.b.textBox(sOrBs, (xpt, ypt, wpt, hpt)) # Render rectangle units to value tuple

    def openTypeFeatures(self, features):
        """Set the current of opentype features in the context canvas.

        >>> context = DrawBotContext()
        >>> context.openTypeFeatures(dict(smcp=True, zero=True))
        """
        self.b.openTypeFeatures(**features)

    #   A N I M A T I O N

    def frameDuration(self, secondsPerFrame):
        """Set the self._frameDuretion for animated gifs to a number of seconds
        per frame. Used when initializing a new page."""
        self.b.frameDuration(secondsPerFrame or DEFAULT_FRAME_DURATION)

    #   C O L O R

    def fill(self, c):
        u"""Set the color for global or the color of the formatted string.

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
        assert isinstance(c, Color), ('DrawBotContext.fill: %s should be of type Color' % c)
        if c is inheritColor: # Keep color setting as it is.
            pass
        elif c is noColor:
            self.b.fill(None) # Set color to no-color
        elif c.isCmyk:
            c, m, y, k = c.cmyk # DrawBot.fill has slight API difference with FormattedString.fill
            self.b.cmykFill(c, m, y, k, alpha=c.a)
        else:
            r, g, b = c.rgb # DrawBot.fill has slight API difference with FormattedString.fill
            self.b.fill(r, g, b, alpha=c.a) # Convert to rgb, whatever the type of color

    setFillColor = fill # DrawBot compatible API

    def stroke(self, c, w=None):
        u"""Set the color for global or the color of the formatted string.

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
        assert isinstance(c, Color), ('DrawBotContext.stroke: %s should be of type Color' % c)
        if c is inheritColor: # Keep color setting as it is.
            pass
        if c is noColor:
            self.b.stroke(None) # Set color to no-color
        elif c.isCmyk:
            cc, cm, cy, ck = c.cmyk # DrawBot.stroke has slight API difference with FormattedString.stroke
            self.b.cmykStroke(cc, cm, cy, ck, alpha=c.a)
        else:
            r, g, b = c.rgb # DrawBot.stroke has slight API difference with FormattedString.stroke
            self.b.stroke(r, g, b, alpha=c.a)
        if w is not None:
            self.strokeWidth(w)

    setStrokeColor = stroke # DrawBot compatible API

    def strokeWidth(self, w):
        u"""Set the current stroke width.

        >>> from pagebot.toolbox.units import unit, pt, mm
        >>> context = DrawBotContext()
        >>> context.setStrokeWidth(pt(0.5))
        >>> context.setStrokeWidth(mm(0.5))
        """
        wpt = upt(w)
        self.b.strokeWidth(wpt)

    setStrokeWidth = strokeWidth

    def rotate(self, angle):
        """Rotate the canvas by angle."""
        self.b.rotate(angle)

    #   I M A G E

    def imagePixelColor(self, path, p):
        ppt = point2D(upt(p))
        return self.b.imagePixelColor(path, ppt)

    def imageSize(self, path):
        u"""Answer the (w, h) image size of the image file at path."""
        return pt(self.b.imageSize(path))

    def image(self, path, p, alpha=1, pageNumber=None, w=None, h=None):
        """Draw the image. If w or h is defined, then scale the image to fit."""
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

        # else both w and h are defined, scale disproportional
        xpt, ypt, = point2D(upt(p))
        sx, sy = wpt/iw, hpt/ih
        self.save()
        self.scale(sx, sy)
        #self.b.image(path, ((xpt*sx), (ypt*sy)), alpha=alpha, pageNumber=pageNumber)
        self.b.image(path, ((xpt*sx), (ypt*sy)), alpha=alpha, pageNumber=pageNumber)
        self.restore()

    def getImageObject(self, path):
        """Answer the ImageObject that knows about image filters.
        For names and parameters of filters see:
        http://www.drawbot.com/content/image/imageObject.html

        >>> from pagebot import getResourcesPath
        >>> context = DrawBotContext()
        >>> path = getResourcesPath() + '/images/peppertom_lowres_398x530.png'
        >>> imo = context.getImageObject(path)

        """
        return self.b.ImageObject(path)


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
