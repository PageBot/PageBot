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
#     basecontext.py
#

import os
from os.path import exists
from math import radians, sin, cos
import xml.etree.ElementTree as ET
from PyPDF2 import PdfFileReader

from pagebot.constants import (LEFT, RIGHT, CENTER, DEFAULT_FRAME_DURATION,
        DEFAULT_FONT_SIZE, DEFAULT_LANGUAGE, DEFAULT_WIDTH, FILETYPE_SVG,
        FILETYPE_PDF, DEFAULT_FONT, XXXL)
from pagebot.contexts.basecontext.abstractcontext import AbstractContext
from pagebot.contexts.basecontext.babelstring import BabelString
from pagebot.errors import PageBotFileFormatError
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.style import makeStyle
from pagebot.toolbox.color import (color, noColor, Color, inheritColor,
        blackColor)
from pagebot.toolbox.transformer import path2Extension
from pagebot.toolbox.units import upt, pt, point2D, Angle, Pt

HAS_PIL = True

try:
    from PIL import Image
except:
    print('FlatContext: Warning, missing PIL')
    HAS_PIL = False

class BaseContext(AbstractContext):
    """Base API for all contexts. Extends the DrawBot interface.
    """
    # Tells Typesetter that by default tags should not be included in output.
    useTags = False
    EXPORT_TYPES = None

    def __init__(self, name=None):
        self.name = name or self.__class__.__name__
        # Holds current open Bézier path.
        self._bezierpath = None

        self._fill = blackColor
        self._stroke = noColor
        self._strokeWidth = 0
        self._textFill = blackColor
        self._textStroke = noColor
        self._textStrokeWidth = 0
        font = findFont(DEFAULT_FONT)
        self._font = font.path
        self._fontSize = DEFAULT_FONT_SIZE
        self._frameDuration = 0
        self._fonts = {}

        # Origin set by self.translate()
        self._ox = pt(0)
        self._oy = pt(0)
        self._sx = 1
        self._sy = 1
        #self._sz = 1
        self._rotationCenter = (0, 0)
        self._rotate = 0
        self._hyphenation = True
        self._language = DEFAULT_LANGUAGE
        self._openTypeFeatures = None # FIXME: what type?

        # Stack of graphic states.
        self._gState = []

        self._pages = []
        self.style = None
        self.units = Pt.UNIT
        self.hasPIL = False

        if HAS_PIL:
            self.hasPIL = True

    def __repr__(self):
        return '<%s>' % self.name

    def _get_pages(self):
        return self._pages
    pages = property(_get_pages)

    def _get_bezierpath(self):
        """Answers the open drawing self._bezierpath. Creates one if it does
        not exist.

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> path = context.bezierpath
        >>> path is not None
        True
        >>> #len(path.points)
        #0
        >>> path.moveTo((0, 0))
        >>> path.lineTo((100, 100))
        >>> #len(context.bezierpath.points)
        >>> #len(path.points)
        #2
        """
        if self._bezierpath is None:
            self._bezierpath = self.newPath()
        return self._bezierpath

    bezierpath = property(_get_bezierpath)

    '''
    FIXME: Conflict with def language().

    def _get_language(self):
        return self._language
    def _set_language(self, language):
        self._language = language or DEFAULT_LANGUAGE

    language = property(_get_language, _set_language)
    '''

    # Saving / export.

    def saveImage(self, path, *args, **options):
        pass

    def export(self, fileName, folderName=None, extension=None):
        pass

    # Image scaling.

    def scaleImage(self, path, w, h, index=None, showImageLoresMarker=False,
            exportExtension=None, force=False):
        """Scales image and stores it to _scaled/image-name.ext.

        TODO: show optional low resolution marker? Or remove it?
        TODO: add optional extensions.
        TODO: move to shared base.
        TODO: check if index is still necessary.
        """
        assert exists(path)
        assert self.hasPIL
        im = Image.open(path)
        path, ext = self.getResizedPathName(path, w, h)

        if ext == 'jpg':
            ext = 'jpeg'

        if force or not exists(path):
            try:
                im = im.resize((w, h), Image.ANTIALIAS)
            except OverflowError as e:
                print('%s: Caught an OverflowError:' % self.name, e)
                print('Image path is %s' % path)
            im.save(path, ext)

        return path

    # Older implementation, shows image and optional message.
    '''
    cachePath, fileName = self.path2ScaledImagePath(path, w, h, index, exportExtension)

    # If default _scaled directory does not exist, then create it.
    if not exists(cachePath):
        os.makedirs(cachePath)
    cachedFilePath = cachePath + fileName

    if force or not os.path.exists(cachedFilePath):
        # Clean the drawing stack.
        self.image(path, (0, 0), w=w, h=h, pageNumber=index or 0)

        if showImageLoresMarker:
            bs = self.newString('LO-RES',
                    style=dict(font=DEFAULT_FALLBACK_FONT_PATH,
                        fontSize=pt(64), fill=color(0, 1, 1),
                        textFill=color(1, 0, 0)))
            tw, th = bs.textSize
            self.text(bs, (w/2-tw/2, h/2-th/4))
        self.saveImage(cachedFilePath)

        # Clean the drawing stack again.
    return cachedFilePath
    '''


    def printImage(self, pdf=None):
        return self.b.printImage(pdf=pdf)

    def pdfImage(self):
        return self.b.pdfImage()

    def clear(self):
        pass

    # Graphics state.

    def save(self):
        """Saves the current graphic state, in case it needs to be restored later."""
        self.saveGraphicState()

    def restore(self):
        """Restores the previous graphic state."""
        self.restoreGraphicState()

    # Basic shapes.

    def rect(self, x, y, w, h):
        """Draws a rectangle in the canvas.
        TODO: draw as path?

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> context.newPage(420, 420)
        >>> context.rect(pt(0), pt(0), pt(100), pt(100))
        >>> context.rect(0, 0, 100, 100)
        """
        xpt, ypt, wpt, hpt = upt(x, y, w, h)
        # Render units to points for DrawBot.
        self.b.rect(xpt, ypt, wpt, hpt)

    def oval(self, x, y, w, h):
        """Draw an oval in rectangle where `(x, y)` is the bottom-left and size
        `(w, h)`.
        TODO: draw as path?

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> context.newPage(420, 420)
        >>> context.oval(pt(0), pt(0), pt(100), pt(100))
        >>> context.oval(0, 0, 100, 100)
        """
        # Render units to points.
        xpt, ypt, wpt, hpt = upt(x, y, w, h)
        self.b.oval(xpt, ypt, wpt, hpt)

    def circle(self, x, y, r):
        """Circle draws a `circle` with (x, y) as middle point and radius r.
        TODO: draw as path?

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> context.newPage(420, 420)
        >>> context.circle(pt(100), pt(200), pt(50))
        >>> context.circle(100, 200, 50)
        """
        # Render units to points.
        xpt, ypt, rpt = upt(x, y, r)
        self.b.oval(xpt-rpt, ypt-rpt, 2*rpt, 2*rpt)

    # Path.

    def newPath(self):
        """Makes a new Bezierpath to draw in and answers it. This will not
        initialize self._bezierpath, which is accessed by the property
        self.bezierpath. This method uses a BezierPath class path to draw.

        NOTE: PageBot function.

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> context.newPage(420, 420)
        >>> path = context.newPath()
        """
        # Defaults to DrawBot at the moment, should create a BaseBezier here.
        raise NotImplementedError
        #self._bezierpath = BaseBezierPath(self.b)
        #return self._bezierpath

    def moveTo(self, p):
        """Move to point `p` in the open path. Create a new self._bezierpath if none
        is open.

        >>> from pagebot.toolbox.units import pt
        >>> from pagebot import getContext
        >>> context = getContext()
        >>> context.newPage(420, 420)
        >>> context.moveTo(pt(100, 100))
        >>> context.moveTo((100, 100))
        >>> # Drawing on a separate path.
        >>> path = context.newPath()
        >>> path.moveTo(pt(100, 100))
        >>> path.curveTo(pt(100, 200), pt(200, 200), pt(200, 100))
        >>> path.closePath()
        >>> context.drawPath(path)

        """
        # Render units point tuple to tuple of values.
        ppt = upt(point2D(p))
        self.bezierpath.moveTo(ppt)

    def lineTo(self, p):
        """Line to point p in the open path. Create a new self._bezierpath if none
        is open.

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> context.newPage(420, 420)
        >>> # Create a new self._bezierpath by property self.bezierpath.
        >>> context.moveTo(pt(100, 100))
        >>> context.lineTo(pt(100, 200))
        >>> context.closePath()
        >>> # Drawing on a separate path
        >>> path = context.newPath()
        >>> path.moveTo(pt(100, 100))
        >>> path.lineTo(pt(100, 200))
        >>> path.closePath()
        >>> context.drawPath(path)
        """
        # Render units point tuple to tuple of values.
        ppt = upt(point2D(p))
        self.bezierpath.lineTo(ppt)


    # FIXME: should get n points, add curveToOne(bcp1, bcp2, p).
    #def curveTo(self, *points):
    def curveTo(self, bcp1, bcp2, p):
        """Curve to point p i nthe open path. Create a new path if none is
        open.

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> hasattr(context, 'newPath')
        True
        >>> context.newPage(420, 420)
        >>> # Create a new self._bezierpath by property self.bezierpath
        >>> context.moveTo(pt(100, 100))
        >>> context.curveTo(pt(100, 200), pt(200, 200), pt(200, 100))
        >>> context.closePath()
        >>> # Drawing on a separate path
        >>> path = context.newPath()
        >>> path.moveTo(pt(100, 100))
        >>> path.curveTo(pt(100, 200), pt(200, 200), pt(200, 100))
        >>> path.closePath()
        >>> context.drawPath(path)
        """
        b1pt = upt(point2D(bcp1))
        b2pt = upt(point2D(bcp2))
        ppt = upt(point2D(p))
        self.bezierpath.curveTo(b1pt, b2pt, ppt)

    def qCurveTo(self, *points):
        # TODO: call on self.bezierpath.
        return self.b.qCurveTo(*points)

    '''
    def quadTo(self, bcp, p):
        # TODO: Convert to Bezier with 0.6 rule
        # Same output as qCurveTo()?
        return self.b.quadTo(bcp, p)
    '''

    def arc(self, center, radius, startAngle, endAngle, clockwise):
        # TODO: call on self.bezierpath.
        return self.b.arc(center, radius, startAngle, endAngle, clockwise)

    def arcTo(self, xy1, xy2, radius):
        # TODO: call on self.bezierpath.
        return self.b.arcTo(xy1, xy2, radius)

    def closePath(self):
        """Closes the open path if it exists, otherwise ignore it.

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> context.newPage(420, 420)
        >>> # Creates. a new self._bezierpath by property self.bezierpath.
        >>> context.moveTo(pt(100, 100))
        >>> context.curveTo(pt(100, 200), pt(200, 200), pt(200, 100))
        >>> context.closePath()
        >>> # Drawing on a separate path.
        >>> path = context.newPath()
        >>> path.moveTo(pt(100, 100))
        >>> path.curveTo(pt(100, 200), pt(200, 200), pt(200, 100))
        >>> path.closePath()
        >>> context.drawPath(path)
        """
        if self._bezierpath is not None: # Only if an open path exists.
            self._bezierpath.closePath()

    def drawPath(self, path=None, p=None, sx=1, sy=None, fill=None,
            stroke=None, strokeWidth=None):
        """Draws the BezierPath. Scaled image is drawn on (x, y), in that
        order. Use self._bezierpath if path is omitted. PageBot function.

        NOTE: Flat uses native shape, Y-coordinates need to be inverted.
        TODO: update tests, counting contour points.
        TODO: add curve tests.

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> path = context.newPath()
        >>> path.points
        ()
        >>> context.newPage(420, 420)
        >>> # Property self.bezierpath creates a self._bezierpath BezierPath.
        >>> len(context.bezierpath.points)
        0
        >>> context.moveTo((10, 10)) # moveTo and lineTo are drawing on context._bezierpath
        >>> context.lineTo((110, 10))
        >>> context.lineTo((110, 110))
        >>> context.lineTo((10, 110))
        >>> context.closePath()
        >>> #len(context.bezierpath.points) #5
        >>> #len(context.bezierpath.points) #5
        >>> context.fill((1, 0, 0))
        >>> context.drawPath(p=(0, 0)) # Draw self._bezierpath with various offsets
        >>> context.drawPath(p=(200, 200))
        >>> context.drawPath(p=(0, 200))
        >>> context.drawPath(p=(200, 0))
        >>> context.saveImage('_export/DrawBotContext1.pdf')
        >>> # Drawing directly on a path, created by context
        >>> path = context.newPath() # Leaves current self._bezierpath untouched
        >>> len(path.points)
        0
        >>> path.moveTo((10, 10)) # Drawing on context._bezierpath
        >>> path.lineTo((110, 10))
        >>> path.lineTo((110, 110))
        >>> path.lineTo((10, 110))
        >>> path.lineTo((10, 10))
        >>> path.closePath()
        >>> len(path)
        1
        >>> contour = path.contours[0]
        >>> len(contour)
        5
        """

        """
        FIXME: oval gives different results.
        >>> context = getContext()
        >>> path = context.newPath()
        >>> path.oval(160-50, 160-50, 100, 100) # path.oval draws directly on the path
        >>> #len(path.points) #6
        >>> context.fill((0, 0.5, 1))
        >>> context.drawPath(path, p=(0, 0)) # Draw self._bezierpath with various offsets
        >>> context.drawPath(path, p=(200, 200))
        >>> context.drawPath(path, p=(0, 200))
        >>> context.drawPath(path, p=(200, 0))
        >>> context.saveImage('_export/DrawBotContext2.pdf')
        >>> # Oval and rect don't draw on self._bezierpath (yet).
        >>> context.oval(160-50, 160-50, 100, 100)
        >>> context.bezierpath.points
        ((110.0, 260.0), (160.0, 310.0), (210.0, 260.0), (160.0, 210.0), (110.0, 260.0))
        """
        if path is None:
            path = self.bezierpath

        # If it's a BezierPath, get the BezierPath.
        if hasattr(path, 'bp'):
            bezierPath = path.bp
            # If not forced as attribute, then try to get from the
            # BezierPath.style.
            if fill is None:
                fill = path.style.get('fill')
            if stroke is None:
                stroke = path.style.get('stroke')
            if strokeWidth is None:
                stroke = path.style.get('strokeWidth')
        else:
            # Otherwise we assume it is a context BezierPath instance.
            bezierPath = path

        self.save()

        if sy is None:
            sy = sx

        if p is None:
            xpt = ypt = 0
        else:
            xpt, ypt = point2D(upt(p))

        self.scale(sx, sy)
        self.translate(xpt/sx, ypt/sy)

        # Set fill and stroke if they are defined by attribute or by path.style
        # Otherwise ignore and use the setting as defined already in the
        # graphic state.
        if fill is not None:
            self.fill(color(fill))
        if stroke is not None and strokeWidth:
            self.stroke(color(stroke), upt(strokeWidth))
        self.b.drawPath(bezierPath)
        self.restore()

    def clipPath(self, clipPath=None):
        """Sets the clipPath of the DrawBot builder in a new saved graphics
        state. Clip paths cannot be restored, so they should be inside a
        context.save() and context.restore().

        TODO: add unit tests.
        """
        self.b.clipPath(clipPath)

    def line(self, p1, p2):
        """Draw a line from p1 to p2. This method is using the BezierPath
        as path to draw on.

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> context.newPage(420, 420)
        >>> context.line(pt(100, 100), pt(200, 200))
        >>> context.line((100, 100), (200, 200))
        """
        p1pt = upt(point2D(p1))
        p2pt = upt(point2D(p2))
        self.b.line(p1pt, p2pt) # Render tuple of units point

    def polygon(self, *points, **kwargs):
        return self.b.polygon(*points, **kwargs)

    # Color

    def colorSpace(self, colorSpace):
        return self.b.colorSpace(colorSpace)

    def listColorSpaces(self):
        return self.b.listColorSpaces()

    def blendMode(self, operation):
        return self.b.blendMode(operation)

    def fill(self, c):
        """Sets the global fill color.

        >>> from pagebot.toolbox.color import color
        >>> from pagebot import getContext
        >>> context = getContext()
        >>> context.newPage(420, 420)
        >>> context.fill(color(0.5)) # Same as setFillColor
        >>> context.fill(color('red'))
        >>> context.fill(inheritColor)
        >>> context.fill(noColor)
        >>> context.fill(0.5)
        """
        if c is None:
            c = noColor
        elif isinstance(c, (tuple, list)):
            c = color(*c)
        elif isinstance(c, (int, float)):
            c = color(c)

        msg = 'BaseContext.fill: %s should be of type Color'
        assert isinstance(c, Color), (msg % c)

        if c is inheritColor:
            # Keep color setting as it is.
            pass
        elif c is noColor:
            self.b.fill(None) # Set color to no-color
        elif c.isCmyk:
            # DrawBot.fill has slight API differences compared to
            # FormattedString fill().
            c_, m_, y_, k_ = c.cmyk
            self.b.cmykFill(c_, m_, y_, k_, alpha=c.a)
        else:
            # DrawBot.fill has slight API differences compared to
            # FormattedString fill(). Convert to RGB, whatever the color type.
            r, g, b = c.rgb
            self.b.fill(r, g, b, alpha=c.a)

    setFillColor = fill

    def stroke(self, c, w=0.5):
        """Set the color for global or the color of the formatted string.

        >>> from pagebot.toolbox.color import color
        >>> from pagebot import getContext
        >>> context = getContext()
        >>> context.newPage(420, 420)
        >>> context.stroke(color(0.5)) # Same as setStrokeColor
        >>> context.stroke(color('red'))
        >>> context.stroke(inheritColor)
        >>> context.stroke(noColor)
        >>> context.stroke(0.5)
        """
        if c is None:
            c = noColor
        elif isinstance(c, (tuple, list)):
            c = color(*c)
        elif isinstance(c, (int, float)):
            c = color(c)

        msg = 'BaseContext.stroke: %s should be of type Color'
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

    setStrokeColor = stroke

    def shadow(self, eShadow):
        """Set the graphics state for shadow if parameters are set."""
        if eShadow is not None and eShadow.offset is not None:
            if eShadow.color.isCmyk:
                self.b.shadow(upt(eShadow.offset), # Convert units to values
                              blur=upt(eShadow.blur),
                              color=color(eShadow.color).cmyk)
            else:
                self.b.shadow(upt(eShadow.offset),
                              blur=upt(eShadow.blur),
                              color=color(eShadow.color).rgb)

    setShadow = shadow

    def resetShadow(self):
        pass

    def gradient(self, gradient, origin, w, h):
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

    setGradient = gradient

    def linearGradient(self, startPoint=None, endPoint=None, colors=None,
            locations=None):
        return self.b.linearGradient(startPoint=startPoint, endPoint=endPoint,
                color=colors, locations=locations)

    def radialGradient(self, startPoint=None, endPoint=None, colors=None,
            locations=None, startRadius=0, endRadius=100):
        return self.b.radialGradient(startPoint=startPoint, endPoint=endPoint,
                colors=colors, locations=locations, startRadius=startRadius,
                endRadius=endRadius)

    cmykFill = fill
    cmykStroke = stroke
    cmykShadow = shadow
    cmykLinearGradient = linearGradient
    cmykRadialGradient = radialGradient

    # Path drawing behavior.

    def strokeWidth(self, w):
        """Sets the current stroke width."""

    setStrokeWidth = strokeWidth

    def miterLimit(self, value):
        pass

    def lineJoin(self, value):
        pass

    def lineCap(self, value):
        """Possible values are butt, square and round."""

    def lineDash(self, value):
        """LineDash is None or a list of dash lengths."""

    # Scale.

    def getScaledWH(self, w, h):
        """Scales width and height according to previously set scale."""
        return w * self._sx, h * self._sy

    # Transformations.

    def translatePoint(self, p):
        """Simpler function to translate a point based on origin coordinates
        (`self._ox` and `self._oy`).

        TODO: merge with getTransformed.
        """
        x, y = point2D(upt(p))
        x = self._ox + x

        '''Because the origin is at the bottom, like in DrawBot and as opposed
        to Flat, we need to subtract all vertical coordinates from the page
        height before an object gets placed. In case of (bounding) boxes, we
        also need to subtract the box height.'''
        y = self.height - (self._oy + y)
        return upt(x, y)

    def transform(self, matrix, center=(0, 0)):
        """Transform canvas over matrix t, e.g. (1, 0, 0, 1, dx, dy) to shift
        over vector (dx, dy)"""
        self.b.transform(matrix, center=center)

    def translate(self, x=0, y=0):
        """Translate the origin to this point."""
        xpt, ypt = point2D(upt(x, y))
        self.b.translate(xpt, ypt)

    def rotate(self, angle, center=None):
        """Rotate the canvas by angle. If angle is not a units.Angle instance,
        then convert.

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> context.newPage(420, 420)
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

    def scale(self, sx=1, sy=None, center=(0, 0)):
        """Sets the drawing scale."""
        if isinstance(sx, (tuple, list)):
            assert len(sx) in (2, 3)
            sx, sy = sx[0], sx[1] # FIXME: where are sz and s?

        if sy is None:
            sy = sx

        msg = 'DrawBotContext.scale: Values (%s, %s) must all be of numbers'
        assert isinstance(sx, (int, float)) and isinstance(sy, (int, float)), (msg % (sx, sy))
        self.b.scale(sx, sy, center=center)

    def skew(self, angle1, angle2=0, center=(0, 0)):
        return self.b.skew(angle1, angle2=angle2, center=center)

    # Font.

    def font(self, fontName, fontSize=None):
        """Tries to find a PageBot font based on name, else assumes it is a
        system font. Also optionally sets fontSize unit to value."""
        font = findFont(fontName)

        if font:
            self.b.font(font.path)
        else:
            self.b.font(fontName)

        if fontSize is not None:
            self.fontSize(fontSize)

    def fallbackFont(self, fontName):
        return self.b.fallbackFont(fontName)

    def fontSize(self, fontSize):
        """Sets the font size in the context.

        >>> from pagebot.toolbox.units import pt
        >>> from pagebot import getContext
        >>> context = getContext()
        >>> context.newPage(420, 420)
        >>> context.fontSize(pt(12))
        """
        fspt = upt(fontSize)
        self._fontSize = fspt
        self.b.fontSize(fspt) # Render fontSize unit to value

    # Babelstring

    def asBabelString(self, s, style=None):
        """Converts  another string based class to BabelString."""
        if isinstance(s, str):
            # Creates a new string with default styles.
            style = makeStyle(style=style)
            bs = self.newString(s, style=style)
            return bs
        else:
            raise PageBotFileFormatError('type is %s' % type(bs))

    # ...

    def lineHeight(self, value):
        return self.b.lineHeight(value)

    def tracking(self, value):
        return self.b.tracking(value)

    def baselineShift(self, value):
        return self.b.baselineShift(value)

    def underline(self, value):
        return self.b.underline(value)

    def hyphenation(self, onOff):
        """DrawBot needs an overall hyphenation flag set on / off, as it is not
        part of the FormattedString style attributes."""
        assert isinstance(onOff, bool)
        self._hyphenation = onOff
        self.b.hyphenation(onOff)

    def tabs(self, *tabs):
        return self.b.tabs(*tabs)

    def language(self, language):
        """DrawBot needs an overall language flag set to code, it is not a
        FormattedString style attribute. For available ISO language codes, see
        pagebot.constants."""
        # TODO: assert language is correct
        self.b.language(language)

    def listLanguages(self):
        return self.b.listLanguages()

    # Features.

    def openTypeFeatures(self, features):
        """Enables OpenType features and returns the current openType features
        settings. If no arguments are given `openTypeFeatures()` will just
        return the current openType features settings.

        NOTE: signature differs from DrawBot:

        ``def openTypeFeatures(self, *args, **features):``
        """
        #raise NotImplementedError

    def listOpenTypeFeatures(self, fontName=None):
        """Answers the list of opentype features available in the named
        font."""
        #raise NotImplementedError

    def fontVariations(self, *args, **axes):
        pass
        #raise NotImplementedError

    def listFontVariations(self, fontName=None):
        pass
        #raise NotImplementedError

    # Text.

    def drawString(self, bs, p):
        """Draws the BabelString at position p.

        >>> from pagebot.contexts import getContext
        >>> from pagebot.toolbox.units import pt, em
        >>> from pagebot.document import Document
        >>> from pagebot.elements import *
        >>> context = getContext()
        >>> style = dict(font='PageBot-Regular', fontSize=pt(100), leading=em(1))
        >>> bs = BabelString('Hkpx'+chr(10)+'Hkpx', style, context=context)
        >>> context.drawString(bs, pt(100, 100))
        """

        if not isinstance(bs, BabelString):
            try:
                bs = self.asBabelString(bs)
            except TypeError as e:
                print('TypeError: %s is not a string compatible type, %s' % (type(bs), e))
                return

        if bs._w is None and bs._h is None:
            x, y = p
            p = (pt(x), pt(y))
            self.text(bs, p)
        else:
            x, y = p
            x = pt(x)
            y = pt(y)
            # x, y = point2D(upt(p))
            box = (x, y, bs.w or DEFAULT_WIDTH, bs.h or 1000)
            self.textBox(bs, box)

    def drawText(self, bs, box):
        """Draws the text block, in case a width or height is defined."""
        assert isinstance(bs, BabelString),\
            'drawText needs a BabelString: %s' % (bs.__class__.__name__)
        _, _, w, h = box
        if bs.w is None:
            bs.w = w
        if bs.h is None:
            bs.h = h

        self.textBox(bs, upt(box))

    def textOverflow(self, lines, h, align=None):
        """Answers the part of the text that doesn't fit in the box.

        >>> from pagebot.toolbox.loremipsum import loremIpsum
        >>> from pagebot.toolbox.units import pt
        >>> from pagebot import getContext
        >>> context = getContext()
        >>> style = dict(font='PageBot-Regular', fontSize=pt(24))
        >>> bs = context.newString(loremIpsum(), style, w=pt(400))
        >>> bs.w
        400pt
        >>> lines = bs.lines # Same as context.textLines(bs.cs, bs.w)
        """
        """
        >>> len(lines)
        144
        >>> len(context.textOverflow(lines, h=None))
        144
        >>> of = context.textOverflow(lines, h=pt(100))
        >>> of[1]
        <BabelLineInfo x=0pt y=24pt runs=1>
        """
        if h is None:
            return lines

        overflow = []
        if lines:
            originY = lines[0].y

        for line in lines:
            y = line.y - originY
            if y > h:
                break
            line.y -= originY
            overflow.append(line)

        return overflow

    def getBaselines(self, bs, w=None, h=None):
        """Answers the dictionary of baseline positions, relative
        to the firstline. If @h is defined, the clip on the height.


        See also doctests/string*.txt.
        """
        if h is None:
            h = XXXL

        baselines = {}

        if w is not None:
            lines = self.getTextLines(bs, w, h=h)
        else:
            lines = bs.lines

        if lines:
            y = lines[0].y

        for lineInfo in lines:
            if lineInfo.y - y > h:
                break
            baselines[upt(lineInfo.y - y)] = lineInfo

        return baselines

    # String.

    def newString(self, bs=None, style=None, w=None, h=None):
        """Creates a new BabelString instance from `bs` (converted to plain
        unicode string), using style as typographic parameters or `e` as
        cascading style source.  Ignore and just answer `bs` if it is already a
        BabelString instance and no style is forced. PageBot function.

        >>> from pagebot.toolbox.units import pt
        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> bs = context.newString('ABCD', dict(fontSize=pt(12)))
        >>> bs, bs.__class__.__name__
        ($ABCD$, 'BabelString')
        """
        style = makeStyle(style=style)
        if not bs:
            bs = ''
        if not isinstance(bs, BabelString):
            # Otherwise convert bs into a BabelString, from whatever it is now.
            # Set the babelString.context as self.
            bs = BabelString(bs, style=style, w=w, h=h, context=self)
        assert isinstance(bs, BabelString)
        return bs

    def newBulletString(self, bullet, style=None):
        return self.newString(bullet, style=style)

    # Images.

    def image(self, path, p, alpha=1, pageNumber=None, w=None, h=None,
            scaleType=None, clipPath=None):
        # TODO: implement clipPath.
        return self.b.image(path, p, alpha=alpha, pageNumber=pageNumber, w=w,
                h=h, scaleType=scaleType)

    '''
    Should be same as pageCount().

    def numberOfPages(self, path):
        """Answer the number of pages, if the image paths points to a PDF.
        https://www.journaldev.com/33281/pypdf2-python-library-for-pdf-files

        >>> from pagebot.contexts import getContext
        >>> from pagebot.document import Document
        >>> from pagebot.toolbox.transformer import path2Dir
        >>> context = getContext()
        >>> doc = Document(w=100, h=100, context=context, autoPages=12)
        >>> filePath = '_export/TestPDFPages.pdf'
        >>> doc.export(filePath)
        >>> context.numberOfPages(filePath)
        12
        """
        if path.lower().endswith('.'+FILETYPE_PDF):
            with open(path, 'rb') as f:
                pdf = PdfFileReader(f)
                information = pdf.getDocumentInfo()
                return pdf.getNumPages()
        return None
    '''

    def imageSize(self, path, index=0):
        """Answer the images size of path.

        >>> from pagebot.contexts import getContext
        >>> from pagebot.document import Document
        >>> from pagebot.filepaths import getResourcesPath
        >>> #from pagebot.toolbox.transformer import path2Dir
        >>> context = getContext()
        >>> #doc = Document(w=123, h=345, context=context, autoPages=1)
        >>> resourcesPath = getResourcesPath()
        >>> path = resourcesPath + '/images/cookbot1.jpg'
        >>> context.imageSize(path)
        (1376pt, 1350pt)
        >>> path = resourcesPath + '/templates/test.pdf'
        >>> context.imageSize(path)
        (400pt, 200pt)
        """
        extension = path2Extension(path)

        if extension == FILETYPE_PDF:
            im = PdfFileReader(open(path, 'rb'))
            r = im.getPage(0).mediaBox # RectangleObject([0, 0, w, h])
            w = float(r.getWidth())
            h = float(r.getHeight())
            return pt(w, h)
        elif extension == FILETYPE_SVG:
            svgTree = ET.parse(path)
            # FIXME: Answer the real size from the XML tree
            return pt(1000, 1000)

        elif self.hasPIL:
            # Using Pillow for other image formats.
            # TODO: check compatible formats first.
            image = Image.open(path)
            return pt(image.size)
        else:
            return None

    def imagePixelColor(self, path, p):
        return self.b.imagePixelColor(path, p)

    # Some drawing macros.

    def marker(self, x, y, r=1, fontSize=5, prefix=None, color=None):
        # TODO: move to elements.
        x = round(x)
        y = round(y)
        red = (1, 0, 0)
        s = '(%s, %s)' % (x, y)

        if prefix:
            s = '%s %s' % (prefix, s)

        if color is None:
            color = red

        style = dict(font='PageBot-Regular', fontSize=pt(fontSize), textFill=color)
        bs = self.newString(s, style=style)
        oldStroke = self._stroke
        oldFill = self._fill
        self.text(bs, (x+1, y+1))
        self.fill(color)
        self.stroke(None)
        self.circle(x, y, r)
        self.fill(oldFill)
        self.stroke(oldStroke)

    def bluntCornerRect(self, x, y, w, h, offset=5):
        """Draws a rectangle in the canvas. This method is using the Bézier
        path to draw on.

        TODO: move to elements.

        >>> from pagebot import getContext
        >>> context = getContext()
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
        """Draw a rectangle in the canvas. This method is using the Bézier path
        as path to draw on.

        TODO: move to elements.

        >>> from pagebot import getContext
        >>> context = getContext()
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

    # Mov.

    def frameDuration(self, secondsPerFrame, **kwargs):
        """Set the self._frameDuration for animated GIFs to a number of seconds
        per frame. Used when initializing a new page."""
        self.b.frameDuration(secondsPerFrame or DEFAULT_FRAME_DURATION)

    # PDF links.

    def linkDestination(self, name, x=None, y=None):
        return self.b.linkDestination(name, x=x, y=y)

    def linkRect(self, name, xywh):
        return self.b.linkRect(name, xywh)

    # System fonts listing, installation, font properties.

    def installedFonts(self, patterns=None):
        """Should Answer the list of all fonts (name or path) that are
        installed on the OS."""
        self.b.installedFonts(patterns=patterns)

    def installFont(self, fontOrName):
        """Should install the font in the context. fontOrName can be a Font
        instance (in which case the path is used) or a full font path."""
        self.b.installFont(fontOrName)

    def uninstallFont(self, fontOrName):
        self.b.uninstallFont(fontOrName)

    def fontContainsCharacters(self, characters):
        return self.b.fontContainsCharacters(characters)

    def fontContainsGlyph(self, glyphName):
        return self.b.fontContainsGlyph(glyphName)

    def fontFilePath(self):
        return self.b.fontFilePath()

    def listFontGlyphNames(self):
        return self.b.listFontGlyphNames()

    def fontAscender(self):
        return self.b.fontAscender()

    def fontDescender(self):
        return self.b.fontDescender()

    def fontXHeight(self):
        return self.b.fontXHeight()

    def fontCapHeight(self):
        return self.b.fontCapHeight()

    def fontLeading(self):
        return self.b.fontLeading()

    def fontLineHeight(self):
        return self.b.fontLineHeight()

    #

    def BezierPath(self, path=None, glyphSet=None):
        # FIXME: should be basecontext BezierPath instead.
        return self.b.BezierPath(path=path, glyphSet=glyphSet)

    def ImageObject(self, path=None):
        """Answers an ImageObject that knows about image filters.

        >>> from pagebot import getContext
        >>> from pagebot.filepaths import getResourcesPath
        >>> context = getContext()
        >>> path = getResourcesPath() + '/images/peppertom.png'
        >>> #imo = context.getImageObject(path)
        """

    getImageObject = ImageObject

    # Glyphs.

    def drawGlyph(self, glyph, x, y, fill=noColor, stroke=noColor,
            strokeWidth=0, fontSize=None, xTextAlign=LEFT):
        """Draw the font[glyphName] at the defined position with the defined
        fontSize."""
        font = glyph.font

        if fontSize is None:
            fontSize = font.info.unitsPerEm
        s = fontSize / font.info.unitsPerEm

        if xTextAlign == CENTER:
            x -= (glyph.width or 0) / 2*s
        elif xTextAlign == RIGHT:
            x -= glyph.width*s

        #self.save()
        self.fill(fill)
        self.stroke(stroke, w=strokeWidth)
        self.translate(x, y)
        self.scale(s)
        self.drawGlyphPath(glyph)
        self.scale(1/s)
        self.translate(-x, -y)
        #self.restore()


    def drawGlyphPath(self, glyph):
        """Converts the cubic commands to a drawable path."""
        path = self.getGlyphPath(glyph)
        self.drawPath(path)

    def getGlyphPath(self, glyph, p=None, path=None):
        """PageBot function."""
        raise NotImplementedError

    def intersectGlyphWithCircle(self, glyph, m, r, spokes=16):
        mx, my = m
        lines = []
        angle = radians(360/spokes)
        p1 = None
        for n in range(spokes+1):
            p = mx + cos(angle*n)*r, my + sin(angle*n)*r
            if p1 is not None:
                lines.append((p1, p))
            p1 = p
        return self.intersectGlyphWithLines(glyph, lines)

    def intersectGlyphWithLines(self, glyph, lines):
        intersections = set()
        glyphPath = self.getGlyphPath(glyph)
        for line in lines:
            points = self.intersectPathWithLine(glyphPath, line)
            if points is not None:
                intersections = intersections.union(points)
        return intersections

    def intersectGlyphWithLine(self, glyph, line):
        """Answers the sorted set of intersecting points between the straight
        line and the flatteded glyph path."""
        glyphPath = self.getGlyphPath(glyph)
        return self.intersectPathWithLine(glyphPath, line)

    def intersectPathWithLine(self, path, line):
        intersections = set() # As set,  make sure to remove any doubles.

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        contours = self.getFlattenedContours(path)

        if not contours:
            # Could not generate path or flattenedPath. Or there are no
            # contours. Give up.
            return None

        (lx0, ly0), (lx1, ly1) = line
        maxX = round(max(lx0, lx1))
        minX = round(min(lx0, lx1))
        maxY = round(max(ly0, ly1))
        minY = round(min(ly0, ly1))

        for contour in contours:
            for n, _ in enumerate(contour):
                pLine = contour[n], contour[n-1]
                (px0, py0), (px1, py1) = pLine
                if minY > round(max(py0, py1)) or maxY < round(min(py0, py1)) or \
                        minX > round(max(px0, px1)) or maxX < round(min(px0, px1)):
                    continue # Skip if boundings boxes don't overlap.

                xdiff = lx0 - lx1, px0 - px1
                ydiff = ly0 - ly1, py0 - py1

                div = det(xdiff, ydiff)
                if div == 0:
                   continue # No intersection

                # Calculate the intersection
                d = det(*line), det(*pLine)
                ix = det(d, xdiff) / div
                iy = det(d, ydiff) / div

                # Determine is the intersection points is indeed part of the line segment
                if (round(lx0) <= round(ix) <= round(lx1) or round(lx1) <= round(ix) <= round(lx0)) and\
                   (round(ly0) <= round(iy) <= round(ly1) or round(ly1) <= round(iy) <= round(ly0)):
                    intersections.add((ix, iy))

        # Answer the set as sorted list, increasing x, from left to right.
        return sorted(intersections)

    def getFlattenedPath(self, path=None):
        raise NotImplementedError

    def getFlattenedContours(self, path=None):
        raise NotImplementedError

    def onBlack(self, p, path=None):
        """Should answers if the single point (x, y) is on black."""

    # File export.

    def checkExportPath(self, path):
        """If the path starts with "_export" make sure it exists, otherwise
        create it. The _export folders are used to export documents locally,
        without saving them to git. The _export name is included in the git
        .gitignore file. PageBot function.

        >>> context = BaseContext()
        >>> context.checkExportPath('_export/myFile.pdf')
        >>> os.path.exists('_export')
        True
        """
        if path.startswith('_export'):
            dirPath = '/'.join(path.split('/')[:-1])

            if not os.path.exists(dirPath):
                os.makedirs(dirPath)

    # User interface.

    def screenSize(self):
        """Answers the current screen size. PageBot function."""

    def Variable(self, variables, workSpace):
        """Offers interactive global value manipulation. Requires access to a
        UI toolkit sush as Cocoa or QT. Can be ignored in most contexts except
        DrawBot for now.  """

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
