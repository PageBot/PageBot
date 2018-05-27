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
# -----------------------------------------------------------------------------
#
#     cube.py
#
from __future__ import division # Make integer division result in float.

from pagebot.elements.variablefonts.basefontshow import BaseFontShow
from pagebot.constants import LEFT, RIGHT, TOP, CENTER # Used for axis direction in the cube
from pagebot.toolbox.transformer import pointOffset

class Cube(BaseFontShow): 
    u"""Showing the specified (variable) font as full page with a matrix
    of all glyphs in the font.

    Usage of standard style parameters
    fill        Fill color for the background of the element
    stroke      Draw frame around the element
    textFill    Color of the text. Default is black.
    padding     Use in case of background color or frame. Default is 0

    """
    def __init__(self, f, label=None, dx=None, dy=None, steps=None, axes=None, **kwargs):
        u"""   
        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> from pagebot.document import Document
        >>> from pagebot.constants import Letter
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> from pagebot.conditions import *
        >>> c = DrawBotContext()
        >>> w, h = Letter
        >>> doc = Document(w=w, h=h, padding=80, originTop=False, autoPages=2, context=c)
        >>> style = dict(fill=0.95, rLeading=1.4, fontSize=28)
        >>> conditions = [Fit()]
        >>> page = doc[1]
        >>> font1 = findFont('AmstelvarAlpha-VF')
        >>> gs = Cube(font1, parent=page, conditions=conditions, padding=50, style=style, context=c)
        >>> style = dict(stroke=0, strokeWidth=0.25, fontSize=20, rLeading=1.4)
        >>> page = doc[2]
        >>> font2 = findFont('RobotoDelta-VF')
        >>> gs = Cube(font2, parent=page, conditions=conditions, style=style, steps=7, padding=40, context=c)
        >>> score = doc.solve()
        >>> doc.export('_export/%sCube.pdf' % font1.info.familyName)
        """
        BaseFontShow.__init__(self, **kwargs)
        self.f = f # Font instance
        self.label = label or 'Hn'
        self.steps = steps or 5
        self.dx = dx 
        self.dy = dy
        # Set the relation between the axes and the cube ribs
        if axes is None:
            axes = {LEFT: 'wght', RIGHT: 'wdth', TOP: 'opsz'}
        self.axes = axes

    def build(self, view, origin, drawElements=True):
        u"""Default drawing method just drawing the frame.
        Probably will be redefined by inheriting element classes."""
        c = self.context
        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(view, p)
        p = self._applyAlignment(p) # Ignore z-axis for now.

        self.buildFrame(view, p) # Draw optional background fill, frame or borders.

        # Let the view draw frame info for debugging, in case view.showElementFrame == True
        view.drawElementFrame(self, p) 

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        # Draw that actual content of the element by stacked specimen rectangles.
        self.drawCube(view, p)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreScale(view)
        view.drawElementMetaInfo(self, origin) # Depends on flag 'view.showElementInfo'

    def drawCube(self, view, origin):
        u"""Draw the content of the element, responding to size, styles, font and content.
        Create 2 columns for the self.fontSizes ranges that show the text with and without [opsz]
        if the axis exists.

        TODO: If the axis does not exist, do something else with the right column
        """

        c = self.context

        r = 20
        ox, oy, _ = origin
        mx = self.w/2
        my = self.pb
        dx = self.dx or self.pw/(2*self.steps-2)
        dy = self.dy or dx/2 + 6

        fontSize = self.css('fontSize', 24)
        opszRange = (8, 12, 20, 30, 45, 64, 96, 144)

        for xzStep in range(self.steps):
            for yStep in range(self.steps):
                opsz = opszRange[yStep]
                x = ox + mx + xzStep * dx 
                y = oy + my + xzStep * dy + 2 * yStep * dy
                # Calculate the location
                location = self.getLocation(wght=-xzStep/2+1, wdth=1, opsz=opsz)
                instance = self.getInstance(location)
                style = dict(font=instance.path, fontSize=fontSize, xTextAligh=CENTER)
                bs = c.newString(self.label, style=style)
                tw, th = bs.textSize()
                c.text(bs, (x-tw/2, y))

                if xzStep > 0:
                    x = ox + mx - xzStep * dx 
                    location = self.getLocation(wght=1, wdth=-xzStep/2+1, opsz=opsz)
                    instance = self.getInstance(location)
                    style = dict(font=instance.path, fontSize=fontSize, xTextAligh=CENTER)
                    bs = c.newString(self.label, style=style)
                    tw, th = bs.textSize()
                    c.text(bs, (x-tw/2, y))


                if yStep == self.steps-1: # Cover the top row
                    # TODO: Make the drawing of toplayer work.
                    tx = ox + mx + xzStep * dx 
                    ty = oy + my + xzStep * dy + 2 * self.steps * dy
                    location = self.getLocation(wght=-xzStep/2+1, wdth=-yStep/2+1, opsz=opsz)
                    instance = self.getInstance(location)
                    style = dict(font=instance.path, fontSize=fontSize, xTextAligh=CENTER)
                    bs = c.newString(self.label, style=style)
                    tw, th = bs.textSize()
                    c.text(bs, (x-tw/2, y))




if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
