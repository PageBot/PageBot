#!/usr/bin/env python
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
from pagebot.contexts.basecontext import BaseContext
from pagebot.style import CENTER, RIGHT, DEFAULT_FRAME_DURATION
from pagebot.toolbox.color import color, Color, noColor, inheritColor
from pagebot.toolbox.units import pt, upt, point2D, Angle # Render units to points
from pagebot.constants import *
#from sys import platform

try:
#if platform == 'darwin':
    #from CoreText import CTFontDescriptorCreateWithNameAndSize, \
    #    CTFontDescriptorCopyAttribute, kCTFontURLAttribute, \
    #    CTFramesetterCreateWithAttributedString, CTFramesetterCreateFrame, \
    #    CTFrameGetLines, CTFrameGetLineOrigins
    #from Quartz import CGPathAddRect, CGPathCreateMutable, CGRectMake
    import drawBot
    from drawBot import Variable

    from pagebot.contexts.strings.drawbotstring import DrawBotString as stringClass
    drawBotBuilder = drawBot
    # Id to make builder hook name. Views will try to call e.build_html()
    drawBotBuilder.PB_ID = 'drawBot'
except (AttributeError, ImportError):
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
        self.b = drawBotBuilder #  Builder for this canvas.
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
        u"""Ignore for DrawBot, as document opens automatically if first page
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

    #   C L I P P I N G

    def clipPath(self, clipPath):
        """Set the clipPath of the DrawBot builder in a new saved graphics state.
        Clip paths cannot be restore, so they should be inside a context.save() and context.restore()
        """
        self.b.clipPath(clipPath)

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

    def bluntCornerRect(self, x, y, w, h, offset=5):
        """Draw a rectangle in the canvas.

        >>> context = DrawBotContext()
        >>> context.rect(pt(0), pt(0), pt(100), pt(100))
        >>> context.rect(0, 0, 100, 100)
        """
        path = self.newPath()
        path.moveTo((x+offset, y))
        path.lineTo((x+w-offset, y))
        path.lineTo((x+w, y+offset))
        path.lineTo((x+w, y+h-offset))
        path.lineTo((x+w-offset, y+h))
        path.lineTo((x+offset, y+h))
        path.lineTo((x, y+h-offset))
        path.lineTo((x, y+offset))
        self.closePath()
        self.drawPath(path)

    def roundedRect(self, x, y, w, h, offset=25):
        """Draw a rectangle in the canvas.

        >>> context = DrawBotContext()
        >>> context.rect(pt(0), pt(0), pt(100), pt(100))
        >>> context.rect(0, 0, 100, 100)
        """
        path = self.newPath()
        path.moveTo((x+offset, y))
        path.lineTo((x+w-offset, y))
        path.curveTo((x+w, y), (x+w, y), (x+w, y+offset))
        path.lineTo((x+w, y+h-offset))
        path.curveTo((x+w, y+h), (x+w, y+h), (x+w-offset, y+h))
        path.lineTo((x+offset, y+h))
        path.curveTo((x, y+h), (x, y+h), (x, y+h-offset))
        path.lineTo((x, y+offset))
        path.curveTo((x, y), (x, y), (x+offset, y))
        self.closePath()
        self.drawPath(path)

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
        """Make a new DrawBot Bezierpath() to draw in and answer it.
        This will not initialize self._path, which is accessed by the property self.path

        >>> context = DrawBotContext()
        >>> context.newPath() is not None
        True
        """
        return self.b.BezierPath()

    def _get_path(self):
        """Answers the open drawing self._path. Create one if it does not exist.

        >>> context = DrawBotContext()
        >>> context.path is not None
        True
        """
        if self._path is None:
            self._path = self.newPath()
        return self._path
    path = property(_get_path)

    def drawPath(self, path=None, p=None, sx=1, sy=None):
        """Draw the NSBezierPath, or equivalent in other contexts. Scaled image
        is drawn on (x, y), in that order."""
        if path is None:
            path = self.path

        self.save()
        if sy is None:
            sy = sx
        if p is None:
            xpt = ypt = 0
        else:
            xpt, ypt = point2D(upt(p))
        self.scale(sx, sy)
        self.translate(xpt/sx, ypt/sy)
        self.b.drawPath(path)
        self.restore()

    def drawGlyphPath(self, glyph):
        """Converts the cubic commands to a drawable path."""
        path = self.getGlyphPath(glyph)
        self.drawPath(path)

    def getGlyphPath(self, glyph, p=None, path=None):
        u"""Answer the DrawBot path. Allow optional position offset and path, in case
        we do recursive component drawing.

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
                path.curveTo((px+t[0][0], py+t[0][1]), (px+t[1][0], py+t[1][1]), (px+t[2][0], py+t[2][1]))
            elif command == 'closePath':
                path.closePath()
            elif command == 'component':
                (x, y), componentGlyph = t
                self.getGlyphPath(componentGlyph, (px+x, py+y), path)
        return path

    def getFlattenedContours(self, path=None):
        """Answers the flattened NSBezier path As contour list [contour,
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

    def onBlack(self, p, path=None):
        """Answers the boolean flag if the single point (x, y) is on black.
        For now this only works in DrawBotContext.
        """
        if path is None:
            path = self.path
        p = point2D(p)
        return path._path.containsPoint_(p)

    def moveTo(self, p):
        """Move to point p in the running path. Create a new self._path if none is open.

        >>> from pagebot.toolbox.units import pt
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
        ppt = point2D(upt(p))
        self.path.moveTo(ppt) # Render units point tuple to tuple of values

    def lineTo(self, p):
        """Line to point p in the running path. Create a new self._path if none is open.

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
        ppt = point2D(upt(p))
        self.path.lineTo(ppt) # Render units point tuple to tuple of values

    def quadTo(bcp, p):
        # TODO: Convert to Bezier with 0.6 rule
        pass

    def curveTo(self, bcp1, bcp2, p):
        """Curve to point p i nthe running path. Create a new path if none is open.

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
        b1pt = point2D(upt(bcp1))
        b2pt = point2D(upt(bcp2))
        ppt = point2D(upt(p))
        self.path.curveTo(b1pt, b2pt, ppt) # Render units tuples to value tuples

    def closePath(self):
        """Close the current path, if it exists. Otherwise ignore.

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

    def getFlattenedPath(self, path=None):
        """Use the NSBezier flatten path. Answer None if the flattened path
        could not be made."""
        if path is None:
            path = self.path
        return path._path.getNSBezierPath().bezierPathByFlatteningPath()

    def getFlattenedContours(self, path=None):
        """Answers the flattened NSBezier path As contour list [contour,
        contour, ...] where contours are lists of point2D() points."""
        contour = []
        flattenedContours = [contour]
        flatPath = self.getFlattenedPath(path)

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
                self.b.shadow(upt(eShadow.offset), # Convert units to values
                              blur=upt(eShadow.blur),
                              color=color(eShadow.color).cmyk)
            else:
                self.b.shadow(upt(eShadow.offset),
                              blur=upt(eShadow.blur),
                              color=color(eShadow.color).rgb)

    def setGradient(self, gradient, origin, w, h):
        """Define the gradient call to match the size of element e., Gradient position
        is from the origin of the page, so we need the current origin of e."""
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

    def installedFonts(self, patterns=None):
        """Answer a list of all fonts (name or path) that are installed in the OS.

        >>> from pagebot.contexts.platform import getContext
        >>> context = getContext()
        >>> installed = context.installedFonts()
        >>> installed
        []
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
        if hasattr(fontOrName, 'path'):
            fontOrName = fontOrName.path
        return self.b.installFont(fontOrName)
        
    def unInstallFont(self, fontOrName):
        if hasattr(fontOrName, 'path'):
            fontOrName = fontOrName.path
        return self.b.uninstallFont(fontOrName)
        
    #   G L Y P H

    def drawGlyph(self, glyph, x, y, fill=noColor, stroke=noColor, strokeWidth=0, fontSize=None, xAlign=CENTER):
        u"""Draw the font[glyphName] at the defined position with the defined fontSize.

        """
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

    def textSize(self, bs, w=None, h=None, align=None):
        """Answer the width/height of the formatted string for an optional given w or h."""
        return self.b.textSize(bs.s, width=w, height=h, align=align)

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

    def language(self, language):
        u"""DrawBot needs an overall language flag set to code, as it is not part of the FormattedString
        style attributes. For availabel ISO language codes, see pageboy.constants."""
        self.b.language(language)

    def hyphenation(self, onOff):
        u"""DrawBot needs an overall hyphenation flag set on/off, as it is not part of the FormattedString
        style attributes."""
        self.b.hyphenation(onOff)

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

        >>> from pagebot.toolbox.units import pt, mm
        >>> context = DrawBotContext()
        >>> context.setStrokeWidth(pt(0.5))
        >>> context.setStrokeWidth(mm(0.5))
        """
        wpt = upt(w)
        self.b.strokeWidth(wpt)

    setStrokeWidth = strokeWidth

    def rotate(self, angle, center=None):
        """Rotate the canvas by angle. If angle is not a units.Angle instance, then convert.

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

    def imagePixelColor(self, path, p):
        ppt = point2D(upt(p))
        return self.b.imagePixelColor(path, ppt)

    def imageSize(self, path):
        u"""Answer the (w, h) image size of the image file at path."""
        return pt(self.b.imageSize(path))

    def numberOfImages(self, path):
        u"""Answer the number of images in the file referenced by path."""
        return self.b.numberOfPages(path)

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
        else: # Both are defined, scale disproportional
            wpt = upt(w)
            hpt = upt(h)

        # else both w and h are defined, scale disproportional
        xpt, ypt, = point2D(upt(p))
        sx, sy = (wpt/iw).rv, (hpt/ih).rv # We need ration values, not units
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
