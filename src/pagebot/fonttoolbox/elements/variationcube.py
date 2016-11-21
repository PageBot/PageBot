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
from drawBot import fill, rect, stroke, strokeWidth

class VariationCube(Element):
    # Initialize the default behavior tags as different from Element.

    def __init__(self, style=None, eId=None, **kwargs):
        self.eId = eId
        self.style = makeStyle(style, **kwargs) # Combine self.style from
        # Each element should check at this point if the minimum set of style values
        # are set and if their values are valid.
        assert self.w is not None and self.h is not None # Make sure that these are defined.
        # Make sure that this is a formatted string. Otherwise create it with the current style.
        # Note that in case there is potential clash in the double usage of fill and stroke.

    def draw(self, page, x, y):
    	stroke(0)
    	strokeWidth(0.5)
    	fill(None)
    	rect(x, y, self.w, self.h)

	def makeMatrix(rs, page, s, steps):
	    u"""Add more parametric layout behavior here.
	    x = rs['ml']
	    y = rs['mb']
	    for weight in range(0, 1000, int(1000/steps)):
	        for width in range(0, 1000, int(1000/steps)):
	            fontName = getFontByLocation(weight, width)
	            fs = FormattedString(s, font=fontName,  fontSize=72, fill=0)
	            w, h = fs.size()
	            page.text(fs, x+weight/2-w/2, y+width/2)  
		"""