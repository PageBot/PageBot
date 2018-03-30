#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supperting usage of Svg, https://pypi.python.org/pypi/svgwrite
# -----------------------------------------------------------------------------
#
#     svgcontext.py
#
#     https://svgwrite.readthedocs.io/en/master/
#
import os

from pagebot.toolbox.transformer import uniqueID
from pagebot.contexts.basecontext import BaseContext
from pagebot.contexts.builders.svgbuilder import svgBuilder
from pagebot.contexts.strings.htmlstring import HtmlString, DEFAULT_FONT_SIZE, DEFAULT_FONT_PATH

class SvgContext(BaseContext):
    u"""An SvgContext uses svgwrite to export as SVG drawing."""

    # In case of specific builder addressing, callers can check here.
    isSvg = True

    TMP_PATH = '/tmp/pagebot%s.svg'

    # Used by the generic BaseContext.newString( )
    STRING_CLASS = HtmlString

    def __init__(self):
        u"""Constructor of SvgContext.

        >>> context = SvgContext()
        >>> context.saveDocument('~/SvgContext.svg')

        """
        self.b = svgBuilder
        self._filePath = self.TMP_PATH % uniqueID()
        self._fill = 'none'
        self._stroke = 'none'
        self._strokeWidth = 0
        self._frameDuration = 1
        self._fontSize = DEFAULT_FONT_SIZE
        self._font = DEFAULT_FONT_PATH
        self._ox = 0 # Origin set by self.translate()
        self._oy = 0
        self._rotate = 0
        self._gState = [] # Stack of graphic states.
        self.save() # Save current set of values on gState stack.

        self.newDrawing()

        self._path = None # Hold current open SVG path

    def newDocument(self, w, h):
        u"""Ignore for SvgContext, as Drawing open automatic if first page is created."""
        pass

    def saveDocument(self, path, multiPage=None):
        u"""Select other than standard DrawBot export builders here.
        Save the current image as path, rendering depending on the extension of the path file.
        In case the path starts with "_export", then create it directories.

        >>> context = SvgContext()
        >>> context.saveImage('_export/MyFile.svg')

        """
        self._drawing.save()
        self.checkExportPath(path)
        os.system('mv %s %s' % (self._filePath, path))

    saveImage = saveDocument # Compatible API with DrawBot

    def newPage(self, w, h):
        u"""Create a new SVG page.

        >>> context = SvgContext()
        >>> context.newPage(100, 100)
        """

    def newDrawing(self):
        u"""Clear output canvas, start new export file.

        >>> context = SvgContext()
        >>> context.newDrawing()
        """
        self._drawing = self.b.Drawing(self._filePath, profile='tiny')

    def rect(self, x, y, w, h):
        u"""Draw a rectangle in the canvas.

        >>> path = '~/SvgContext_rect.svg'
        >>> context = SvgContext()
        >>> context.fill((1, 0, 0.5))
        >>> context.rect(0, 100, 600, 200)
        >>> context.stroke(0, 20)
        >>> context.fill((0.4, 0.1, 0.9))
        >>> context.rect(300, 150, 400, 600)
        >>> context.saveDocument(path)
        >>> #r = os.system('open %s' % path)
        """
        rect = self._drawing.rect(insert=(self._ox+x, self._oy+y), size=(w, h), 
                           stroke_width=self._strokeWidth,
                           stroke=self._stroke, fill=self._fill)
        self._drawing.add(rect)

    def oval(self, x, y, w, h):
        u"""Draw an oval in rectangle, where (x,y) is the bottom-left and size (w,h).

        >>> path = '~/SvgContext_oval.svg'
        >>> context = SvgContext()
        >>> context.fill((1, 0, 0.5))
        >>> context.oval(0, 100, 600, 200)
        >>> context.stroke(0, 20)
        >>> context.fill((0.4, 0.1, 0.9))
        >>> context.oval(300, 150, 400, 600)
        >>> context.saveDocument(path)
        >>> #r = os.system('open %s' % path)
        """
        oval = self._drawing.ellipse(center=(self._ox+x+w/2, self._oy+y+h/2), r=(w/2, h/2), 
                                             stroke_width=self._strokeWidth,
                                             stroke=self._stroke, fill=self._fill)
        self._drawing.add(oval)

    def circle(self, x, y, r):
        u"""Circle draws a DrawBot oval with (x,y) as middle point and radius r.

        >>> path = '~/SvgContext_circle.svg'
        >>> context = SvgContext()
        >>> context.fill((1, 0, 0.5))
        >>> context.circle(0, 100, 300)
        >>> context.stroke(0, 20)
        >>> context.fill((0.6, 0.1, 0.5))
        >>> context.circle(300, 150, 200)
        >>> context.saveDocument(path)
        >>> #r = os.system('open %s' % path)
        """
        circle = self._drawing.circle(center=(self._ox+x+r, self._oy+y+r), r=r, 
                                      stroke_width=self._strokeWidth, 
                                      stroke=self._stroke, fill=self._fill)
        self._drawing.add(circle)

    def line(self, p1, p2):
        u"""Draw a line from p1 to p2.

        >>> path = '~/SvgContext_line.svg'
        >>> context = SvgContext()
        >>> context.stroke((1, 0, 0.5), 30)
        >>> context.line((0, 100), (300, 300))
        >>> context.stroke((0.6, 0.1, 0.5), 20)
        >>> context.line((300, 150), (200, 100))
        >>> context.saveDocument(path)
        >>> #r = os.system('open %s' % path)
        """
        line = self._drawing.line((self._ox+p1[0], self._oy+p1[1]), (self._ox+p2[0], self._oy+p2[1]), 
                                  stroke_width=self._strokeWidth, 
                                  stroke=self._stroke, )
        self._drawing.add(line)

    def setFillColor(self, c):
        if isinstance(c, (int, float)):
            c = (c, c, c)
        if c is None:
            self._fill = 'none'
        else:
            r, g, b = c
            self._fill = self.b.rgb(100*r, 100*g, 100*b, '%')

    fill = setFillColor

    def setStrokeColor(self, c, strokeWidth=1):
        if isinstance(c, (int, float)):
            c = (c, c, c)
        if c is None:
            self._stroke = 'none'
        else:
            r, g, b = c
            self._stroke = self.b.rgb(100*r, 100*g, 100*b, '%')
            self._strokeWidth = strokeWidth

    stroke = setStrokeColor

    def saveGraphicState(self):
        u"""Save the current graphic state.

        >>> context = SvgContext()
        >>> context.font('Verdana')
        >>> context._font
        'Verdana'
        >>> context.save()
        >>> context.font('Verdana-Bold')
        >>> context._font
        'Verdana-Bold'
        >>> context.restore()
        >>> context._font
        'Verdana'
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
        )
        self._gState.append(gState)

    save = saveGraphicState

    def restoreGraphicState(self):
        gState = self._gState.pop()
        self._font = gState['font']
        self._fontSize = gState['fontSize']
        self._fill = gState['fill']
        self._stroke = gState['stroke']
        self._strokeWidth = gState['strokeWidth']
        self._ox = gState['ox']
        self._oy = gState['oy']
        self._rotate = gState['rotate']

    restore = restoreGraphicState
    
    #   T E X T 

    def fontSize(self, fontSize):
        u"""Set the current graphic state to fontSize.

        """
        self._fontSize = fontSize

    def font(self, font, fontSize=None):
        u"""Set the current graphic state to font. 
        TODO: Make this match the font.path.
        """
        self._font = font
        if fontSize is not None:
            self.fontSize(fontSize)

    def text(self, sOrBs, p):
        u"""Draw the sOrBs text string, can be a str or BabelString, including a DrawBot FormattedString
        at position p.

        >>> path = '~/SvgContext_text.svg'
        >>> context = SvgContext()
        >>> context.fontSize(100)
        >>> context.font('Verdana-Bold') # TODO: Match with font path.
        >>> context.fill((1, 0, 0.5))
        >>> context.text('ABCDEF', (100, 200))
        >>> context.fill((1, 0, 1))
        >>> context.stroke((0.5, 0, 0.5), 5)
        >>> context.text('ABCDEF', (100, 300))
        >>> context.saveDocument(path)
        >>> #r = os.system('open %s' % path)

        """
        if not isinstance(sOrBs, str):
            sOrBs = sOrBs.s # Assume here is's a BabelString with a FormattedString inside.
        t = self._drawing.text(sOrBs, insert=(p[0], p[1]), 
                               stroke=self._stroke, stroke_width=self._strokeWidth,
                               fill=self._fill, font_size=self._fontSize, font_family=self._font)
        self._drawing.add(t)

    def textBox(self, sOrBs, r):
        u"""Draw the sOrBs text string, can be a str or BabelString, including a DrawBot FormattedString
        in rectangle r."""
        if not isinstance(sOrBs, str):
            sOrBs = sOrBs.s # Assume here is's a BabelString with a FormattedString inside.
        x, y, w, h = r
        t = self._drawing.text(sOrBs, insert=(x, y),
                               stroke=self._stroke, stroke_width=self._strokeWidth,
                               fill=self._fill, font_size=self._fontSize, font_family=self._font)
        self._drawing.add(t)

    def translate(self, dx, dy):
        u"""Translate the origin by (dx, dy)."""
        self._ox += dx
        self._oy += dy

    def rotate(self, angle):
        u"""Rotate by angle."""
        self._rotate = angle

    def textSize(self, s):
        return 100, 20

    #   A N I M A T I O N

    def frameDuration(self, secondsPerFrame):
        u"""Set the frame duretion for animated gifs to a number of seconds per frame."""
        self._frameDuration = secondsPerFrame

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
