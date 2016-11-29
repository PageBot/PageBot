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
    def __init__(self, path, s=None, style=None, eId=None, dimensions=None, **kwargs):
        self.fontPath = path
        self.familyName = path.split('/')[-1].split('-')[0]
        self.fontDir = '/'.join(path.split('/')[:-1])
        self.eId = eId
        self.style = makeStyle(style, **kwargs) # Combine self.style from
        # Try to figure out the requested dimensions per axes.
        if dimensions is None:
            dimensions = (('wght',4), ('wdth',6))
        self.dimensions = dimensions
        # Each element should check at this point if the minimum set of style values
        # are set and if their values are valid.
        assert self.w is not None and self.h is not None # Make sure that these are defined.
        # Make sure that this is a formatted string. Otherwise create it with the current style.
        # Note that in case there is potential clash in the double usage of fill and stroke.
        self.glyphNames = s or 'a'

    FONT_PATH = '../../../fonts/'
    #VFONT_PATH = 'PromisePageBot-GX.ttf'
    #VFONT_NAME = 'PromisePageBot-Bold'
    VFONT_NAME = 'BitcountGrid-Double'

    def installMaster(self):
        if not self.VFONT_NAME in installedFonts():
            installFont(self.fontPath)

    def getFontByLocation(self, location):
        name = '%s-' % self.familyName
        for axisName, axisValue in sorted(location.items()):
            name += '-%s%d' % (axisName, axisValue)
        
        if not name in installedFonts():
            masterPath = self.fontPath
            targetDir = self.fontDir + '/instances/'
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)
            instancePath = targetDir + name + '.ttf'
            if not os.path.exists(instancePath):
                print targetDir, instancePath
                fontName, fontPath = generateInstance(masterPath, location, targetDirectory=targetDir)
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
        if len(self.dimensions) == 1:
            raise ValueError('Not supporting 1 axis now')
        if len(self.dimensions) > 2:
            raise ValueError('Not supporting >2 axis now')
        
        axisNames = sorted(self.dimensions.keys())
        axisX = axisNames[0]
        sizeX = self.dimensions[axisX]
        axisY = axisNames[1]
        sizeY = self.dimensions[axisY]
        stepX = self.w / (sizeX+1)
        stepY = self.h / (sizeY+1)
        """Add more parametric layout behavior here."""
        RANGE = 1000
        for indexX in range(sizeX+1):
            for indexY in range(sizeY+1):
                fontName = self.getFontByLocation({axisX:indexX * RANGE / sizeX, axisY:indexY * RANGE / sizeY})
                fs = FormattedString(self.glyphNames, font=fontName, fontSize=self.style['fontSize'], fill=0)
                w, h = fs.size()
                ox = 40
                oy = 30
                page.text(fs, ox + x + indexX * stepX - w / 2, oy + y + indexY * stepY)  
                fs = FormattedString('%s %d\n%s %d' % (axisX, indexX * RANGE / sizeX, axisY, indexY * RANGE / sizeY), fontSize=6, fill=0)
                w, h = fs.size()
                page.text(fs, ox + x + indexX * stepX - w / 2, oy + y + indexY * stepY - 16)  

		