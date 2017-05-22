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
from pagebot.fonttoolbox.objects.fontinfo import FontInfo
from pagebot.toolbox.transformer import point3D
from pagebot.fonttoolbox.objects.glyph import *
from pagebot.fonttoolbox.objects.font import Font


C = 0.5
F = 2 / 3
glyphName = 'a'
dx = 200
x = 50
r = 10

PATH = u"/Library/Fonts/F5MultiLanguageFontVar.ttf"
font = Font(PATH, install=False)
glyph = font[glyphName]
path = BezierPath()

def drawSegment(segment):
    assert len(segment) > 1

    if len(segment) == 2:
        point = segment[-1]
        #print 'bla'
        path.lineTo((point.x, point.y))
        print '     * line to %d, %d' % (point.x, point.y)

    elif len(segment) == 3:
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
        print '     * curve to (%s, %s, %s)' % (offCurve0, offCurve1, onCurve)
    else:
        curve0 = segment[:2]
        curve1 = segment[2:]
        offCurve0 = segment[1]
        offCurve1 = segment[2]
            
        # Implied point.
        x = offCurve0.x + (offCurve1.x - offCurve0.x) * 0.5
        y = offCurve0.y + (offCurve1.y - offCurve0.y) * 0.5
        newOnCurve = Point(x, y, True)
        circle(x, y, r/2, color='green')
        curve0.append(newOnCurve)
        curve1.insert(0, newOnCurve)

        # Recurse.
        drawSegment(curve0)
        drawSegment(curve1)

def circle(x, y, r, color='pink'):
    if color == 'pink':
        fill(1, 0, 1)
    elif color == 'green':
        fill(0, 1, 0)
    elif color == 'blue':
        fill(0, 0, 1)
    oval(x - r, y - r, r*2, r*2)

contours = []
contour = None    
coordinates = glyph.ttGlyph.coordinates

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

# Draws oncurve and (slightly smaller) offcurve points
for contour in contours:
    for i, point in enumerate(contour):
        x = point.x
        y = point.y
            
        if point.onCurve:
            circle(x, y, r)
        else:
            circle(x, y, r/ 2)
    
numSegs = 0

for n, contour in enumerate(contours):
    print ' * contour %d' % n, contour

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
        print '   * segment %d' % j, segment
        drawSegment(segment)
    
    numSegs += len(segments)
        
fill(None)
stroke(1, 0, 0)
strokeWidth(1)
drawPath(path)

print '\nPageBot\n'

c = glyph.contours
pbSegments = glyph._segments
print len(segments)
print len(pbSegments)
for segment in pbSegments:
    print segment
    
fill(0)
drawPath(glyph._path)


