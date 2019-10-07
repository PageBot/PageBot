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
#	  variablescatter.py
#

from random import random, choice
from pagebot.elements.element import Element
from pagebot.style import makeStyle
from pagebot.toolbox.units import pointOffset
from pagebot.toolbox.color import blackColor


class VariableScatter(Element):
    """
    >>> from pagebot.fonttoolbox.objects.font import findFont
    >>> from pagebot.document import Document
    >>> vfFont = findFont('RobotoDelta_v2-VF')
    >>> from pagebot.fonttoolbox.objects.font import findFont
    >>> doc = Document(w=500, h=500, originTop=False, autoPages=1)
    >>> page = doc[1]
    >>> page.padding = 40
    >>> vc = VariableScatter(vfFont, parent=page, x=40, y=40, w=page.pw)
    """
    # Initialize the default behavior tags as different from Element.

    def __init__(self, s=None, style=None,
                 sizeX=5, sizeY=5, recipeAxes=None,
                 designSpace=None, locations=None, **kwargs):
        Element.__init__(self, **kwargs)
        self.style = makeStyle(style, **kwargs) # Combine self.style from
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.recipeAxes = recipeAxes # Ordered name list of axes to show in legenda. Ignore if None.
        self.designSpace = designSpace or {}
        self.locations = locations
        # Each element should check at this point if the minimum set of style values
        # are set and if their values are valid.
        assert self.w is not None and self.h is not None # Make sure that these are defined.
        # Make sure that this is a formatted string. Otherwise create it with the current style.
        # Note that in case there is potential clash in the double usage of fill and stroke.
        self.glyphNames = s or 'e'
    
    def location2Recipe(self, location, start=0, end=3):
        recipe = ''
        if self.recipeAxes:
            for name in self.recipeAxes[start:end]:
                if name in location:
                    recipe += '%s %d\n' % (name, location[name])
        return recipe

    def getRandomLocation(self):
        RANGE = 1000
        location = {}
        for axisName in self.font.axes.keys():
            if axisName in self.designSpace:
                minValue, maxValue = self.designSpace[axisName]
            else:
                minValue = 0
                maxValue = RANGE
            value = minValue + random() * (maxValue - minValue)
            location[axisName] = value

        return location

    def draw(self, view, origin):
        c = self.doc.context

        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)    
        px, py, _ = self._applyAlignment(p) # Ignore z-axis for now.

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        fillColor = self.style.get('fill')
        if fillColor is not None:
            c.fill(fillColor)
        c.stroke(None)

        stepX = self.w / (self.sizeX+1)
        stepY = self.h / (self.sizeY+1)
        """Add more parametric layout behavior here."""
        for indexX in range(self.sizeX+1):
            for indexY in range(self.sizeY+1):
                ox = 30
                oy = 25
                ppx = ox + px + indexX * stepX
                ppy = oy + py + indexY * stepY
                if self.locations is not None:
                    location = choice(self.locations)
                else:
                    location = self.getRandomLocation()
                glyphPathScale = self.fontSize/self.font.info.unitsPerEm
                fillColor = self.style.get('textFill') or (0, 0, 0)
                c.drawGlyphPath(self.font.ttFont, self.glyphNames[0],
                              px, py, location, s=glyphPathScale,
                              fillColor=fillColor)
                if self.recipeAxes:
                    recipe = self.location2Recipe(location)
                    bs = c.newString(recipe, fontSize=4, fill=blackColor)
                    w, h = bs.size()
                    c.text(bs, ppx - stepX/4, ppy - 24) # Bit of hack, we need the width of the glyph here.
                    if len(self.recipeAxes) > 3:
                        recipe = self.location2Recipe(location, 3, 6)
                        bs = c.newString(recipe, fontSize=4, fill=blackColor)
                        w, h = bs.size()
                        c.text(bs, point=(ppx - stepX/4 + 30, ppy - 24)) # Bit of hack, we need the width of the glyph here.

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
