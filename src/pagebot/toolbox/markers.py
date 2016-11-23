# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     markers.py
#
from drawBot import stroke, newPath, drawPath, moveTo, lineTo, strokeWidth, oval, text, rect, fill, curveTo, closePath, FormattedString

def drawRegistrationMark(x, y, cmSize, cmStrokeWidth, vertical):
    u"""Draw registration mark as position x, y."""
    if vertical:
        dx = cmSize/2
        dy = cmSize
    else:
        dx = cmSize
        dy = cmSize/2
    fill(None)
    stroke(0)
    strokeWidth(cmStrokeWidth)
    newPath()
    # Registration circle
    oval(x - cmSize/4, y - cmSize/4, cmSize/2, cmSize/2)
    # Registration cross, in length of direction.
    moveTo((x - dx, y)) # Horizontal line.
    lineTo((x + dx, y))
    moveTo((x, y + dy)) # Vertical line.
    lineTo((x, y - dy))
    drawPath()

def drawRegistrationMarks(ox, oy, w, h, cmSize, cmStrokeWidth):
    u"""Draw standard registration mark, to show registration of CMYK colors.
    https://en.wikipedia.org/wiki/Printing_registration."""
    drawRegistrationMark(ox + w/2, oy - cmSize, cmSize, cmStrokeWidth, False) # Bottom registration mark
    drawRegistrationMark(ox - cmSize, oy + h/2, cmSize, cmStrokeWidth, True) # Left registration mark
    drawRegistrationMark(ox + w + cmSize, oy + h/2, cmSize, cmStrokeWidth, True) # Right registration mark
    drawRegistrationMark(ox + w/2, oy + h + cmSize, cmSize, cmStrokeWidth, False) # Top registration mark

def drawCropMarks(x, y, w, h, bleed, cmSize, cmStrokeWidth, folds=None):
    u"""If the show flag is set, then draw the cropmarks or page frame."""
    fill(None)
    stroke(0)
    strokeWidth(cmStrokeWidth)
    newPath()
    # Bottom left
    moveTo((x - bleed, y))
    lineTo((x - cmSize, y))
    moveTo((x, y - bleed))
    lineTo((x, y - cmSize))
    # Bottom right
    moveTo((x + w + bleed, y))
    lineTo((x + w + cmSize, y))
    moveTo((x + w, y - bleed))
    lineTo((x + w, y - cmSize))
    # Top left
    moveTo((x - bleed, y + h))
    lineTo((x - cmSize, y + h))
    moveTo((x, y + h + bleed))
    lineTo((x, y + h + cmSize))
    # Top right
    moveTo((x + w + bleed, y + h))
    lineTo((x + w + cmSize, y + h))
    moveTo((x + w, y + h + bleed))
    lineTo((x + w, y + h + cmSize))
    # Any fold lines to draw?
    if folds is not None:
        for fx, fy in folds:
            if fx is not None:
                moveTo((x + fx, y - bleed))
                lineTo((x + fx, y - cmSize))
                moveTo((x + fx, y + h + bleed))
                lineTo((x + fx, y + h + cmSize))
            if fy is not None:
                moveTo((x - bleed, y + fy))
                lineTo((x - cmSize, y + fy))
                moveTo((x + w + bleed, y + fy))
                lineTo((x + w + cmSize, y + fy))
    drawPath()


