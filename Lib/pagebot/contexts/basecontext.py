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
from pagebot.constants import DISPLAY_BLOCK

class BaseContext:
    """A BaseContext instance abstracts the specific functions of a platform
    (for instance DrawBot, Flat or HTML), thus hiding e.g. the type of
    BabelString instance needed, and the type of HTML/CSS file structure to be
    created.

    Should comply to:

    * https://github.com/typemytype/drawbot/blob/master/drawBot/drawBotDrawingTools.py

    """

    # In case of specific builder addressing, callers can check here.
    isDrawBot = False
    isFlat = False
    isSvg = False
    isInDesign = False

    # Indication to Typesetter that by default tags should not be included in
    # output.
    useTags = False

    # To be redefined by inheriting context classes.
    STRING_CLASS = None
    EXPORT_TYPES = None

    def __repr__(self):
        return '<%s>' % self.name

    #   T E X T

    def newString(self, s, e=None, style=None, w=None, h=None, pixelFit=True):
        """Creates a new styles BabelString instance of self.STRING_CLASS from
        `s` (converted to plain unicode string), using e or style as
        typographic parameters. Ignore and just answer `s` if it is already a
        self.STRING_CLASS instance."""
        if not isinstance(s, self.STRING_CLASS):
            # Otherwise convert s into plain string, from whatever it is now.
            s = str(s)
            s = self.STRING_CLASS.newString(s, context=self, e=e,
                    style=style, w=w, h=h, pixelFit=pixelFit)
        assert isinstance(s, self.STRING_CLASS)
        return s

    def fitString(self, s, e=None, style=None, w=None, h=None, pixelFit=True):
        """Creates a new styles BabelString instance of self.STRING_CLASS from
        s assuming that style['font'] is a Variable Font instnace, or a path
        pointing to one. If the for is not a VF, then behavior is the same as
        newString. (converted to plain unicode string), using e or style as
        typographic parameters. Ignore and just answer s if it is already a
        `self.STRING_CLASS` instance.
        """
        if not isinstance(s, self.STRING_CLASS):
            # Otherwise convert s into plain string, from whatever it is now.
            s = str(s)
            s = self.STRING_CLASS.fitString(s, context=self, e=e, style=style, w=w, h=h,
                pixelFit=pixelFit)
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

    #   G L Y P H

    def intersectWithLine(self, glyph, line):
        """Answers the sorted set of intersecting points between the straight
        line and the flatteded glyph path."""
        intersections = set() # As set,  make sure to remove any doubles.

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        (lx0, ly0), (lx1, ly1) = line
        maxX = max(lx0, lx1)
        minX = min(lx0, lx1)
        maxY = max(ly0, ly1)
        minY = min(ly0, ly1)
        glyphPath = self.getGlyphPath(glyph)
        contours = self.getFlattenedContours(glyphPath)
        if not contours:
            # Could not generate path or flattenedPath. Or there are no
            # contours. Give up.
            return None
        for contour in contours:
            for n in range(len(contour)):
                pLine = contour[n], contour[n-1]
                (px0, py0), (px1, py1) = pLine
                if minY > max(py0, py1) or maxY < min(py0, py1) or minX > max(px0, px1) or maxX < min(px0, px1):
                    continue # Skip if boundings boxes don't overlap.

                xdiff = (line[0][0] - line[1][0], pLine[0][0] - pLine[1][0])
                ydiff = (line[0][1] - line[1][1], pLine[0][1] - pLine[1][1])

                div = det(xdiff, ydiff)
                if div == 0:
                   continue # No intersection

                d = (det(*line), det(*pLine))
                intersections.add((det(d, xdiff) / div, det(d, ydiff) / div))

        # Answer the set as sorted list, increasing x, from left to right.
        return sorted(intersections)

    #   P A T H

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
        """Answers the current screen size."""
        return None

    # Gradient & Shadow.

    # Animation.

    def frameDuration(self, secondsPerFrame):
        raise NotImplementedError

    # Fonts.

    # Canvas.

    def save(self):
        raise NotImplementedError

    def restore(self):
        raise NotImplementedError

    # Text

    def hyphenation(self, onOff):
        raise NotImplementedError

    def language(self, language):
        raise NotImplementedError

    # Document.

    def newDocument(self, w, h):
        raise NotImplementedError

    def saveDocument(self, path, multiPage=None):
        raise NotImplementedError

    def newPage(self, w, h):
        raise NotImplementedError

    def newDrawing(self):
        raise NotImplementedError

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

    # Drawing.

    def rect(self, x, y, w, h):
        raise NotImplementedError

    def oval(self, x, y, w, h):
        raise NotImplementedError

    def circle(self, x, y, r):
        raise NotImplementedError

    def line(self, p1, p2):
        raise NotImplementedError

    def polygon(self, *points, **kwargs):
        raise NotImplementedError

    def newPath(self):
        raise NotImplementedError
    def drawPath(self, path=None, p=None, sx=1, sy=None):
        raise NotImplementedError
    #def clipPath(self, clipPath):
    #def roundedRect(self, x, y, w, h, offset=25):
    #def bluntCornerRect(self, x, y, w, h, offset=5):
    #def drawGlyphPath(self, glyph):
    #def getGlyphPath(self, glyph, p=None, path=None):

    # Color.

    def fill(self, c):
        raise NotImplementedError

    def stroke(self, c, w=None):
        raise NotImplementedError

    def strokeWidth(self, w):
        raise NotImplementedError

    def colorSpace(self, colorSpace):
        raise NotImplementedError

    def listColorSpaces(self):
        raise NotImplementedError

    def blendMode(self, operation)
        raise NotImplementedError

    # def miterLimit(self, value):
    # def lineJoin(self, value):
    # def lineCap(self, value):
    # def lineDash(self, *value):

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

    # Image.

    def image(self, path, p, alpha=1, pageNumber=None, w=None, h=None):
        raise NotImplementedError

    #def imagePixelColor(self, path, p):

    def imageSize(self, path):
        raise NotImplementedError

    #def numberOfImages(self, path):
    #def getImageObject(self, path):

    # Objects.

    def BezierPath(self, path=None, glyphSet=None):
        raise NotImplementedError

    def ImageObject(self, path=None):
        raise NotImplementedError

    def Variable(self, ui, globals):
        """Offers interactive global value manipulation in DrawBot. Can be
        ignored in other contexts."""
        pass

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
