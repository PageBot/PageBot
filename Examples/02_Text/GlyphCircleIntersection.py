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
#     GlyphContourCircles.py
#
#     Draw a number of circles on the contour with equal distance.
#
from pagebot.fonttoolbox.objects.font import findFont
from pagebot import getContext
from pagebot.toolbox.color import color, noColor, blackColor

GLYPH_NAME = 'ampersand'

c = getContext()

c.newPage(1000, 1000)
c.scale(0.5)

font = findFont('Roboto-Regular')
glyph = font[GLYPH_NAME]

c.stroke(blackColor, 1)
c.fill(None)
print('Left margin:', glyph.leftMargin)
x = y = 100

# Draw markers on the glyph points
c.fill((1, 0, 0))
c.stroke(None)
for p in glyph.points:
	# TODO: Add drawing of off-on-off lines here
	if p.onCurve:
		r = 12
	else:
		r = 10
	c.oval(x+p.x-r/2, x+p.y-r/2, r, r)

c.fill(noColor)
c.stroke(blackColor)

# Draw the outline of the glyph
glyphPath = c.getGlyphPath(glyph)
#c.drawPath(glyphPath, (x+12, y-12))
# Draw the flattened outline of the glyph
flattenedPath = c.bezierPathByFlatteningPath(glyphPath)
c.fill(0.95)
c.drawPath(flattenedPath, (x, y))
# Draw the flattened contours/points
r = 6
c.fill(color(0, 0.5, 0))
c.stroke(noColor, 2)
for contour in c.getFlattenedContours(glyphPath):
    for p in contour:
        c.oval(x+p[0]-r/2, y+p[1]-r/2, r, r)

# Draw intersecting points with a circle

from math import radians, sin, cos
def drawIntersectingCircle(m, rr, spokes):
    # Draw intersecting circle with spokes
    # Similar to c.intersectGlyphWithCircle which is doing actual intersections
    c.fill(noColor)
    c.stroke(color(0, 0, 0.6, 0.5), 1)
    c.oval(x+m[0]-rr, y+m[1]-rr, rr*2, rr*2)
    
    mx, my = m
    lines = []
    angle = radians(360/spokes)
    p1 = None
    for n in range(spokes+1):
        p = mx + cos(angle*n)*rr, my + sin(angle*n)*rr
        if p1 is not None:
            lines.append((p1, p))
            c.line((x+mx, y+my), (x+p[0], y+p[1]))
        p1 = p
        
# Calculate the intersecting circle and draw it
spokes = 128 # Accuracy of the intersections
m = (glyph.width/2, font.info.capHeight/2) # Middle point of the intersection circle
rr = glyph.width/3 # Radius of the intersection circle
drawIntersectingCircle(m, rr, spokes)

# Calculate intersection points with the circle. And draw the point markers
r = 32
c.fill(None)
c.stroke(color(1, 0, 0.6), 4)
for p in c.intersectGlyphWithCircle(glyph, m, rr, spokes):
    c.oval(x+p[0]-r/2, y+p[1]-r/2, r, r)

c.saveImage('_export/GlyphCircleIntersection.pdf')
