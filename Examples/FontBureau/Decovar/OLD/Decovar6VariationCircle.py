# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     DecovarVariationCircle.py
#
from __future__ import division

import myglobals
import pagebot
from pagebot import newFS
from pagebot.style import getRootStyle
from pagebot.document import Document
from pagebot.page import Template
# For Variation Fonts we can use the plain Font-->TTFont wrapper for all styles. No need to use Family.
from pagebot.fonttoolbox.objects.font import Font

from pagebot.publications.typespecimen import TypeSpecimen
#from pagebot.fonttoolbox.elements.variationcircle import VariationCircle

#====================
from math import pi, sin, cos
import os
from random import random, choice
from copy import copy
from fontTools.ttLib import TTFont
from pagebot.elements import Element
from pagebot.style import makeStyle
from pagebot.fonttoolbox.variationbuilder import generateInstance, drawGlyphPath
from drawBot import fill, rect, oval, stroke, strokeWidth, installFont, installedFonts, FormattedString, moveTo, lineTo, newPath, drawPath
#====================


DEBUG = False # Make True to see grid and element frames.


FONT_PATH = pagebot.getFontPath()
fontPath = FONT_PATH + 'fontbureau/Decovar-VF-chained3.ttf'
#fontPath = FONT_PATH + 'fontbureau/Decovar-VF-2axes.subset.ttf'fontPath = FONT_PATH + 'fontbureau/Decovar-VF-2axes.ttf'#fontPath = FONT_PATH + 'fontbureau/Decovar-VF-chained3.ttf'
fontPath = FONT_PATH + 'fontbureau/Decovar-VF_2017-02-06.ttf'
fontPath = FONT_PATH + 'fontbureau/AmstelvarAlpha-Variations.ttf'
#fontPath = FONT_PATH + 'PromiseVar.ttf'
#fontPath = FONT_PATH + 'BitcountGridVar.ttf'
EXPORT_PATH = '_export/'+ fontPath.split('/')[-1].replace('ttf', 'pdf')
varFont = Font(fontPath)
varFontName = varFont.install() # Do DrawBot font install.

axes = varFont.axes
print axes

RS = getRootStyle()
RS['w'] = W = 600
RS['h'] = H = 600
M = 50 # Margin of page.

#====================

def makeAxisName(axisName):
    if not axisName in ('wght', 'wdth', 'opsz'):
        return axisName.upper()
    return axisName
    
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

    def _drawGlyphMarker(self, mx, my, glyphName, markerSize, location, strokeW=2):
        # Middle circle 
        fill(1)
        stroke(0)
        strokeWidth(strokeW)
        oval(mx-markerSize/2, my-markerSize/2, markerSize, markerSize)

        glyphPathScale = markerSize/self.font.info.unitsPerEm*3/4
        drawGlyphPath(self.font.ttFont, glyphName, mx, my-markerSize/4, location, s=glyphPathScale, fillColor=0)
           
    def draw(self, page, x, y):
        u"""Draw the circle info-graphic, showing most info about the variation font as can be interpreted from the file."""
        fill(0.9)
        stroke(None)
        mx = x + self.w/2
        my = y + self.h/2

        # Gray circle that defines the area of
        oval(x, y, self.w, self.h)
        
        # Draw axis spikes first, so we can cover them by the circle markers.
        axes = self.font.axes
        markerSize = self.style.get('fontSize', self.DEFAULT_FONT_SIZE)
        
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
                if abs(a2 - a1) < CONNECT: # Max angle to connect
                    anglePairs.append((a1, a2))
            a1 = a2    
                        
        # Draw name of the font
        fill(0)
        text(FormattedString(self.font.info.familyName, font=self.style['labelFont'],
            fontSize=self.style['titleFontSize']), (x-markerSize/2, y+self.h+markerSize/4))

        # Draw spokes
        fill(None)
        stroke(0.7)
        strokeWidth(1)
        # Gray on full circle
        newPath()
        for axisName, angle in self.angles.items():
            markerX, markerY = self._angle2XY(angle, self.w/2)
            moveTo((mx-markerX, my-markerY))
            lineTo((mx+markerX, my+markerY))
        drawPath()
        
        # Black on range of axis.
        stroke(0)
        newPath()
        for axisName, angle in self.angles.items():
            minValue, defaultValue, maxValue = axes[axisName]
            markerX, markerY = self._angle2XY(angle, self.w/2)
            if minValue < defaultValue:
                moveTo((mx, my))
                lineTo((mx-markerX, my-markerY))
            if defaultValue < maxValue:
                moveTo((mx, my))
                lineTo((mx+markerX, my+markerY))                
        drawPath()

        # Pair combinations
        if anglePairs:
            newPath()
            for a1, a2 in anglePairs:
                markerX1, markerY1 = self._angle2XY(a1, self.w/2)
                markerX2, markerY2 = self._angle2XY(a2, self.w/2)
                moveTo((mx+markerX1, my+markerY1))
                lineTo((mx+markerX2, my+markerY2))
                moveTo((mx+markerX1*INTERPOLATION, my+markerY1*INTERPOLATION))
                lineTo((mx+markerX2*INTERPOLATION, my+markerY2*INTERPOLATION))
            stroke(0, 0, 1)
            fill(None)
            drawPath()
            
        # Draw default glyph marker in middle.
        glyphName = self.glyphNames[0]
        defaultLocation = {}
        self._drawGlyphMarker(mx, my, glyphName, markerSize, defaultLocation)

        # http://stackoverflow.com/questions/1734745/how-to-create-circle-with-bézier-curves
        
        # Draw DeltaLocation circles.
        for axisName, (minValue, defaultValue, maxValue) in axes.items():
            angle = self.angles[axisName]
            if defaultValue < maxValue:
                # Outside maxValue 
                location = {axisName: maxValue}
                markerX, markerY = self._angle2XY(angle, self.w/2)
                self._drawGlyphMarker(mx+markerX, my+markerY, glyphName, markerSize, location)
            
                # Interpolated DeltaLocation circles.
                location = {axisName: defaultValue + (maxValue - defaultValue)*INTERPOLATION}
                markerX, markerY = self._angle2XY(angle, self.w/4)
                self._drawGlyphMarker(mx+markerX*INTERPOLATION*2, my+markerY*INTERPOLATION*2, glyphName, markerSize, location)

            if minValue < defaultValue:
                # Outside minValue.
                location = {axisName: minValue}
                markerX, markerY = self._angle2XY(angle, self.w/2)
                self._drawGlyphMarker(mx-markerX, my-markerY, glyphName, markerSize, location)

                # Interpolated DeltaLocation circles.
                location = {axisName: minValue + (defaultValue - minValue)*INTERPOLATION}
                markerX, markerY = self._angle2XY(angle, self.w/4)
                self._drawGlyphMarker(mx-markerX*2*INTERPOLATION, my-markerY*2*INTERPOLATION, glyphName, markerSize, location)

            # If there are any pairs, draw the interpolation between them
            #if anglePairs:
            #    for a1, a2 in anglePairs:
            #        axis1 = 
        # Draw axis names and DeltaLocation values
        if self.showAxisNames:
            for axisName, (minValue, defaultValue, maxValue) in axes.items():
                if minValue < defaultValue:
                    angle = self.angles[axisName]
                    valueFontSize = self.style.get('valueFontSize', 12)
                    axisNameFontSize = self.style.get('axisNameFontSize', 12)
                    markerX, markerY = self._angle2XY(angle, self.w/2)
                    fs = FormattedString(makeAxisName(axisName), font=self.style.get('labelFont', 'Verdana'),
                        fontSize=axisNameFontSize, fill=self.style.get('axisNameColor', 0))
                    tw, th = textSize(fs)
                    fill(0.7, 0.7, 0.7, 0.6)
                    stroke(None)
                    rect(mx-markerX-tw/2-4, my-markerY-axisNameFontSize/2-th*1.5-4, tw+8, th)
                    text(fs, (mx-markerX-tw/2, my-markerY-axisNameFontSize/2-th*1.5)) 
                
                    # DeltaLocation master value
                    if 0 < minValue < 10:
                        sMinValue = '%0.2f' % minValue
                    else:
                        sMinValue = `int(round(minValue))`
                    fs = FormattedString(sMinValue, font=self.style.get('labelFont', 'Verdana'),
                        fontSize=valueFontSize, fill=self.style.get('axisValueColor', 0))
                    tw, th = textSize(fs)
                    fill(0.7, 0.7, 0.7, 0.6)
                    stroke(None)
                    rect(mx-markerX-tw/2-4, my-markerY+valueFontSize/2+th*1.5-4, tw+8, th)
                    text(fs, (mx-markerX-tw/2, my-markerY+valueFontSize/2+th*1.5)) 

                    # DeltaLocation value
                    interpolationValue = minValue + (defaultValue - minValue)*INTERPOLATION
                    if 0 < interpolationValue < 10:
                        sValue = '%0.2f' % interpolationValue
                    else:
                        sValue = `int(round(interpolationValue))`
                    fs = FormattedString(sValue, font=self.style.get('labelFont', 'Verdana'),
                        fontSize=valueFontSize, fill=self.style.get('axisValueColor', 0))
                    tw, th = textSize(fs)
                    fill(0.7, 0.7, 0.7, 0.6)
                    stroke(None)
                    rect(mx-markerX*INTERPOLATION-tw/2-4, my-markerY*INTERPOLATION+valueFontSize/2+th*1.5-4, tw+8, th)
                    text(fs, (mx-markerX*INTERPOLATION-tw/2, my-markerY*INTERPOLATION+valueFontSize/2+th*1.5)) 

                    # DeltaLocation value
                    if 0 < defaultValue < 10:
                        sValue = '%0.2f' % defaultValue
                    else:
                        sValue = `int(round(defaultValue))`
                    fs = FormattedString(sValue, font=self.style.get('labelFont', 'Verdana'),
                        fontSize=valueFontSize, fill=self.style.get('axisValueColor', 0))
                    tw, th = textSize(fs)
                    fill(0.7, 0.7, 0.7, 0.6)
                    stroke(None)
                    minM = 0.15
                    rect(mx-markerX*minM-tw/2-4, my-markerY*minM-8, tw+8, th)
                    text(fs, (mx-markerX*minM-tw/2, my-markerY*minM-4)) 
                
                if defaultValue < maxValue:
                    angle = self.angles[axisName]
                    valueFontSize = self.style.get('valueFontSize', 12)
                    axisNameFontSize = self.style.get('axisNameFontSize', 12)
                    markerX, markerY = self._angle2XY(angle, self.w/2)
                    fs = FormattedString(makeAxisName(axisName), font=self.style.get('labelFont', 'Verdana'),
                        fontSize=axisNameFontSize, fill=self.style.get('axisNameColor', 0))
                    tw, th = textSize(fs)
                    fill(0.7, 0.7, 0.7, 0.6)
                    stroke(None)
                    rect(mx+markerX-tw/2-4, my+markerY-axisNameFontSize/2-th*1.5-4, tw+8, th)
                    text(fs, (mx+markerX-tw/2, my+markerY-axisNameFontSize/2-th*1.5)) 
                
                    # DeltaLocation master value
                    if 0 < maxValue < 10:
                        sMaxValue = '%0.2f' % maxValue
                    else:
                        sMaxValue = `int(round(maxValue))`
                    fs = FormattedString(sMaxValue, font=self.style.get('labelFont', 'Verdana'),
                        fontSize=valueFontSize, fill=self.style.get('axisValueColor', 0))
                    tw, th = textSize(fs)
                    fill(0.7, 0.7, 0.7, 0.6)
                    stroke(None)
                    rect(mx+markerX-tw/2-4, my+markerY+valueFontSize/2+th*1.5-4, tw+8, th)
                    text(fs, (mx+markerX-tw/2, my+markerY+valueFontSize/2+th*1.5)) 

                    # DeltaLocation value
                    interpolationValue = defaultValue + (maxValue - defaultValue)*INTERPOLATION
                    if 0 < interpolationValue < 10:
                        sValue = '%0.2f' % interpolationValue
                    else:
                        sValue = `int(round(interpolationValue))`
                    fs = FormattedString(sValue, font=self.style.get('labelFont', 'Verdana'),
                        fontSize=valueFontSize, fill=self.style.get('axisValueColor', 0))
                    tw, th = textSize(fs)
                    fill(0.7, 0.7, 0.7, 0.6)
                    stroke(None)
                    rect(mx+markerX*INTERPOLATION-tw/2-4, my+markerY*INTERPOLATION+valueFontSize/2+th*1.5-4, tw+8, th)
                    text(fs, (mx+markerX*INTERPOLATION-tw/2, my+markerY*INTERPOLATION+valueFontSize/2+th*1.5)) 

                    # DeltaLocation value
                    if defaultValue < 10:
                        sValue = '%0.2f' % defaultValue
                    else:
                        sValue = `int(round(defaultValue))`
                    fs = FormattedString(sValue, font=self.style.get('labelFont', 'Verdana'),
                        fontSize=valueFontSize, fill=self.style.get('axisValueColor', 0))
                    tw, th = textSize(fs)
                    fill(0.7, 0.7, 0.7, 0.6)
                    stroke(None)
                    minM = 0.15
                    rect(mx+markerX*minM-tw/2-4, my+markerY*minM-8, tw+8, th)
                    text(fs, (mx+markerX*minM-tw/2, my+markerY*minM-4)) 

#====================

FONT_SIZE = VariationCircle.DEFAULT_FONT_SIZE
INTERPOLATION = 0.5
CONNECT = 30 # Max angle to connect neighbors

VARIABLES = [
    dict(name='FONT_SIZE', ui='Slider', args=dict(value=60, minValue=24, maxValue=180)),
    dict(name='INTERPOLATION', ui='Slider', args=dict(value=0.5, minValue=0, maxValue=1)),
    dict(name='CONNECT', ui='Slider', args=dict(value=30, minValue=0, maxValue=90)),
]
angle = -90
for axisName in axes:
    VARIABLES.append(dict(name=axisName, ui='Slider', 
        args=dict(value=angle, minValue=-90, maxValue=270)))
    globals()[axisName] = axes[axisName][1]
    angle += 360/len(axes)
Variable(VARIABLES, globals())

def makeDocument(rs):
    
    # Create new document with (w,h) and fixed amount of pages.
    # Make number of pages with default document size.
    # Initially make all pages default with template
    doc = Document(rs, pages=1) 
     
    # Change template of page 1
    page = doc[1]
    glyphName = 'A' 
    angles = {}
    style = dict(fontSize=FONT_SIZE, labelFont='Verdana', axisNameFontSize=14, 
        titleFontSize=18, valueFontSize=10, axisNameColor=(1, 0, 0))
    for axisName in axes:
        angles[axisName] = globals()[axisName]
    variationCircle = VariationCircle(varFont, w=W-M*2, h=H-M*2, s=glyphName, angles=angles,
        style=style, showAxisNames=True)
    page.place(variationCircle, M, M)
      
    
    return doc
        
d = makeDocument(RS)
if 0: # Not saving image
    d.drawPages(None)
else:
    print EXPORT_PATH
    d.export(EXPORT_PATH) 

