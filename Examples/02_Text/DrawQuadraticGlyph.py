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
#     DrawQuadraticGlyph.py
#
#     Shows how to draw quadratic curves with cubic curves.
#
#    TODO: test with Flat.
#    TODO: switch to document level.

import weakref
from AppKit import NSFont
from fontTools.ttLib import TTFont, TTLibError
from drawBot import BezierPath, translate, line, text, stroke, fill, oval, drawPath
from drawBot import font as DBFont
from pagebot.fonttoolbox.objects.fontinfo import FontInfo
from pagebot.toolbox.units import point3D
from pagebot.fonttoolbox.fontpaths import getFontPaths
from pagebot.fonttoolbox.objects.glyph import *
from pagebot.fonttoolbox.objects.font import Font
from pagebot import getContext
from pagebot.toolbox.color import blueColor, redColor, greenColor, pinkColor, orangeColor

R = 12
ONCURVE_COLOR = orangeColor
ONCURVE_SIZE = R
IMPLIED_ONCURVE_COLOR = redColor
IMPLIED_ONCURVE_SIZE = R
QUADRATIC_CONTROLPOINT_COLOR = greenColor
QUADRATIC_CONTROLPOINT_SIZE = R
CUBIC_CONTROLPOINT_COLOR = pinkColor
CUBIC_CONTROLPOINT_SIZE = R / 2

context = getContext()

class Point:
    # FIX: See more generic implentation in PageBotPath
    def __init__(self, x, y, onCurve=True, smooth=False, start=False):
        self.x = x
        self.y = y
        self.onCurve = onCurve
        self.smooth = smooth
        self.start = start

def drawSegment(path, segment, implied, cps, verbose=False):
    """
    Draws a quadratic segment as a cubic Bézier curve in drawBot. Each segment
    starts and ends with an oncurve point with 0 ... n offcurve control points.

    NOTE: PageBot implementation in glyph adds the first oncurve
    as a separate `cp` parameter.

    >>> p0 = Point(100, 100, True)
    >>> p1 = Point(200, 100, False)
    >>> p2 = Point(200, 200, True)
    >>> segment = [p0, p1, p2]
    >>> path = BezierPath()
    >>> drawSegment(path, segment)
    """
    assert len(segment) > 1

    if len(segment) == 2:
        # Two on curves gives a line.
        point = segment[-1]
        path.lineTo((point.x, point.y))
        prevOnCurve = (point.x, point.y)

        if verbose:
            print('     * line to %d, %d' % (point.x, point.y))

    elif len(segment) == 3:
        # Quadratic offcurve is split into two cubic offcurves.
        onCurve0 = segment[0]
        offCurve = segment[1]
        onCurve1 = segment[2]

        x0 = onCurve0.x + (offCurve.x - onCurve0.x) * F
        y0 = onCurve0.y + (offCurve.y - onCurve0.y) * F
        offCurve0 = (x0, y0)
        x1 = onCurve1.x - (onCurve1.x - offCurve.x) * F
        y1 = onCurve1.y - (onCurve1.y - offCurve.y) * F
        offCurve1 = (x1, y1)
        context.fill(CUBIC_CONTROLPOINT_COLOR)
        context.circle(x0, y0, CUBIC_CONTROLPOINT_SIZE)
        context.circle(x1, y1, CUBIC_CONTROLPOINT_SIZE)
        onCurve = (onCurve1.x, onCurve1.y)
        path.curveTo(offCurve0, offCurve1, onCurve)
        context.stroke(0.7)
        context.line((onCurve0.x, onCurve0.y), offCurve0)
        context.line(offCurve1, onCurve)
        context.stroke(None)

        # Store these so they can be used in the infographic.
        cps.append(offCurve0)
        cps.append(offCurve1)

        if verbose:
            print('     * curve to (%s, %s, %s)' % (offCurve0, offCurve1, onCurve))
    else:
        # Implied points are calculated and inserted. Number depends on amount
        # of consecutive offcurves.
        curve0 = segment[:2]
        curve1 = segment[2:]
        offCurve0 = segment[1]
        offCurve1 = segment[2]
        x = offCurve0.x + (offCurve1.x - offCurve0.x) * 0.5
        y = offCurve0.y + (offCurve1.y - offCurve0.y) * 0.5
        newOnCurve = Point(x, y, True)

        # Store these so they can be used in the infographic.
        implied.append(newOnCurve)
        context.fill(IMPLIED_ONCURVE_COLOR)
        context.circle(x, y, IMPLIED_ONCURVE_SIZE)
        curve0.append(newOnCurve)
        curve1.insert(0, newOnCurve)

        if verbose:
            print('     * Implied point %s' % newOnCurve)

        # Recurse.
        # NOTE: PageBot implementation in glyph uses a loop instead of
        # recursion.
        drawSegment(path, curve0, implied, cps)
        drawSegment(path, curve1, implied, cps)

def cross(x, y, d, r=1, g=0, b=0, a=1):
    """
    >>> cross(100, 100, 5, r=0.5, g=0.3, b=0.2, a=0.4)
    """
    x0 = x - d
    y0 = y - d
    x1 = x + d
    y1 = y + d
    x2 = x + d
    y2 = y - d
    x3 = x - d
    y3 = y + d
    context.stroke(r, g, b)
    line((x0, y0), (x1, y1))
    line((x2, y2), (x3, y3))

def draw():
    W, H = 1750, 2250
    X0 = 75
    Y0 = 500
    C = 0.5
    F = 2 / 3
    glyphName = 'Q'
    x = 50
    context.newPage(W, H)
    DBFont('LucidaGrande', 24)
    PATH = getFontPaths()['Roboto-Black']
    font = Font(PATH)
    glyph = font[glyphName]
    path = BezierPath()
    contours = []
    contour = None
    coordinates = glyph.ttGlyph.coordinates
    context.fill((0, 1, 1, 0.2))
    # Move glyph up so we can see results below descender level.
    translate(X0, Y0)

    # Draws the glyph.
    c = glyph.contours
    pbSegments = glyph._segments
    context.stroke((0, 0.3, 0.3))
    context.drawGlyphPath(glyph)
    context.stroke(None)
    context.fill(0)

    # Converts coordinates to PageBot Points and assigns points
    # to contours.
    for i, (x, y) in enumerate(coordinates):
        start = i - 1 in glyph.endPtsOfContours
        p = Point(x, y, glyph.flags[i])

        if i == 0:
            contour = [p]
        elif start:
            contour.append(contour[0])
            contours.append(contour)
            contour = [p]
        else:
            contour.append(p)

        if i == len(coordinates) - 1:
            contour.append(contour[0])
            contours.append(contour)

        d = 15
        x += d
        y += d
        context.text('%d' % i, (x, y))

    segments = []
    implied = []
    cps = []

    for n, contour in enumerate(contours):
        point = contour[0]
        segment = [point]
        path.moveTo((point.x, point.y))

        for i, point in enumerate(contour[1:]):
            if point.onCurve:
                segment.append(point)
                segments.append(segment)
                segment = [point]
            else:
                segment.append(point)

        for j, segment in enumerate(segments):
            # Lets this script calculate and draw implied points and derived cubic
            # control points. Optionally draw path itself later by calling
            # drawPath(path) (see below.)
            drawSegment(path, segment, implied, cps)

    # Draws oncurve points and offcurve control points.
    for contour in contours:
        for i, point in enumerate(contour):
            x = point.x
            y = point.y

            if point.onCurve:
                context.fill(ONCURVE_COLOR)
                context.circle(x, y, ONCURVE_SIZE)
            else:
                # Quadratic offcurves.
                context.fill(QUADRATIC_CONTROLPOINT_COLOR)
                context.circle(x, y, QUADRATIC_CONTROLPOINT_SIZE)

    x = 500
    y = 400
    d = 30
    context.fill(0.2)

    context.stroke((1, 0, 0))
    context.line((0, 0), (W -2*X0, 0))

    x = 0
    y = -100 + 24
    context.line((x, y), (x, y - 114))

    x += 30
    y = -100 + ONCURVE_SIZE

    context.stroke(None)
    context.fill(ONCURVE_COLOR)
    context.circle(x, y, ONCURVE_SIZE)
    y -= 30
    context.fill(IMPLIED_ONCURVE_COLOR)
    context.circle(x, y, IMPLIED_ONCURVE_SIZE)
    y -= 30
    context.fill(CUBIC_CONTROLPOINT_COLOR)
    context.circle(x, y, CUBIC_CONTROLPOINT_SIZE)
    y -= 30
    context.fill(QUADRATIC_CONTROLPOINT_COLOR)
    context.circle(x, y, QUADRATIC_CONTROLPOINT_SIZE)

    context.fill(0)
    x += 30
    y = -100
    context.text('On-curve point', (x, y))
    y -= 30
    context.text('Implied on-curve point', (x, y))
    y -= 30
    context.text('Cubic control point', (x, y))
    y -= 30
    context.text('Quadratic control point', (x, y))

draw()
