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
#     Supporting usage of InDesign API-scripting
# -----------------------------------------------------------------------------
#
#     indesigncontext.py
#
#     Documentation for InDesign API:
#
#     https://www.adobe.com/devnet/indesign/documentation.html
#     https://wwwimages2.adobe.com/content/dam/acom/en/devnet/indesign/sdk/cs6/scripting/InDesign_ScriptingGuide_JS.pdf
#
from pagebot.contexts.basecontext import BaseContext
from pagebot.contexts.builders.indesignbuilder import InDesignBuilder
from pagebot.contexts.strings.indesignstring import InDesignString
from pagebot.constants import CENTER, RIGHT
from pagebot.toolbox.units import upt, pt
from pagebot.toolbox.mathematics import *
from pagebot.toolbox.color import noColor, blackColor, Color, inheritColor, color

class InDesignContext(BaseContext):
    """The InDesignContext implements the InDesign JS-API within the PageBot
    framework."""

    # Used by the generic BaseContext.newString( )
    STRING_CLASS = InDesignString
    EXPORT_TYPES = ('jsx',)

    def __init__(self):
        """Constructor of InDesignContext.

        >>> context = InDesignContext()
        """
        super().__init__()
        self.b = InDesignBuilder() # cls.b builder for this canvas.
        self.name = self.__class__.__name__
        self.save() # Save current set of values on gState stack.

    def getInDesignScriptPath(self):
        """Answers the user local script path. For now this assumes one version
        of InDesign.

        TODO: Should be made more generic.

        >>> context = InDesignContext()
        >>> context.getInDesignScriptPath().endswith('/PageBot/')
        True
        """
        return self.b.getInDesignScriptPath()

    #   S C R E E N

    def screenSize(self):
        """Answers the current screen size. Otherwise default is to do
        nothing."""
        return None

    #   D O C U M E N T

    def newDocument(self, w, h):
        """Creates a new document."""
        self.b.newDocument(w, h)

    def saveDocument(self, path, multiPage=None):
        """Select other than standard InDesign export builders here. Save the
        current image as path, rendering depending on the extension of the path
        file. In case the path starts with "_export", then create it
        directories.

        >>> from pagebot.constants import A4Rounded
        >>> H, W = A4Rounded # Initialize as landscape
        >>> context = InDesignContext()
        >>> context.newDocument(W, H)
        >>> context.saveImage('_export/MyFile.'+context.EXPORT_TYPES[0])

        """
        if not path.endswith(self.EXPORT_TYPES[0]):
            path += '.'+self.EXPORT_TYPES[0]
        self.checkExportPath(path)
        self.b.writeJs(path)

    saveImage = saveDocument

    def getDocument(self):
        pass

    def newPage(self, w, h):
        """Create a new InDesign page.

        >>> from pagebot.toolbox.units import pt
        >>> context = InDesignContext()
        >>> context.newPage(pt(100), pt(100))
        """
        self.b.newPage(w, h)

    def newDrawing(self):
        """Clear output canvas, start new export file.

        >>> context = InDesignContext()
        >>> context.newDrawing()
        """
        self.b.newDrawing()

    # Basic shapes.

    def rect(self, x, y, w, h):
        """Draw a rectangle in the canvas.

        >>> from pagebot.toolbox.units import pt
        >>> context = InDesignContext()
        >>> context.rect(pt(10), pt(20), pt(110), pt(120))
        """
        #TODO default to points.
        self.b.rect(x, y, w, h)

    def oval(self, x, y, w, h):
        """Draw an oval in rectangle, where (x,y) is the bottom-left and size
        (w,h).

        >>> from pagebot.toolbox.units import pt
        >>> context = InDesignContext()
        >>> context.oval(pt(0), pt(0), pt(100), pt(100))
        """
        #TODO default to points.
        self.b.oval(x, y, w, h)

    def circle(self, x, y, r):
        """Circle draws an InDesign oval with (x,y) as middle point and radius
        r.

        >>> from pagebot.toolbox.units import pt
        >>> context = InDesignContext()
        >>> context.circle(pt(100), pt(100), pt(150))
        """
        #TODO default to points.
        self.b.oval(x-r, y-r, r*2, r*2)

    def line(self, p1, p2):
        """Draw a line from p1 to p2.

        >>> from pagebot.toolbox.units import pt, mm
        >>> context = InDesignContext()
        >>> context.line(pt(100, 100), pt(200, 200))
        >>> context.line(mm(100, 100), mm(200, 200))
        """
        self.b.line(p1, p2)

    # Color.

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

        msg = 'InDesignContext.fill: %s should be of type Color'
        assert isinstance(c, Color), (msg % c)

        if c is inheritColor:
            # Keep color setting as it is.
            pass
        elif c is noColor:
            self.b.fill(None) # Set color to no-color
        elif c.isCmyk:
            cyan, magenta, yellow, key = to100(color.cmyk)
            self.b.cmykFill(cyan, magenta, yellow, key, alpha=color.a)
        else:
            r, g, b = to255(c.rgb)
            self.b.fill(r, g, b, alpha=c.a)

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
            cyan, magenta, yellow, key = to100(c.cmyk)
            self.b.cmykStroke(cyan, magenta, yellow, key, alpha=c.a)
        else:
            # DrawBot.stroke has slight API differences compared to
            # FormattedString stroke(). Convert to RGB, whatever the color type.
            r, g, b = to255(c.rgb)
            self.b.stroke(r, g, b, alpha=c.a)

        if w is not None:
            self.strokeWidth(w)

    # Path.

    def newPath(self):
        """Make a new InDesign Bezierpath to draw in.

        >>> context = InDesignContext()
        >>> context.path is not None
        True
        """
        self._path = self.b.BezierPath()
        return self._path

    def _get_path(self):
        """Answers the open drawing path. Create one if it does not exist.

        >>> context = InDesignContext()
        >>> context.path is not None
        True
        """
        if self._path is None:
            self.newPath()
        return self._path
    path = property(_get_path)

    def drawPath(self, path=None, p=(0, 0), sx=1, sy=None):
        """Draw the path, or equivalent in other contexts. Scaled image is
        drawn on (x, y), in that order."""
        if path is None:
            path = self._path
        if path is not None:
            self.save()
        if sy is None:
            sy = sx
            #self.scale(sx, sy)
            #self._translate(p[0]/sx, p[1]/sy)
            #self.b.drawPath(path)
            #self.restore()

    def moveTo(self, p):
        """Move to point p. Create a new path if none is open.

        >>> context = InDesignContext()
        >>> path = context.newPath()
        >>> path.moveTo((100, 100))
        """
        if self._path is None:
            self.newPath()
        self._path.moveTo((p[0], p[1]))

    def lineTo(self, p):
        """Line to point p. Create a new path if none is open.

        >>> context = InDesignContext()
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
        """Curve to point p. Create a new path if none is open.

        >>> context = InDesignContext()
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
        """Curve to point p. Create a new path if none is open.

        >>> context = InDesignContext()
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
        """Use the NSBezier flatten path."""
        return path.getNSBezierPath().bezierPathByFlatteningPath()

    def scale(self, sx, sy=None):
        """Set the drawing scale."""
        if sy is None:
            sy = sx
        self.b.scale(sx, sy)

    def translate(self, dx, dy):
        """Translates the origin to this point."""
        self.b.translate(dx, dy)

    def transform(self, t):
        """Transforms canvas over matrix t, e.g. (1, 0, 0, 1, dx, dy) to shift
        over vector (dx, dy)"""
        self.b.transform(t)

    #   G R A D I E N T  &  S H A D O W

    def setShadow(self, eShadow):
        """Sets the InDesign graphics state for shadow if all parameters are
        set."""
        if eShadow is not None and eShadow.offset is not None:
            if eShadow.color.isCmyk:
                self.b.shadow(upt(eShadow.offset),
                              blur=upt(eShadow.blur),
                              color=eShadow.color.cmyk)
            else:
                self.b.shadow(upt(eShadow.offset),
                              blur=upt(eShadow.blur),
                              color=eShadow.color.rgb)

    def setGradient(self, gradient, origin, w, h):
        """Defines the gradient call to match the size of element e., Gradient
        position is from the origin of the page, so we need the current origin
        of e."""
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

    def lineDash(self, lineDash):
        pass
        #self.b.lineDash(lineDash)

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
        """Save the current graphic state.

        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> context = InDesignContext()
        >>> context._font.endswith('Roboto-Regular.ttf')
        True
        >>> context.save()
        >>> boldFont = findFont('Roboto-Bold')
        >>> context.font(boldFont) # Set by Font instance
        >>> context._font.path.endswith('Roboto-Bold.ttf')
        True
        >>> context.restore() # Restore to original graphic state values
        >>> context._font.endswith('Roboto-Regular.ttf')
        True
        """
        gState = dict(
            font=self._font,
            fontSize=self._fontSize,
            fill=self._fill,
            stroke=self._stroke,
            strokeWidth=self._strokeWidth,
            ox=self._ox,
            oy=self._oy,
            rotate=self._rotate,
            hyphenation=self._hyphenation,
            openTypeFeatures=self._openTypeFeatures,
        )
        self._gState.append(gState)

    save = saveGraphicState

    def restoreGraphicState(self):
        """Restores current graphic state."""
        gState = self._gState.pop()
        self._font = gState['font']
        self._fontSize = gState['fontSize']
        self._fill = gState['fill']
        self._stroke = gState['stroke']
        self._strokeWidth = gState['strokeWidth']
        self._ox = gState['ox']
        self._oy = gState['oy']
        self._rotate = gState['rotate']
        self._hyphenation = gState['hyphenation']
        self._openTypeFeatures = gState['openTypeFeatures']
    restore = restoreGraphicState

    #   F O N T S

    def listOpenTypeFeatures(self, fontName=None):
        """Answers the list of opentype features available in the named font."""
        return [] #self.b.listOpenTypeFeatures(fontName)

    #   G L Y P H

    def drawGlyph(self, glyph, x, y, fill=None, stroke=None, strokeWidth=0, fontSize=None, xAlign=CENTER):
        """Draw the font[glyphName] at the defined position with the defined fontSize.

        """
        if fill is None:
            fill = blackColor
        if stroke is None:
            stroke = noColor

        font = glyph.font
        s = fontSize/font.info.unitsPerEm
        if xAlign == CENTER:
            x -= (glyph.width or 0)/2*s
        elif xAlign == RIGHT:
            x -= glyph.width*s
        self.save()
        self.fill(fill)
        self.stroke(stroke, strokeWidth)
        self.transform((1, 0, 0, 1, x, y))
        self.scale(s)
        self.drawGlyphPath(glyph)
        self.restore()

    def drawGlyphPath(self, glyph):
        """Converts the cubic commands to a drawable path.

        TODO:
        path = self.newPath()

        for command, t in glyph.cubic:
            if command == 'moveTo':
                path.moveTo(t)
            elif command == 'lineTo':
                path.lineTo(t)
            elif command == 'curveTo':
                path.curveTo(*t)
            elif command == 'closePath':
                path.closePath()

        self.drawPath(path)
        """
        pass

    #   T E X T

    def fontSize(self, fontSize):
        """Set the font size in the context.

        >>> context = InDesignContext()
        >>> context.fontSize(12)
        >>> context._fontSize
        12
        """
        self._fontSize = fontSize

    def font(self, font, fontSize=None):
        self._font = font
        if fontSize is not None:
            self._fontSize = fontSize

    def newBulletString(self, bullet, e=None, style=None):
        return self.newString(bullet, e=e, style=style)

    def text(self, sOrBs, p):
        """Draw the sOrBs text string, can be a str or BabelString, including a InDesign FormattedString
        at position p."""
        if not isinstance(sOrBs, str):
            sOrBs = sOrBs.s # Assume here is's a BabelString with a FormattedString inside.
        self.b.text(sOrBs, p)

    def textBox(self, sOrBs, r):
        """Draw the sOrBs text string, can be a str or BabelString, including a InDesign FormattedString
        in rectangle r."""
        if not isinstance(sOrBs, str):
            sOrBs = sOrBs.s # Assume here is's a BabelString with a FormattedString inside.
        self.b.textBox(sOrBs, r)

    def openTypeFeatures(self, features):
        """Set the current of opentype features in the context canvas.

        >>> context = InDesignContext()
        >>> context.openTypeFeatures(dict(smcp=True, zero=True))
        """
        self._openTypeFeatures = features

    def hyphenation(self, onOff=True):
        """Set the hyphenation on/off flag.

        >>> context = InDesignContext()
        >>> context.hyphenation(True)
        >>> context.hyphenation(False)
        """
        self._hyphenation = onOff

    #   A N I M A T I O N

    def frameDuration(self, secondsPerFrame):
        """Nothing to do in InDesignContext."""

    #   C O L O R

    '''
    def setTextFillColor(self, fs, c):
        assert isinstance(c, Color)
        self._textFill = c

    def setTextStrokeColor(self, fs, c, w=None):
        assert isinstance(c, Color)
        self._textStroke = c
        self.setStrokeWidth(w)

    def setFillColor(self, c, b=None):
        """Set the color for global or the color of the formatted string."""
        assert isinstance(c, Color)
        self._fill = c

    fill = setFillColor # InDesign compatible API

    def setStrokeColor(self, c, w=None):
        """Set global stroke color or the color of the formatted string."""
        assert isinstance(c, Color)
        self._stroke = c
        self.strokeWidth(w)

    stroke = setStrokeColor # InDesign compatible API

    def setStrokeWidth(self, w):
        self._strokeWidth = w

    strokeWidth = setStrokeWidth

    def rotate(self, angle, center=None):
        """Rotate the canvas by angle."""
        self.b.rotate(angle, center=center)
    '''

    #   I M A G E

    def imagePixelColor(self, path, p):
        return self.b.imagePixelColor(path, p)

    def imageSize(self, path):
        """Answers the (w, h) image size of the image file at path. If the path is an SVG
        image, then determine by parsing the SVG-XML.

        if path.lower().endswith('.'+FILETYPE_SVG):
            import xml.etree.ElementTree as ET
            svgTree = ET.parse(path)
            print(svgTree)
            return pt(1000, 1000)

        return pt(self.b.imageSize(path))
        """
        return pt(1000, 1000)

    def saveImage(self, path):
        """Ignore for now in this context."""

    def image(self, path, p, alpha=1, pageNumber=None, w=None, h=None):
        """Draw the image. If w or h is defined, then scale the image to
        fit."""
        iw, ih = self.imageSize(path)
        if w and not h: # Scale proportional
            h = ih * w/iw # iw : ih = w : h
        elif not w and h:
            w = iw * h/ih
        elif not w and not h:
            w = iw
            h = ih
        # else both w and h are defined, scale disproportional
        x, y = p[0], p[1]
        sx, sy = w/iw, h/ih
        self.save()
        self.scale(sx, sy)
        self.b.image(path, (x*sx, y*sy), alpha=alpha, pageNumber=pageNumber)
        self.restore()

    def getImageObject(self, path):
        """Answers the ImageObject that knows about image filters.

        >>> from pagebot import getResourcesPath
        >>> from pagebot.contexts.indesigncontext import InDesignContext
        >>> context = InDesignContext()
        >>> path = getResourcesPath() + '/images/peppertom_lowres_398x530.png'
        >>> imo = context.getImageObject(path)

        """
        """Ignore for now in this context."""
        pass
        #return self.b.ImageObject(path)

    def scale(self, sx=1, sy=None, center=(0, 0)):
        """Ignore for now in this context."""

    def image(self, path, p, alpha=1, pageNumber=None, w=None, h=None):
        """Ignore for now in this context."""

    def endDrawing(self):
        pass

    def getFlattenedContours(self, glyph):
        return None

    def getFlattenedPath(self, glyph):
        return None

    def getGlyphPath(self, glyph):
        return None

    def newDocument(self):
        return None

    def numberOfImages(self):
        return 0

    def saveDocument(self, path):
        pass

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
