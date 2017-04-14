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
#	  variationcircle.py
#
#     Draw a variation space default glyph in the middle and spikes around it fir each axis.
#     The aim is to derive as much information directly from the font, without the need
#     for additional parameters.
#
from __future__ import division

import os
from math import pi, sin, cos
from random import random, choice
from copy import copy

from fontTools.ttLib import TTFont

from drawBot import fill, rect, oval, stroke, strokeWidth, installFont, installedFonts, FormattedString, moveTo, lineTo, newPath, drawPath

from pagebot.elements.element import Element
from pagebot.style import makeStyle
from pagebot.fonttoolbox.variationbuilder import generateInstance, drawGlyphPath
from pagebot.toolbox.transformer import pointOffset

class VariationCircle(Element):
    u"""Interpret the content of the self.font variation font and draw a circle info graphic on that info."""

    DEFAULT_FONT_SIZE = 64
    R = 2/3 # Fontsize factor to draw glyph markers.

    def __init__(self, font, point=None, parent=None, style=None, eId=None, s=None, **kwargs):
        Element.__init__(self, point=point, parent=parent, style=style, eId=eId, **kwargs)
        # Initialize the default Element behavior tags.
        self.isContainer = False
        self.isText = False
        self.isFlow = False
        self.font = font
        self.glyphNames = s or 'e'
    
    def location2Recipe(self, location, start=0, end=3):
        recipe = ''
        if self.recipeAxes:
            for name in self.recipeAxes[start:end]:
                if name in location:
                    recipe += '%s %d\n' % (name, location[name])
        return recipe

    def _angle2XY(self, angle, r):
        u"""Answer the XY position for a given angled (degrees) and r, located on the origin."""
        return cos(angle/180*pi) * r, sin(angle/180*pi) * r

    def _drawGlyphMarker(self, mx, my, glyphName, fontSize, location, strokeW=2):
        # Middle circle 
        fill(1)
        stroke(0)
        strokeWidth(strokeW)
        oval(mx-fontSize*self.R, my-fontSize*self.R, fontSize*2*self.R, fontSize*2*self.R)

        glyphPathScale = fontSize/self.font.info.unitsPerEm
        drawGlyphPath(self.font.ttFont, glyphName, mx, my-fontSize/4, location, s=glyphPathScale, fillColor=0)

    def draw(self, origin):
        u"""Draw the circle info-graphic, showing most info about the variation font as can be interpreted from the file."""
        p = pointOffset(self.point, origin)
        p = self._applyOrigin(p)    
        p = self._applyScale(p)    
        px, py, _ = self._applyAlignment(p) # Ignore z-axis for now.
   
        fill(0.9)
        stroke(None)
        mx = px + self.w/2
        my = py + self.h/2
        # Gray circle that defines the area of
        oval(px, py, self.w, self.h)
        # Draw axis spikes first, so we can cover them by the circle markers.
        angle = 0
        axes = self.font.axes
        fill(None)
        stroke(0)
        strokeWidth(1)
        newPath()
        while angle < 360:
            markerX, markerY = self._angle2XY(angle, self.w/2)
            moveTo((mx, my))
            lineTo((mx+markerX, my+markerY))
            angle += 360/len(axes)
        drawPath()

        # Draw default glyph marker in middle.
        glyphName = self.glyphNames[0]
        fontSize = self.style.get('fontSize', self.DEFAULT_FONT_SIZE)
        defaultLocation = {}
        self._drawGlyphMarker(mx, my, glyphName, fontSize, defaultLocation, strokeW=3)

        angle = 0
        for axisName, (minValue, defaultValue, maxValue) in axes.items():
            location = {axisName: maxValue}
            markerX, markerY = self._angle2XY(angle, self.w/2)
            self._drawGlyphMarker(mx+markerX, my+markerY, glyphName, fontSize/2, location)
            angle += 360/len(axes)

        self._restoreScale()



		