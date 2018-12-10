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

GLYPH_NAME = 'P' # 'ampersand'

c = getContext()

c.newPage(1000, 1000)
c.scale(0.5)

font = findFont('Roboto-Regular')
#print(font.analyzer )
#print(font.analyzer.name )
glyph = font[GLYPH_NAME]
ga = glyph.analyzer
# Three ways to access the glyph metrics
print('Glyph width:', ga.width, ga.glyph.width, glyph.width)
print('Glyph bounding box:', ga.boundingBox)
# X position of vertical lines also includes sides of serifs.
verticals = sorted(ga.verticals.keys())
print('x-position of detected verticals:', verticals)
# Y position of horizontal lines
horizontals = sorted(ga.horizontals.keys())
print('y-position of deteted horizontals:', horizontals)


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

# Draw flattened path next to it on glyph.width distance.
c.fill(noColor)
c.stroke(blackColor)

# Draw the outline of the glyph
glyphPath = c.getGlyphPath(glyph)
#c.drawPath(glyphPath, (x+12, y-12))
# Draw the flattened outline of the glyph
flattenedPath = c.bezierPathByFlatteningPath(glyphPath)
c.drawPath(flattenedPath, (x, y))
# Draw the flattened contours/points
r = 6
c.fill(color(0, 0.5, 0))
c.stroke(noColor, 2)
for contour in c.getFlattenedContours(glyphPath):
    for p in contour:
        c.oval(x+p[0]-r/2, y+p[1]-r/2, r, r)
# Draw intersecting points from beam lines
r = 16
c.fill(noColor)
c.stroke(color(0, 0, 0.6), 2)

from math import radians, sin, cos
def intersectGlyphWithCircle(m, r, numPoints):
    mx, my = m
    lines = []
    angle = radians(360/numPoints)
    p1 = None
    for n in range(numPoints+1):
        p = mx + cos(angle*n)*r, my + sin(angle*n)*r
        if p1 is not None:
            lines.append((p1, p))
            c.line((x+mx, y+my), (x+p[0], y+p[1]))
        p1 = p
# Calculate an intersection beam. Draw the line and intersection points.
BeamY = 446 # Vertical position of the beam
c.line((x, y+BeamY), (x+glyph.width, y+BeamY))
beam = ((0, BeamY), (glyph.width, BeamY))
r = 24 # Radius of the beam markers
c.stroke(color(0, 0, 0.5), 2)
c.fill(noColor)

spokes = 128
m = (glyph.width/2, font.info.capHeight/2)
rr = glyph.width/2
intersectGlyphWithCircle(m, rr, spokes)
oval(x+m[0]-rr, y+m[1]-rr, rr*2, rr*2)
for p in c.intersectGlyphWithCircle(glyph, m, rr, spokes):
    c.rect(x+p[0]-r/2, y+p[1]-r/2, r, r)

c.saveImage('_export/GlyphBeamIntersection.pdf')
