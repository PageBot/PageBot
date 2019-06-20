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
# -----------------------------------------------------------------------------
#
#     cube.py
#


from pagebot.elements.variablefonts.basefontshow import BaseFontShow
from pagebot.constants import LEFT, RIGHT, TOP, CENTER # Used for axis direction in the cube
from pagebot.toolbox.units import pointOffset
from pagebot.fonttoolbox.objects.font import getInstance

class Cube(BaseFontShow): 
    """Showing the specified (variable) font as full page with a matrix
    of all glyphs in the font.

    Usage of standard style parameters
    fill        Fill color for the background of the element
    stroke      Draw frame around the element
    textFill    Color of the text. Default is black.
    padding     Use in case of background color or frame. Default is 0

    """
    def __init__(self, f, label=None, dx=None, dy=None, steps=None, axes=None, **kwargs):
        """   
        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> from pagebot.document import Document
        >>> from pagebot.constants import Letter
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> from pagebot.conditions import *
        >>> from pagebot.toolbox.units import em
        >>> from pagebot.toolbox.color import color
        >>> c = DrawBotContext()
        >>> w, h = Letter
        >>> doc = Document(w=w, h=h, padding=80, originTop=False, autoPages=2, context=c)
        >>> style = dict(fill=color(0.95), leading=em(1.4), fontSize=28)
        >>> conditions = [Fit()]
        >>> page = doc[1]
        >>> font1 = findFont('AmstelvarAlpha-VF')
        >>> gs = Cube(font1, parent=page, conditions=conditions, padding=50, steps=4, style=style, label="An", context=c)
        >>> style = dict(stroke=0, strokeWidth=0.25, fontSize=24, leading=em(1.4))
        >>> page = doc[2]
        >>> font2 = findFont('RobotoDelta-VF')
        >>> gs = Cube(font2, parent=page, conditions=conditions, style=style, steps=3, padding=40, context=c)
        >>> score = doc.solve()
        >>> doc.export('_export/%sCube.pdf' % font1.info.familyName)
        >>> #doc.export('_export/%sCube.svg' % font1.info.familyName)
        >>> #doc.export('_export/%sCube.gif' % font1.info.familyName)
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

    def build(self, view, origin, drawElements=True, **kwargs):
        """Default drawing method just drawing the frame.
        Probably will be redefined by inheriting element classes."""
        c = self.context
        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        p = self._applyAlignment(p) # Ignore z-axis for now.

        self.buildFrame(view, p) # Draw optional background fill, frame or borders.

        # Let the view draw frame info for debugging, in case view.showFrame == True
        view.drawElementFrame(self, p) 

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        # Draw that actual content of the element by stacked specimen rectangles.
        self.drawCube(view, p, **kwargs)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreScale(view)
        view.drawElementInfo(self, origin) # Depends on flag 'view.showElementInfo'

    def drawCube(self, view, origin, **kwargs):
        """Draw the content of the element, responding to size, styles, font and content.
        Create 2 columns for the self.fontSizes ranges that show the text with and without [opsz]
        if the axis exists.

        TODO: 
        If the axis does not exist or not selected, do something else with the right column
        Add optional relation between VF-axes and cube ribs
        Automatic calculation of incrementing opsz range
        Add axis labels and/or values
        Draw the cube as lines and panes.
        Auto center vertical and horizontal
        Auto fontSize calculation
        Export as animation of rotating cube.
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
        #opszRange = (8, 10, 12, 14, 16, 18, 22, 24, 28, 32, 36, 42, 48, 56, 64)

        for xzStep in range(self.steps):
            for yStep in range(self.steps):
                # Draw right side of the cube.
                opsz = opszRange[yStep]
                x = ox + mx + xzStep * dx 
                y = oy + my + xzStep * dy + 2 * yStep * dy
                # Calculate the location
                location = self.getLocation(wght=-xzStep/2+1, wdth=1, opsz=opsz)
                instance = getInstance(self.f, location)
                #print(instance.location)
                style = dict(font=instance.path, fontSize=fontSize, xTextAlign=CENTER)
                bs = c.newString(self.label, style=style)
                tw, th = bs.size
                c.text(bs, (x-tw/2, y))

                if xzStep > 0: 
                    # Draw left side of the cube. Avoid double drawing on front axis
                    x = ox + mx - xzStep * dx 
                    location = self.getLocation(wght=1, wdth=-xzStep/2+1, opsz=opsz)
                    instance = getInstance(self.f, location)
                    style = dict(font=instance.path, fontSize=fontSize, xTextAlign=CENTER)
                    bs = c.newString(self.label, style=style)
                    tw, th = bs.size
                    c.text(bs, (x-tw/2, y))

        # Draw top part of the cube
        for xStep in range(1, self.steps):
            for zStep in range(1, self.steps):
                    x = ox + mx + xStep * dx - zStep * dx 
                    y = oy + my + (2 * self.steps - 2) * dy + xStep * dy + zStep * dy
                    
                    location = self.getLocation(wght=-xStep/2+1, wdth=-zStep/2+1, opsz=opsz)
                    instance = getInstance(self.f, location)
                    style = dict(font=instance.path, fontSize=fontSize, xTextAlign=CENTER)
                    bs = c.newString(self.label, style=style)
                    tw, th = bs.size
                    c.text(bs, (x-tw/2, y))




if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
