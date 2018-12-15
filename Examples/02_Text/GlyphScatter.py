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
#     UseGlyphBeamIntersection.py
#
#     Implements a PageBot font classes to get info from a TTFont.
#     Show drawing of outline points and intersection beam with flattened path
#
from random import random

from pagebot.fonttoolbox.objects.font import findFont
from pagebot import getContext
from pagebot.toolbox.color import color, noColor, blackColor


c = getContext()

c.newPage(2000, 550)
c.scale(0.5)

font = findFont('PageBot-Bold')
print(font.analyzer )
print(font.analyzer.name )

def drawGlyph(px, py, glyph):
    ga = glyph.analyzer
    # Three ways to access the glyph metrics
    #print('Glyph width:', ga.width, ga.glyph.width, glyph.width)
    #print('Glyph bounding box:', ga.boundingBox)
    # X position of vertical lines also includes sides of serifs.
    #verticals = sorted(ga.verticals.keys())
    #print('x-position of detected verticals:', verticals)
    # Y position of horizontal lines
    #horizontals = sorted(ga.horizontals.keys())
    #print('y-position of deteted horizontals:', horizontals)
    
    c.stroke(blackColor, 1)
    c.fill(None)
    #print('Left margin:', glyph.leftMargin)

    # Draw markers on the glyph points
    c.fill((1, 0, 0))
    c.stroke(None)
    for p in glyph.points:
    	# TODO: Add drawing of off-on-off lines here
    	if p.onCurve:
    		r = 12
    	else:
    		r = 10
    	c.oval(px+p.x-r/2, py+p.y-r/2, r, r)

    c.fill(noColor)
    # Draw the outline of the glyph
    c.stroke(color(0.4, 0.4,0.4, 0.6), 10)
    glyphPath = c.getGlyphPath(glyph)
    c.drawPath(glyphPath, (x+12, y-12))
    # Draw flattened path next to it on glyph.width distance.
    c.stroke(color(0.7, 0.7,0.7, 0.6), 6)
    flattenedPath = c.getFlattenedContours(glyphPath)
    c.drawPath(flattenedPath, (x, y))

    tt = 30
    c.fill(blackColor)
    c.stroke(noColor)
    for xx in range(0, glyph.width, tt):
        for yy in range(font.info.descender, font.info.ascender, tt):
            if c.onBlack((xx, yy), c.getGlyphPath(glyph)):
                r = 8
                r2 = r/2
                c.fill(color(random()*0.5, 0.5, random()*0.5))
                c.oval(px+xx-r2, py+yy-r2, r, r)

                r = 40
                r2 = r/2
                c.stroke(0, 2)
                c.fill(noColor)
                c.oval(px+xx+random()*r-r2, py+yy+random()*r-r2, r, r)

    # Draw the flattened contours/points
    for contour in c.getFlattenedContours(glyphPath):
        for p in contour:
            r = 10 + random()*50
            c.fill(color(random(), 0.5, random(), 0.5))
            c.stroke(noColor, 2)
            c.oval(x+p[0]-r/2 + random()*20-10, y+p[1]-r/2 + random()*20-10, r, r)

            r = 40
            c.stroke(color(random(), 0.5, random(), 0.5))
            c.fill(noColor)
            c.oval(x+p[0]-r/2 + random()*20-10, y+p[1]-r/2 + random()*20-10, r, r)

x, y = 120, 300
for cName in 'PageBot':
    g = font[cName]
    drawGlyph(x, y, g)
    x += g.width
c.saveImage('_export/GlyphScatter.pdf')
c.saveImage('_export/GlyphScatter.png')
