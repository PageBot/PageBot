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
from pagebot import newFS
from pagebot.style import getRootStyle
from pagebot.document import Document
from pagebot.elements.pbpage import Template
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
#from pagebot.fonttoolbox.variationbuilder import generateInstance, drawGlyphPath
from drawBot import fill, rect, oval, stroke, strokeWidth, installFont, installedFonts, FormattedString, moveTo, lineTo, newPath, drawPath
#====================

def init():


    DEBUG = False # Make True to see grid and element frames.


    FONT_PATH = pagebot.getFontPath()
    #fontPath = FONT_PATH + 'fontbureau/Decovar-VF-chained3.ttf'
    #fontPath = FONT_PATH + 'fontbureau/Decovar-VF-2axes.subset.ttf'
    #fontPath = FONT_PATH + 'fontbureau/Decovar-VF-2axes.ttf'
    fontPath = FONT_PATH + 'fontbureau/Decovar-VF-chained3.ttf'
    #fontPath = FONT_PATH + 'fontbureau/AmstelvarAlpha-Variations.ttf'
    fontPath = FONT_PATH + 'PromiseVar.ttf'
    #fontPath = FONT_PATH + 'BitcountGridVar.ttf'
    EXPORT_PATH = '_export/'+ fontPath.split('/')[-1].replace('ttf', 'pdf')
    varFont = Font(fontPath)
    varFontName = varFont.install() # Do DrawBot font install.

    axes = varFont.axes
    print axes

    RS = getRootStyle()
    RS['w'] = W = 600
    RS['h'] = H = 600
    M = 50
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

    def _drawGlyphMarker(self, mx, my, glyphName, fontSize, location, strokeW=2):
        # Middle circle 
        fill(1)
        stroke(0)
        strokeWidth(strokeW)
        oval(mx-fontSize*self.R, my-fontSize*self.R, fontSize*2*self.R, fontSize*2*self.R)

        glyphPathScale = fontSize/self.font.info.unitsPerEm
        drawGlyphPath(self.font.ttFont, glyphName, mx, my-fontSize/4, location, s=glyphPathScale, fillColor=0)
           
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
        fontSize = self.style.get('fontSize', self.DEFAULT_FONT_SIZE)
        
        # Draw name of the font
        fill(0)
        text(FormattedString(self.font.info.familyName, font=self.style['labelFont'],
            fontSize=self.style['axisNameFontSize']), (x-fontSize/2, y+self.h+fontSize/2))

        # Draw spokes
        fill(None)
        stroke(0)
        strokeWidth(1)
        newPath()
        for axisName, angle in self.angles.items():
            markerX, markerY = self._angle2XY(angle, self.w/2)
            moveTo((mx, my))
            lineTo((mx+markerX, my+markerY))
        drawPath()

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

        # Draw axis names and DeltaLocation values
        if self.showAxisNames:
            for axisName, (minValue, defaultValue, maxValue) in axes.items():
                angle = self.angles[axisName]
                location = {axisName: maxValue}
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
                if maxValue < 10:
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
                interpolationValue = minValue + (maxValue - minValue)*INTERPOLATION
                if interpolationValue < 10:
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
                if minValue < 10:
                    sValue = '%0.2f' % minValue
                else:
                    sValue = `int(round(minValue))`
                fs = FormattedString(sValue, font=self.style.get('labelFont', 'Verdana'),
                    fontSize=valueFontSize, fill=self.style.get('axisValueColor', 0))
                tw, th = textSize(fs)
                fill(0.7, 0.7, 0.7, 0.6)
                stroke(None)
                minM = 0.2
                rect(mx+markerX*minM-tw/2-4, my+markerY*minM+th*0.5-4, tw+8, th)
                text(fs, (mx+markerX*minM-tw/2, my+markerY*minM+th*0.5)) 

#====================

if 0:

    FONT_SIZE = VariationCircle.DEFAULT_FONT_SIZE
    INTERPOLATION = 0.5
     
    VARIABLES = [
        dict(name='FONT_SIZE', ui='Slider', args=dict(value=60, minValue=24, maxValue=180)),
        dict(name='INTERPOLATION', ui='Slider', args=dict(value=0.5, minValue=0, maxValue=1)),
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
        doc = Document(rs, autoPages=1) 
         
        # Change template of page 1
        page = doc[1]
        glyphName = 'A' 
        angles = {}
        style = dict(fontSize=FONT_SIZE, labelFont='Verdana', axisNameFontSize=14, 
            valueFontSize=10, axisNameColor=(1, 0, 0))
        for axisName in axes:
            angles[axisName] = globals()[axisName]
        variationCircle = VariationCircle(varFont, w=W-M*2, h=H-M*2, s=glyphName, angles=angles,
            style=style, showAxisNames=True)
        page.place(variationCircle, M, M)
          
        
        return doc
            
    d = makeDocument(RS)
    if 1: # Not saving image
        d.drawPages()
    else:
        d.export(EXPORT_PATH) 

