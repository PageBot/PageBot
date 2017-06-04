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
#	  variablecircle.py
#
#     Draw a variable space default glyph in the middle and spikes around it fir each axis.
#     The aim is to derive as much information directly from the font, without the need
#     for additional parameters.
#
from __future__ import division

import os
from math import pi, sin, cos
from random import random, choice
from copy import copy

from fontTools.ttLib import TTFont

from drawBot import textSize, text, fill, rect, oval, stroke, strokeWidth, installFont, installedFonts, FormattedString, moveTo, lineTo, newPath, drawPath

from pagebot import newFS
from pagebot.elements.element import Element
from pagebot.style import makeStyle, MIN_WIDTH
from pagebot.fonttoolbox.variablefontbuilder import generateInstance, drawGlyphPath, getVariableFont
from pagebot.toolbox.transformer import pointOffset

class VariableCircle(Element):
    u"""Interpret the content of the self.font variable font and draw a circle info graphic on that info."""

    isText = False
    isFlow = False

    DEFAULT_FONT_SIZE = 64
    R = 2/3 # Fontsize factor to draw glyph markers.

    def __init__(self, font, s=None, **kwargs):
        Element.__init__(self, **kwargs)
        # Initialize the default Element behavior tags.
        self.font = font
        self.glyphNames = s or 'e'

    #   Always keep square

    def _get_w(self): # Width
        return min(self.maxW, max(self.minW, self.style['w'], MIN_WIDTH)) # From self.style, don't inherit.
    def _set_w(self, w):
        self.style['w'] = self.style['h'] = w or MIN_WIDTH # Overwrite element local style from here, parent css becomes inaccessable.
    h = w = property(_get_w, _set_w)

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

    def _drawGlyphMarker(self, axisName, mx, my, glyphName, fontSize, location, strokeW=2):
        # Middle circle 
        fill(1)
        stroke(0)
        strokeWidth(strokeW)
        oval(mx-fontSize*self.R, my-fontSize*self.R, fontSize*2*self.R, fontSize*2*self.R)

        variableFont = getVariableFont(self.font, location)
        if axisName is not None:
            fs = newFS(axisName, style=dict(font=variableFont.installedName, fontSize=fontSize/4, textFill=0))
            tw, th = textSize(fs)
            text(fs, (mx-tw/2, my-fontSize*self.R-th*2/3))
        glyphPathScale = fontSize/self.font.info.unitsPerEm
        drawGlyphPath(variableFont, glyphName, mx, my-fontSize/3, s=glyphPathScale, fillColor=0)


    def draw(self, origin, view):
        u"""Draw the circle info-graphic, showing most info about the variable font as can be interpreted from the file."""
        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(p)    
        px, py, _ = self._applyAlignment(p) # Ignore z-axis for now.

        self.drawFrame(p, view) # Draw optional frame or borders.

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, p, view)

        # Draw actual circle
        self._drawFontCircle(px, py)

        # If there are child elements, draw them over the text.
        self._drawElements(p, view)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, p, view)

        self._restoreScale()
        view.drawElementMetaInfo(self, origin) # Depends on css flag 'showElementInfo'



    def _drawFontCircle(self, px, py):
        fontSize = self.css('fontSize', self.DEFAULT_FONT_SIZE)
        markerSize = fontSize*self.R

        # Calculate the max square size
        w = self.w - markerSize
        h = self.h - markerSize

        fill(0.9)
        stroke(None)
        mx = px + self.pw/2
        my = py + self.ph/2
        # Gray circle that defines the area of the axis extremes.
        oval(px+markerSize/2, py+markerSize/2, w, h)
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
        defaultLocation = {}
        self._drawGlyphMarker(None, mx, my, glyphName, fontSize, defaultLocation, strokeW=3)

        angle = 0
        for axisName, (minValue, defaultValue, maxValue) in axes.items():
            location = {axisName: maxValue}
            markerX, markerY = self._angle2XY(angle, w/2)
            self._drawGlyphMarker(axisName, mx+markerX, my+markerY, glyphName, fontSize/2, location)
            angle += 360/len(axes)

        self._restoreScale()



		