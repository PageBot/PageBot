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
#     glyphpath.py
#

from pagebot.elements.bezierpaths import BezierPaths
from pagebot.toolbox.units import units
from pagebot.toolbox.color import noColor
from pagebot.constants import DEFAULT_HEIGHT, DEFAULT_WIDTH, ORIGIN

class GlyphPath(BezierPaths):
    """GlyphPath is an element to show the path of a glyph with additional features.

    >>> from pagebot.fonttoolbox.fontpaths import getTestFontsPath
    >>> from pagebot.fonttoolbox.objects.font import Font
    >>> fontPath = getTestFontsPath() + '/google/roboto/Roboto-Medium.ttf'
    >>> font = Font(fontPath)
    >>> from pagebot.document import Document
    >>> W = H = 500
    >>> M = 50
    >>> doc = Document(w=W, h=H, autoPages=1, padding=30)
    >>> page = doc[1]
    >>> e = GlyphPath(font['e'], x=20, parent=page, w=125)
    >>> page[e.eId].w # Show that this is a regular element, placed no the page.
    125pt
    >>> e.w = 150
    >>> e.w, e.w == page[e.eId].w
    (150pt, True)

    """
    def __init__(self, glyph, w=None, h=None, pathFilter=None, **kwargs):
        BezierPaths.__init__(self, **kwargs)
        # Store separately, to avoid disappearing weakref.
        self.font = glyph.font
        self.glyph = glyph

        # One of the two needs to be defined, the other should be None to scale
        # proportionally. If both are set, then the image scales
        # disproportionally.
        self.w = w
        self.h = h
        # Image width of the element equals the glyph width.
        self.iw = max(1, glyph.width)
        # Image height is the font em size.
        self.ih = self.font.info.unitsPerEm
        # Optional pathFilter method, called with self as param.
        self.pathFilter = pathFilter

    def _get_w(self):
        # Sets the intended width and calculates the new proportional height."""
        # Width is undefined.
        if not self._w:
            if self._h and self.ih:
                # Proportion is based on the height, calculate width.
                return self.iw * self._h / self.ih
            # Undefined and without parent, answer default width.
            return DEFAULT_WIDTH

        # Proportion is based on width, defined as not 0 or None.
        return self._w

    def _set_w(self, w):
        # If self._h is set too, do disproportioan sizing. Otherwise set to 0 or None.
        self._w = units(w or DEFAULT_WIDTH)
    w = property(_get_w, _set_w)

    def _get_h(self):
        # Width is undefined.
        if not self._h:
            if self._w and self.iw:
                # Width is lead, calculate height.
                return self.ih * self._w / self.iw
            # Undefined and without parent, answer default width.
            return DEFAULT_HEIGHT
        # Height is lead and defined as not 0 or None.
        return self._h

    def _set_h(self, h):
        # If self._w is set too, do disproportional sizing. Otherwise set to 0
        # or None.
        self._h = units(h or DEFAULT_HEIGHT)
    h = property(_get_h, _set_h)

    def build(self, view, origin=ORIGIN, **kwargs):
        p = self.getPosition(view, origin)
        self.buildFrame(view, p) # Draw optional frame, shadow or borders.
        px, py, _ = p

        #self.context.save() # TODO: fix in Flat.
        self.context.translate(px, py)
        # Scale needs to bev a ratio value, not a unit.
        sx, sy = (self.w/self.iw).rv, (self.h/self.ih).rv
        self.context.scale(sx, sy)

        # If a path filter is defined, call it and ignore regular drawing.
        if self.pathFilter is not None:
            self.pathFilter(self, self.glyph, view)
        else:
            # No path filter defined, draws regular stroke and fill.
            self.context.fill(self.css('fill'))
            self.context.stroke(self.css('stroke', noColor), (self.css('strokeWidth') or 0.5))
            self.context.drawGlyphPath(self.glyph)
        #self.context.restore() # TODO: fix in Flat.
        self.context.scale(1/sx, 1/sy)
        self.context.translate(-px, -py)

        self.buildChildElements(view, p, **kwargs)
        self.restore(view, p)
        self.drawMeta(view, origin)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
