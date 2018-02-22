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

import os
from math import pi, sin, cos
from random import random, choice
from copy import copy
from fontTools.ttLib import TTFont

from pagebot.contexts.platform import getRootFontPath
from pagebot.contexts import defaultContext as context
from pagebot.style import getRootStyle, makeStyle
from pagebot.toolbox.transformer import pointOffset, point2D
from pagebot.document import Document
from pagebot.fonttoolbox.objects.font import Font
from pagebot.publications.typespecimen import TypeSpecimen
from pagebot.elements import Element, Template

DEBUG = False # Make True to see grid and element frames.

SHOW_VARIABLES = False # If true, open a window with sliders on the axes.

# Get font path in the PageBot repostory, so we know it is there.
FONT_PATH = getRootFontPath()
fontPath = FONT_PATH + 'fontbureau/DecovarAlpha-VF.ttf'

EXPORT_PATH = '_export/'+ fontPath.split('/')[-1].replace('ttf', 'pdf')
varFont = Font(fontPath)
varFontName = varFont.install()

axes = varFont.axes
#print sorted(axes.keys())

W = H = 600
M = 30 # Page padding

#====================

def makeAxisName(axisName):
    if not axisName in ('wght', 'wdth', 'opsz'):
        return axisName.upper()
    return axisName
    
class VariationCircle(Element):
    u"""Interpret the content of the self.font variation font and draw a circle info graphic on that info."""

    DEFAULT_FONT_SIZE = 64
    R = 2/3 # Fontsize factor to draw glyph markers.

    def __init__(self, font, x=None, y=None, w=None, h=None, glyphNames=None, location=None, angles=None, showAxisNames=True,
        **kwargs):
        Element.__init__(self, **kwargs)
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.font = font
        if angles is None:
            angles = self.initAngles() # Initialize the angles in equal parts if not defined.
        self.angles = angles
        self.showAxisNames = showAxisNames
        # Make sure that this is a formatted string. Otherwise create it with the current style.
        # Note that in case there is potential clash in the double usage of fill and stroke.
        self.glyphNames = glyphNames or 'e'
    
    def initAngles(self):
        totalAxes = len(self.font.axes)
        angle = -90
        angles = {}
        for axisIndex, axisName in enumerate(sorted(self.font.axes)):
            angles[axisName] = angle + axisIndex*360/totalAxes
        return angles 
        
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

    def _drawGlyphIcon(self, mx, my, glyphName, fontSize, location, strokeW=2):
        # Middle circle 
        context = self.context # Get context from the parent doc.
        context.fill(1)
        context.stroke(0, strokeW)
        context.oval(mx-fontSize*self.R, my-fontSize*self.R, fontSize*2*self.R, fontSize*2*self.R)

        context.drawGlyphPath(self.font, glyphName, mx, my-fontSize/4, fontSize=fontSize, fillColor=0)
           
    def build(self, view, origin):
        u"""Draw the circle info-graphic, showing most info about the variation font as can be interpreted from the file."""
        context = self.context # Get context from the parent doc.
        context.fill(0.9)
        context.stroke(None)
        x, y = point2D(pointOffset(self.oPoint, origin))
        mx = x + self.w/2
        my = y + self.h/2

        # Gray circle that defines the area of
        context.oval(x, y, self.w, self.h)
        
        # Draw axis spikes first, so we can cover them by the circle markers.
        axes = self.font.axes
        fontSize = self.style.get('fontSize', self.DEFAULT_FONT_SIZE)
        
        # Draw name of the font   
        bs = context.newString(self.font.info.familyName,
                                style=dict(font=self.style['labelFont'],
                                fontSize=self.style['axisNameFontSize'], textFill=0))     
        context.text(bs, (x-fontSize/2, y+self.h+fontSize/2))

        # Draw spokes
        context.fill(None)
        context.stroke(0)
        context.strokeWidth(1)
        context.newPath()
        for axisName, angle in self.angles.items():
            markerX, markerY = self._angle2XY(angle, self.w/2)
            context.moveTo((mx, my))
            context.lineTo((mx+markerX, my+markerY))
        context.drawPath()

        # Draw default glyph marker in middle.
        print '@#@##@', self.glyphNames
        glyphName = self.glyphNames[0]
        defaultLocation = {}
        self._drawGlyphIcon(mx, my, glyphName, fontSize, defaultLocation, strokeW=3)

        # Draw DeltaLocation circles.
        for axisName, (minValue, defaultValue, maxValue) in axes.items():
            angle = self.angles[axisName]
            # Outside maxValue 
            location = {axisName: maxValue}
            markerX, markerY = self._angle2XY(angle, self.w/2)
            self._drawGlyphIcon(mx+markerX, my+markerY, glyphName, fontSize/2, location)
            
            # Interpolated DeltaLocation circles.
            location = {axisName: minValue + (maxValue - minValue)*INTERPOLATION}
            markerX, markerY = self._angle2XY(angle, self.w/4)
            self._drawGlyphIcon(mx+markerX*INTERPOLATION*2, my+markerY*INTERPOLATION*2, glyphName, fontSize/2, location)

        # Draw axis names and DeltaLocation values
        if self.showAxisNames:
            for axisName, (minValue, defaultValue, maxValue) in axes.items():
                angle = self.angles[axisName]
                location = {axisName: maxValue}
                valueFontSize = self.style.get('valueFontSize', 12)
                axisNameFontSize = self.style.get('axisNameFontSize', 12)
                markerX, markerY = self._angle2XY(angle, self.w/2)
                fs = context.newString(makeAxisName(axisName),
                                 style=dict(font=self.style.get('labelFont', 'Verdana'),
                                            fontSize=axisNameFontSize,
                                            fill=self.style.get('axisNameColor', 0)))
                tw, th = context.textSize(fs)
                context.fill((0.7, 0.7, 0.7, 0.6))
                context.stroke(None)
                context.rect(mx+markerX-tw/2-4, my+markerY-axisNameFontSize/2-th*1.5-4, tw+8, th)
                context.text(fs, (mx+markerX-tw/2, my+markerY-axisNameFontSize/2-th*1.5)) 
                
                # DeltaLocation master value
                if maxValue < 10:
                    sMaxValue = '%0.2f' % maxValue
                else:
                    sMaxValue = `int(round(maxValue))`
                fs = context.newString(sMaxValue,
                                 style=dict(font=self.style.get('labelFont', 'Verdana'),
                                            fontSize=valueFontSize,
                                            fill=self.style.get('axisValueColor', 0)))
                tw, th = context.textSize(fs)
                context.fill((0.7, 0.7, 0.7, 0.6))
                context.stroke(None)
                context.rect(mx+markerX-tw/2-4, my+markerY+valueFontSize/2+th*1.5-4, tw+8, th)
                context.text(fs, (mx+markerX-tw/2, my+markerY+valueFontSize/2+th*1.5)) 

                # DeltaLocation value
                interpolationValue = minValue + (maxValue - minValue)*INTERPOLATION
                if interpolationValue < 10:
                    sValue = '%0.2f' % interpolationValue
                else:
                    sValue = `int(round(interpolationValue))`
                bs = context.newString(sValue,
                                 style=dict(font=self.style.get('labelFont', 'Verdana'),
                                            fontSize=valueFontSize,
                                            fill=self.style.get('axisValueColor', 0)))
                tw, th = context.textSize(bs)
                context.fill((0.7, 0.7, 0.7, 0.6))
                context.stroke(None)
                context.rect(mx+markerX*INTERPOLATION-tw/2-4, my+markerY*INTERPOLATION+valueFontSize/2+th*1.5-4, tw+8, th)
                context.text(fs, (mx+markerX*INTERPOLATION-tw/2, my+markerY*INTERPOLATION+valueFontSize/2+th*1.5)) 

                # DeltaLocation value
                if minValue < 10:
                    sValue = '%0.2f' % minValue
                else:
                    sValue = `int(round(minValue))`
                bs = context.newString(sValue,
                                 style=dict(font=self.style.get('labelFont', 'Verdana'),
                                            fontSize=valueFontSize,
                                            fill=self.style.get('axisValueColor', 0)))
                tw, th = context.textSize(bs)
                context.fill((0.7, 0.7, 0.7, 0.6))
                context.stroke(None)
                minM = 0.2
                context.rect(mx+markerX*minM-tw/2-4, my+markerY*minM+th*0.5-4, tw+8, th)
                context.text(fs, (mx+markerX*minM-tw/2, my+markerY*minM+th*0.5)) 

#====================

FONT_SIZE = VariationCircle.DEFAULT_FONT_SIZE
INTERPOLATION = 0.5
    
# Create new document with (w,h) and fixed amount of pages.
# Make number of pages with default document size.
# Initially make all pages default with template
doc = Document(w=W, h=H, autoPages=1) 
 
# Change template of page 1
page = doc[0]
glyphName = 'A' 

#print(sorted(varFont.axes.keys()))
# ['BLDA', 'BLDB', 'SKLA', 'SKLB', 'SKLD', 'TRMA', 'TRMB', 'TRMC', 'TRMD', 'TRME', 'TRMF', 'TRMG', 'TRMK', 'TRML', 'WMX2']
location = varFont.getDefaultVarLocation()

style = dict(fontSize=FONT_SIZE, labelFont='Verdana', axisNameFontSize=14, 
    valueFontSize=10, axisNameColor=(1, 0, 0))

VariationCircle(varFont, x=M, y=H+M, w=W-M*2, h=H-M*2, glyphNames=glyphName,
    location=location, parent=page, style=style, showAxisNames=True, fill=0.8)

doc.export(EXPORT_PATH) 

