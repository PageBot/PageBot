#!/usr/bin/env python
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
from pagebot.elements.paths.pbpath import Path
from pagebot.toolbox.units import pointOffset
from pagebot.toolbox.color import noColor
from pagebot.style import DEFAULT_HEIGHT, DEFAULT_WIDTH, ORIGIN

class GlyphPath(Path):
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
    125
    >>> e.w = 150
    >>> e.w, e.w == page[e.eId].w
    (150, True)
    
    """
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
        
        context = self.context # Get current context

        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)    
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        context.save()
        sh = 1.0*self.h/self.ih
        context.transform((1, 0, 0, 1, px, py))
        context.scale(sh)
        # If there is a path filter defined, then call that the draw and ignore regular drawing.
        if self.pathFilter is not None:
            self.pathFilter(self, self.glyph.path, view)
        elif self.css('fill') is not noColor or self.css('stroke') is not noColor:
            # Not path filter defined, draw by regular stroke/fill.
            context.fill(self.css('fill'))
            context.stroke(self.css('stroke', noColor), (self.css('strokeWidth') or 20))
            context.strokeWidth(20)
            context.drawPath(self.glyph.path)
        context.restore()

        if drawElements:
            for e in self.elements:
                e.build_flat(view, p)

        # Draw optional bounding box.
        #self.drawFrame(origin, view)
 
        self._restoreScale(view)
        view.drawElementMetaInfo(self, origin) # Depends on css flag 'showElementInfo'


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
