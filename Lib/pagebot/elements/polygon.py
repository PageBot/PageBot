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
from pagebot.constants import XXXL, ORIGIN
from pagebot.toolbox.units import point2D, units, pt
from pagebot.toolbox.color import noColor

class Polygon(Element):
    """The Polygon element is a simple implementation of the polygon DrawBot
    function. More complex path-like elements inherit from the Path element.
    The (w, y) dependent on the point positions in the self.points list.  The
    (x, y) position defines the relative position of the path on output."""

    def __init__(self, points=None, closed=True, **kwargs):
        self.closed = closed
        if points is None:
            points = []

        # Force copy, so calling function can't change size cache.
        self.points = points[:]
        self.closed = closed
        Element.__init__(self, **kwargs)

    def append(self, p):
        p = units(point2D(p))
        assert p is not None
        self.points.append(p)

    def _get_w(self):
        return self.box[2]
    def _set_w(self, w):
        """Scale horizontal to w
        """
        if self.w:
            self._set_scale(w/self.w, 1)

    w = property(_get_w, _set_w)

    def _get_h(self):
        return self.box[3]
    def _set_h(self, newH):
        """Scale horizontal to w
        """
        if self.h:
            self._set_scale(1, newH/self.h)
    h = property(_get_h, _set_h)

    #   D R A W B O T / F L A T  S U P P O R T

    def build(self, view, origin=ORIGIN, **kwargs):
        p = self.getPosition(view, origin)
        self.buildFrame(view, p)
        view.drawPageMetaInfoBackground(self, p)
        self.context.fill(self.css('fill'))
        self.context.stroke(self.css('stroke', noColor), self.css('strokeWidth'))
        points = []

        # Calculate offsets.
        for point in self.points:
            px = point[0] + p[0]
            py = point[1] + p[1]
            points.append((px, py))

        self.context.polygon(*points)
        self.buildChildElements(view, p, **kwargs)
        view.drawPageMetaInfo(self, p)
        self.restore(view, p)
        self.drawMeta(view, origin)

    #   H T M L  /  C S S  S U P P O R T

    def build_html(self, view, origin=None):
        """Drawing HTML Polygon through SVG?

        TODO: implement, SVG or pixels?
        """

    def translate(self, p):
        """
        >>> pn = Polygon(x=120, y=130)
        >>> pn.rect(10, 10, 200, 360)
        >>> pn.x, pn.left
        (120pt, 120pt)
        >>> pn.box
        (130pt, 140pt, 200pt, 360pt)
        >>> # Move the position of the embedded points, not (self.x, self.y).
        >>> pn.translate((120, 10))
        >>> pn.x, pn.left
        (120pt, 120pt)
        >>> pn.box
        (250pt, 150pt, 200pt, 360pt)
        """
        dx, dy = point2D(p)
        points = []
        for point in self.points:
            points.append((point[0] + dx, point[1] + dy))
        self.points = points

    def _set_scale(self, sx, sy=None):
        """
        >>> pn = Polygon(x=33, y=44)
        >>> pn.rect(10, 10, 200, 360)
        >>> pn.x, pn.left
        (33pt, 33pt)
        >>> # Element position + point positions.
        >>> pn.box
        (43pt, 54pt, 200pt, 360pt)
        >>> pn._set_scale(0.6)
        >>> pn.x, pn.left
        (33pt, 33pt)
        >>> pn.box
        (39pt, 50pt, 120pt, 216pt)
        """
        points = []

        if sy is None:
            sy = sx

        for point in self.points:
            # Scale relative to (self.x, self.y) origin.
            px = point[0] * sx
            py = point[1] * sy
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
            x = min(x, self.x+point[0])
            y = min(y, self.y+point[1])
            w = max(w, self.x+point[0]-x)
            h = max(h, self.y+point[1]-y)

        # (x, y) including (self.x, self.y).
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
        # Relative offset to (self.x, self.y).
        self.append((x, y))
        self.append((x, y+h))
        self.append((x+w, y+h))
        self.append((x+w, y))
        self.closePath = True

    def _get_block(self):
        """Answers the bounding box of the contained points,
        relative to (self.x, self.y).

        >>> e = Polygon(x=125, y=230)
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

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
