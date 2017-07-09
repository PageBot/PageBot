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

ONCURVE = None
QUADRATIC_OFFCURVE = None
CUBIC_OFFCURVE = None
IMPLIED_ONCURVE = None
G =10

def drawSegment(segment, implied, cps, verbose=False):
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
        
        # Store these so they can be used in the infographic.
        cps.append(offCurve0)
        cps.append(offCurve1)

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

        # Store these so they can be used in the infographic.
        implied.append(newOnCurve)
        
        circle(x, y, r/2, color='pink')
        curve0.append(newOnCurve)
        curve1.insert(0, newOnCurve)

        if verbose:
            print '     * Implied point %s' % newOnCurve

        # Recurse.
        # NOTE: PageBot implementation in glyph uses a loop instead of
        # recursion.
        drawSegment(curve0, implied, cps)
        drawSegment(curve1, implied, cps)

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
glyphName = 'Q'
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
            if ONCURVE is None:
                ONCURVE = point
            circle(x, y, r)
        else:
            if QUADRATIC_OFFCURVE is None:
                QUADRATIC_OFFCURVE = point
            # Quadratic offcurves.
            circle(x, y, r/ 4, color='green')


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
        drawSegment(segment, implied, cps)

if len(implied) > 0:
    IMPLIED_ONCURVE = implied[0]

if len(cps) > 0:
    CUBIC_OFFCURVE = cps[0]


# Enable to draw path as built by PageBot glyph.
c = glyph.contours
pbSegments = glyph._segments
fill(0, 0, 0, 0.3)
stroke(0, 1, 0)
drawPath(glyph._path)
DBFont('LucidaGrande', 16)
stroke(None)
fill(0)

x = 500
y = 400
d = 30

if ONCURVE:
    stroke(0, 1, 1)
    p1 = (ONCURVE.x, ONCURVE.y)
    p = (ONCURVE.x + d, ONCURVE.y + d)
    line(p, p1)
    stroke(None)
    text('On-curve point', p)        
    y -= 20

if QUADRATIC_OFFCURVE:

    stroke(0, 1, 1)
    p1 = (QUADRATIC_OFFCURVE.x, QUADRATIC_OFFCURVE.y)
    p = (QUADRATIC_OFFCURVE.x + d, QUADRATIC_OFFCURVE.y + d)
    line(p, p1)
    stroke(None)
    text('Quadratic control point', p)
    
if CUBIC_OFFCURVE:


    stroke(0, 1, 1)
    p1 = (CUBIC_OFFCURVE[0], CUBIC_OFFCURVE[1])
    p = (CUBIC_OFFCURVE[0] + d, CUBIC_OFFCURVE[1]+ d)
    line(p, p1)
    stroke(None)
    text('Cubic control point', p)

if IMPLIED_ONCURVE:
    stroke(0, 1, 1)
    p1 = (IMPLIED_ONCURVE.x, IMPLIED_ONCURVE.y)
    p = (IMPLIED_ONCURVE.x + d, IMPLIED_ONCURVE.y + d)
    line(p, p1)
    stroke(None)
    text('Implied on-curve point', p)
