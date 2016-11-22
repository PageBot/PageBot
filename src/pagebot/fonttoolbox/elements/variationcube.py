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
from pagebot.elements import Element
from pagebot.style import makeStyle
from drawBot import fill, rect, stroke, strokeWidth, installFont, installedFonts, FormattedString
from pagebot.fonttoolbox.variationbuilder import generateInstance

class VariationCube(Element):
    # Initialize the default behavior tags as different from Element.

    def __init__(self, s=None, style=None, eId=None, **kwargs):
        self.eId = eId
        self.style = makeStyle(style, **kwargs) # Combine self.style from
        # Each element should check at this point if the minimum set of style values
        # are set and if their values are valid.
        assert self.w is not None and self.h is not None # Make sure that these are defined.
        # Make sure that this is a formatted string. Otherwise create it with the current style.
        # Note that in case there is potential clash in the double usage of fill and stroke.
        self.glyphNames = s or 'a'

    FONT_PATH = '../../../fonts/'

    def getFontByLocation(self, weight, width):
        name = 'PromisePageBot-wght%d-wdth%d' % (weight, width)
        location = dict(wght=weight, wdth=width)
        
        VFONT_PATH = 'PromisePageBot-GX.ttf'
        if not name in installedFonts():
            path = self.FONT_PATH + VFONT_PATH
            installFont(path)
            fontName, fontPath = generateInstance(self.FONT_PATH + VFONT_PATH, 
                location, targetDirectory=self.FONT_PATH + 'instances')
        else:
            fontName =  name
        return fontName
	    
    def draw(self, page, x, y):
        stroke(0)
        strokeWidth(0.5)
        fill(None)
        rect(x, y, self.w, self.h)
        steps = 5
        """Add more parametric layout behavior here."""
        
        for weight in range(0, 1000, int(1000/steps)):
            for width in range(0, 1000, int(1000/steps)):
                fontName = self.getFontByLocation(weight, width)
                fs = FormattedString(self.glyphNames, font=fontName,  fontSize=72, fill=0)
                w, h = fs.size()
                ox = oy = 40
                page.text(fs, ox + x + weight / 2 - w / 2, oy + y + width / 2)  
		