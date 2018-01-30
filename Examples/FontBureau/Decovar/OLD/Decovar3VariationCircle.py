#!/usr/bin/env python
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     DecovarVariationCircle.py
#
from __future__ import division

import pagebot
from pagebot.contexts import defaultContext as c
from pagebot.document import Document

import os
from math import pi, sin, cos
from pagebot.elements import Element
from pagebot.style import makeStyle
from pagebot.fonttoolbox.variablefontbuilder import drawGlyphPath


class VariationCircle(Element):
    u"""Interpret the content of the self.font variation font and draw a circle info graphic on that info."""

    DEFAULT_FONT_SIZE = 64
    R = 2/3 # Fontsize factor to draw glyph markers.

    def __init__(self, font, s=None, style=None, eId=None, angles=None, showAxisNames=True,
        **kwargs):
        self.font = font
        self.eId = eId
        self.style = makeStyle(style, **kwargs) # Combine self.style from
        self.initAngles(angles) # Initialize the angles in equal parts if not defined.
        self.showAxisNames = showAxisNames
        # Make sure that this is a formatted string. Otherwise create it with the current style.
        # Note that in case there is potential clash in the double usage of fill and stroke.
        self.glyphNames = s or 'e'
    
    def initAngles(self, angles):
        if angles is None:
            angles = {}
        self.angles = {}
        totalAxes = len(self.font.axes)
        for axisName in self.font.axes:
            self.angles[axisName] = angles.get(axisName, 360/totalAxes)

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
        c.fill(1)
        c.stroke(0)
        c.strokeWidth(strokeW)
        c.oval(mx-fontSize*self.R, my-fontSize*self.R, fontSize*2*self.R, fontSize*2*self.R)

        glyphPathScale = fontSize/self.font.info.unitsPerEm
        drawGlyphPath(self.font.ttFont, glyphName, mx, my-fontSize/4, location, s=glyphPathScale, fillColor=0)
           
    def draw(self, page, x, y):
        u"""Draw the circle info-graphic, showing most info about the variation font as can be interpreted from the file."""
        c.fill(0.9)
        c.stroke(None)
        mx = x + self.w/2
        my = y + self.h/2

        # Gray circle that defines the area of
        c.oval(x, y, self.w, self.h)
        
        # Draw axis spikes first, so we can cover them by the circle markers.
        axes = self.font.axes
        fontSize = self.style.get('fontSize', self.DEFAULT_FONT_SIZE)
        
        # Calculate sorted relative angle pairs.
        xAngles = {} # X-ref, key is angle, value is list of axisName
        for axisName in axes:
            angle = globals()[axisName]
            if not angle in xAngles: # Ignore overlapping 
                xAngles[angle] = axisName
        #print xAngles
        sortedAngles = sorted(xAngles)
        anglePairs = []
        a1 = None
        for a2 in sortedAngles:
            if a1 is not None:
                if abs(a2 - a1) < 35:
                    anglePairs.append((a1, a2))
            a1 = a2    
                        
        # Draw name of the font
        c.fill(0)
        c.text(c.newString(self.font.info.familyName,
                           style=dict(font=self.style['labelFont'],
                                      fontSize=self.style['titleFontSize'])),
               (x-fontSize/2, y+self.h+fontSize/4))

        # Draw spokes
        c.fill(None)
        c.stroke(0.7)
        c.strokeWidth(1)
        # Gray on full circle
        c.newPath()
        for axisName, angle in self.angles.items():
            markerX, markerY = self._angle2XY(angle, self.w/2)
            c.moveTo((mx-markerX, my-markerY))
            c.lineTo((mx+markerX, my+markerY))
        c.drawPath()
        
        # Black on range of axis.
        c.stroke(0)
        c.newPath()
        for axisName, angle in self.angles.items():
            markerX, markerY = self._angle2XY(angle, self.w/2)
            c.moveTo((mx, my))
            c.lineTo((mx+markerX, my+markerY))
        c.drawPath()

        # Pair combinations
        if anglePairs:
            c.newPath()
            for a1, a2 in anglePairs:
                markerX1, markerY1 = self._angle2XY(a1, self.w/2)
                markerX2, markerY2 = self._angle2XY(a2, self.w/2)
                c.moveTo((mx+markerX1, my+markerY1))
                c.lineTo((mx+markerX2, my+markerY2))
                c.moveTo((mx+markerX1*INTERPOLATION, my+markerY1*INTERPOLATION))
                c.lineTo((mx+markerX2*INTERPOLATION, my+markerY2*INTERPOLATION))
            c.stroke(0, 0, 1)
            c.fill(None)
            c.drawPath()
            
        # Draw default glyph marker in middle.
        glyphName = self.glyphNames[0]
        defaultLocation = {}
        self._drawGlyphMarker(mx, my, glyphName, fontSize, defaultLocation, strokeW=3)

        # Draw DeltaLocation circles.
        for axisName, (minValue, defaultValue, maxValue) in axes.items():
            angle = self.angles[axisName]
            # Outside maxValue 
            location = {axisName: maxValue}
            markerX, markerY = self._angle2XY(angle, self.w/2)
            self._drawGlyphMarker(mx+markerX, my+markerY, glyphName, fontSize/2, location)
            
            # Interpolated DeltaLocation circles.
            location = {axisName: minValue + (maxValue - minValue)*INTERPOLATION}
            markerX, markerY = self._angle2XY(angle, self.w/4)
            self._drawGlyphMarker(mx+markerX*INTERPOLATION*2, my+markerY*INTERPOLATION*2, glyphName, fontSize/2, location)

            # If there are any pairs, draw the interpolation between them
            #if anglePairs:
            #    for a1, a2 in anglePairs:
            #        axis1 = 

        # helper function:
        def makeAxisName(axisName):
            if not axisName in ('wght', 'wdth', 'opsz'):
                return axisName.upper()
            return axisName

        # Draw axis names and DeltaLocation values
        if self.showAxisNames:
            for axisName, (minValue, defaultValue, maxValue) in axes.items():
                angle = self.angles[axisName]
                location = {axisName: maxValue}
                valueFontSize = self.style.get('valueFontSize', 12)
                axisNameFontSize = self.style.get('axisNameFontSize', 12)
                markerX, markerY = self._angle2XY(angle, self.w/2)
                fs = c.newString(makeAxisName(axisName),
                                 style=dict(font=self.style.get('labelFont', 'Verdana'),
                                            fontSize=axisNameFontSize,
                                            fill=self.style.get('axisNameColor', 0)))
                tw, th = c.textSize(fs)
                c.fill(0.7, 0.7, 0.7, 0.6)
                c.stroke(None)
                c.rect(mx+markerX-tw/2-4, my+markerY-axisNameFontSize/2-th*1.5-4, tw+8, th)
                c.text(fs, (mx+markerX-tw/2, my+markerY-axisNameFontSize/2-th*1.5)) 
                
                # DeltaLocation master value
                if maxValue < 10:
                    sMaxValue = '%0.2f' % maxValue
                else:
                    sMaxValue = `int(round(maxValue))`
                fs = c.newString(sMaxValue,
                                 style=dict(font=self.style.get('labelFont', 'Verdana'),
                                            fontSize=valueFontSize,
                                            fill=self.style.get('axisValueColor', 0)))
                tw, th = c.textSize(fs)
                c.fill(0.7, 0.7, 0.7, 0.6)
                c.stroke(None)
                c.rect(mx+markerX-tw/2-4, my+markerY+valueFontSize/2+th*1.5-4, tw+8, th)
                c.text(fs, (mx+markerX-tw/2, my+markerY+valueFontSize/2+th*1.5)) 

                # DeltaLocation value
                interpolationValue = minValue + (maxValue - minValue)*INTERPOLATION
                if interpolationValue < 10:
                    sValue = '%0.2f' % interpolationValue
                else:
                    sValue = `int(round(interpolationValue))`
                fs = c.newString(sValue,
                                 style=dict(font=self.style.get('labelFont', 'Verdana'),
                                            fontSize=valueFontSize,
                                            fill=self.style.get('axisValueColor', 0)))
                tw, th = c.textSize(fs)
                c.fill(0.7, 0.7, 0.7, 0.6)
                c.stroke(None)
                c.rect(mx+markerX*INTERPOLATION-tw/2-4, my+markerY*INTERPOLATION+valueFontSize/2+th*1.5-4, tw+8, th)
                c.text(fs, (mx+markerX*INTERPOLATION-tw/2, my+markerY*INTERPOLATION+valueFontSize/2+th*1.5)) 

                # DeltaLocation value
                if minValue < 10:
                    sValue = '%0.2f' % minValue
                else:
                    sValue = `int(round(minValue))`
                fs = c.newString(sValue,
                                 style=dict(font=self.style.get('labelFont', 'Verdana'),
                                            fontSize=valueFontSize,
                                            fill=self.style.get('axisValueColor', 0)))
                tw, th = c.textSize(fs)
                c.fill(0.7, 0.7, 0.7, 0.6)
                c.stroke(None)
                minM = 0.2
                c.rect(mx+markerX*minM-tw/2-4, my+markerY*minM-8, tw+8, th)
                c.text(fs, (mx+markerX*minM-tw/2, my+markerY*minM-4)) 


FONT_SIZE = VariationCircle.DEFAULT_FONT_SIZE
INTERPOLATION = 0.5
CONNECT = 15 # Max angle to connect neighbors

VARIABLES = [
    dict(name='FONT_SIZE', ui='Slider', args=dict(value=60, minValue=24, maxValue=180)),
    dict(name='INTERPOLATION', ui='Slider', args=dict(value=0.5, minValue=0, maxValue=1)),
    dict(name='CONNECT', ui='Slider', args=dict(value=15, minValue=0, maxValue=90)),
]

#FIXME: put something into this axes dict:
#       shouldn't it be loaded from the varfont metadata ?
axes = {}
angle = -90
for axisName in axes:
    VARIABLES.append(dict(name=axisName,
                          ui='Slider', 
                          args=dict(value=angle,
                                    minValue=-90,
                                    maxValue=270)))
    globals()[axisName] = axes[axisName][1]
    angle += 360/len(axes)

c.Variable(VARIABLES, globals())


def makeDocument(rs):   
    # Create new document with (w,h) and fixed amount of pages.
    # Make number of pages with default document size.
    # Initially make all pages default with template
    doc = Document(rs, autoPages=1) 
         
    # Change template of page 1
    page = doc[1]
    glyphName = 'A'
    angles = {}
    style = dict(fontSize=FONT_SIZE,
                 labelFont='Verdana',
                 axisNameFontSize=14,
                 titleFontSize=18,
                 valueFontSize=10,
                 axisNameColor=(1, 0, 0))
    for axisName in axes:
        angles[axisName] = globals()[axisName]

    variationCircle = VariationCircle(varFont,
                                      w=W-M*2,
                                      h=H-M*2,
                                      s=glyphName,
                                      angles=angles,
                                      style=style,
                                      showAxisNames=True)
    page.place(variationCircle, M, M)
    return doc


from pagebot.style import getRootStyle
RS = getRootStyle()
d = makeDocument(RS)

if 0: # Not saving image
    d.drawPages()
else:
    d.export(EXPORT_PATH)
