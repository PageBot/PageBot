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
#     markers.py
#
from pagebot.toolbox.units import point3D
from pagebot.toolbox.color import color, noColor

def drawRegistrationMark(context, origin, cmSize, cmStrokeWidth, vertical):
    """Draw registration mark as position x, y.

    >>> from pagebot.toolbox.units import pt
    >>> from pagebot.contexts.flatcontext import FlatContext
    >>> context = FlatContext()
    >>> context.newPage(pt(100), pt(100))
    >>> drawRegistrationMark(context, pt(0,0), pt(20), pt(1), True)
    """
    x, y = origin
    if vertical:
        dx = cmSize/2
        dy = cmSize
    else:
        dx = cmSize
        dy = cmSize/2
    context.fill(noColor)
    context.stroke(color(c=1, m=1, y=1, k=1), w=cmStrokeWidth)
    context.newPath()
    # Registration circle
    context.oval(x - cmSize/4, y - cmSize/4, cmSize/2, cmSize/2)
    # Registration cross, in length of direction.
    context.moveTo((x - dx, y)) # Horizontal line.
    context.lineTo((x + dx, y))
    context.moveTo((x, y + dy)) # Vertical line.
    context.lineTo((x, y - dy))
    context.drawPath()

def drawRegistrationMarks(context, origin, w, h, cmSize, cmStrokeWidth):
    """Draw standard registration mark, to show registration of CMYK colors.
    https://en.wikipedia.org/wiki/Printing_registration.

    >>> from pagebot.toolbox.units import pt
    >>> from pagebot.contexts.flatcontext import FlatContext
    >>> c = FlatContext()
    >>> c.newPage(pt(100), pt(100))
    >>> drawRegistrationMarks(c, pt(0,0), pt(100), pt(100), pt(20), pt(1))
    """
    x, y, _ = point3D(origin)
    drawRegistrationMark(context, (x + w/2, y - cmSize), cmSize, cmStrokeWidth, False) # Bottom registration mark
    drawRegistrationMark(context, (x - cmSize, y + h/2), cmSize, cmStrokeWidth, True) # Left registration mark
    drawRegistrationMark(context, (x + w + cmSize, y + h/2), cmSize, cmStrokeWidth, True) # Right registration mark
    drawRegistrationMark(context, (x + w/2, y + h + cmSize), cmSize, cmStrokeWidth, False) # Top registration mark

def drawCropMarks(context, origin, w, h, bleed, cmSize, cmStrokeWidth, folds=None):
    """If the show flag is set, then draw the cropmarks or page frame.

    >>> from pagebot.toolbox.units import pt
    >>> from pagebot.contexts.flatcontext import FlatContext
    >>> c = FlatContext()
    >>> c.newPage(pt(100), pt(100))
    >>> drawCropMarks(c, pt(0,0), pt(100), pt(100), False, pt(20), pt(1))
    """
    x, y, _ = point3D(origin) # Ignore z-axus for now.
    context.fill(noColor)
    context.stroke(color(cmyk=(1,1,1,1)), w=cmStrokeWidth)
    context.newPath()
    # Bottom left
    context.moveTo((x - bleed, y))
    context.lineTo((x - cmSize, y))
    context.moveTo((x, y - bleed))
    context.lineTo((x, y - cmSize))
    # Bottom right
    context.moveTo((x + w + bleed, y))
    context.lineTo((x + w + cmSize, y))
    context.moveTo((x + w, y - bleed))
    context.lineTo((x + w, y - cmSize))
    # Top left
    context.moveTo((x - bleed, y + h))
    context.lineTo((x - cmSize, y + h))
    context.moveTo((x, y + h + bleed))
    context.lineTo((x, y + h + cmSize))
    # Top right
    context.moveTo((x + w + bleed, y + h))
    context.lineTo((x + w + cmSize, y + h))
    context.moveTo((x + w, y + h + bleed))
    context.lineTo((x + w, y + h + cmSize))
    # Any fold lines to draw?
    if folds is not None:
        for fx, fy in folds:
            if fx is not None:
                context.moveTo((x + fx, y - bleed))
                context.lineTo((x + fx, y - cmSize))
                context.moveTo((x + fx, y + h + bleed))
                context.lineTo((x + fx, y + h + cmSize))
            if fy is not None:
                context.moveTo((x - bleed, y + fy))
                context.lineTo((x - cmSize, y + fy))
                context.moveTo((x + w + bleed, y + fy))
                context.lineTo((x + w + cmSize, y + fy))
    context.drawPath()

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
