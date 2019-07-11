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
#     beziercontour.py
#

class BezierContour(list):

    """
    A Bezier contour object.
    """

    def __init__(self, *args, **kwargs):
        super(BezierContour, self).__init__(*args, **kwargs)
        self.open = True

    def __repr__(self):
        return "<BezierContour>"

    def _get_clockwise(self):
        from fontTools.pens.areaPen import AreaPen
        pen = AreaPen()
        pen.endPath = pen.closePath
        self.drawToPen(pen)
        return pen.value < 0

    clockwise = property(_get_clockwise, doc="A boolean representing if the contour has a clockwise direction.")

    def drawToPointPen(self, pointPen):
        pointPen.beginPath()
        for i, segment in enumerate(self):
            if len(segment) == 1:
                segmentType = "line"
                if i == 0 and self.open:
                    segmentType = "move"
                pointPen.addPoint(segment[0], segmentType=segmentType)
            else:
                pointPen.addPoint(segment[0])
                pointPen.addPoint(segment[1])
                pointPen.addPoint(segment[2], segmentType="curve")
        pointPen.endPath()

    def drawToPen(self, pen):
        for i, segment in enumerate(self):
            if i == 0:
                pen.moveTo(*segment)
            elif len(segment) == 1:
                pen.lineTo(*segment)
            else:
                pen.curveTo(*segment)
        if self.open:
            pen.endPath()
        else:
            pen.closePath()

    def _get_points(self):
        return [point for segment in self for point in segment]

    points = property(_get_points, doc="Return a list of all the points making up this contour, regardless of whether they are on curve or off curve.")
