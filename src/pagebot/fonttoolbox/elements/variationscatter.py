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
#	  variationscatter.py
#
from __future__ import division

import os
from random import random, choice
from copy import copy
from fontTools.ttLib import TTFont
from pagebot.elements import Element
from pagebot.style import makeStyle
from pagebot.fonttoolbox.variationbuilder import generateInstance, drawGlyphPath
from drawBot import fill, rect, stroke, strokeWidth, installFont, installedFonts, FormattedString


class VariationScatter(Element):
    # Initialize the default behavior tags as different from Element.

    def __init__(self, font, s=None, style=None, eId=None, fontSize=72, sizeX=5, sizeY=5, showRecipe=False, designSpace=None, locations=None, **kwargs):
        self.font = font
        self.eId = eId
        self.style = makeStyle(style, **kwargs) # Combine self.style from
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.showRecipe = showRecipe
        self.fontSize = fontSize
        self.designSpace = designSpace or {}
        self.locations = locations
        # Each element should check at this point if the minimum set of style values
        # are set and if their values are valid.
        assert self.w is not None and self.h is not None # Make sure that these are defined.
        # Make sure that this is a formatted string. Otherwise create it with the current style.
        # Note that in case there is potential clash in the double usage of fill and stroke.
        self.glyphNames = s or 'e'
    
    def location2Recipe(self, location):
        recipe = ''
        for axisName, value in sorted(location.items()):
            recipe += '%s %d\n' % (axisName, value)
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

        return location,

    def draw(self, page, x, y):
        fillColor = self.style.get('fill')
        if fillColor is not None:
            setFillColor(fillColor)
            setStrokColor(None)

        stroke(0.8)
        strokeWidth(0.5)
        fill(None)
        rect(x, y, self.w, self.h)
        
        stepX = self.w / (self.sizeX+1)
        stepY = self.h / (self.sizeY+1)
        """Add more parametric layout behavior here."""
        for indexX in range(self.sizeX+1):
            for indexY in range(self.sizeY+1):
                ox = 30
                oy = 25
                px = ox + x + indexX * stepX
                py = oy + y + indexY * stepY
                if self.locations is not None:
                    location = choice(self.locations)
                else:
                    location = self.getRandomLocation()
                recipe = self.location2Recipe(location)
                glyphPathScale = self.fontSize/self.font.info.unitsPerEm
                drawGlyphPath(self.font.ttFont, self.glyphNames[0], px, py, location, s=glyphPathScale, fillColor=(0, 0, 0))
                if self.showRecipe:
                    fs = FormattedString(recipe, fontSize=6, fill=0)
                    w, h = fs.size()
                    page.text(fs, px - stepX/4, py - 24) # Bit of hack, we need the width of the glyph here.

		