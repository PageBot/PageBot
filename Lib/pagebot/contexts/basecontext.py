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
from pagebot.constants import (DISPLAY_BLOCK, DEFAULT_FRAME_DURATION)
from pagebot.toolbox.units import upt, pt, point2D
from pagebot.contexts.abstractdrawbotcontext import AbstractDrawBotContext

class BaseContext(AbstractDrawBotContext):
    """Extends the DrawBot interface.
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

    def __init__(self):
        self._path = None # Hold current open DrawBot path.

    def newDocument(self, w, h):
        raise NotImplementedError

    def saveDocument(self, path, multiPage=None):
        raise NotImplementedError

    def newString(self, s, e=None, style=None, w=None, h=None, pixelFit=True):
        """Creates a new styles BabelString instance of self.STRING_CLASS from
        `s` (converted to plain unicode string), using e or style as
        typographic parameters. Ignore and just answer `s` if it is already a
        self.STRING_CLASS instance and no style is forced."""
        if not isinstance(s, self.STRING_CLASS):
            # Otherwise convert s into plain string, from whatever it is now.
            s = self.STRING_CLASS.newString(str(s), context=self, e=e,
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
                if minY > max(py0, py1) or maxY < min(py0, py1) or \
                        minX > max(px0, px1) or maxX < min(px0, px1):
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
        do nothing.

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> size = context.screenSize()
        >>> size[0] > 100 and size[1] > 100
        True
        """
        return pt(self.b.sizes().get('screen', None))

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


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
