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
#     glyphpath.py
#
from pbpath import Path
from pagebot.toolbox.transformer import pointOffset
from pagebot.style import NO_COLOR, DEFAULT_HEIGHT, DEFAULT_WIDTH, ORIGIN

class GlyphPath(Path):

    def __init__(self, glyph, w=None, h=None, pathFilter=None, **kwargs):
        Path.__init__(self, **kwargs)
        self.font = glyph.font # Store separate, to avoid disappearing weakref.
        self.glyph = glyph 
        # One of the two needs to be defined, the other can be None.
        # If both are set, then the image scales disproportional.
        self.w = w
        self.h = h
        self.iw = glyph.width
        self.ih = self.font.info.unitsPerEm
        self.pathFilter = pathFilter # Optional pathFilter method, called with self as param.

    # Set the intended width and calculate the new scale, validating the
    # width to the image minimum width and the height to the image minimum height.
    # Also the proportion is calculated, depending on the ratio of """
    def _get_w(self):
        if not self._w: # Width is undefined
            if self._h and self.ih:
                return self.iw * self._h / self.ih  # Height is lead, calculate width.
            return DEFAULT_WIDTH # Undefined and without parent, answer default width.
        return self._w # Width is lead and defined as not 0 or None.
    def _set_w(self, w):
        self._w = w # If self._h is set too, do disproportioan sizing. Otherwise set to 0 or None.
    w = property(_get_w, _set_w)

    def _get_h(self):
        if not self._h: # Width is undefined
            if self._w and self.iw:
                return self.ih * self._w / self.iw  # Width is lead, calculate height.
            return DEFAULT_HEIGHT # Undefined and without parent, answer default width.
        return self._h # Height is lead and defined as not 0 or None.
    def _set_h(self, h):
        self._h = h # If self._w is set too, do disproportional sizing. Otherwise set to 0 or None.
    h = property(_get_h, _set_h)

    def build_drawBot(self, view, origin=ORIGIN, drawElements=True):
        
        c = self.context # Get current context
        b = c.b # Get context builder

        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(view, p)    
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        c.saveGraphicState()
        sh = 1.0*self.h/self.ih
        b.transform((1, 0, 0, 1, px, py))
        c.scale(sh)
        # If there is a path filter defined, then call that the draw and ignore regular drawing.
        if self.pathFilter is not None:
            self.pathFilter(self, self.glyph.path, view)
        elif self.css('fill') != NO_COLOR or self.css('stroke') != NO_COLOR:
            # Not path filter defined, draw by regular stroke/fill.
            c.setFillColor(self.css('fill'))
            c.setStrokeColor(self.css('stroke', NO_COLOR), (self.css('strokeWidth') or 20))
            c.strokeWidth(20)
            c.drawPath(self.glyph.path)
        c.restoreGraphicState()

        if drawElements:
            for e in self.elements:
                e.build_flat(view, p)

        # Draw optional bounding box.
        #self.drawFrame(origin, view)
 
        self._restoreScale(view)
        view.drawElementMetaInfo(self, origin) # Depends on css flag 'showElementInfo'
