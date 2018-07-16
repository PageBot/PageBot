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
from pagebot.toolbox.units import ru, isUnit # Render units
from pagebot.constants import *

# FIXME: bad exception usage. (How to check otherwise if running in DrawBot context?)
#import ForceErrorHere # When debugging: Uncheck in case of forcing noneDrawBotBuilder testing

try:
    #import ForceErrorHere # Uncheck in case of forcing noneDrawBotBuilder testing
    from AppKit import NSFont
    usingDrawBot = True
except (ImportError, AttributeError):
    usingDrawBot = False

if usingDrawBot:
    from CoreText import CTFontDescriptorCreateWithNameAndSize, CTFontDescriptorCopyAttribute
    from CoreText import kCTFontURLAttribute, CTFramesetterCreateWithAttributedString
    from CoreText import CTFramesetterCreateFrame, CTFrameGetLines, CTFrameGetLineOrigins
    from Quartz import CGPathAddRect, CGPathCreateMutable, CGRectMake
    from drawBot import Variable
    from pagebot.contexts.builders.drawbotbuilder import drawBotBuilder
    from pagebot.contexts.strings.drawbotstring import DrawBotString as stringClass
else:
    # If DrawBot is not available on the platform, then use a noneDrawBotBuilder instance, that
    # can be used to run all DrawBot related docTests.
    from pagebot.contexts.builders.nonebuilder import NoneDrawBotBuilder
    from pagebot.contexts.strings.drawbotstring import NoneDrawBotString as stringClass
    drawBotBuilder = NoneDrawBotBuilder()
    NSFont = None
    CTFontDescriptorCreateWithNameAndSize = None
    CTFontDescriptorCopyAttribute = None
    kCTFontURLAttribute = None
    Variable = None
    print('Using drawBotContext-->NoneDrawBotBuilder')

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
        """Create a new drawbot page.

        >>> from pagebot.toolbox.units import px
        >>> context = DrawBotContext()
        >>> context.newPage(pt(100), pt(100))
        >>> context = DrawBotContext()
        >>> context.newPage(px(100), px(100))
        """
        self.b.newPage(w.r, h.r)

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
        """
        self.b.rect(x.r, y.r, w.r, h.r)

    def oval(self, x, y, w, h):
        """Draw an oval in rectangle, where (x,y) is the bottom-left and size
        (w,h).

        >>> context = DrawBotContext()
        >>> context.oval(pt(0), pt(0), pt(100), pt(100))
        """
        self.b.oval(x.r, y.r, w.r, h.r)

    def circle(self, x, y, r):
        u"""Circle draws a DrawBot oval with (x,y) as middle point and radius r."""
        self.b.oval((x-r).r, (y-r).r, (r*2).r, (r*2).r) # Render the unit values

    def line(self, p1, p2):
        """Draw a line from p1 to p2.

        >>> context = DrawBotContext()
        >>> context.line(pt(100, 100), pt(200, 200))
        """
        self.b.line(ru(p1), ru(p2)) # Render tuple of units point

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

    def drawPath(self, path=None, p=(0,0), sx=1, sy=None):
        """Draw the NSBezierPath, or equivalent in other contexts. Scaled image is drawn on (x, y),
        in that order."""
        if path is None:
            path = self._path
        if path is not None:
            self.save()
            if sy is None:
                sy = sx
            self.scale(sx, sy)
            self.b.translate(p[0]/sx, p[1]/sy)
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
        self._path.moveTo(ru(p)) # Render units point tuple to tuple of values

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
        self._path.lineTo(ru(p)) # Render units point tuple to tuple of values

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
        self._path.curveTo(ru(bcp1), ru(bcp2), ru(p)) # Render units tuples to value tuples

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
        self.b.scale(sx, sy)

    def translate(self, dx, dy):
        """Translate the origin to this point."""
        self.b.translate(dx, dy)

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
            if not gradient.colors[0].isCmyk:
                colors = [color.rgb for color in gradient.colors]
                b.linearGradient(startPoint=start, endPoint=end,
                    colors=colors, locations=gradient.locations)
            else:
                colors = [color.cmyk for color in gradient.colors]
                b.cmykLinearGradient(startPoint=start, endPoint=end,
                    colors=colors, locations=gradient.locations)
        else: # Gradient must be radial.
            if not gradient.colors[0].isCmyk:
                colors = [color.rgb for color in gradient.colors]
                b.radialGradient(startPoint=start, endPoint=end,
                    colors=colors, locations=gradient.locations,
                    startRadius=gradient.startRadius, endRadius=gradient.endRadius)
            else:
                colors = [color.cmyk for color in gradient.colors]
                b.cmykRadialGradient(startPoint=start, endPoint=end,
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
        self.b.text(sOrBs, ru(p)) # Render point units to value tuple

    def textBox(self, sOrBs, r):
        """Draw the sOrBs text string, can be a str or BabelString, including a DrawBot FormattedString
        in rectangle r."""
        if not isinstance(sOrBs, str):
            sOrBs = sOrBs.s # Assume here is's a BabelString with a FormattedString inside.
        self.b.textBox(sOrBs, ru(r)) # Render rectangle units to value tuple

    def textSize(self, bs, w=None, h=None):
        """Answer the size tuple (w, h) of the current text. Answer (0, 0) if there is no text defined.
        Answer the height of the string if the width w is given."""
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
        """Set the self._frameDuretion for animated gifs to a number of seconds per frame.
        Used when initializing a new page."""
        self.b.frameDuration(secondsPerFrame or DEFAULT_FRAME_DURATION)

    #   C O L O R

    def setTextFillColor(self, fs, c):
        u"""Set the fill color of the formatted string.

        >>> context = DrawBotContext()
        >>> fs = context.newString('Hello')
        >>> context.textFill(fs, color(0.5)) # Same as setTextFillColor
        >>> context.textFill(fs, color('red'))
        """
        self.fill(c, builder=fs)

    textFill = setTextFillColor

    def setTextStrokeColor(self, fs, c, w=None):
        u"""Set the stroke color of the formatted string.

        >>> context = DrawBotContext()
        >>> fs = context.newString('Hello')
        >>> context.textStroke(fs, color(0.5)) # Same as setTextStrokeColor
        >>> context.textStroke(fs, color('red'), w=pt(10))
        """
        self.stroke(c, w=w, builder=fs)

    textStroke = setTextStrokeColor

    def setTextStrokeWidth(self, fs, w):
        u"""Set the stroke width of the formatted string.

        >>> context = DrawBotContext()
        >>> fs = context.newString('Hello')
        >>> context.setTextStrokeWidth(fs, pt(10))
        """
        self.setStrokeWidth(w, builder=fs)

    def fill(self, c, builder=None):
        u"""Set the color for global or the color of the formatted string.

        >>> context = DrawBotContext()
        >>> context.fill(color(0.5)) # Same as setFillColor
        >>> context.fill(color('red'))
        >>> context.fill(inheritColor)
        >>> context.fill(noColor)
        """
        if not isinstance(c, Color):
            print('Error in DrawBotContext.fill(): c should be of type Color')
            raise AssertionError

        if builder is None: # Builder can be optional DrawBot FormattedString
            builder = self.b

        if c is inheritColor: # Keep color setting as it is.
            pass
        elif c is noColor:
            builder.fill(None) # Set color to no-color
        elif c.isCmyk:
            builder.cmykFill(c.cmyk)
        else:
            builder.fill(c.rgb)

    setFillColor = fill # DrawBot compatible API

    def stroke(self, c, w=None, builder=None):
        u"""Set the color for global or the color of the formatted string.

        >>> context = DrawBotContext()
        >>> context.stroke(color(0.5)) # Same as setStrokeColor
        >>> context.stroke(color('red'))
        >>> context.stroke(inheritColor)
        >>> context.stroke(noColor)
        """
        assert isinstance(c, Color)

        if builder is None: # Builder can be optional DrawBot FormattedString
            builder = self.b

        if c is inheritColor: # Keep color setting as it is.
            pass
        if c is noColor:
            builder.stroke(None) # Set color to no-color
        elif c.isCmyk:
            builder.cmykStroke(c.cmyk)
        else:
            builder.stroke(c.rgb)
        if w is not None:
            self.setStrokeWidth(w)

    setStrokeColor = stroke # DrawBot compatible API

    def setStrokeWidth(self, w, builder=None):
        u"""Set the current stroke width.

        >>> from pagebot.toolbox.units import unit, pt, mm
        >>> context = DrawBotContext()
        >>> context.setStrokeWidth(pt(0.5))
        >>> context.setStrokeWidth(mm(0.5))

        """
        if builder is None: # Builder can be optional DrawBot FormattedString
            builder = self.b

        builder.strokeWidth(w)

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
        self.b.image(path, ((x*sx).r, (y*sy).r), alpha=alpha, pageNumber=pageNumber)
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
