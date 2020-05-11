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
#     polygon.py
#
from pagebot.elements.element import Element
from pagebot.constants import XXXL
from pagebot.toolbox.units import pointOffset
from pagebot.toolbox.color import noColor
from pagebot.toolbox.units import point2D, units, pt

class Polygon(Element):
    """The Polygon element is a simple implementation of the polygon DrawBot
    function. More complex path-like elements inherit from the Path element."""

    def __init__(self, points=None, closed=True, **kwargs):
        self.closed = closed
        if points is None:
            points = []
        self.points = points[:] # Force copy, so caller cannot change and not change size cache.
        Element.__init__(self, **kwargs)

    def append(self, p):
        p = units(point2D(p))
        assert p is not None
        self.points.append(p)

    def _get_x(self):
        """
        >>> pn = Polygon()
        >>> pn.rect(10, 10, 200, 360)
        >>> pn.x, pn.left
        (10pt, 10pt)
        >>> pn.x = 300
        >>> pn.x, pn.left, pn.box
        (300pt, 300pt, (300pt, 10pt, 200pt, 360pt))
        """
        return self.box[0]
    def _set_x(self, x):
        self.move((x - self.x, 0))
    x = property(_get_x, _set_x)

    def _get_y(self):
        return self.box[1]
    def _set_y(self, y):
        self.move((0, y - self.y))
    y = property(_get_y, _set_y)

    def _get_w(self):
        return self.box[2]
    def _set_w(self, w):
        """Scale horizontal to w
        """
        if self.w:
            self.scale(w/self.w, 1)
    w = property(_get_w, _set_w)

    def _get_h(self):
        return self.box[3]
    def _set_h(self, newH):
        """Scale horizontal to w
        """
        if self.h:
            self.scale(1, h/self.h)
    h = property(_get_h, _set_h)

    def move(self, p):
        """
        >>> pn = Polygon()
        >>> pn.rect(10, 10, 200, 360)
        >>> pn.x, pn.left
        (10pt, 10pt)
        >>> pn.move((120, 10))
        >>> pn.x, pn.left, pn.box
        (130pt, 130pt, (130pt, 20pt, 200pt, 360pt))
        """
        dx, dy = point2D(p)
        points = []
        for point in self.points:
            points.append((point[0] + dx, point[1] + dy))
        self.points = points

    def scale(self, sx, sy=None):
        """
        >>> pn = Polygon()
        >>> pn.rect(10, 10, 200, 360)
        >>> pn.x, pn.left
        (10pt, 10pt)
        >>> pn.scale(0.6)
        >>> pn.x, pn.left, pn.box
        (10pt, 10pt, (10pt, 10pt, 80pt, 144pt))
        """
        if sy is None:
            sy = sx
        x, y, w, h = self.box
        points = []
        for point in self.points:
            px = (x - point[0]) * sx + point[0]
            py = (y - point[1]) * sy + point[1]
            points.append((px, py))
        self.points = points

    def _get_box(self):
        """ Get the (x, y, w, h) box of all points.

        >>> e = Polygon()
        >>> e.rect(100, 100, 220, 330)
        >>> e.points
        [(100pt, 100pt), (100pt, 430pt), (320pt, 430pt), (320pt, 100pt)]

        >>> e.box
        (100pt, 100pt, 220pt, 330pt)
        """
        x = y = XXXL
        w = h = 0
        if not self.points:
            return pt(0, 0, 0, 0)
        for point in self.points:
            x = min(x, point[0])
            y = min(y, point[1])
            w = max(w, point[0]-x)
            h = max(h, point[1]-y)
        return x, y, w, h
    box = property(_get_box)

    def rect(self, x, y, w, h):
        """Creates a rectangle polygon.

        >>> e = Polygon()
        >>> e.rect(10, 10, 220, 330)
        >>> e.points
        [(10pt, 10pt), (10pt, 340pt), (230pt, 340pt), (230pt, 10pt)]
        >>> e.block
        (220pt, 330pt)
        """
        self.points = []
        self.append((x, y))
        self.append((x, y+h))
        self.append((x+w, y+h))
        self.append((x+w, y))
        self.closePath = True

    def _get_block(self):
        """Answer the bounding box of the containted points.

        >>> e = Polygon()
        >>> e.append((0, 0))
        >>> e.append((100, 0))
        >>> e.append((50, 80))
        >>> e.closePath = True
        >>> e.points
        [(0pt, 0pt), (100pt, 0pt), (50pt, 80pt)]
        >>> e.block
        (100pt, 80pt)
        """
        return self.box[2:]
    block = property(_get_block)

    def getBezierPath(self, p=None):
        """Answer a BezierPath representation, in the data-format of self.context,
        translated to optional position p

        >>> from pagebot.contexts import getContext
        >>> context = getContext('DrawBot')
        >>> e = Polygon(context=context)
        >>> e.rect(100, 100, 300, 400)
        >>> e.getBezierPath((150, 150))
        <BezierPath>
        """
        if p is None:
            p = (0, 0)
        """
        # create a bezier path
        path = self.context.b.BezierPath()
        # draw a triangle
        # move to a point
        path.moveTo((200, 200))
        # line to a point
        path.lineTo((200, 300))
        path.lineTo((400, 300))
        path.lineTo((400, 100))
        path.lineTo((300, 50))
        # close the path
        path.closePath()
        # save the graphics state so the clipping happens only
        # temporarily
        return path
        """
        context = self.context # Should be None
        assert context is not None
        path = context.b.BezierPath()
        if self.points:
            for pIndex, point in enumerate(self.points):
                print('dssdsdds', p)
                x = point[0] + p[0]
                y = point[1] + p[1]
                if pIndex == 0:
                    path.moveTo((x, y))
                else:
                    path.lineTo((x, y))
        path.closePath()
        return path

    #   D R A W B O T / F L A T  S U P P O R T

    def build(self, view, origin, drawElements=True, **kwargs):
        context = self.context # Get current context and builder.
        b = context.b # This is a bit more efficient than self.b once we got context

        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        self._applyRotation(view, p)

        self.buildFrame(view, p) # Draw optional frame or borders.

        # Let the view draw frame info for debugging, in case view.showFrame == True
        # and self.isPage or if self.showFrame. Mark that we are drawing background here.
        view.drawPageMetaInfo(self, p)

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        #context.fill(self.css('fill'))
        #context.stroke(self.css('stroke', noColor), self.css('strokeWidth'))
        #bezierPath = self.getBezierPath(p)
        #b.drawPath(bezierPath)

        # Debugging where it moved.
        context.b.fill(0, 0, 1, 0.5)
        context.b.rect(px, py, self.w, self.h)

        if drawElements:
            # If there are child elements, recursively draw them over the pixel image.
            self.buildChildElements(view, p, **kwargs)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        # Let the view draw frame info for debugging, in case view.showFrame == True
        # and self.isPage or if self.showFrame. Mark that we are drawing foreground here.
        view.drawPageMetaInfoBackground(self, p)

        self._restoreRotation(view, p)
        self._restoreScale(view)
        view.drawElementInfo(self, origin) # Depends on flag 'view.showElementInfo'

    #   H T M L  /  C S S  S U P P O R T

    def build_html(self, view, origin=None, drawElements=True):
        """Drawing HTML Polygon through SVG?"""
        context = self.context # Get current context and builder.
        b = context.b # This is a bit more efficient than self.b once we got context
        # TODO: Needs a solution, SVG or pixels?

class Mask(Polygon):
    """Masks don't draw by themselves. They get interpreted by sibling elements,
    such as Image.
    """
    def XXXbuild(self, view, origin, drawElements=True, **kwargs):
        pass

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
