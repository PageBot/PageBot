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
#     variableglyphs.py
#
#     Show a string of variable glyphs, using spacing and kerning of the
#     defined instance locations.
#

from copy import copy
from pagebot import getContext
from pagebot.constants import ORIGIN
from pagebot.elements.element import Element
from pagebot.style import makeStyle
from pagebot.toolbox.units import pointOffset

context = getContext()

class VariableGlyphs(Element):
    # Initialize the default behavior tags as different from Element.

    def __init__(self, ttFont, s=None, style=None, eId=None,
                 fontSize=50, location=None, **kwargs):
        super().__init__()
        self.font = ttFont
        self.eId = eId
        self.fontSize = fontSize
        self.style = makeStyle(style, **kwargs) # Combine self.style from
        # Each element should check at this point if the minimum set of style values
        # are set and if their values are valid.
        assert self.w is not None and self.h is not None # Make sure that these are defined.
        # Make sure that this is a formatted string. Otherwise create it with the current style.
        # Note that in case there is potential clash in the double usage of fill and stroke.
        self.glyphNames = s or 'e'
        # Store the external location, to allow other axis values to be set.
        if location is None:
            location = {}
        self.location = copy(location)

    def build(self, view, origin=ORIGIN, **kwargs):
        c = self.context
        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        px, py, _ = self._applyAlignment(p) # Ignore z-axis for now.
        view.drawElementFrame(self, p, **kwargs)
        fillColor = self.style.get('fill')
        #fillColor = (0, 0, 0)
        #if fillColor is not None:
        #    c = self.doc.context
        #    c.setFillColor(fillColor)
        #    c.setStrokeColor(None)
        #else:
        #    fillColor = (0, 0, 0)
        glyphPathScale = self.fontSize/self.font.info.unitsPerEm
        context.drawGlyphPath(c, self.font.ttFont, self.glyphNames[0], px, py,
                      self.location, glyphPathScale, fillColor)
        self.buildChildElements(view, p)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
