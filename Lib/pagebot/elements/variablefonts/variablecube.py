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
#	  variablecube.py
#

from copy import copy
from pagebot.elements.element import Element
from pagebot.style import makeStyle
from pagebot.toolbox.units import pointOffset
from pagebot.toolbox.color import blackColor


class VariableCube(Element):
    # Initialize the default behavior tags as different from Element.

    def __init__(self, font, s=None, point=None, style=None, eId=None, dimensions=None, location=None, **kwargs):
        self.__init__
        self.font = font
        self.eId = eId
        self.style = makeStyle(style, **kwargs) # Combine self.style from
        # Try to figure out the requested dimensions if the element display per axes.
        if dimensions is None:
            dimensions = dict(wght=4, wdth=6)
        self.dimensions = dimensions
        # Each element should check at this point if the minimum set of style values
        # are set and if their values are valid.
        assert self.w is not None and self.h is not None # Make sure that these are defined.
        # Make sure that this is a formatted string. Otherwise create it with the current style.
        # Note that in case there is potential clash in the double usage of fill and stroke.
        self.glyphNames = s or 'e'
        # Store the external location, to allow other axis values to be set.
        if location is None:
            location = {}
        self.location = copy(location)
    
    def draw(self, view, origin):
        c = self.doc.context

        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)    
        px, py, _ = self._applyAlignment(p) # Ignore z-axis for now.

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, (px, py))

        fillColor = self.style.get('fill')
        if fillColor is not None:
            c.fill(fillColor)
        else:
            c.fill(None)
        c.stroke((0.8, 0.8, 0.8), 0.5)
        c.rect(px, py, self.w, self.h)
        if len(self.dimensions) == 1:
            raise ValueError('Not supporting 1 axis now')
        if len(self.dimensions) > 2:
            raise ValueError('Not supporting >2 axis now')
        
        axisNames = sorted(self.dimensions.keys())
        axisX = axisNames[0]
        sizeX = self.dimensions[axisX]
        axisY = axisNames[1]
        sizeY = self.dimensions[axisY]
        stepX = self.w / (sizeX+1)
        stepY = self.h / (sizeY+1)
        """Add more parametric layout behavior here."""
        RANGE = 1000
        for indexX in range(sizeX+1):
            for indexY in range(sizeY+1):
                ox = 30
                oy = 25
                ppx = ox + px + indexX * stepX
                ppy = oy + py + indexY * stepY
                self.location[axisX] = indexX * RANGE / sizeX
                self.location[axisY] = indexY * RANGE / sizeY
                glyphPathScale = self.fontSize/self.font.info.unitsPerEm

                c.drawGlyphPath(self.font.ttFont, self.glyphNames[0], ppx, ppy, self.location, s=glyphPathScale, fillColor=(0, 0, 0))

                fs = c.newString('%s %d\n%s %d' % (axisX, indexX * RANGE / sizeX, axisY, indexY * RANGE / sizeY), fontSize=6, fill=blackColor)
                w, h = fs.size()
                c.text(fs, ppx - stepX/4, ppy - 16) # Bit of hack, we need the width of the glyph here.
        fs = c.newString('Other axes: %s' % self.location, fontSize=6, fill=blackColor)
        w, h = fs.size()
        c.text(fs, px, py - 16)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)



if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
