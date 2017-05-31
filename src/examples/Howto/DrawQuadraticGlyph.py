# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     DrawQuadraticGlyph.py
#
#     Shows how to draw quadratic curves with cubic curves.
#
import weakref
from AppKit import NSFont
from fontTools.ttLib import TTFont, TTLibError
from drawBot import BezierPath
from drawBot import font as DBFont
from drawBot import translate, line, text, stroke, fill, oval, drawPath, \
        textSize
from pagebot.fonttoolbox.objects.fontinfo import FontInfo
from pagebot.toolbox.transformer import point3D
from pagebot.fonttoolbox.objects.glyph import *
from pagebot.fonttoolbox.objects.font import Font

def drawSegment(segment, verbose=False):
    u"""
    Draws a quadratic segment as a cubic Bézier curve in drawBot. Each segment
    starts and ends with an oncurve point with 0 ... n offcurve control points.

    NOTE: PageBot implementation in glyph adds the first oncurve
    as a separate `cp` parameter.

    >>> p0 = Point(100, 100, True)
    >>> p1 = Point(200, 100, False)
    >>> p2 = Point(200, 200, True)
    >>> segment = [p0, p1, p2]
    >>> drawSegment(segment)
    """
    assert len(segment) > 1

    if len(segment) == 2:
        # Two on curves gives a line.
        point = segment[-1]
        path.lineTo((point.x, point.y))
        prevOnCurve = (point.x, point.y)

        if verbose:
            print '     * line to %d, %d' % (point.x, point.y)

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
        circle(x0, y0, r/4, color='blue')
        circle(x1, y1, r/4, color='blue')
        onCurve = (onCurve1.x, onCurve1.y)
        path.curveTo(offCurve0, offCurve1, onCurve)
        stroke(0, 0, 0, 0.4)
        line((onCurve0.x, onCurve0.y), offCurve0)
        line(offCurve1, onCurve)
        stroke(None)

        if verbose:
            print '     * curve to (%s, %s, %s)' % (offCurve0, offCurve1, onCurve)
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
        circle(x, y, r/2, color='pink')
        curve0.append(newOnCurve)
        curve1.insert(0, newOnCurve)

        if verbose:
            print '     * Implied point %s' % newOnCurve

        # Recurse.
        # NOTE: PageBot implementation in glyph uses a loop instead of
        # recursion.
        drawSegment(curve0)
        drawSegment(curve1)

def circle(x, y, r, color='pink'):
    u"""
    >>> circle(100, 100, 5, color='green')
    """
    stroke(None)
    # Draws on/offcurve dots.
    if color == 'pink':
        fill(1, 0, 1, 0.5)
    elif color == 'green':
        fill(0, 1, 0, 0.5)
    elif color == 'blue':
        fill(0, 0.5, 1, 0.5)
    oval(x - r, y - r, r*2, r*2)
    stroke(1)

def cross(x, y, d, r=1, g=0, b=0, a=1):
    u"""
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
    stroke(r, g, b)
    line((x0, y0), (x1, y1))
    line((x2, y2), (x3, y3))

C = 0.5
F = 2 / 3
glyphName = 'C'
dx = 200
x = 50
r = 10

PATH = u"/Library/Fonts/F5MultiLanguageFontVar.ttf"
PATH = u"/Library/Fonts/BigCaslon.ttf"
font = Font(PATH, install=False)
glyph = font[glyphName]
path = BezierPath()
contours = []
contour = None
coordinates = glyph.ttGlyph.coordinates

# Move glyph up so we can see results below descender level.
translate(0, 200)

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

    d = 3
    x += d
    y += d
    text('%d' % i, (x, y))

# Draws oncurve points (pink) and offcurve control points (green).
for contour in contours:
    for i, point in enumerate(contour):
        x = point.x
        y = point.y

        if point.onCurve:
            circle(x, y, r)
        else:
            # Quadratic offcurves.
            circle(x, y, r/ 4, color='green')

for n, contour in enumerate(contours):
    segments = []
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
        drawSegment(segment)


# Enable to let this script draw the path.
fill(None)
stroke(1, 0, 0)
strokeWidth(1)
drawPath(path)


# Enable to draw path as built by PageBot glyph.
c = glyph.contours
pbSegments = glyph._segments

fill(0, 0, 0, 0.5)
stroke(0, 1, 0)
drawPath(glyph._path)

# Some annotations specifically for the letter 'Q'.
if glyphName == 'Q':
    textSize('32')
    line((730, 370), (750, 350))
    line((730, 200), (750, 190))
    line((725, 260), (750, 250))
    line((685, 590), (750, 650))
    line((560, 725), (750, 652))

    DBFont('LucidaGrande', 20)
    stroke(None)
    fill(0)
    text('On-curve point', (755, 350))
    text('Quadratic control point', (755, 185))
    text('Cubic control point', (755, 245))
    text('Implied on-curve point', (755, 650))

u"""
# This is not being parsed by doctest!
>>> print a
'a'
"""
