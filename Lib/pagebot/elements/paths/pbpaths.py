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
#     bppaths.py
#
#     The Paths element holds an ordered list of PageBotPath elements, where each can
#     have its own optional style, that overwrites the generic style of self.
#
from pagebot.elements.element import Element
from pagebot.elements.paths import PageBotPath
from pagebot.toolbox.units import pointOffset, upt

class Paths(Element):
    """Draw rectangle, default identical to Element itself.

    >>> from pagebot.document import Document
    >>> from pagebot.toolbox.color import color
    >>> from pagebot.toolbox.units import pt, inch
    >>> from pagebot.contexts import getContext
    >>> context = getContext()
    >>> path1 = PageBotPath(context=context)
    >>> path1.style['fill'] = color(1, 0, 0)
    >>> path1.oval(100, 100, 200, 200)
    >>> context.drawPath(path1)

    >>> path2 = PageBotPath(context=context) # Leaves current self._path untouched
    >>> path2.style['fill'] = color(rgb='blue') # Add color with the path style.
    >>> len(path2.points)
    0
    >>> ox, oy = pt(50, 50)
    >>> path2.moveTo((ox, oy)) # Drawing on context._path
    >>> path2.lineTo((ox+100, oy))
    >>> path2.lineTo((ox+100, oy+100))
    >>> path2.lineTo((ox, oy+100))
    >>> path2.lineTo((ox, oy))
    >>> path2.closePath()
    >>> path2.oval(160-50, 160-50, 100, 100) # path.oval does draw directly on the path
    >>> len(path2.points)
    10
    >>> context.drawPath(path2, p=(0, 0)) # Draw self._path with various offsets
    >>> context.drawPath(path2, p=(200, 200))
    >>> context.drawPath(path2, p=(0, 200))
    >>> context.drawPath(path2, p=(200, 0))
    >>> context.saveImage('_export/DrawBotPath1.pdf')

    >>> size = pt(1000, 1000)
    >>> doc = Document(size=size, padding=30, originTop=False, context=context)
    >>> view = doc.view
    >>> view.padding = inch(1)
    >>> view.showPadding = True
    >>> view.showCropMarks = True
    >>> page = doc[1]
    >>> e = Paths([path1, path2], x=100, y=100, parent=page)
    >>> doc.export('_export/DrawBotPaths.pdf')
    >>>
    """

    PATH_CLASS = PageBotPath

    def __init__(self, paths=None, **kwargs):
        if paths is None:
            paths = []
        elif not isinstance(paths, (tuple, list)):
            paths = [paths] # Create an ordered list of PageBotPath instances
        self.paths = paths
        for path in paths:
            assert isinstance(path, self.PATH_CLASS)
        Element.__init__(self, **kwargs)

    def rect(self, x, y, w, h):
        path = PageBotPath(self.context)
        path.rect(x, y, w, h)
        self.paths.append(path)

    def _get_pathsW(self):
        """Read only property that answers the cumulated total width of all paths."""
        minX = 0 # At least cover the origin of the element, or smaller.
        maxX = 0
        for path in self.paths:
            bounds = path.bounds()
            minX = min(minX, bounds[0])
            maxX = max(maxX, bounds[2])
        return max(0, maxX - minX)
    pathsW = property(_get_pathsW)

    def _get_w(self):
        """Get the cumulated width of the bounding box of all paths combined.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path1 = PageBotPath(context=context)
        >>> path1.oval(100, 100, 200, 200)
        >>> path2 = PageBotPath(context=context)
        >>> path2.oval(200, 200, 200, 200)
        >>> e = Paths([path1, path2])
        >>> e.w
        400.0
        """
        return self.pathsW * self.scaleX
    def _set_w(self, w):
        """Set the scale accordingly, as the width of the cumulated paths is fixed."""
        bpw = self.pathsW
        if w and bpw:
            self.scaleX = self.scaleY = w/bpw # Default is proportional scaling
    w = property(_get_w, _set_w)

    def _get_pathsH(self):
        """Read only property that answers the cumulated total height of all paths."""
        minY = 0 # At least cover the origin of the element, or smaller.
        maxY = 0
        for path in self.paths:
            bounds = path.bounds()
            minY = min(minY, bounds[1])
            maxY = max(maxY, bounds[3])
        return max(0, maxY - minY)
    pathsH = property(_get_pathsH)

    def _get_h(self):
        """Get the cumulated height of the bounding box of all paths combined.

        >>> from pagebot.contexts import getContext
        >>> context = getContext()
        >>> path1 = PageBotPath(context=context)
        >>> path1.oval(100, 100, 200, 300)
        >>> path2 = PageBotPath(context=context)
        >>> path2.oval(200, 200, 200, 500)
        >>> e = Paths([path1, path2])
        >>> e.h
        700.0
        """
        return self.pathsH * self.scaleY
    def _set_h(self, h):
        """Set the scale accordingly, as the width of the cumulated paths is fixed."""
        bph = self.pathsH
        if h and bph:
            self.scaleX = self.scaleY = h/bph # Default is proportional scaling
    h = property(_get_h, _set_h)

    def build(self, view, origin, drawElements=True, **kwargs):
        """Default drawing method just drawing the frame.
        Probably will be redefined by inheriting element classes."""

        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        self._applyRotation(view, p)

        # No automatic frame drawing on Paths elements
        #self.buildFrame(view, p) # Draw optional frame or borders.

        # Let the view draw frame info for debugging, in case view.showFrame == True
        # and self.isPage or if self.showFrame. Mark that we are drawing background here.
        view.drawPageMetaInfo(self, p, background=True)

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        for path in self.paths:
            # Get the style file/stroke if defined in the path. Otherwise use the settings of self.
            context = self.context
            context.fill(path.style.get('fill', self.fill))
            context.stroke(path.style.get('stroke', self.stroke), path.style.get('strokeWidth', self.strokeWidth))
            context.drawPath(path, p=p, sx=self.scaleX, sy=self.scaleY)

        if drawElements:
            # If there are child elements, recursively draw them over the pixel image.
            self.buildChildElements(view, p, **kwargs)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        # Let the view draw frame info for debugging, in case view.showFrame == True
        # and self.isPage or if self.showFrame. Mark that we are drawing foreground here.
        view.drawPageMetaInfo(self, p, background=False)

        self._restoreRotation(view, p)
        self._restoreScale(view)
        view.drawElementInfo(self, origin) # Depends on flag 'view.showElementInfo'

class Mask(Paths):

    def build(self, view, origin, drawElements=True, **kwargs):
        """Default drawing method just drawing the frame.
        Probably will be redefined by inheriting element classes."""

        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        self._applyRotation(view, p)

        self.b.save()

        unifiedPath = None
        for path in self.paths:
            if unifiedPath is None:
                unifiedPath = path
            else:
                unifiedPath = unifiedPath.union(path)

        if unifiedPath is not None:
            self.b.translate(upt(px), upt(py))
            #self.b.fill(1, 0, 0)
            #self.b.drawPath(unifiedPath.bp)
            self.b.clipPath(unifiedPath.bp)

            self.b.translate(upt(-px), upt(-py))

        if drawElements:
            # If there are child elements, recursively draw them over the pixel image.
            self.buildChildElements(view, p, **kwargs)

        self.b.restore()


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
