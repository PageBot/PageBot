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
#     bpbezierpath.py
#

from pagebot.elements.element import Element
from pagebot.toolbox.units import pointOffset

class BezierPath(Element):
    """Draw rectangle, default identical to Element itself.

    >>> from pagebot.document import Document
    >>> from pagebot.toolbox.color import color
    >>> from pagebot.toolbox.units import pt, inch
    >>> from pagebot.contexts import getContext
    >>> context = getContext()
    >>> bp = context.newPath()
    >>> bp.oval(100, 100, 200, 200)

    >>> path = context.newPath() # Leaves current self._path untouched
    >>> len(path.points)
    0
    >>> path.moveTo((10, 10)) # Drawing on context._path
    >>> path.lineTo((110, 10))
    >>> path.lineTo((110, 110))
    >>> path.lineTo((10, 110))
    >>> path.lineTo((10, 10))
    >>> path.closePath()
    >>> path.oval(160-50, 160-50, 100, 100) # path.oval does draw directly on the path
    >>> len(path.points)
    19
    >>> context.fill((0, 0.5, 1))
    >>> context.drawPath(path, p=(0, 0)) # Draw self._path with various offsets
    >>> context.drawPath(path, p=(200, 200))
    >>> context.drawPath(path, p=(0, 200))
    >>> context.drawPath(path, p=(200, 0))
    >>> context.saveImage('_export/DrawBotContext2.pdf')

    >>> size = pt(1000, 1000)
    >>> doc = Document(size=size, padding=30, originTop=False, context=context)
    >>> view = doc.view
    >>> view.padding = inch(1)
    >>> view.showPadding = True
    >>> view.showCropMarks = True
    >>> page = doc[1]
    >>> e = BezierPath(bp, parent=page, fill=(0, 0, 0.5))
    >>> e.size, e.box
    ((200.0, 200.0), (0pt, 0pt, 200.0, 200.0))
    >>> e.scale
    (1, 1)
    >>> doc.export('_export/BezierPath1.pdf')
    >>> e.fill = 1, 0, 1
    >>> e.xy = 200, 200
    >>> doc.export('_export/BezierPath2.pdf')
    >>> e.fill = 1, 0, 0
    >>> e.w = 175
    >>> e.xy = 100, 100
    >>> e.w, e.scale
    (175.0, (0.875, 0.875))
    >>> doc.export('_export/BezierPath3.pdf')
    """
    def __init__(self, bezierPath, **kwargs):
        self.bezierPath = bezierPath
        Element.__init__(self, **kwargs)

    def _get_w(self):
        if self.bezierPath is None:
            return 0
        minX, _, maxX, _ = self.bezierPath.bounds()
        return (maxX - minX) * self.scaleX
    def _set_w(self, w):
        """Set the scale accordingly, as the with of the self._bezierPath is fixed."""
        bpw = self.w
        if w and bpw:
            self.scaleX = self.scaleY = w/self.w # Default is proportional scaling
    w = property(_get_w, _set_w)

    def _get_h(self):
        if self.bezierPath is None:
            return 0
        _, minY, _, maxY = self.bezierPath.bounds()
        return (maxY - minY) * self.scaleY
    def _set_h(self, h):
        """Set the scale accordingly, as the with of the self._bezierPath is fixed."""
        bph = self.h
        if h and bph:
            self.scaleX = self.scaleY = h/self.h # Default is propotional scaling
    h = property(_get_h, _set_h)

    def build(self, view, origin, drawElements=True):
        """Default drawing method just drawing the frame.
        Probably will be redefined by inheriting element classes."""
        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        self._applyRotation(view, p)

        self.buildFrame(view, p) # Draw optional frame or borders.

        # Let the view draw frame info for debugging, in case view.showFrame == True
        # and self.isPage or if self.showFrame. Mark that we are drawing background here.
        view.drawPageMetaInfo(self, p, background=True)

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        if self.bezierPath is not None:
            context = self.context
            context.fill(self.fill)
            context.stroke(self.stroke, self.strokeWidth)
            context.drawPath(self.bezierPath, p=p, sx=self.scaleX, sy=self.scaleY)

        if drawElements:
            # If there are child elements, recursively draw them over the pixel image.
            self.buildChildElements(view, p)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        # Let the view draw frame info for debugging, in case view.showFrame == True
        # and self.isPage or if self.showFrame. Mark that we are drawing foreground here.
        view.drawPageMetaInfo(self, p, background=False)

        self._restoreRotation(view, p)
        self._restoreScale(view)
        view.drawElementInfo(self, origin) # Depends on flag 'view.showElementInfo'

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
