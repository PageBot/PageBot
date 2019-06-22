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

from pagebot.elements.paths.pbpaths import Paths
from pagebot.toolbox.units import pointOffset, units
from pagebot.toolbox.color import noColor
from pagebot.constants import DEFAULT_HEIGHT, DEFAULT_WIDTH, ORIGIN

class GlyphPath(Paths):
    """GlyphPath is an element to show show the path of a glyph with additional features.

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
        Paths.__init__(self, **kwargs)
        self.font = glyph.font # Store separate, to avoid disappearing weakref.
        self.glyph = glyph
        # One of the two needs to be defined, the other should be None to scale proportional.
        # If both are set, then the image scales disproportional.
        self.w = w
        self.h = h
        self.iw = max(1, glyph.width) # Image width of the element equals the glyph width.
        self.ih = self.font.info.unitsPerEm # Image height is the font em size.
        self.pathFilter = pathFilter # Optional pathFilter method, called with self as param.

    # Set the intended width and calculate the new proportional height."""
    def _get_w(self):
        if not self._w: # Width is undefined
            if self._h and self.ih:
                return self.iw * self._h / self.ih  # Height is lead, calculate width.
            return DEFAULT_WIDTH # Undefined and without parent, answer default width.
        return self._w # Width is lead and defined as not 0 or None.
    def _set_w(self, w):
        self._w = units(w or DEFAULT_WIDTH) # If self._h is set too, do disproportioan sizing. Otherwise set to 0 or None.
    w = property(_get_w, _set_w)

    def _get_h(self):
        if not self._h: # Width is undefined
            if self._w and self.iw:
                return self.ih * self._w / self.iw  # Width is lead, calculate height.
            return DEFAULT_HEIGHT # Undefined and without parent, answer default width.
        return self._h # Height is lead and defined as not 0 or None.
    def _set_h(self, h):
        self._h = units(h or DEFAULT_HEIGHT) # If self._w is set too, do disproportional sizing. Otherwise set to 0 or None.
    h = property(_get_h, _set_h)

    def build(self, view, origin=ORIGIN, drawElements=True, **kwargs):

        context = self.context # Get current context

        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        context.save()
        context.translate(px, py)
        sx, sy = (self.w/self.iw).rv, (self.h/self.ih).rv # We need the scale as ration value, not as unit.
        context.scale(sx, sy)
        # If there is a path filter defined, then call that the draw and ignore regular drawing.
        if self.pathFilter is not None:
            self.pathFilter(self, self.glyph, view)
        else: # Not path filter defined, draw by regular stroke/fill.
            context.fill(self.css('fill'))
            context.stroke(self.css('stroke', noColor), (self.css('strokeWidth') or 20))
            context.drawGlyphPath(self.glyph)
        context.restore()

        if drawElements:
            for e in self.elements:
                e.build(view, p, **kwargs)

        # Draw optional bounding box if view.showFrame = True
        self.buildFrame(view, p) # Draw optional frame, shadow or borders.

        self._restoreScale(view)
        view.drawElementInfo(self, origin) # Depends on css flag 'showElementInfo'


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
