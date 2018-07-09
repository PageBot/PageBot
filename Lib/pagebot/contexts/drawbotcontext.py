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
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     drawbotcontext.py
#
import os

# FIXME: bad exception usage.
try:
    #import ForceErrorHere # Uncheck in case of forcing noneDrawBotBuilder testing
    from AppKit import NSFont
    from CoreText import CTFontDescriptorCreateWithNameAndSize, CTFontDescriptorCopyAttribute
    from CoreText import kCTFontURLAttribute, CTFramesetterCreateWithAttributedString
    from CoreText import CTFramesetterCreateFrame, CTFrameGetLines, CTFrameGetLineOrigins
    from Quartz import CGPathAddRect, CGPathCreateMutable, CGRectMake
    from drawBot import Variable
    from pagebot.contexts.builders.drawbotbuilder import drawBotBuilder
    from pagebot.contexts.strings.drawbotstring import DrawBotString as stringClass
except (ImportError, AttributeError):
    # If DrawBot is not available on the platform, then use a noneDrawBotBuilder instance, that
    # can be used to run all DrawBot related docTests.
    from pagebot.contexts.builders.nonebuilder import NoneDrawBotBuilder
    from pagebot.contexts.strings.drawbotstring import NoneDrawBotString as stringClass
    drawBotBuilder = NoneDrawBotBuilder()
    NSFont = None
    CTFontDescriptorCreateWithNameAndSize = CTFontDescriptorCopyAttribute = kCTFontURLAttribute = None
    Variable = None
    print('Using drawBotContext-->NoneDrawBotBuilder')

from pagebot.contexts.basecontext import BaseContext
from pagebot.style import NO_COLOR, LEFT, CENTER, RIGHT, DEFAULT_FRAME_DURATION
from pagebot.toolbox.color import Color

class DrawBotContext(BaseContext):
    u"""A DrawBotContext instance combines the specific functions of the DrawBot library
    This way it way it hides e.g. the type of BabelString
    instance needed, and the type of HTML/CSS file structure to be created."""

    # In case of specific builder addressing, callers can check here.
    isDrawBot = True

    # Used by the generic BaseContext.newString( )
    STRING_CLASS = stringClass
    EXPORT_TYPES = ('pdf', 'svg', 'png', 'jpg', 'gif', 'mov')

    def __init__(self):
        u"""Constructor of DrawBotContext if drawBot import exists.

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

    #   S C R E E N

    def screenSize(self):
        u"""Answer the current screen size in DrawBot. Otherwise default is to do nothing.

        >>> context = DrawBotContext()
        >>> size = context.screenSize()
        >>> size[0] > 100 and size[1] > 100
        True
        """
        return self.b.sizes().get('screen', None)

    #   D O C U M E N T

    def newDocument(self, w, h, title=None, pageCount=None, units='pt'):
        u"""Ignore for DrawBot, as document open automatic if first page is created."""
        self.title = title
        self.pageCount = pageCount
        self.units = units

    def saveDocument(self, path, multiPage=None):
        u"""Select other than standard DrawBot export builders here.
        Save the current image as path, rendering depending on the extension of the path file.
        In case the path starts with "_export", then create it directories.

        >>> context = DrawBotContext()
        >>> context.saveImage('_export/MyFile.pdf')

        """
        self.checkExportPath(path)
        self.b.saveImage(path, multipage=multiPage)

    saveImage = saveDocument # Compatible API with DrawBot

    def newPage(self, w, h):
        u"""Create a new drawbot page.

        >>> context = DrawBotContext()
        >>> context.newPage(100, 100)
        """
        self.b.newPage(w, h)

    def newDrawing(self):
        u"""Clear output canvas, start new export file.

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
        u"""Draw a rectangle in the canvas.

        >>> context = DrawBotContext()
        >>> context.rect(0, 0, 100, 100)
        """
        self.b.rect(x, y, w, h)

    def oval(self, x, y, w, h):
        u"""Draw an oval in rectangle, where (x,y) is the bottom-left and size (w,h).

        >>> context = DrawBotContext()
        >>> context.oval(0, 0, 100, 100)
        """
        self.b.oval(x, y, w, h)

    def circle(self, x, y, r):
        u"""Circle draws a DrawBot oval with (x,y) as middle point and radius r."""
        self.b.oval(x-r, y-r, r*2, r*2)

    def line(self, p1, p2):
        u"""Draw a line from p1 to p2.

        >>> context = DrawBotContext()
        >>> context.line((100, 100), (200, 200))
        """
        self.b.line(p1, p2)

    def newPath(self):
        u"""Make a new DrawBot Bezierpath() to draw in.

        >>> context = DrawBotContext()
        >>> context.path is not None
        True
        """
        self._path = self.b.BezierPath()
        return self._path

    def _get_path(self):
        u"""Answer the open drawing path. Create one if it does not exist.

        >>> context = DrawBotContext()
        >>> context.path is not None
        True
        """
        if self._path is None:
            self.newPath()
        return self._path
    path = property(_get_path)

    def drawPath(self, path=None, p=(0,0), sx=1, sy=None):
        u"""Draw the NSBezierPath, or equivalent in other contexts. Scaled image is drawn on (x, y),
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
        u"""Move to point p. Create a new path if none is open.

        >>> context = DrawBotContext()
        >>> path = context.newPath()
        >>> path.moveTo((100, 100))
        """
        if self._path is None:
            self.newPath()
        self._path.moveTo((p[0], p[1]))

    def lineTo(self, p):
        u"""Line to point p. Create a new path if none is open.

        >>> context = DrawBotContext()
        >>> # Draw directly on th epath
        >>> # Draw on the context cached path
        >>> _ = context.newPath()
        >>> context.moveTo((100, 100))
        >>> context.curveTo((100, 200), (200, 200), (200, 100))
        >>> context.closePath()
        >>> path = context.newPath()
        >>> path.moveTo((100, 100))
        >>> path.curveTo((100, 200), (200, 200), (200, 100))
        >>> path.closePath()
        >>> context.drawPath(path)
        """
        if self._path is None:
            self.newPath()
        self._path.lineTo((p[0], p[1]))

    def quadTo(bcp, p):
        # TODO: Convert to Bezier with 0.6 rule
        pass

    def curveTo(self, bcp1, bcp2, p):
        u"""Curve to point p. Create a new path if none is open.

        >>> context = DrawBotContext()
        >>> # Draw directly on th epath
        >>> # Draw on the context cached path
        >>> _ = context.newPath()
        >>> context.moveTo((100, 100))
        >>> context.curveTo((100, 200), (200, 200), (200, 100))
        >>> context.closePath()
        >>> path = context.newPath()
        >>> path.moveTo((100, 100))
        >>> path.curveTo((100, 200), (200, 200), (200, 100))
        >>> path.closePath()
        """
        if self._path is None:
            self.newPath()
        self._path.curveTo((bcp1[0], bcp1[1]), (bcp2[0], bcp2[1]), (p[0], p[1]))

    def closePath(self):
        u"""Curve to point p. Create a new path if none is open.

        >>> context = DrawBotContext()
        >>> # Draw directly on th epath
        >>> # Draw on the context cached path
        >>> _ = context.newPath()
        >>> context.moveTo((100, 100))
        >>> context.curveTo((100, 200), (200, 200), (200, 100))
        >>> context.closePath()
        >>> path = context.newPath()
        >>> path.moveTo((100, 100))
        >>> path.curveTo((100, 200), (200, 200), (200, 100))
        >>> path.closePath()
        """
        if self._path is not None:
            self._path.closePath()

    def bezierPathByFlatteningPath(self, path):
        u"""Use the NSBezier flatten path."""
        return path.getNSBezierPath().bezierPathByFlatteningPath()

    def scale(self, sx, sy=None):
        u"""Set the drawing scale."""
        if sy is None:
            sy = sx
        self.b.scale(sx, sy)

    def translate(self, dx, dy):
        u"""Translate the origin to this point."""
        self.b.translate(dx, dy)

    def transform(self, t):
        u"""Transform canvas over matrix t, e.g. (1, 0, 0, 1, dx, dy) to shift over vector (dx, dy)"""
        self.b.transform(t)

    #   G R A D I E N T  &  S H A D O W

    def setShadow(self, eShadow):
        u"""Set the DrawBot graphics state for shadow if all parameters are set."""
        if eShadow is not None and eShadow.offset is not None:
            if eShadow.cmykColor is not None:
                self.b.shadow(eShadow.offset,
                              blur=eShadow.blur,
                              color=eShadow.cmykColor)
            else:
                self.b.shadow(eShadow.offset,
                              blur=eShadow.blur,
                              color=eShadow.color)

    def setGradient(self, gradient, origin, w, h):
        u"""Define the gradient call to match the size of element e., Gradient position
        is from the origin of the page, so we need the current origin of e."""
        b = self.b
        start = origin[0] + gradient.start[0] * w, origin[1] + gradient.start[1] * h
        end = origin[0] + gradient.end[0] * w, origin[1] + gradient.end[1] * h

        if gradient.linear:
            if gradient.cmykColors is None:
                b.linearGradient(startPoint=start, endPoint=end,
                    colors=gradient.colors, locations=gradient.locations)
            else:
                b.cmykLinearGradient(startPoint=start, endPoint=end,
                    colors=gradient.cmykColors, locations=gradient.locations)
        else: # Gradient must be radial.
            if gradient.cmykColors is None:
                b.radialGradient(startPoint=start, endPoint=end,
                    colors=gradient.colors, locations=gradient.locations,
                    startRadius=gradient.startRadius, endRadius=gradient.endRadius)
            else:
                b.cmykRadialGradient(startPoint=start, endPoint=end,
                    colors=gradient.cmykColors, locations=gradient.locations,
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
        u"""Answer the font name of the font related to fontPath. This is done by installing it (again).
        Answer None if the font cannot be installed or if the path does not exists.

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
        u"""Answer the unchanged path, if it exists as file. Answer the path that is source of the given font name.
        Answer None if the font cannot be found."""
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
        u"""Answer the list of opentype features available in the named font."""
        return self.b.listOpenTypeFeatures(fontName)

    #   G L Y P H

    def drawGlyphPath(self, font, glyphName, x, y, fillColor=0, strokeColor=None, strokeWidth=0, fontSize=None, xAlign=CENTER):
        u"""Draw the font[glyphName] at the defined position with the defined fontSize.

        """
        s = fontSize/font.info.unitsPerEm
        glyph = font[glyphName]
        if xAlign == CENTER:
            x -= (glyph.width or 0)/2*s
        elif xAlign == RIGHT:
            x -= glyph.width*s
        self.save()
        self.setFillColor(fillColor)
        self.setStrokeColor(strokeColor, strokeWidth)
        self.transform((1, 0, 0, 1, x, y))
        self.scale(s)
        self.drawPath(glyph.path)
        self.restore()

    #   T E X T

    def fontSize(self, fontSize):
        u"""Set the font size in the context.

        >>> context = DrawBotContext()
        >>> context.fontSize(12)
        """
        self.b.fontSize(fontSize)

    def font(self, font, fontSize=None):
        self.b.font(font)
        if fontSize is not None:
            self.b.fontSize(fontSize)

    def newBulletString(self, bullet, e=None, style=None):
        return self.newString(bullet, e=e, style=style)

    def text(self, sOrBs, p):
        u"""Draw the sOrBs text string, can be a str or BabelString, including a DrawBot FormattedString
        at position p."""
        if not isinstance(sOrBs, str):
            sOrBs = sOrBs.s # Assume here is's a BabelString with a FormattedString inside.
        self.b.text(sOrBs, p)

    def textBox(self, sOrBs, r):
        u"""Draw the sOrBs text string, can be a str or BabelString, including a DrawBot FormattedString
        in rectangle r."""
        if not isinstance(sOrBs, str):
            sOrBs = sOrBs.s # Assume here is's a BabelString with a FormattedString inside.
        self.b.textBox(sOrBs, r)

    def textSize(self, bs, w=None, h=None):
        u"""Answer the size tuple (w, h) of the current text. Answer (0, 0) if there is no text defined.
        Answer the height of the string if the width w is given."""
        if w is not None:
            return self.b.textSize(bs.s, width=w)
        if h is not None:
            return self.b.textSize(bs.s, height=h)
        return self.b.textSize(bs.s)

    def textOverflow(self, bs, bounds, align=LEFT):
        u"""Answer the overflowing of from the box (0, 0, w, h)
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
        u"""Set the current of opentype features in the context canvas.

        >>> context = DrawBotContext()
        >>> context.openTypeFeatures(dict(smcp=True, zero=True))
        """
        self.b.openTypeFeatures(**features)

    def hyphenation(self, onOff=True):
        u"""Set the hyphenation on/off flag.

        >>> context = DrawBotContext()
        >>> context.hyphenation(True)
        >>> context.hyphenation(False)
        """
        self.b.hyphenation(onOff)

    #   A N I M A T I O N

    def frameDuration(self, secondsPerFrame):
        u"""Set the self._frameDuretion for animated gifs to a number of seconds per frame.
        Used when initializing a new page."""
        self.b.frameDuration(secondsPerFrame or DEFAULT_FRAME_DURATION)

    #   C O L O R

    def setTextFillColor(self, fs, c, cmyk=False):
        self.setFillColor(c, cmyk, fs)

    def setTextStrokeColor(self, fs, c, w=1, cmyk=False):
        self.setStrokeColor(c, w, cmyk, fs)

    def setFillColor(self, c, cmyk=False, b=None):
        u"""Set the color for global or the color of the formatted string."""
        if b is None: # Builder can be optional DrawBot FormattedString
            b = self.b

        if c is NO_COLOR:
            pass # Color is undefined, do nothing.

        elif isinstance(c, Color):
            #from pprint import pprint
            #pprint(vars(c))
            b.fill(c.r, c.g, c.b)

        elif c is None or isinstance(c, (float, int)): # Because None is a valid value.
            if cmyk:
                b.cmykFill(c)
            else:
                b.fill(c)
        elif isinstance(c, (list, tuple)) and len(c) in (3, 4):
            if cmyk:
                b.cmykFill(*c)
            else:
                b.fill(*c)
        else:
            raise ValueError('DrawBotContext.setFillColor: Error in color format "%s"' % repr(c))

    fill = setFillColor # DrawBot compatible API

    def strokeWidth(self, w):
        u"""Set the current stroke width."""
        self.b.strokeWidth(w)

    def setStrokeColor(self, c, w=1, cmyk=False, b=None):
        u"""Set global stroke color or the color of the formatted string."""
        if b is None: # Builder can be optional DrawBot FormattedString
            b = self.b
        if c is NO_COLOR:
            pass # Color is undefined, do nothing.
        elif c is None or isinstance(c, (float, int)): # Because None is a valid value.
            if cmyk:
                b.cmykStroke(c)
            else:
                b.stroke(c)
        elif isinstance(c, (list, tuple)) and len(c) in (3, 4):
            if cmyk:
                b.cmykStroke(*c)
            else:
                b.stroke(*c)
        else:
            raise ValueError('DrawBotContext.setStrokeColor: Error in color format "%s"' % repr(c))
        if w is not None:
            b.strokeWidth(w)

    stroke = setStrokeColor # DrawBot compatible API

    def rotate(self, angle):
        u"""Rotate the canvas by angle."""
        self.b.rotate(angle)

    #   I M A G E

    def imagePixelColor(self, path, p):
        return self.b.imagePixelColor(path, p)

    def imageSize(self, path):
        u"""Answer the (w, h) image size of the image file at path."""
        return self.b.imageSize(path)

    def image(self, path, p, alpha=1, pageNumber=None, w=None, h=None):
        u"""Draw the image. If w or h is defined, then scale the image to fit."""
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
        self.b.image(path, (x*sx, y*sy), alpha=alpha, pageNumber=pageNumber)
        self.restore()

    def getImageObject(self, path):
        u"""Answer the ImageObject that knows about image filters.
        For names and parameters of filters see:
        http://www.drawbot.com/content/image/imageObject.html

        >>> from pagebot import getResourcesPath
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> path = getResourcesPath() + '/images/peppertom_lowres_398x530.png'
        >>> imo = context.getImageObject(path)

        """
        return self.b.ImageObject(path)


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
