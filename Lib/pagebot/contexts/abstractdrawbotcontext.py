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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

    saveGraphicState = save

    def restore(self):
        raise NotImplementedError

    restoreGraphicState = restore

    def savedState(self):
        raise NotImplementedError

    # Basic shapes.

    def rect(self, x, y, w, h):
        raise NotImplementedError

    def oval(self, x, y, w, h):
        raise NotImplementedError

    # Path.

    def newPath(self):
        raise NotImplementedError

    def moveTo(self, p):
        raise NotImplementedError

    def lineTo(self, p):
        raise NotImplementedError

    def curveTo(self, bcp1, bcp2, p):
        raise NotImplementedError

    def qCurveTo(self, *points):
        raise NotImplementedError

    def arc(self, center, radius, startAngle, endAngle, clockwise):
        raise NotImplementedError

    def arcTo(self, xy1, xy2, radius):
        raise NotImplementedError

    def closePath(self):
        raise NotImplementedError

    def drawPath(self, path=None, p=None, sx=1, sy=None, fill=None,
            stroke=None, strokeWidth=None):
        raise NotImplementedError

    def clipPath(self, clipPath):
        raise NotImplementedError

    def line(self, p1, p2):
        raise NotImplementedError

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
        # FIXME: signature differs from DrawBot.
        raise NotImplementedError

    def cmykFill(self, c):
        # FIXME: signature differs from DrawBot.
        raise NotImplementedError

    def stroke(self, c, w=None):
        # NOTE: signature differs from DrawBot.
        raise NotImplementedError

    def cmykStroke(self, c):
        # FIXME: signature differs from DrawBot.
        raise NotImplementedError

    def shadow(self, offset, blur=None, color=None):
        raise NotImplementedError

    def cmykShadow(self, offset, blur=None, color=None):
        # FIXME: signature differs from DrawBot.
        raise NotImplementedError

    def linearGradient(self, startPoint=None, endPoint=None, colors=None,
            locations=None):
        raise NotImplementedError

    def cmykLinearGradient(self, startPoint=None, endPoint=None, colors=None,
            locations=None):
        # FIXME: signature differs from DrawBot.
        raise NotImplementedError

    def radialGradient(self, startPoint=None, endPoint=None, colors=None,
            locations=None, startRadius=0, endRadius=100):
        raise NotImplementedError

    # Path drawing behavior.

    def strokeWidth(self, w):
        raise NotImplementedError

    def miterLimit(self, value):
        raise NotImplementedError

    def lineJoin(self, value):
        raise NotImplementedError

    def lineCap(self, value):
        raise NotImplementedError

    def lineDash(self, value):
        raise NotImplementedError

    # Transform.

    def transform(self, matrix, center=(0, 0)):
        raise NotImplementedError

    def translate(self, x=0, y=0):
        raise NotImplementedError

    def rotate(self, angle, center=None):
        raise NotImplementedError

    def scale(self, x=1, y=None, center=(0, 0)):
        raise NotImplementedError

    def skew(self, angle1, angle2=0, center=(0, 0)):
        raise NotImplementedError

    # Text.

    def font(self, fontName, fontSize=None):
        raise NotImplementedError

    def fallbackFont(self, fontName):
        raise NotImplementedError

    def fontSize(self, fontSize):
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
        raise NotImplementedError

    def tabs(self, *tabs):
        raise NotImplementedError

    def language(self, language):
        raise NotImplementedError

    def listLanguages(self):
        raise NotImplementedError

    def openTypeFeatures(self, features):
        raise NotImplementedError

    def listOpenTypeFeatures(self, fontName=None):
        raise NotImplementedError

    def fontVariations(self, *args, **axes):
        raise NotImplementedError

    def listFontVariations(self, fontName=None):
        raise NotImplementedError

    # Drawing text.

    def text(self, sOrBs, p):
        raise NotImplementedError

    def textOverflow(self, txt, box, align=None):
        raise NotImplementedError

    def textBox(self, sOrBs, r=None, clipPath=None):
        raise NotImplementedError

    def textBoxBaselines(self, txt, box, align=None):
        raise NotImplementedError

    def FormattedString(self, *args, **kwargs):
        raise NotImplementedError

    # Images

    def image(self, path, p, alpha=1, pageNumber=None, w=None, h=None):
        raise NotImplementedError

    def imageSize(self, path):
        raise NotImplementedError

    def imagePixelColor(self, path, p):
        raise NotImplementedError

    def numberOfPages(self, path):
        raise NotImplementedError

    # Mov.

    def frameDuration(self, secondsPerFrame):
        raise NotImplementedError

    # PDF links.

    def linkDestination(self, name, x=None, y=None):
        raise NotImplementedError

    def linkRect(self, name, xywh):
        raise NotImplementedError

    # Helpers.

    def textSize(self, bs, w=None, h=None, align=None):
        raise NotImplementedError

    def installedFonts(self, patterns=None):
        raise NotImplementedError

    def installFont(self, fontOrName):
        raise NotImplementedError

    def uninstallFont(self, fontOrName):
        raise NotImplementedError

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
        raise NotImplementedError

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
