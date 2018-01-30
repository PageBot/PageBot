#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     variableglyphs.py
#
#     Show a string of variable glyphs, using spacing and kerning of the
#     defined instance locations.
#
from __future__ import division

from copy import copy
from pagebot.contexts import defaultContext as context
from pagebot.elements import Element
from pagebot.style import makeStyle
from pagebot.fonttoolbox.variationbuilder import drawGlyphPath
from pagebot.toolbox.transformer import pointOffset


class VariableGlyphs(Element):
    # Initialize the default behavior tags as different from Element.

    def __init__(self, ttFont, s=None, style=None, eId=None,
                 fontSize=50, location=None, **kwargs):
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
    
    def draw(self, view, origin):

        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(view, p)    
        px, py, _ = self._applyAlignment(p) # Ignore z-axis for now.

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        fillColor = self.style.get('fill')
        #fillColor = (0, 0, 0)
        #if fillColor is not None:
        #    c = self.doc.context
        #    c.setFillColor(fillColor)
        #    c.setStrokeColor(None)
        #else:
        #    fillColor = (0, 0, 0)
        glyphPathScale = self.fontSize/self.font.info.unitsPerEm
        drawGlyphPath(self.font.ttFont, self.glyphNames[0], px, py,
                      self.location, s=glyphPathScale, fillColor=fillColor)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)
