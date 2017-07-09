# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     drawPart.py
#
from drawBot import cmykStroke, newPath, drawPath, moveTo, lineTo, strokeWidth, oval, text, rect, fill, curveTo, closePath, FormattedString
from pagebot.toolbox.transformer import point3D

#   Additional drawing stuff.

def drawArrow(e, view, xs, ys, xt, yt, onText=1, startMarker=False, endMarker=False):
    u"""Draw curved arrow marker between the two points.
    TODO: Add drawing of real arrow-heads, rotated in the right direction."""
    fms = e.css('flowMarkerSize')
    fmf = e.css('flowCurvatureFactor')
    if onText == 1:
        c = e.css('flowConnectionStroke2', NO_COLOR)
    else:
        c = e.css('flowConnectionStroke1', NO_COLOR)
    setStrokeColor(c, e.css('flowConnectionStrokeWidth'))
    if startMarker:
        setFillColor(e.css('flowMarkerFill', NO_COLOR))
        oval(xs - fms, ys - fms, 2 * fms, 2 * fms)
    xm = (xt + xs)/2
    ym = (yt + ys)/2
    xb1 = xm + onText * (yt - ys) * fmf
    yb1 = ym - onText * (xt - xs) * fmf
    xb2 = xm - onText * (yt - ys) * fmf
    yb2 = ym + onText * (xt - xs) * fmf
    # Arrow head position
    arrowSize = 12
    arrowAngle = 0.4
    angle = atan2(xt-xb2, yt-yb2)
    hookedAngle = radians(degrees(angle)-90)
    ax1 = xt - cos(hookedAngle+arrowAngle) * arrowSize
    ay1 = yt + sin(hookedAngle+arrowAngle) * arrowSize
    ax2 = xt - cos(hookedAngle-arrowAngle) * arrowSize
    ay2 = yt + sin(hookedAngle-arrowAngle) * arrowSize
    newPath()
    setFillColor(None)
    moveTo((xs, ys))
    curveTo((xb1, yb1), (xb2, yb2), ((ax1+ax2)/2, (ay1+ay2)/2)) # End in middle of arrow head.
    drawPath()

    #  Draw the arrow head.
    newPath()
    setFillColor(c)
    setStrokeColor(None)
    moveTo((xt, yt))
    lineTo((ax1, ay1))
    lineTo((ax2, ay2))
    closePath()
    drawPath()
    if endMarker:
        oval(xt - fms, yt - fms, 2 * fms, 2 * fms)

