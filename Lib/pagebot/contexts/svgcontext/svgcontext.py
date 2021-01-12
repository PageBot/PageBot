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
#     Supperting usage of Svg, https://pypi.python.org/pypi/svgwrite
# -----------------------------------------------------------------------------
#
#     svgcontext.py
#
#     https://svgwrite.readthedocs.io
#

import shutil
from pagebot.constants import (DEFAULT_FONT_SIZE, DEFAULT_LANGUAGE,
        FILETYPE_SVG, EXPORT)
from pagebot.contexts.svgcontext.svgbuilder import svgBuilder
from pagebot.contexts.basecontext.basecontext import BaseContext
from pagebot.contexts.svgcontext.svgbezierpath import SvgBezierPath
from pagebot.contexts.basecontext.babelstring import BabelString
from pagebot.fonttoolbox.fontpaths import getDefaultFontPath
from pagebot.toolbox.color import noColor, color
from pagebot.toolbox.dating import seconds
from pagebot.toolbox.transformer import uniqueID
from pagebot.toolbox.units import pt, upt, point2D

class SvgContext(BaseContext):
    """The SvgContext implements SVG functionality within the PageBot framework
    using the svgwrite library to export a drawing."""


    # Indication to Typesetter that by default tags should be included in
    # output.
    useTags = True

    TMP_PATH = '/tmp/pagebot%s.' + FILETYPE_SVG

    # Used by the generic BaseContext.newString( )
    STRING_CLASS = BabelString
    EXPORT_TYPES = (FILETYPE_SVG,)
    VALID_EXTENSIONS = ('svg', 'svgz')

    def __init__(self):
        """Constructor of SvgContext.

        >>> context = SvgContext()
        >>> context.newPage(1000, 1000)
        >>> context.saveDrawing('_export/SvgContext.%s' % FILETYPE_SVG)

        """
        super().__init__()
        self.b = svgBuilder
        self.name = self.__class__.__name__
        self._language = DEFAULT_LANGUAGE
        self._filePath = self.TMP_PATH % uniqueID()
        self.fill(noColor) # Sets self._svgFill
        self.stroke(noColor) # Sets self._svgStroke
        self._strokeWidth = pt(0)
        self._frameDuration = seconds(1)
        self._fontSize = DEFAULT_FONT_SIZE
        self._font = getDefaultFontPath()
        self._ox = pt(0) # Origin set by self.translate()
        self._oy = pt(0)
        self._rotate = 0
        self._gState = [] # Stack of graphic states.
        self.save() # Save current set of values on gState stack.
        self._numberOfPages = 1
        self._bezierpath = None # Hold current open SVG path
        self._w = None
        self._h = None
        self.drawing = []

    # Drawing.

    def newPage(self, w=None, h=None, doc=None, **kwargs):
        """Create a new SVG page.

        TODO: test with document as argument.

        >>> context = SvgContext()
        >>> context.newPage(1000, 1000)
        """
        self._w = upt(w)
        self._h = upt(h)

        # Copies document dimensions if available.
        if doc is not None:
            w = w or doc.w
            h = h or doc.h

        svgDrawing = self.newSvgDrawing(w=w, h=h)
        self.drawing.append(svgDrawing)
        self._numberOfPages += 1

    def newDrawing(self, w=None, h=None, doc=None):
        pass

    def newSvgDrawing(self, w=None, h=None, doc=None):
        """The @doc is the optional Document instance of the calling function. Clear
        output canvas, start new export file.

        >>> context = SvgContext()
        >>> drawing = context.newDrawing(1000, 1000)
        """
        size = (self._w, self._h)
        drawing =  self.b.Drawing(self._filePath, size=size, profile='tiny')
        self._drawing = drawing
        return drawing

    def endDrawing(self):
        pass

    def _get_width(self):
        return self._w

    width = property(_get_width)

    def _get_height(self):
        return self._h

    height = property(_get_height)

    # Save / export.

    def saveDrawing(self, path, multiPage=None):
        """Select other than standard DrawBot export builders here. Save the
        current image as path, rendering depending on the extension of the path
        file. In case the path starts with "_export", then create it
        directories.

        >>> context = SvgContext()
        >>> context.newPage(1000, 1000)
        >>> context.saveImage('_export/MyFile.svg')

        """
        # Only save to SVG for now. Maybe use Flat context to save PDF / bitmap?
        parts = path.split('.')
        ext = parts[-1]
        assert ext.lower() == 'svg'
        self._drawing.save()
        self.checkExportPath(path)
        shutil.move(self._filePath, path)

    saveImage = saveDrawing # Compatible API with DrawBot

    def export(self, fileName, folderName=None, extension=None):
        """Saves file to filename with default folder name and extension."""
        if not folderName:
            folderName = EXPORT
        if not extension:
            extension = 'svg'

        assert extension in self.VALID_EXTENSIONS

        path = '%s/%s.%s' % (folderName, fileName, extension)
        self.saveImage(path)

    def getDrawing(self):
        """Returns the drawing object in the current state."""
        return self._drawing

    def pageCount(self):
        return self._numberOfPages

    def newPath(self):
        """
        TODO: wrap in a compatible SvgBezierPath object.

        >>> context = SvgContext()
        >>> context.newPage(1000, 1000)
        >>> path = context.newPath()
        >>> from svgwrite.path import Path
        >>> isinstance(path, Path)
        True
        """
        self._bezierpath = SvgBezierPath(self.b)
        return self._bezierpath

    def moveTo(self, p):
        """Move to point `p` in the open path. Create a new self._bezierpath if none
        is open.
        """
        p = self.translatePoint(p)
        super().moveTo(p)

    def lineTo(self, p):
        """Line to point p in the open path. Create a new self._bezierpath if none
        is open.
        """
        print('lineTo')

    def curveTo(self, bcp1, bcp2, p):
        """Curve to point p i nthe open path. Create a new path if none is
        open."""
        bcp1 = self.translatePoint(bcp1)
        bcp2 = self.translatePoint(bcp2)
        p = self.translatePoint(p)
        super().curveTo(bcp1, bcp2, p)

    def qCurveTo(self, *points):
        """
        """

    def arc(self, center, radius, startAngle, endAngle, clockwise):
        """
        """

    def arcTo(self, xy1, xy2, radius):
        """
        """

    def rect(self, x, y, w, h):
        """Draw a rectangle in the canvas.

        >>> from pagebot.toolbox.color import Color
        >>> path = '_export/SvgContext_rect.svg'
        >>> context = SvgContext()
        >>> context.newPage(1000, 1000)
        >>> context.fill((color(r=1, g=0, b=0.5)))
        >>> context.rect(pt(0), pt(100), pt(600), pt(200))
        >>> context.stroke((0.4, 0.6, 0.1), pt(20))
        >>> context.fill((color(r=0.4, g=0.1, b=0.9)))
        >>> context.rect(pt(300), pt(150), pt(400), pt(600))
        >>> context.saveDrawing(path)
        >>> #r = os.system('open %s' % path)
        """
        rect = self._drawing.rect(insert=((self._ox+x).pt, (self._oy+y).pt), size=(w.pt, h.pt),
                           stroke_width=upt(self._strokeWidth),
                           stroke=self._svgStroke, fill=self._svgFill)
        self._drawing.add(rect)

    def oval(self, x, y, w, h):
        """Draw an oval in rectangle, where (x, y) is the bottom-left and size
        (w, h).

        >>> from pagebot.toolbox.color import color, blackColor
        >>> path = '_export/SvgContext_oval.svg'
        >>> context = SvgContext()
        >>> context.newPage(1000, 1000)
        >>> context.fill(color(r=1, g=0, b=0.5))
        >>> context.oval(pt(0), pt(100), pt(600), pt(200))
        >>> context.stroke(blackColor, pt(20))
        >>> context.fill(color(r=0.4, g=0.1, b=0.9))
        >>> context.oval(pt(300), pt(150), pt(400), pt(600))
        >>> context.saveDrawing(path)
        >>> #r = os.system('open %s' % path)
        """
        oval = self._drawing.ellipse(center=upt((self._ox+x+w/2),
            (self._oy+y+h/2)), r=upt((w/2), (h/2)),
            stroke_width=upt(self._strokeWidth), stroke=self._svgStroke,
            fill=self._svgFill)
        self._drawing.add(oval)

    def circle(self, x, y, r):
        """Circle draws a DrawBot oval with (x,y) as middle point and radius r.

        >>> from pagebot.toolbox.color import color, blackColor
        >>> path = '_export/SvgContext_circle.svg'
        >>> context = SvgContext()
        >>> context.newPage(1000, 1000)
        >>> context.fill(color(r=1, g=0, b=0.5))
        >>> context.circle(pt(0), pt(100), pt(300))
        >>> context.stroke(blackColor, pt(20))
        >>> context.fill(color(r=0.6, g=0.1, b=0.5))
        >>> context.circle(pt(300), pt(150), pt(200))
        >>> context.saveDrawing(path)
        >>> #r = os.system('open %s' % path)
        """
        circle = self._drawing.circle(center=upt((self._ox+x+r),
            (self._oy+y+r)), r=upt(r), stroke_width=upt(self._strokeWidth),
            stroke=self._svgStroke, fill=self._svgFill)
        self._drawing.add(circle)

    def line(self, p1, p2):
        """Draw a line from p1 to p2.

        >>> path = '_export/SvgContext_line.svg'
        >>> context = SvgContext()
        >>> context.newPage(1000, 1000)
        >>> context.stroke((1, 0, 0.5), 30)
        >>> context.line((0, 100), (300, 300))
        >>> context.stroke((0.6, 0.1, 0.5), 20)
        >>> context.line((300, 150), (200, 100))
        >>> context.saveDrawing(path)
        >>> #r = os.system('open %s' % path)
        """
        line = self._drawing.line(upt((self._ox+p1[0]), (self._oy+p1[1])),
                upt((self._ox+p2[0]), (self._oy+p2[1])),
                stroke_width=upt(self._strokeWidth), stroke=self._svgStroke)
        self._drawing.add(line)

    def fill(self, c):
        c = color(c)
        if c is noColor:
            self._svgFill = 'none'
        else:
            r, g, b = c.rgb
            self._svgFill = self.b.rgb(100*r, 100*g, 100*b, '%')

    setFillColor = fill
    cmykFill = fill

    def stroke(self, c, strokeWidth=None):

        if c is noColor:
            self._svgStroke = 'none'
        else:
            c = color(c)
            r, g, b = c.rgb
            self._svgStroke = self.b.rgb(100*r, 100*g, 100*b, '%')

        self._strokeWidth = upt(strokeWidth or pt(1))

    setStrokeColor = stroke
    cmykStroke = stroke

    def saveGraphicState(self):
        """Save the current graphic state.

        >>> context = SvgContext()
        >>> context.newPage(1000, 1000)
        >>> context.font('PageBot-Regular')
        >>> context._font
        'PageBot-Regular'
        >>> context.save()
        >>> context.font('PageBot-Bold')
        >>> context._font
        'PageBot-Bold'
        >>> context.restore()
        >>> context._font
        'PageBot-Regular'
        """
        gState = dict(
            font=self._font,
            fontSize=self._fontSize,
            svgFill=self._svgFill,
            svgStroke=self._svgStroke,
            strokeWidth=self._strokeWidth,
            ox=self._ox,
            oy=self._oy,
            rotate=self._rotate,
        )
        self._gState.append(gState)

    save = saveGraphicState

    def restoreGraphicState(self):
        gState = self._gState.pop()
        self._font = gState['font']
        self._fontSize = gState['fontSize']
        self._svgFill = gState['svgFill']
        self._svgStroke = gState['svgStroke']
        self._strokeWidth = gState['strokeWidth']
        self._ox = gState['ox']
        self._oy = gState['oy']
        self._rotate = gState['rotate']

    restore = restoreGraphicState

    #   T E X T

    def fontSize(self, fontSize):
        """Set the current graphic state to fontSize.

        """
        self._fontSize = fontSize

    def font(self, font, fontSize=None):
        """Set the current graphic state to font.

        TODO: Make this match the font.path.
        """
        self._font = font
        if fontSize is not None:
            self.fontSize(fontSize)

    def text(self, sOrBs, p):
        """Draw the sOrBs text string, can be a str or BabelString, including a
        DrawBot FormattedString at position p.

        >>> path = '_export/SvgContext_text.svg'
        >>> context = SvgContext()
        >>> context.newPage(1000, 1000)
        >>> context.fontSize(pt(100))
        >>> context.font('PageBot-Bold') # TODO: Match with font path.
        >>> context.fill(color(r=1, g=0, b=0.5))
        >>> context.text('ABCDEF', pt(100, 200))
        >>> context.fill(color(r=1, g=0, b=1))
        >>> context.stroke(color(r=0.5, g=0, b=0.5), pt(5))
        >>> context.text('ABCDEF', (pt(100), pt(300)))
        >>> context.saveDrawing(path)
        >>> #r = os.system('open %s' % path)

        """
        if not isinstance(sOrBs, str):
            sOrBs = sOrBs.s # Assume here is's a BabelString with a FormattedString inside.
        t = self._drawing.text(sOrBs, insert=point2D(upt(p)),
                               stroke=self._svgStroke, stroke_width=upt(self._strokeWidth),
                               fill=self._svgFill, font_size=upt(self._fontSize), font_family=self._font)
        self._drawing.add(t)

    def textBox(self, sOrBs, r):
        """Draw the sOrBs text string, can be a str or BabelString, including a
        DrawBot FormattedString in rectangle r."""
        if not isinstance(sOrBs, str):
            sOrBs = sOrBs.s # Assume here is's a BabelString with a FormattedString inside.
        x, y, w, h = r
        t = self._drawing.text(sOrBs, insert=point2D(upt(x, y)),
                               stroke=self._svgStroke, stroke_width=upt(self._strokeWidth),
                               fill=self._svgFill, font_size=upt(self._fontSize), font_family=self._font)
        self._drawing.add(t)

    def textOverflow(self, sOrBs, box, align=None):
        pass

    def getTextLines(self, bs, w=None, h=None):
        pass

    def textSize(self, bs, w=None, h=None):
        # https://stackoverflow.com/questions/24337531/how-to-determine-text-width-and-height-when-using-svgwrite-for-python
        pass

    def fromBabelString(self, bs):
        pass

    # Transformations.

    # TODO: implement actual transformations. Use own Transform3D (like
    # Flatcontext) or svgwrite.mixins.Transform?
    # im = svgwrite.drawing.Drawing()
    # g = svgwrite.container.Group(transform='translate(50,50)')
    # im.add(g)
    # g.add(im.line( start = (-10,-10),\
    #                 end   = (20,20),\
    #                 stroke= 'black'))
    # im.saveas('example.svg')

    def transform(self, matrix, center=(0, 0)):
        """NOTE: not used, implemented as a transform3D object for now."""

    def translate(self, dx, dy):
        """Translate the origin by (dx, dy)."""
        self._ox += dx
        self._oy += dy

    def rotate(self, angle):
        """Rotate by angle."""
        self._rotate = angle

    def scale(self, sx=1, sy=None, center=(0, 0)):
        self._sx = self._sx * sx
        sy = sy or sx
        self._sy = self._sy * sy
        self._scaleCenter = center
        self._strokeWidth = self._strokeWidth * sx

    def textSize(self, s):
        # FIXME: this is wrong.
        return pt(100, 20)

    def skew(self, angle1, angle2=0, center=(0, 0)):
        pass

    #   A N I M A T I O N

    #   https://svgwrite.readthedocs.io/en/latest/classes/animate.html

    def frameDuration(self, secondsPerFrame):
        """Set the frame duration for animated gifs to a number of seconds per
        frame."""
        self._frameDuration = secondsPerFrame

    # Paths.

    def getFlattenedPath(self, path=None):
        pass

    def getFlattenedContours(self, path=None):
        pass

    def getGlyphPath(self, glyph, p=None, path=None):
        pass


    def drawPath(self, path=None, p=None, sx=1, sy=None):
        # TODO: call drawing.path() inside SvgBezierPath.draw()
        #bezierpath = self._drawing.path()
        print(self._bezierpath)
    #

    def shadow(self, eShadow, e=None):
        pass

    def linearGradient(self, startPoint=None, endPoint=None, colors=None,
            locations=None):
        pass

    cmykShadow = shadow
    cmykLinearGradient = linearGradient
    cmykRadialGradient = linearGradient

    def setStyles(self, styles):
        pass

    # System fonts listing, installation, font properties.

    def installedFonts(self, patterns=None):
        """Should Answer the list of all fonts (name or path) that are
        installed on the OS."""

    def installFont(self, fontOrName):
        """Should install the font in the context. fontOrName can be a Font
        instance (in which case the path is used) or a full font path."""

    def uninstallFont(self, fontOrName):
        pass

    def fontContainsCharacters(self, characters):
        pass

    def fontContainsGlyph(self, glyphName):
        pass

    def fontFilePath(self):
        pass

    def listFontGlyphNames(self):
        pass

    def fontAscender(self):
        pass

    def fontDescender(self):
        pass

    def fontXHeight(self):
        pass

    def fontCapHeight(self):
        pass

    def fontLeading(self):
        pass

    def fontLineHeight(self):
        pass

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
