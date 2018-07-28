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
from pagebot.toolbox.color import Color, noColor, inheritColor
from pagebot.toolbox.units import rv, isUnit, isUnits # Render units
from pagebot.constants import *
from sys import platform

if platform == 'darwin':
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
else:
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
        >>> context = DrawBotContext()
        >>> context.newPage(px(100), px(100))
        """
        assert isUnits(w, h), ('DrawBotContext.newPage: Values (%s, %s) must all be of type Unit' % (w, h))
        self.b.newPage(w.pt, h.pt)

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
        >>> #context.rect(0, 0, 100, 100)
        """
        assert isUnits(x, y, w, h), ('DrawBotContext.rect: Values (%s, %s, %s, %s) must all be of type Unit' % (x, y, w, h))
        self.b.rect(x.pt, y.pt, w.pt, h.pt) # Render units to points for DrawBot.

    def oval(self, x, y, w, h):
        """Draw an oval in rectangle, where (x,y) is the bottom-left and size
        (w,h).

        >>> context = DrawBotContext()
        >>> context.oval(pt(0), pt(0), pt(100), pt(100))
        >>> #context.oval(0, 0, 100, 100)
        """
        assert isUnits(x, y, w, h), ('DrawBotContext.oval: Values (%s, %s, %s, %s) must all be of type Unit' % (x, y, w, h))
        self.b.oval(x.pt, y.pt, w.pt, h.pt) # Render units to points for DrawBot.

    def circle(self, x, y, r):
        u"""Circle draws a DrawBot oval with (x,y) as middle point and radius r.
        >>> context = DrawBotContext()
        >>> context.circle(pt(100), pt(200), pt(50))
        >>> #context.circle(100, 200, 50)
        """
        assert isUnits(x, y, r), ('DrawBotContext.circle: Values (%s, %s, %s) must all be of type Unit' % (x, y, r))
        self.b.oval((x-r).pt, (y-r).pt, (r*2).pt, (r*2).pt) # Render the unit values

    def line(self, p1, p2):
        """Draw a line from p1 to p2.

        >>> context = DrawBotContext()
        >>> context.line(pt(100, 100), pt(200, 200))
        >>> #context.line((100, 100), (200, 200))
        """
        assert isUnits(p1, p2), ('DrawBotContext.line: Values (%s, %s) must all be of type Unit' % (p1, p2))
        self.b.line(rv(p1, maker=pt), rv(p2, maker=pt)) # Render tuple of units point

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
                p = pt(0, 0)
            assert isUnits(p), ('DrawBotContext.drawPath: Values %s must all be of type Unit' % str(p))
            self.scale(sx, sy)
            self.b.translate(p[0].pt/sx, p[1].pt/sy)
            self.b.drawPath(path)
            self.restore()

    def moveTo(self, p):
        """Move to point p. Create a new path if none is open.

        >>> from pagebot.toolbox.units import pt
        >>> context = DrawBotContext()
        >>> path = context.newPath()
        >>> path.moveTo(pt(100, 100))
        """
        if self._path is None:
            self.newPath()
        assert isUnits(p), ('DrawBotContext.moveTo: Values %s must all be of type Unit' % str(p))
        self._path.moveTo(rv(p, maker=pt)) # Render units point tuple to tuple of values

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
        assert isUnits(p), ('DrawBotContext.curveTo: Values %s must all be of type Unit' % str(p))
        self._path.lineTo(rv(p, maker=pt)) # Render units point tuple to tuple of values

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
        assert isUnits(bcp1, bcp2, p), ('DrawBotContext.curveTo: Values (%s, %s, %s) must all be of type Unit' % (bcp1, bcp2, p))
        self._path.curveTo(rv(bcp1, maker=pt), rv(bcp2, maker=pt), rv(p, maker=pt)) # Render units tuples to value tuples

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
        assert isUnits(dx, dy), ('DrawBotContext.translate: Values (%s, %s) must all be of type Unit' % (dx, dy))
        self.b.translate(dx.pt, dy.pt)

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

    def drawGlyphPath(self, font, glyphName, x, y, fill=None, stroke=None, strokeWidth=0, fontSize=None, xAlign=CENTER):
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
        assert isUnit(fontSize)
        self.b.fontSize(fontSize.r) # Render fontSize unit to value

    def font(self, font, fontSize=None):
        self.b.font(font)
        if fontSize is not None:
            assert isUnit(fontSize)
            self.b.fontSize(fontSize.r) # Render fontSize unit to value

    def newBulletString(self, bullet, e=None, style=None):
        return self.newString(bullet, e=e, style=style)

    def text(self, sOrBs, p):
        """Draw the sOrBs text string, can be a str or BabelString, including a
        DrawBot FormattedString at position p."""
        if not isinstance(sOrBs, str):
            sOrBs = sOrBs.s # Assume here is's a BabelString with a FormattedString inside.

        self.b.text(sOrBs, rv(p, maker=pt)) # Render point units to value tuple

    def textBox(self, sOrBs, r):
        """Draw the sOrBs text string, can be a str or BabelString, including a
        DrawBot FormattedString in rectangle r."""
        if not isinstance(sOrBs, str):
            sOrBs = sOrBs.s # Assume here is's a BabelString with a FormattedString inside.

        self.b.textBox(sOrBs, rv(r, maker=pt)) # Render rectangle units to value tuple

    def textSize(self, bs, w=None, h=None):
        """Answer the size tuple (w, h) of the current text. Answer (0, 0) if
        there is no text defined.  Answer the height of the string if the width
        w is given."""
        if w is not None:
            return self.b.textSize(bs.s, width=w)
        if h is not None:
            return self.b.textSize(bs.s, height=h)
        return self.b.textSize(bs.s)

    def textOverflow(self, bs, bounds, align=LEFT):
        """Answer the overflowing of from the box (0, 0, w, h)
        as new DrawBotString in the current context."""
        return stringClass(self.b.textOverflow(bs.s, bounds, align), self)

    def textBoxBaseLines(self, txt, box):
        x, y, w, h = box
        attrString = txt.getNSObject()
        setter = CTFramesetterCreateWithAttributedString(attrString)
        path = CGPathCreateMutable()
        CGPathAddRect(path, None, CGRectMake(*box))
        box = CTFramesetterCreateFrame(setter, (0, 0), path, None)
        ctLines = CTFrameGetLines(box)
        origins = CTFrameGetLineOrigins(box, (0, len(ctLines)), None)
        return [(x + o.x, y + o.y) for o in origins]

    def openTypeFeatures(self, features):
        """Set the current of opentype features in the context canvas.

        >>> context = DrawBotContext()
        >>> context.openTypeFeatures(dict(smcp=True, zero=True))
        """
        self.b.openTypeFeatures(**features)

    def hyphenation(self, onOff=True):
        """Set the hyphenation on/off flag.

        >>> context = DrawBotContext()
        >>> context.hyphenation(True)
        >>> context.hyphenation(False)
        """
        self.b.hyphenation(onOff)

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
        >>> #context.fill(123)
        """
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
        >>> #context.stroke(123)
        """
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
        assert isUnit(w), ('DrawBotContext.strokeWidth: Strokewidth value %s should be of type Unit' % w)
        self.b.strokeWidth(w.pt)

    setStrokeWidth = strokeWidth

    def rotate(self, angle):
        """Rotate the canvas by angle."""
        self.b.rotate(angle)

    #   I M A G E

    def imagePixelColor(self, path, p):
        return self.b.imagePixelColor(path, p)

    def imageSize(self, path):
        u"""Answer the (w, h) image size of the image file at path."""
        return pt(self.b.imageSize(path))

    def image(self, path, p, alpha=1, pageNumber=None, w=None, h=None):
        """Draw the image. If w or h is defined, then scale the image to fit."""
        iw, ih = self.imageSize(path)

        if w and not h: # Scale proportional
            h = ih * w/iw # iw : ih = w : h
        elif not w and h:
            w = iw * h/ih
        elif not w and not h:
            w = iw
            h = ih

        # else both w and h are defined, scale disproportional
        x, y, = p[0], p[1]
        sx, sy = w/iw, h/ih
        self.save()
        self.scale(sx, sy)
        #self.b.image(path, ((x*sx).r, (y*sy).r), alpha=alpha, pageNumber=pageNumber)
        self.b.image(path, ((x*sx), (y*sy)), alpha=alpha, pageNumber=pageNumber)
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
