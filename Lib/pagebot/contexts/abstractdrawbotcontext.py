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
#     abstractdrawbot.py
#

from pagebot.constants import DEFAULT_FRAME_DURATION
from pagebot.toolbox.units import upt, pt, point2D
from pagebot.toolbox.color import color

class AbstractDrawBotContext:
    """All contexts should at least contain the same (public) functions DrawBot does.

    * https://github.com/typemytype/drawbot/blob/master/drawBot/drawBotDrawingTools.py
    """

    def newDrawing(self):
        """Clear output canvas, start new export file.

        >>> from pagebot.toolbox.units import px
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> context.newDrawing()
        """
        self.b.newDrawing()

    def endDrawing(self):
        raise NotImplementedError

    # Magic variables.

    def width(self):
        raise NotImplementedError

    def height(self):
        raise NotImplementedError

    def sizes(self, paperSize=None):
        raise NotImplementedError

    def pageCount(self):
        raise NotImplementedError

    # Public callbacks.

    def size(self, width, height=None):
        raise NotImplementedError

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

    def pages(self):
        raise NotImplementedError

    def saveImage(self, path, *args, **options):
        raise NotImplementedError

    def printImage(self, pdf=None):
        raise NotImplementedError

    def pdfImage(self):
        raise NotImplementedError

    # Graphics state.

    def save(self):
        self.b.save()

    saveGraphicState = save

    def restore(self):
        self.b.restore()

    restoreGraphicState = restore

    def savedState(self):
        raise NotImplementedError

    # Basic shapes.

    def rect(self, x, y, w, h):
        """Draws a rectangle in the canvas.  This method is using the core
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

    # Path.

    def newPath(self):
        """Makes a new Bezierpath to draw in and answers it. This will not
        initialize self._path, which is accessed by the property self.path.
        This method is using the BezierPath as path to draw on. For a more
        rich environment use PageBotPath(context) instead.

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> context.newPath()
        <BezierPath>
        """
        return self.b.BezierPath()

    def moveTo(self, p):
        """Move to point p in the running path. Create a new self._path if none
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
        """Line to point p in the running path. Create a new self._path if none
        is open.

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
        ppt = upt(point2D(p))
        self.path.lineTo(ppt) # Render units point tuple to tuple of values

    def curveTo(self, bcp1, bcp2, p):
        """Curve to point p i nthe running path. Create a new path if none is
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
        raise NotImplementedError

    def arc(self, center, radius, startAngle, endAngle, clockwise):
        raise NotImplementedError

    def arcTo(self, xy1, xy2, radius):
        raise NotImplementedError

    def closePath(self):
        """Closes the current path if it exists, otherwise ignore it.

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

    def drawPath(self, path=None, p=None, sx=1, sy=None, fill=None, stroke=None, strokeWidth=None):
        """Draws the BezierPath. Scaled image is drawn on (x, y), in that order.
        Use self._path if path is omitted.

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
        raise NotImplementedError

    # Color.

    def colorSpace(self, colorSpace):
        raise NotImplementedError

    def listColorSpaces(self):
        raise NotImplementedError

    def blendMode(self, operation):
        raise NotImplementedError

    def fill(self, c):
        # NOTE: signature differs from DrawBot.
        raise NotImplementedError

    setFillColor = fill
    cmykFill = fill

    def stroke(self, c, w=None):
        # NOTE: signature differs from DrawBot.
        raise NotImplementedError

    setStrokeColor = stroke
    cmykStroke = stroke

    def shadow(self, offset, blur=None, color=None):
        raise NotImplementedError

    cmykShadow = shadow

    def linearGradient(self, startPoint=None, endPoint=None, colors=None, locations=None):
        raise NotImplementedError

    cmykLinearGradient = linearGradient

    def radialGradient(self, startPoint=None, endPoint=None, colors=None,
            locations=None, startRadius=0, endRadius=100):
        raise NotImplementedError

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
        raise NotImplementedError

    def translate(self, x=0, y=0):
        raise NotImplementedError

    def rotate(self, angle, center=(0, 0)):
        raise NotImplementedError

    def scale(self, x=1, y=None, center=(0, 0)):
        raise NotImplementedError

    def skew(self, angle1, angle2=0, center=(0, 0)):
        raise NotImplementedError

    # Text.

    def font(self, fontName, fontSize=None):
        # FIXME: fontSize?
        self.b.font(fontName)

        # Also renders fontSize unit to value.
        if fontSize is not None:
            fspt = upt(fontSize)
            self.b.fontSize(fspt)

    def fallbackFont(self, fontName):
        raise NotImplementedError

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
        raise NotImplementedError

    def tracking(self, value):
        raise NotImplementedError

    def baselineShift(self, value):
        raise NotImplementedError

    def underline(self, value):
        raise NotImplementedError

    def hyphenation(self, onOff):
        """DrawBot needs an overall hyphenation flag set on/off, as it is not
        part of the FormattedString style attributes."""
        self.b.hyphenation(onOff)

    def tabs(self, *tabs):
        raise NotImplementedError

    def language(self, language):
        """DrawBot needs an overall language flag set to code, as it is not
        part of the FormattedString style attributes. For availabel ISO
        language codes, see pageboy.constants."""
        self.b.language(language)

    def listLanguages(self):
        raise NotImplementedError

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
        raise NotImplementedError

    def listFontVariations(self, fontName=None):
        raise NotImplementedError

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

    def textOverflow(self, txt, box, align=None):
        raise NotImplementedError

    def textBox(self, sOrBs, r=None, clipPath=None):
        """Draw the sOrBs text string, can be a str or BabelString, including a
        DrawBot FormattedString in rectangle r.

        NOTE: signature differs from DrawBot.

        >>> from pagebot.toolbox.units import pt
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> context.textBox('ABC', (10, 10, 200, 200))
        """
        if not isinstance(sOrBs, str):
            sOrBs = sOrBs.s # Assume here is's a BabelString with a FormattedString inside.
        if clipPath is not None:
            self.b.textBox(sOrBs, clipPath) # Render rectangle units to value tuple
        elif r is not None:
            xpt, ypt, wpt, hpt = upt(r)
            # Render rectangle units to value tuple
            self.b.textBox(sOrBs, (xpt, ypt, wpt, hpt))

    def textBoxBaselines(self, txt, box, align=None):
        raise NotImplementedError

    def FormattedString(self, *args, **kwargs):
        # refer to BabelString?
        pass

    # Images

    def image(self, path, p, alpha=1, pageNumber=None, w=None, h=None):
        raise NotImplementedError

    def imageSize(self, path):
        """Answers the (w, h) image size of the image file at path."""
        return pt(self.b.imageSize(path))

    def imagePixelColor(self, path, p):
        raise NotImplementedError

    def numberOfPages(self, path):
        raise NotImplementedError

    # Mov.

    def frameDuration(self, secondsPerFrame):
        """Set the self._frameDuration for animated GIFs to a number of seconds
        per frame. Used when initializing a new page."""
        self.b.frameDuration(secondsPerFrame or DEFAULT_FRAME_DURATION)

    # PDF links.

    def linkDestination(self, name, x=None, y=None):
        raise NotImplementedError

    def linkRect(self, name, xywh):
        raise NotImplementedError

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
        """Offers interactive global value manipulation in DrawBot. Can be
        ignored in most contexts except DrawBot for now.
        """
        pass

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
