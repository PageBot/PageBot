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
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
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

class SvgContext(BaseContext):
    u"""An SvgContext uses svgwrite to export as SVG drawing."""

    # In case of specific builder addressing, callers can check here.
    isSvg = True

    TMP_PATH = '/tmp/pagebot%s.svg'

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
        >>> r = os.system('open %s' % path)
        """
        rect = self._drawing.rect(insert=(x, y), size=(w, h), 
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
        >>> r = os.system('open %s' % path)
        """
        oval = self._drawing.ellipse(center=(x+w/2, y+h/2), r=(w/2, h/2), 
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
        >>> r = os.system('open %s' % path)
        """
        circle = self._drawing.circle(center=(x+r, y+r), r=r, 
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
        >>> r = os.system('open %s' % path)
        """
        line = self._drawing.line(p1, p2, 
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
        pass

    save = saveGraphicState

    def restoreGraphicState(self):
        pass

    restore = restoreGraphicState
    
    #   A N I M A T I O N

    def frameDuration(self, secondsPerFrame):
        u"""Set the frame duretion for animated gifs to a number of seconds per frame."""
        self._frameDuration = secondsPerFrame

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
