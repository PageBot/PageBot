# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#     
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     UseGlyphAnalyzer.py
#
#     Implements a PageBot font classes to get info from a TTFont.
#     Show the values that the GlyphAnalyzer get derive from font and glyph outline.
#   
from pagebot.fonttoolbox.objects.font import Font
from pagebot.contexts import defaultContext as c

BeamY = 770

newPage(1000, 1000)
font = Font('/Library/Fonts/Georgia.ttf')
print font.analyzer 
print font.analyzer.name 
glyphH = font['H']
gaH = glyphH.analyzer
print gaH
print 'H width:', gaH.width, gaH.glyph.width, glyphH.width
print 'H bounding box:', gaH.boundingBox
# X position of vertical lines also includes sides of serifs.
print 'x-position of verticals:', sorted(gaH.verticals.keys())
# Y position of horizontal lines
print 'y-position of horizontals:', sorted(gaH.horizontals.keys())

c.stroke(0)
c.fill(None)
print gaH.glyph.leftMargin
x = y = 100
s = 0.25
c.drawPath(glyphH.path, (x, y), s)
# Draw markers on the glyph points
c.fill((1, 0, 0))
c.stroke(None)
for p in glyphH.points:
    r = {True:5, False:3}[p.onCurve]
    c.rect(x+p.x*s-r/2, x+p.y*s-r/2, r, r)
    
#c.rect(x, y, 100, 100)
# Draw flattened path next to it on H-width distance.
c.fill(None)
c.stroke(0)
x += glyphH.width*s # Get scaled glyph width
flattenedPath = glyphH.flattenedPath
c.drawPath(flattenedPath, (x, y), s)
# Draw the flattened contours/points
r = 3
c.fill((0, 0.5, 0))
c.stroke(None)
for contour in glyphH.flattenedContours:
    for p in contour:
        c.rect(x+p[0]*s-r/2, y+p[1]*s-r/2, r, r)
# Draw intersecting points from beam lines
r = 5
c.fill((0, 0, 0.5))
c.stroke(None)

beam = ((0, BeamY), (2000, BeamY))
for p in gaH.intersectWithLine(beam):
    c.rect(x+p[0]*s-r/2, y+p[1]*s-r/2, r, r)

Variable([
	dict(name="BeamY", ui='Slider', args=dict(minValue=-300, value=300, maxValue=1000)),
], globals())
    
    