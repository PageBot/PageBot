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
#     drawPart.py
#
from pagebot.toolbox.color import noColor
from math import sin, cos, atan2, radians, degrees

def drawArrow_drawBot(e, view, xs, ys, xt, yt, onText=1, startMarker=False, endMarker=False):
    """Draw curved arrow marker between the two points.
    TODO: Add drawing of real arrow-heads, rotated in the right direction."""
    context = view.context # Get current context
    b = context.b

    fms = e.css('flowMarkerSize')
    fmf = e.css('flowCurvatureFactor')
    if onText == 1:
        c = e.css('flowConnectionStroke2', noColor)
    else:
        c = e.css('flowConnectionStroke1', noColor)
    context.stroke(c, e.css('flowConnectionStrokeWidth'))
    if startMarker:
        context.fill(e.css('flowMarkerFill', noColor))
        context.oval(xs - fms, ys - fms, 2 * fms, 2 * fms)
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
    b.newPath()
    context.fill(None)
    b.moveTo((xs, ys))
    b.curveTo((xb1, yb1), (xb2, yb2), ((ax1+ax2)/2, (ay1+ay2)/2)) # End in middle of arrow head.
    b.drawPath()

    #  Draw the arrow head.
    b.newPath()
    context.fill(c)
    context.stroke(None)
    b.moveTo((xt, yt))
    b.lineTo((ax1, ay1))
    b.lineTo((ax2, ay2))
    b.closePath()
    b.drawPath()
    if endMarker:
        context.oval(xt - fms, yt - fms, 2 * fms, 2 * fms)

