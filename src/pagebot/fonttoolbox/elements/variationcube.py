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
#	  variationcube.py
#
import os
from pagebot.elements import Element
from pagebot.style import makeStyle
from drawBot import fill, rect, stroke, strokeWidth, installFont, installedFonts, FormattedString
from pagebot.fonttoolbox.variationbuilder import generateInstance

class VariationCube(Element):
    # Initialize the default behavior tags as different from Element.

    LABELS = {
        'wgth': ('Weight',),
        'wdth': ('Width',),
        'opsz': ('Optical size',),
    }
    def __init__(self, s=None, style=None, eId=None, dimensions=None, **kwargs):
        self.eId = eId
        self.style = makeStyle(style, **kwargs) # Combine self.style from
        # Try to figure out the requested dimensions per axes.
        if dimensions is None:
            dimensions = dict(wght=6, wdth=6)
        self.dimensions = dimensions
        # Each element should check at this point if the minimum set of style values
        # are set and if their values are valid.
        assert self.w is not None and self.h is not None # Make sure that these are defined.
        # Make sure that this is a formatted string. Otherwise create it with the current style.
        # Note that in case there is potential clash in the double usage of fill and stroke.
        self.glyphNames = s or 'a'

    FONT_PATH = '../../../fonts/'
    VFONT_PATH = 'PromisePageBot-GX.ttf'
    VFONT_NAME = 'PromisePageBot-Bold'

    def installMaster(self):
        if not self.VFONT_NAME in installedFonts():
            path = self.FONT_PATH + VFONT_PATH
            installFont(path)

    def getFontByLocation(self, weight, width):
        name = 'PromisePageBot--wght%d-wdth%d' % (weight, width)
        location = dict(wght=weight, wdth=width)
        
        if not name in installedFonts():
            masterPath= self.FONT_PATH + self.VFONT_PATH
            targetPath = self.FONT_PATH + 'instances/'
            instancePath = targetPath + name + '.ttf'
            if not os.path.exists(instancePath):
                print targetPath, instancePath
                fontName, fontPath = generateInstance(masterPath, location, targetDirectory=targetPath)
            installFont(fontPath)
        else:
            fontName =  name
        return fontName
	    
    def draw(self, page, x, y):
        self.installMaster()
        fillColor = self.style.get('fill')
        if fillColor is not None:
            setFillColor(fillColor)
            setStrokColor(None)

        stroke(0)
        strokeWidth(0.5)
        fill(None)
        rect(x, y, self.w, self.h)
        weights = self.dimensions['wght']
        widths = self.dimensions['wdth']
        stepX = self.w / (weights+1)
        stepY = self.h / (widths+1)
        """Add more parametric layout behavior here."""
        RANGE = 1000
        for weight in range(weights+1):
            for width in range(widths+1):
                fontName = self.getFontByLocation(weight * RANGE / weights, width * RANGE / widths)
                fs = FormattedString(self.glyphNames, font=fontName, fontSize=60, fill=0)
                w, h = fs.size()
                ox = 40
                oy = 40
                page.text(fs, ox + x + weight * stepX - w / 2, oy + y + width * stepY)  
                fs = FormattedString('wght %d\nwdth %d' % (weight * RANGE / weights, width * RANGE / widths), fontSize=6, fill=0)
                w, h = fs.size()
                page.text(fs, ox + x + weight * stepX - w / 2, oy + y + width * stepY - 16)  

		