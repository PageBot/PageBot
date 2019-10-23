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
#	  variablecube2.py
#

from copy import copy
from pagebot.elements.element import Element
from pagebot.style import makeStyle
from pagebot.toolbox.units import pointOffset
from pagebot.toolbox.color import blackColor

class VariableCube2(Element):
    """
    >>> from pagebot.fonttoolbox.objects.font import findFont
    >>> from pagebot.document import Document
    >>> vfFont = findFont('RobotoDelta_v2-VF')
    >>> from pagebot.fonttoolbox.objects.font import findFont
    >>> doc = Document(w=500, h=500, originTop=False, autoPages=1)
    >>> page = doc[1]
    >>> page.padding = 40
    >>> vc = VariableCube2(vfFont, parent=page, x=40, y=40, w=page.pw)
    """
    # Initialize the default behavior tags as different from Element.

    def __init__(self, font, point=None, parent=None, style=None,
                 name=None, captionStyle=None, caption=None, 
                 location=None, dimensions=None, 
                 clipRect=None, mask=None, imo=None, **kwargs):
        Element.__init__(self, point=point, parent=parent, style=style,
                         name=name, **kwargs)

        self.vfFont = font
        self.style = makeStyle(style, **kwargs) # Combine self.style from
        # Try to figure out the requested dimensions if the element display per axes.
        if dimensions is None:
            dimensions = dict(wght=5, wdth=5, opsz=5)
        self.dimensions = dimensions
        # Each element should check at this point if the minimum set of style values
        # are set and if their values are valid.
        assert self.w is not None and self.h is not None # Make sure that these are defined.
        # Make sure that this is a formatted string. Otherwise create it with the current style.
        # Note that in case there is potential clash in the double usage of fill and stroke.

        # FIXME: Review this: the 's' variable below is undefined.
        #self.glyphNames = s or 'e'
        self.glyphNames = 'e'

        # Store the external location, to allow other axis values to be set.
        if location is None:
            location = {}
        self.location = copy(location)
    
    def draw(self, view, origin):
        c = self.doc.context

        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)    
        px, py, _ = self._applyAlignment(p) # Ignore z-axis for now.

        fillColor = self.style.get('fill')
        if fillColor is not None:
            c.fill(fillColor)

        c.stroke((0.8, 0.8, 0.8), 0.5)
        c.rect(px, py, self.w, self.h)
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
                ox = 30
                oy = 25
                ppx = ox + px + indexX * stepX
                ppy = oy + py + indexY * stepY
                self.location[axisX] = indexX * RANGE / sizeX
                self.location[axisY] = indexY * RANGE / sizeY
                glyphPathScale = self.fontSize/self.font.info.unitsPerEm

                c.drawGlyphPath(c, self.vfFont.ttFont, self.glyphNames[0],
                              ppx, ppy, self.location, s=glyphPathScale,
                              fillColor=(0, 0, 0))

                bs = c.newString('%s %d\n%s %d' % (axisX,
                                                       indexX * RANGE / sizeX,
                                                       axisY,
                                                       indexY * RANGE / sizeY),
                                     fontSize=6,
                                     fill=blackColor)
                w, h = bs.size()

                c.text(bs, ppx - stepX/4, ppy - 16)
                # Bit of hack, we need the width of the glyph here.

        bs = c.newString('Other axes: %s' % self.location,
                             fontSize=6, fill=blackColor)
        w, h = bs.size()
        c.text(bs, px, py - 16)


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
