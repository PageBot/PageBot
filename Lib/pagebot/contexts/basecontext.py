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
from math import radians, sin, cos

from pagebot.paths import DEFAULT_FONT_PATH
from pagebot.constants import (DISPLAY_BLOCK, DEFAULT_FRAME_DURATION,
        DEFAULT_FONT_SIZE, DEFAULT_LANGUAGE, FILETYPE_SVG)
from pagebot.toolbox.units import upt, pt, point2D, Angle, Pt
from pagebot.toolbox.color import color, noColor, Color, inheritColor, blackColor
from pagebot.contexts.abstractdrawbotcontext import AbstractDrawBotContext

class BaseContext(AbstractDrawBotContext):
    """Base API for all contexts. Extends the DrawBot interface.
    """
    # Indication to Typesetter that by default tags should not be included in
    # output.
    useTags = False

    # To be redefined by inheriting context classes.
    STRING_CLASS = None
    EXPORT_TYPES = None

    def __init__(self):
        # Holds current open Bézier path.
        self._path = None

        self._fill = blackColor
        self._stroke = noColor
        self._strokeWidth = 0
        self._textFill = blackColor
        self._textStroke = noColor
        self._textStrokeWidth = 0
        self._font = DEFAULT_FONT_PATH
        self._fontSize = DEFAULT_FONT_SIZE
        self._frameDuration = 0

        # Origin set by self.translate()
        self._ox = pt(0)
        self._oy = pt(0)
        self._rotationCenter = (0, 0)
        self._rotate = 0
        self._hyphenation = True
        self._language = DEFAULT_LANGUAGE
        self._openTypeFeatures = None # FIXME: what type?

        # Stack of graphic states.
        self._gState = []

        self.doc = None

        self.page = None
        self._pages = []
        self.style = None
        self.units = Pt.UNIT

    def __repr__(self):
        return '<%s>' % self.name

    def _get_pages(self):
        return self._pages
    pages = property(_get_pages)

    def _get_language(self):
        return self._language
    def _set_language(self, language):
        self._language = language or DEFAULT_LANGUAGE
    language = property(_get_language, _set_language)

    def _get_path(self):
        """Answers the open drawing self._path. Creates one if it does not
        exist.

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> path = context.path
        >>> path is not None
        True
        >>> path.moveTo((0, 0))
        >>> path.lineTo((100, 100)) # Adding 2 points
        >>> len(context.path.points)
        2
        """
        if self._path is None:
            self._path = self.newPath()
        return self._path

    path = property(_get_path)

    # Documents.

    def newDocument(self, w, h):
        """PageBot function."""
        pass

    def saveDocument(self, path, multiPage=None):
        """PageBot function."""
        pass

    def newDrawing(self):
        """Clear output canvas, start new export file. DrawBot function.

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> context.newDrawing()
        """
        self.b.newDrawing()

    def endDrawing(self):
        pass

    # Magic variables.

    def width(self):
        return self.b.width()

    def height(self):
        return self.b.height()

    def sizes(self, paperSize=None):
        return self.b.sizes(paperSize=paperSize)

    def pageCount(self):
        return self.b.pageCount()

    # Public callbacks.

    def size(self, width, height=None):
        return self.b.size(width, height=height)

    def newPage(self, w, h):
        """Creates a new drawbot page.

        >>> from pagebot.toolbox.units import px
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> context.newPage(pt(100), pt(100))
        >>> context.newPage(100, 100)
        """
        wpt, hpt = upt(w, h)
        self.b.newPage(wpt, hpt)

    def saveImage(self, path, *args, **options):
        return self.b.saveImage(path, *args, **options)

    def printImage(self, pdf=None):
        return self.b.printImage(pdf=pdf)

    def pdfImage(self):
        return self.b.pdfImage()

    # Graphics state.

    def save(self):
        self.b.save()

    saveGraphicState = save

    def restore(self):
        self.b.restore()

    restoreGraphicState = restore

    def savedState(self):
        return self.b.savedState()

    # Basic shapes.

    def rect(self, x, y, w, h):
        """Draws a rectangle in the canvas. This method is using the core
        BezierPath as path to draw on. For a more rich environment use
        PageBotPath(context) instead.

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> context.rect(pt(0), pt(0), pt(100), pt(100))
        >>> context.rect(0, 0, 100, 100)
        """
        xpt, ypt, wpt, hpt = upt(x, y, w, h)
        # Render units to points for DrawBot.
        self.b.rect(xpt, ypt, wpt, hpt)

    def oval(self, x, y, w, h):
        """Draw an oval in rectangle where (x,y) is the bottom-left and size
        (w,h).  This method uses BezierPath; for a more rich environment use
        PageBotPath(context) instead.

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> context.oval(pt(0), pt(0), pt(100), pt(100))
        >>> context.oval(0, 0, 100, 100)
        """
        xpt, ypt, wpt, hpt = upt(x, y, w, h)
        self.b.oval(xpt, ypt, wpt, hpt) # Render units to points for DrawBot.

    def circle(self, x, y, r):
        """Circle draws a DrawBot oval with (x,y) as middle point and radius r.
        This method is using the core BezierPath as path to draw on. For a more rich
        environment use PageBotPath(context) instead. PageBot function.

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> context.circle(pt(100), pt(200), pt(50))
        >>> context.circle(100, 200, 50)
        """
        xpt, ypt, rpt = upt(x, y, r)
        self.b.oval(xpt-rpt, ypt-rpt, 2*rpt, 2*rpt) # Render units to points for DrawBot.

    def roundedRect(self, x, y, w, h, offset=25):
        return self.b.roundedRect(x, y, w, h, offset=offset)

    def bluntCornerRect(self, x, y, w, h, offset=5):
        return self.b.bluntCornerRect(x, y, w, h, offset=offset)

    # Path.

    def newPath(self):
        """Makes a new Bezierpath to draw in and answers it. This will not
        initialize self._path, which is accessed by the property self.path.
        This method is using the BezierPath as path to draw on. For a more
        rich environment use PageBotPath(context) instead. PageBot function.

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> context.newPath()
        <BezierPath>
        """
        return self.b.BezierPath()

    def moveTo(self, p):
        """Move to point `p` in the open path. Create a new self._path if none
        is open.

        >>> from pagebot.toolbox.units import pt
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> context.moveTo(pt(100, 100))
        >>> context.moveTo((100, 100))
        >>> # Drawing on a separate path
        >>> path = context.newPath()
        >>> path.moveTo(pt(100, 100))
        >>> path.curveTo(pt(100, 200), pt(200, 200), pt(200, 100))
        >>> path.closePath()
        >>> context.drawPath(path)
        """
        ppt = upt(point2D(p))
        self.path.moveTo(ppt) # Render units point tuple to tuple of values

    def lineTo(self, p):
        """Line to point p in the open path. Create a new self._path if none
        is open.

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> # Create a new self._path by property self.path
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
        ppt = upt(point2D(p))
        self.path.lineTo(ppt) # Render units point tuple to tuple of values

    def curveTo(self, bcp1, bcp2, p):
        """Curve to point p i nthe open path. Create a new path if none is
        open.

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> # Create a new self._path by property self.path
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
        self.path.curveTo(b1pt, b2pt, ppt) # Render units tuples to value tuples

    def qCurveTo(self, *points):
        return self.b.qCurveTo(*points)

    def arc(self, center, radius, startAngle, endAngle, clockwise):
        return self.b.arc(center, radius, startAngle, endAngle, clockwise)

    def arcTo(self, xy1, xy2, radius):
        return self.b.arcTo(xy1, xy2, radius)

    def closePath(self):
        """Closes the open path if it exists, otherwise ignore it.
        PageBot function.

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> # Create a new self._path by property self.path
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
        if self._path is not None: # Only if there is an open path.
            self._path.closePath()

    def drawPath(self, path=None, p=None, sx=1, sy=None, fill=None,
            stroke=None, strokeWidth=None):
        """Draws the BezierPath. Scaled image is drawn on (x, y), in that order.
        Use self._path if path is omitted. PageBot function.

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> context.newDrawing()
        >>> context.newPage(420, 420)
        >>> len(context.path.points) # Property self.path creates a self._path BezierPath
        0
        >>> context.moveTo((10, 10)) # moveTo and lineTo are drawing on context._path
        >>> context.lineTo((110, 10))
        >>> context.lineTo((110, 110))
        >>> context.lineTo((10, 110))
        >>> context.lineTo((10, 10))
        >>> context.closePath()
        >>> context.oval(160-50, 160-50, 100, 100) # Oval and rect don't draw on self._path
        >>> len(context.path.points)
        6
        >>> context.fill((1, 0, 0))
        >>> context.drawPath(p=(0, 0)) # Draw self._path with various offsets
        >>> context.drawPath(p=(200, 200))
        >>> context.drawPath(p=(0, 200))
        >>> context.drawPath(p=(200, 0))
        >>> context.saveImage('_export/DrawBotContext1.pdf')
        >>> # Drawing directly on a path, created by context
        >>> path = context.newPath() # Leaves current self._path untouched
        >>> len(path.points)
        0
        >>> path.moveTo((10, 10)) # Drawing on context._path
        >>> path.lineTo((110, 10))
        >>> path.lineTo((110, 110))
        >>> path.lineTo((10, 110))
        >>> path.lineTo((10, 10))
        >>> path.closePath()
        >>> path.oval(160-50, 160-50, 100, 100) # path.oval does draw directly on the path
        >>> len(path.points)
        19
        >>> context.fill((0, 0.5, 1))
        >>> context.drawPath(path, p=(0, 0)) # Draw self._path with various offsets
        >>> context.drawPath(path, p=(200, 200))
        >>> context.drawPath(path, p=(0, 200))
        >>> context.drawPath(path, p=(200, 0))
        >>> context.saveImage('_export/DrawBotContext2.pdf')
        """
        if path is None:
            path = self.path
        if hasattr(path, 'bp'): # If it's a PageBotPath, get the core BezierPath
            bezierPath = path.bp
            # If not forced as attribute, then try to get from the PageBotPath.style
            if fill is None:
                fill = path.style.get('fill')
            if stroke is None:
                stroke = path.style.get('stroke')
            if strokeWidth is None:
                stroke = path.style.get('strokeWidth')
        else:
            bezierPath = path # Otherwise we assume it is a context core BezierPath instance

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
        # Otherwise ignore and use the setting as defined already in the graphic state.
        if fill is not None:
            self.fill(color(fill))
        if stroke is not None and strokeWidth:
            self.stroke(color(stroke), upt(strokeWidth))
        self.b.drawPath(bezierPath)
        self.restore()

    def clipPath(self, clipPath):
        """Sets the clipPath of the DrawBot builder in a new saved graphics
        state. Clip paths cannot be restored, so they should be inside a
        context.save() and context.restore().

        TODO: add unit tests.
        """
        self.b.clipPath(clipPath)

    def line(self, p1, p2):
        """Draw a line from p1 to p2. This method is using the core BezierPath
        as path to draw on. For a more rich ennvironment use
        PageBotPath(context).

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> context.line(pt(100, 100), pt(200, 200))
        >>> context.line((100, 100), (200, 200))
        """
        p1pt = upt(point2D(p1))
        p2pt = upt(point2D(p2))
        self.b.line(p1pt, p2pt) # Render tuple of units point

    def polygon(self, *points, **kwargs):
        return self.b.polygon(*points, **kwargs)

    def quadTo(self, bcp, p):
        # TODO: Convert to Bezier with 0.6 rule
        # What's difference with qCurveTo()?
        return self.b.quadTo(bcp, p)

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
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
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
            c, m, y, k = c.cmyk
            self.b.cmykFill(c, m, y, k, alpha=c.a)
        else:
            # DrawBot.fill has slight API differences compared to
            # FormattedString fill(). Convert to RGB, whatever the color type.
            r, g, b = c.rgb
            self.b.fill(r, g, b, alpha=c.a)

    setFillColor = fill

    def stroke(self, c, w=None):
        """Set the color for global or the color of the formatted string.

        >>> from pagebot.toolbox.color import color
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
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

    # Path drawing behavior.

    def strokeWidth(self, w):
        """Set the current stroke width.

        >>> from pagebot.toolbox.units import pt, mm
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> context.setStrokeWidth(pt(0.5))
        >>> context.setStrokeWidth(mm(0.5))
        """
        wpt = upt(w)
        self.b.strokeWidth(wpt)

    setStrokeWidth = strokeWidth

    def miterLimit(self, value):
        self.b.miterLimit(value)

    def lineJoin(self, value):
        self.b.lineJoin(value)

    def lineCap(self, value):
        """Possible values are butt, square and round."""
        assert value in ('butt', 'square', 'round')
        self.b.lineCap(value)

    def lineDash(self, value):
        """LineDash is None or a list of dash lengths."""
        if value is None:
            self.b.lineDash(None)
        else:
            self.b.lineDash(*value)

    # Transform.

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

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
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

    # Text.

    def font(self, fontName, fontSize=None):
        # FIXME: fontSize?
        self.b.font(fontName)

        # Also renders fontSize unit to value.
        if fontSize is not None:
            fspt = upt(fontSize)
            self.b.fontSize(fspt)

    def fallbackFont(self, fontName):
        return self.b.fallbackFont(fontName)

    def fontSize(self, fontSize):
        """Set the font size in the context.

        >>> from pagebot.toolbox.units import pt
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> context.fontSize(pt(12))
        """
        fspt = upt(fontSize)
        self.b.fontSize(fspt) # Render fontSize unit to value

    def lineHeight(self, value):
        return self.b.lineHeight(value)

    def tracking(self, value):
        return self.b.tracking(value)

    def baselineShift(self, value):
        return self.b.baselineShift(value)

    def underline(self, value):
        return self.b.underline(value)

    def hyphenation(self, onOff):
        """DrawBot needs an overall hyphenation flag set on/off, as it is not
        part of the FormattedString style attributes."""
        assert isinstance(onOff, bool)
        self._hyphenation = onOff
        self.b.hyphenation(onOff)

    def tabs(self, *tabs):
        return self.b.tabs(*tabs)

    def language(self, language):
        """DrawBot needs an overall language flag set to code, it is not
        a FormattedString style attribute. For available ISO
        language codes, see pagebot.constants."""
        # TODO: assert language is correct
        self.b.language(language)

    def listLanguages(self):
        return self.b.listLanguages()

    def openTypeFeatures(self, features):
        """Set the current of opentype features in the context canvas.

        NOTE: signature differs from DrawBot:

            def openTypeFeatures(self, *args, **features):

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> context.openTypeFeatures(dict(smcp=True, zero=True))
        """
        self.b.openTypeFeatures(**features)

    def listOpenTypeFeatures(self, fontName=None):
        """Answers the list of opentype features available in the named font."""
        return self.b.listOpenTypeFeatures(fontName)

    def fontVariations(self, *args, **axes):
        return self.b.fontVariations(*args, **axes)

    def listFontVariations(self, fontName=None):
        return self.b.listFontVariations(fontName=fontName)

    # Drawing text.

    def text(self, sOrBs, p):
        """Draw the sOrBs text string, can be a str or BabelString, including a
        DrawBot FormattedString at position p.

        NOTE: signature differs from DrawBot.
        """
        if not isinstance(sOrBs, str):
            sOrBs = sOrBs.s # Assume here is's a BabelString with a FormattedString inside.
        ppt = point2D(upt(p))
        self.b.text(sOrBs, ppt) # Render point units to value tuple

    def textOverflow(self, sOrBs, box, align=None):
        """Answer the overflow text if flowing it in the box. The sOrBs can be a
        plain string or a BabelString instance. In case a plain string is given
        then the current font/fontSize/etc. settings of the builder are used.

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> context.font('Verdana')
        >>> context.fontSize(12)
        >>> box = 0, 0, 100, 100
        >>> len(context.textOverflow('AAA ' * 200, box))
        728
        >>> style = dict(font='Verdana', fontSize=12)
        >>> bs = context.newString('AAA ' * 200, style=style)
        >>> len(context.textOverflow(bs, box))
        740
        """
        if isinstance(sOrBs, str):
            return self.b.textOverflow(sOrBs, box, align=align) # Plain string

        # Assume here it's a BabelString with a FormattedString inside
        overflow = self.b.textOverflow(sOrBs.s, box, align=align)
        bs = self.newString('')
        bs.s = overflow
        return bs

    def textBox(self, sOrBs, r=None, clipPath=None, align=None):
        """Draw the sOrBs text string, can be a str or BabelString, including a
        DrawBot FormattedString in rectangle r.

        NOTE: signature differs from DrawBot.

        >>> from pagebot.toolbox.units import pt
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> context.textBox('ABC', (10, 10, 200, 200))
        """
        if hasattr(sOrBs, 's'):
            sOrBs = sOrBs.s # Assume here is's a BabelString with a FormattedString inside.
        else:
            sOrBs = str(sOrBs) # Otherwise convert to string if it is not already

        if clipPath is not None:
            box = clipPath.bp
            self.b.textBox(sOrBs, clipPath.bp) # Render rectangle units to value tuple
        elif isinstance(r, (tuple, list)):
            # Render rectangle units to value tuple
            box = upt(r)
        else:
            raise ValueError('%s.textBox has no box or clipPath defined' % self.__class__.__name__)
        self.b.textBox(sOrBs, box, align=None)

    def textBoxBaselines(self, txt, box, align=None):
        return self.b.textBoxBaselines(txt, box, align=align)

    def FormattedString(self, *args, **kwargs):
        # Refer to BabelString?
        return self.b.FormattedString(*args, **kwargs)

    def newString(self, s, e=None, style=None, w=None, h=None, pixelFit=True):
        """Creates a new styles BabelString instance of self.STRING_CLASS from
        `s` (converted to plain unicode string), using e or style as
        typographic parameters. Ignore and just answer `s` if it is already a
        self.STRING_CLASS instance and no style is forced. PageBot function.
        """
        from pagebot.style import makeStyle

        # Copies style, check keys.
        style = makeStyle(style=style)
        if not isinstance(s, self.STRING_CLASS):
            # Otherwise convert s into plain string, from whatever it is now.
            s = self.STRING_CLASS.newString(str(s), context=self, e=e,
                    style=style, w=w, h=h, pixelFit=pixelFit)
        assert isinstance(s, self.STRING_CLASS)
        return s

    def newBulletString(self, bullet, e=None, style=None):
        return self.newString(bullet, e=e, style=style)

    def fitString(self, s, e=None, style=None, w=None, h=None, pixelFit=True):
        """Creates a new styles BabelString instance of self.STRING_CLASS from
        s assuming that style['font'] is a Variable Font instnace, or a path
        pointing to one. If the for is not a VF, then behavior is the same as
        newString. (converted to plain unicode string), using e or style as
        typographic parameters. Ignore and just answer s if it is already a
        `self.STRING_CLASS` instance. PageBot function.
        """
        if not isinstance(s, self.STRING_CLASS):
            # Otherwise convert s into plain string, from whatever it is now.
            s = self.STRING_CLASS.fitString(str(s), context=self, e=e, style=style,
                w=w, h=h, pixelFit=pixelFit)
        assert isinstance(s, self.STRING_CLASS)
        return s

    def newText(self, textStyles, e=None, w=None, h=None, newLine=False):
        """Answers a BabelString as a combination of all text and styles in
        textStyles, which is should have format

        [(baseString, style), (baseString, style), ...]

        Add return \n to the string is the newLine attribute is True or if a
        style has

        style.get('display') == DISPLAY_BLOCK

        """
        assert isinstance(textStyles, (tuple, list))
        s = None

        for t, style in textStyles:
            if newLine or (style and style.get('display') == DISPLAY_BLOCK):
                t += '\n'
            bs = self.newString(t, style=style, e=e, w=w, h=h)
            if s is None:
                s = bs
            else:
                s += bs
        return s

    # Images

    def numberOfImages(self, path):
        pass

    def image(self, path, p, alpha=1, pageNumber=None, w=None, h=None):
        return self.b.image(path, p, alpha=alpha, pageNumber=pageNumber, w=w, h=h)

    def imageSize(self, path):
        """Answers the (w, h) image size of the image file at path. If the path is an SVG
        image, then determine by parsing the SVG-XML."""
        if path.lower().endswith('.'+FILETYPE_SVG):
            import xml.etree.ElementTree as ET
            svgTree = ET.parse(path)
            print(svgTree)
            return pt(1000, 1000)

        return pt(self.b.imageSize(path))

    def imagePixelColor(self, path, p):
        return self.b.imagePixelColor(path, p)

    def numberOfPages(self, path):
        return self.b.numberOfPages(path)

    # Mov.

    def frameDuration(self, secondsPerFrame):
        """Set the self._frameDuration for animated GIFs to a number of seconds
        per frame. Used when initializing a new page."""
        self.b.frameDuration(secondsPerFrame or DEFAULT_FRAME_DURATION)

    # PDF links.

    def linkDestination(self, name, x=None, y=None):
        return self.b.linkDestination(name, x=x, y=y)

    def linkRect(self, name, xywh):
        return self.b.linkRect(name, xywh)

    # Helpers.

    def textSize(self, bs, w=None, h=None, align=None):
        """Answers the width and height of the formatted string with an
        optional given w or h."""
        return self.b.textSize(bs.s, width=w, height=h, align=align)

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

    def uninstallFont(self, fontOrName):
        if hasattr(fontOrName, 'path'):
            fontOrName = fontOrName.path
        return self.b.uninstallFont(fontOrName)

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

    def BezierPath(self, path=None, glyphSet=None):
        return self.b.BezierPath(path=path, glyphSet=glyphSet)

    def ImageObject(self, path=None):
        """Answers the ImageObject that knows about image filters. For names
        and parameters of filters see:

        * http://www.drawbot.com/content/image/imageObject.html

        >>> from pagebot import getResourcesPath
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> path = getResourcesPath() + '/images/peppertom_lowres_398x530.png'
        >>> imo = context.getImageObject(path)

        """
        return self.b.ImageObject(path=path)

    getImageObject = ImageObject

    def Variable(self, variables, workSpace):
        """Offers interactive global value manipulation in DrawBot. Can be
        ignored in most contexts except DrawBot for now.
        """
        pass

    # Glyphs.

    def drawGlyphPath(self, glyph):
        """Converts the cubic commands to a drawable path."""
        path = self.getGlyphPath(glyph)
        self.drawPath(path)

    def getGlyphPath(self, glyph, p=None, path=None):
        """PageBot function."""
        raise NotImplementedError

    def onBlack(self, p, path=None):
        """Answers if the single point (x, y) is on black. For now this only
        works in DrawBotContext."""
        if path is None:
            path = self.path
        p = point2D(p)
        return path._path.containsPoint_(p)

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
            for n in range(len(contour)):
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

    # Export.

    def checkExportPath(self, path):
        """If the path starts with "_export" make sure it exists, otherwise
        create it. The _export folders are used to export documents locally,
        without saving them to git. The _export name is included in the git
        .gitignore file.

        >>> context = BaseContext()
        >>> context.checkExportPath('_export/myFile.pdf')
        >>> os.path.exists('_export')
        True
        """
        if path.startswith('_export'):
            dirPath = '/'.join(path.split('/')[:-1])
            if not os.path.exists(dirPath):
                os.makedirs(dirPath)

    #   S C R E E N

    def screenSize(self):
        """Answers the current screen size in DrawBot. Otherwise default is to
        do nothing. PageBot function.

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> size = context.screenSize()
        >>> size[0] > 100 and size[1] > 100
        True
        """
        return pt(self.b.sizes().get('screen', None))

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
