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
#	  variablecircle.py
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
from pagebot.toolbox.units import pt, upt

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

    MARKER_RADIUS = pt(5)
    INTERPOLATION = 0.5
    DEFAULT_FONT_SIZE = pt(64)
    """
    >>> from pagebot.fonttoolbox.objects.font import findFont
    >>> from pagebot.document import Document
    >>> vfFont = findFont('RobotoDelta_v2-VF')
    >>> from pagebot.fonttoolbox.objects.font import findFont
    >>> doc = Document(w=500, h=500, originTop=False, autoPages=1)
    >>> page = doc[1]
    >>> page.padding = 40
    >>> vc = VariableCircle(vfFont, parent=page, x=40, y=40, w=page.pw)
    >>> doc.export('_export/testVFCircle.pdf')
    """
 
    R = 1#2/3 # Fontsize factor to draw glyph markers.

    def __init__(self, font, s=None, draw3D=True, location=None, showAxisNames=True, 
        markerRadius=None, labelFont=None, labelFontSize=None, axisNameFontSize=None, **kwargs):
        Element.__init__(self, **kwargs)
        # Initialize the default Element behavior tags.
        self.vfFont = font
        if labelFont is None:
            labelFont = font
        self.labelFont = labelFont
        if axisNameFontSize is None:
            axisNameFontSize = self.fontSize
        self.axisNameFontSize = axisNameFontSize

        self.labelFontSize = labelFontSize or pt(12)
        self.glyphNames = s or 'e'
        self.draw3D = draw3D # TODO: Draw as 3D structure of spheres and needles/spikes.
        self.location = location # Use to visualize a specific location, otherwise all needles are at min value.
        self.showAxisNames = showAxisNames
        self.markerRadius = markerRadius or self.MARKER_RADIUS

        self.angles = {}
        if self.vfFont.axes:
            aIndex = 0
            da = 180/len(self.vfFont.axes)
            for axis, (minValue, defaultValue, maxValue) in sorted(self.vfFont.axes.items()):
                minAngle = maxAngle = None
                if minValue != defaultValue:
                    minAngle = aIndex * da
                if maxValue != defaultValue:
                    maxAngle = aIndex * (da+180)
                self.angles[axis] = minAngle, maxAngle
                aIndex += 1
        print(self.angles)

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
        glyphPathScale = fontSize/self.vfFont.info.unitsPerEm
        context.drawGlyphPath(variableFont, glyphName, mx, my-fontSize/3, s=glyphPathScale, fillColor=0)

    def makeAxisName(self, axisName):
        return self.context.newString(axisName, style=dict(font=self.font, fontSize=7))

    def _drawFontCircle(self, px, py):
        context = self.context # Get context from the parent doc.
        context.fill(0.9)
        context.stroke(None)
        mx = px + self.pl + self.pw/2
        my = py + self.pb + self.ph/2

        # Gray circle that defines the area of
        r = min(self.pw/2, self.ph/2) # Relate to padded with and padded height
        context.circle(mx, my, r)

        # Draw axis spikes first, so we can cover them by the circle markers.
        axes = self.vfFont.axes
        fontSize = self.style.get('fontSize', self.DEFAULT_FONT_SIZE)

        # Draw name of the font
        """
        bs = context.newString(self.vfFont.info.familyName,
                                style=dict(font=self.labelFont,
                                fontSize=self.axisNameFontSize, textFill=blackColor))
        context.text(bs, (px-fontSize/2, py+self.h+fontSize/2))
        """

        # Draw default glyph marker in middle.
        defaultLocation = {}
        #self._drawGlyphIcon(mx, my, self.glyphName, fontSize, defaultLocation, strokeW=3)

        # Draw DeltaLocation circles.
        for axisName, (minValue, defaultValue, maxValue) in sorted(axes.items()):
            angle1, angle2 = self.angles[axisName]
            """
            # Outside maxValue
            location = {axisName: maxValue}
            markerX, markerY = self._angle2XY(angle, r/2)
            #self._drawGlyphIcon(mx+markerX, my+markerY, self.glyphName, fontSize/2, location)
            #content.oval(mx+markerX, my+markerY, 16, 16)
            """
            # Interpolated DeltaLocation circles.
            location = {axisName: minValue + (maxValue - minValue)*self.INTERPOLATION}
            context.fill(1)
            context.stroke(0)
            context.strokeWidth(self.strokeWidth)
            #self._drawGlyphIcon(mx+markerX*self.INTERPOLATION*2, my+markerY*self.INTERPOLATION*2, self.glyphName, fontSize/2, location)

            style = dict(font=self.labelFont, fontSize=self.axisNameFontSize, textFill=blackColor)
            if angle1 is not None and minValue != defaultValue:
                markerX, markerY = self._angle2XY(angle1, r)
                context.circle(mx+markerX, my+markerY, self.markerRadius)
                
                bs = context.newString(axisName, style=style)
                tw, th = bs.size
                context.text(bs, (mx + markerX + upt(markerX)/upt(r) * tw * 1.25 - tw/2, my + markerY + upt(markerY)/upt(r) * th * 1.6 - th/4))

                bs = context.newString('%d' % minValue, style=style)
                tw, th = bs.size
                context.text(bs, (mx + markerX - tw/2, my + markerY - th/4))

            if angle2 is not None and maxValue != defaultValue:
                markerX, markerY = self._angle2XY(angle2, r)
                context.circle(mx+markerX, my+markerY, self.markerRadius)

                bs = context.newString(axisName, style=style)
                tw, th = bs.size
                context.text(bs, (mx + markerX + upt(markerX)/upt(r) * tw * 1.25 - tw/2, my + markerY + upt(markerY)/upt(r) * th * 1.6 - th/4))

                bs = context.newString('%d' % maxValue, style=style)
                tw, th = bs.size
                context.text(bs, (mx + markerX - tw/2, my + markerY - th/4))


        # Draw spokes
        context.fill(None)
        context.stroke(0)
        context.strokeWidth(self.strokeWidth)
        for axisName, (minValue, defaultValue, maxValue) in sorted(axes.items()):
            angle1, angle2 = self.angles[axisName]
            if angle1 is not None and minValue != defaultValue:
                markerX, markerY = self._angle2XY(angle1, r-self.markerRadius)
                context.line((mx, my), (mx+markerX, my+markerY))
            if angle2 is not None and maxValue != defaultValue:
                markerX, markerY = self._angle2XY(angle2, r-self.markerRadius)
                context.line((mx, my), (mx+markerX, my+markerY))

        # Draw Middle circle
        context.fill(1)
        context.stroke(0)
        context.strokeWidth(self.strokeWidth)
        context.circle(mx, my, self.markerRadius)

        
        # Draw axis names and DeltaLocation values
        if 1: #self.showAxisNames:
            for axisName, (minValue, defaultValue, maxValue) in axes.items():
                angle = self.angles[axisName]
                location = {axisName: maxValue}
                valueFontSize = self.style.get('valueFontSize', 8)
                axisNameFontSize = self.style.get('axisNameFontSize', 8)
                markerX, markerY = self._angle2XY(angle, r/2)
                bs = context.newString(self.makeAxisName(axisName),
                                 style=dict(font=self.style.get('labelFont', 'Verdana'),
                                            fontSize=axisNameFontSize,
                                            fill=self.style.get('axisNameColor', 0)))
                tw, th = bs.size
                context.fill((0.7, 0.7, 0.7, 0.6))
                context.stroke(None)
                context.rect(mx+markerX-tw/2-4, my+markerY-axisNameFontSize/2-th*1.5-4, tw+8, th)
                context.text(bs, (mx+markerX-tw/2, my+markerY-axisNameFontSize/2-th*1.5))

                # DeltaLocation master value
                if maxValue < 10:
                    sMaxValue = '%0.2f' % maxValue
                else:
                    sMaxValue = repr(int(round(maxValue)))
                bs = context.newString(sMaxValue,
                                 style=dict(font=self.style.get('labelFont', 'Verdana'),
                                            fontSize=valueFontSize,
                                            fill=self.style.get('axisValueColor', 0)))
                tw, th = bs.size
                context.fill((0.7, 0.7, 0.7, 0.6))
                context.stroke(None)
                context.rect(mx+markerX-tw/2-4, my+markerY+valueFontSize/2+th*1.5-4, tw+8, th)
                context.text(bs, (mx+markerX-tw/2, my+markerY+valueFontSize/2+th*1.5))

                # DeltaLocation value
                interpolationValue = minValue + (maxValue - minValue)*self.INTERPOLATION
                if interpolationValue < 10:
                    sValue = '%0.2f' % interpolationValue
                else:
                    sValue = repr(int(round(interpolationValue)))
                bs = context.newString(sValue,
                                 style=dict(font=self.style.get('labelFont', 'Verdana'),
                                            fontSize=valueFontSize,
                                            fill=self.style.get('axisValueColor', 0)))
                tw, th = bs.size
                context.fill((0.7, 0.7, 0.7, 0.6))
                context.stroke(None)
                context.rect(mx+markerX*self.INTERPOLATION-tw/2-4, my+markerY*self.INTERPOLATION+valueFontSize/2+th*1.5-4, tw+8, th)
                context.text(bs, (mx+markerX*self.INTERPOLATION-tw/2, my+markerY*self.INTERPOLATION+valueFontSize/2+th*1.5))

                # DeltaLocation value
                if minValue < 10:
                    sValue = '%0.2f' % minValue
                else:
                    sValue = repr(int(round(minValue)))
                bs = context.newString(sValue,
                                 style=dict(font=self.style.get('labelFont', 'Verdana'),
                                            fontSize=valueFontSize,
                                            fill=self.style.get('axisValueColor', 0)))
                tw, th = bs.size
                context.fill((0.7, 0.7, 0.7, 0.6))
                context.stroke(None)
                minM = 0.2
                context.rect(mx+markerX*minM-tw/2-4, my+markerY*minM+th*0.5-4, tw+8, th)
                context.text(bs, (mx+markerX*minM-tw/2, my+markerY*minM+th*0.5))

        

    #   D R A W B O T  S U P P O R T

    def build(self, view, origin, drawElements=True, **kwargs):
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
                e.build(view, p, **kwargs)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreScale(view)
        view.drawElementInfo(self, origin) # Depends on css flag 'showElementInfo'


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
