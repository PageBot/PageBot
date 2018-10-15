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

from pagebot.constants import (DISPLAY_BLOCK, DEFAULT_FRAME_DURATION)
from pagebot.toolbox.units import upt, pt, point2D

class AbstractDrawBotContext:
    """All contexts should at least contain the same functions DrawBot does.

    * https://github.com/typemytype/drawbot/blob/master/drawBot/drawBotDrawingTools.py
    """

    ### DrawBot compatible functions start here.

    #   G R A D I E N T    &   S H A D O W

    #   T E X T

    def font(self, fontName, fontSize=None):
        self.b.font(font)

        # Also renders fontSize unit to value.
        if fontSize is not None:
            fspt = upt(fontSize)
            self.b.fontSize(fspt)

    def fontSize(self, fontSize):
        """Set the font size in the context.

        >>> from pagebot.toolbox.units import pt
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> context.fontSize(pt(12))
        """
        fspt = upt(fontSize)
        self.b.fontSize(fspt) # Render fontSize unit to value

    def textSize(self, bs, w=None, h=None, align=None):
        """Answers the width and height of the formatted string with an
        optional given w or h."""
        return self.b.textSize(bs.s, width=w, height=h, align=align)

    def newBulletString(self, bullet, e=None, style=None):
        return self.newString(bullet, e=e, style=style)

    def fallbackFont(self, fontName):
        raise NotImplementedError

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

    #def openTypeFeatures(self, *args, **features):
    def openTypeFeatures(self, features):
        """Set the current of opentype features in the context canvas.

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> context.openTypeFeatures(dict(smcp=True, zero=True))
        """
        self.b.openTypeFeatures(**features)


    def listOpenTypeFeatures(self, fontName=None):
        raise NotImplementedError

    def fontVariations(self, *args, **axes):
        raise NotImplementedError

    def listFontVariations(self, fontName=None):
        raise NotImplementedError

    #   C A N V A S

    def save(self):
        raise NotImplementedError

    def restore(self):
        raise NotImplementedError

    #   D O C U M E N T

    def newDocument(self, w, h):
        raise NotImplementedError

    def saveDocument(self, path, multiPage=None):
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

    def width(self):
        raise NotImplementedError

    def height(self):
        raise NotImplementedError

    def sizes(self, paperSize=None):
        raise NotImplementedError

    def size(self, width, height=None):
        raise NotImplementedError

    def pages(self):
        raise NotImplementedError

    def pageCount(self):
        raise NotImplementedError

    def saveImage(self, path, *args, **options):
        raise NotImplementedError

    def printImage(self, pdf=None):
        raise NotImplementedError

    def pdfImage(self):
        raise NotImplementedError

    #   D R A W I N G

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

    def circle(self, x, y, r):
        """Circle draws a DrawBot oval with (x,y) as middle point and radius r.
        This method is using the core BezierPath as path to draw on. For a more rich
        environment use PageBotPath(context) instead.

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> context.circle(pt(100), pt(200), pt(50))
        >>> context.circle(100, 200, 50)
        """
        xpt, ypt, rpt = upt(x, y, r)
        self.b.oval(xpt-rpt, ypt-rpt, rpt*2, rpt*2) # Render the unit values

    def line(self, p1, p2):
        """Draw a line from p1 to p2.
        This method is using the core BezierPath as path to draw on. For a more rich
        ennvironment use PageBotPath(context).

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

    #   P A T H

    def newPath(self):
        """Make a new core DrawBot.Bezierpath to draw in and answer it. This will
        not initialize self._path, which is accessed by the property self.path
        This method is using the core DrawBot.BezierPath as path to draw on.
        For a more rich environment use PageBotPath(context) instead.

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> context.newPath()
        <BezierPath>
        """
        return self.b.BezierPath()

    def _get_path(self):
        """Answers the open drawing self._path. Create one if it does not exist.

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

    def drawPath(self, path=None, p=None, sx=1, sy=None):
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
        elif hasattr(path, 'bp'): # If it's a PageBotPath, get the core path
            path = path.bp

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

    def onBlack(self, p, path=None):
        """Answers if the single point (x, y) is on black. For now this only
        works in DrawBotContext."""
        if path is None:
            path = self.path
        p = point2D(p)
        return path._path.containsPoint_(p)


    #   C L I P P I N G

    def clipPath(self, clipPath):
        """Sets the clipPath of the DrawBot builder in a new saved graphics
        state. Clip paths cannot be restored, so they should be inside a
        context.save() and context.restore().

        TODO: add unit tests.
        """
        self.b.clipPath(clipPath)

    #def clipPath(self, clipPath):
    #def roundedRect(self, x, y, w, h, offset=25):
    #def bluntCornerRect(self, x, y, w, h, offset=5):
    #def drawGlyphPath(self, glyph):
    #def getGlyphPath(self, glyph, p=None, path=None):

    #   C O L O R

    def fill(self, c):
        raise NotImplementedError

    def stroke(self, c, w=None):
        raise NotImplementedError

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


    def colorSpace(self, colorSpace):
        raise NotImplementedError

    def listColorSpaces(self):
        raise NotImplementedError

    def blendMode(self, operation):
        raise NotImplementedError

    # def miterLimit(self, value):
    # def lineJoin(self, value):
    # def lineCap(self, value):
    # def lineDash(self, *value):

    #   T R A N S F O R M

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

    #   I M A G E

    def image(self, path, p, alpha=1, pageNumber=None, w=None, h=None):
        raise NotImplementedError

    def imagePixelColor(self, path, p):
        raise NotImplementedError

    def imageSize(self, path):
        """Answers the (w, h) image size of the image file at path."""
        return pt(self.b.imageSize(path))


    #def numberOfImages(self, path):
    #def getImageObject(self, path):

    #   O B J E C T S

    def BezierPath(self, path=None, glyphSet=None):
        raise NotImplementedError

    def ImageObject(self, path=None):
        raise NotImplementedError

    def Variable(self, ui, globals):
        """Offers interactive global value manipulation in DrawBot. Can be
        ignored in most contexts except DrawBot for now."""
        pass

    #   A N I M A T I O N

    def frameDuration(self, secondsPerFrame):
        """Set the self._frameDuration for animated GIFs to a number of seconds
        per frame. Used when initializing a new page."""
        self.b.frameDuration(secondsPerFrame or DEFAULT_FRAME_DURATION)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
