# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#	  variablecube.py
#
from __future__ import division

import os
from copy import copy
from fontTools.ttLib import TTFont
from pagebot.elements.element import Element
from pagebot.style import makeStyle
from pagebot.fonttoolbox.variablebuilder import generateInstance, drawGlyphPath
from drawBot import fill, rect, stroke, strokeWidth, installFont, installedFonts, FormattedString


class VariableCube(Element):
    # Initialize the default behavior tags as different from Element.

    def __init__(self, font, s=None, point=point, style=None, eId=None, dimensions=None, location=None, **kwargs):
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
    
    def draw(self, page, x, y):
        fillColor = self.style.get('fill')
        if fillColor is not None:
            setFillColor(fillColor)
            setStrokColor(None)

        stroke(0.8)
        strokeWidth(0.5)
        fill(None)
        rect(x, y, self.w, self.h)
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
                px = ox + x + indexX * stepX
                py = oy + y + indexY * stepY
                self.location[axisX] = indexX * RANGE / sizeX
                self.location[axisY] = indexY * RANGE / sizeY
                glyphPathScale = self.fontSize/self.font.info.unitsPerEm

                drawGlyphPath(self.font.ttFont, self.glyphNames[0], px, py, self.location, s=glyphPathScale, fillColor=(0, 0, 0))

                fs = FormattedString('%s %d\n%s %d' % (axisX, indexX * RANGE / sizeX, axisY, indexY * RANGE / sizeY), fontSize=6, fill=0)
                w, h = fs.size()
                page.text(fs, px - stepX/4, py - 16) # Bit of hack, we need the width of the glyph here.
        fs = FormattedString('Other axes: %s' % self.location, fontSize=6, fill=0)
        w, h = fs.size()
        page.text(fs, x, y - 16)

		