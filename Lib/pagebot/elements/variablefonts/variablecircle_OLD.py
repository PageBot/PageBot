#!/usr/bin/env python
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
#     variablecircle.py
#
#     Draw a variable space default glyph in the middle and spikes around it fir each axis.
#     The aim is to derive as much information directly from the font, without the need
#     for additional parameters.
#
from math import pi, sin, cos

from pagebot import getContext
from pagebot.toolbox.units import pointOffset
from pagebot.elements import Element
from pagebot.fonttoolbox.variablefontbuilder import getVarFontInstance
from pagebot.toolbox.color import blackColor

context = getContext()

class VariableCircle(Element):
    """Interpret the content of the self.font variable font and draw a circle info graphic on that info.
    Information is derived from the Variable Font and automatic converted into
    an info-graphic, showing a simplified model of the design space.
    To show all possible interpolation, it would need to visualize an n-dimensional
    space (where n is the amount of axes in the font). In the simplified model
    all axes are represented as spikes/needles on a wheel, where the amount of
    penetration in the neutral glyph defined the influence of that axis.
    In that respect is it not much better than a list of sliders, but at least this
    model allows to show interactions between axes, by putting them on another
    angle on the circle.
    """
    isText = False
    isFlow = False

    DEFAULT_FONT_SIZE = 64
    R = 1#2/3 # Fontsize factor to draw glyph markers.

    def __init__(self, font, s=None, draw3D=True, location=None, showAxisNames=True, **kwargs):
        Element.__init__(self, **kwargs)
        # Initialize the default Element behavior tags.
        self.font = font
        self.glyphNames = s or 'e'
        self.draw3D = draw3D # TODO: Draw as 3D structure of spheres and needles/spikes.
        self.location = location # Use to visualize a specific location, otherwise all needles are at min value.
        self.showAxisNames = showAxisNames

    def location2Recipe(self, location, start=0, end=3):
        recipe = ''
        if self.recipeAxes:
            for name in self.recipeAxes[start:end]:
                if name in location:
                    recipe += '%s %d\n' % (name, location[name])
        return recipe

    def _angle2XY(self, angle, r):
        """Answers the XY position for a given angled (degrees) and r, located on the origin."""
        return cos(angle/180*pi) * r, sin(angle/180*pi) * r

    def _drawGlyphMarker(self, axisName, mx, my, glyphName, fontSize, location, strokeW=2):
        # Middle circle
        context.fill(1)
        context.stroke(0.7)
        context.strokeWidth(strokeW)
        context.oval(mx-fontSize/2*self.R, my-fontSize/2*self.R, fontSize*self.R, fontSize*self.R)

        variableFont = getVarFontInstance(self.font, location)
        # Show axis name below circle marker?
        if self.showAxisNames and axisName is not None:
            bs = context.newString(axisName,
                                   style=dict(font=variableFont.path,
                                              fontSize=fontSize/4,
                                              textFill=blackColor))
            tw, th = bs.size
            context.text(bs, (mx-tw/2, my-fontSize/2*self.R-th*2/3))
        glyphPathScale = fontSize/self.font.info.unitsPerEm
        context.drawGlyphPath(variableFont, glyphName, mx, my-fontSize/3, s=glyphPathScale, fillColor=0)


    def _drawFontCircle(self, px, py):
        fontSize = self.css('fontSize', self.DEFAULT_FONT_SIZE)
        markerSize = fontSize*self.R

        # Calculate the max square size
        w = self.w - markerSize
        h = self.h - markerSize

        context.fill(0.9)
        context.stroke(None)
        mx = px + self.pw/2
        my = py + self.ph/2
        # Gray circle that defines the area of the axis extremes.
        context.oval(px+markerSize/2, py+markerSize/2, w, h)
        # Draw axis spikes first, so we can cover them by the circle markers.
        axes = self.font.axes

        # Draw default glyph circle marker in middle.
        glyphName = self.glyphNames[0]
        #varLocation = getVarLocation(self.font, self.location) # Show neutral, unless a location is requested
        varLocation = self.location # = getVarLocation(self.font, self.location) # Show neutral, unless a location is requested
        self._drawGlyphMarker(None, mx, my, glyphName, fontSize, varLocation, strokeW=3)

        # Draw
        angle = 0
        for axisName, (minValue, defaultValue, maxValue) in axes.items():
        # Draw needles, depending on the axis values and the status of self.location
            if self.draw3D:
                needleStart = 0.40 # Just enough overlap with edge of neutral circle marker
            else:
                needleStart = 2/3 # Start at edge of neutral circle marker

            rStart = fontSize
            rEnd = w/2
            if self.location is not None and axisName in self.location:
                rEnd = rStart + (rEnd - rStart) * self.location[axisName]
            rStart = fontSize*needleStart
            #print(rStart, rEnd)
            startX, startY = self._angle2XY(angle, rStart)
            endX, endY = self._angle2XY(angle, rEnd)
            if (w/2 + rStart) - rEnd - fontSize > fontSize:
                startX1, startY1 = self._angle2XY(angle-180, fontSize/2)
                endX1, endY1 = self._angle2XY(angle-180, (w/2 + rStart) - rEnd - fontSize)
            else:
                startX1 = None
            context.stroke(None)
            context.fill(0.3)
            context.oval(mx+startX-2, my+startY-2, 4, 4)

            context.fill(None)
            context.stroke(0)
            context.strokeWidth(1)
            context.newPath()
            context.moveTo((mx+startX, my+startY))
            context.lineTo((mx+endX, my+endY))
            if startX1 is not None:
                context.moveTo((mx+startX1, my+startY1))
                context.lineTo((mx+endX1, my+endY1))
            context.drawPath()

            # Show the glyph shape as it is at the max location of the axis.
            location = {axisName: maxValue}
            self._drawGlyphMarker(axisName, mx+endX, my+endY, glyphName, fontSize, location)
            angle += 360/len(axes)

    #   D R A W B O T / F L A T  S U P P O R T

    def build(self, view, origin, drawElements=True):
        """Draw the circle info-graphic, showing most info about the variable font as can be interpreted from the file."""
        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        px, py, _ = self._applyAlignment(p) # Ignore z-axis for now.

        # Let the view draw frame info for debugging, in case view.showFrame == True
        view.drawElementFrame(self, p)

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        # Draw actual circle
        self._drawFontCircle(px, py)

        if drawElements:
            for e in self.elements:
                e.build_flat(view, p)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreScale(view)
        view.drawElementInfo(self, origin) # Depends on css flag 'showElementInfo'
