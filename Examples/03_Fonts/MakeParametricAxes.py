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
#     AlterGlyphCoordinates.py
#
#     This script is using getContext(), so it should be able to run it with flexContext.
#

import pagebot
from pagebot import getContext
from pagebot.fonttoolbox.objects.font import findFont
c = getContext()

EXPORT_PATH = '_export/AlteredGlyphWithPoints.pdf'
f = findFont('Amstelvar-Roman-VF')

W = H = 1000
# Scale em of 2048 back to page size.
s = 0.5
# Offset of drawing origin
c.translate(100, 100)
# Open the font and get the glyph
g = f['H']
print(g.analyzer.stems)

# These are the points we have in the H
print('List of APoints of the glyph:', g.points)
# Get the 4th APoint instance, that has reference back to the glyph.points[p.index]
p = g.points[3]
# This is the point we got.
print('glyph.points[3]:', p.x, p.y, 'Glyph:', p.glyph.name, 'Index:', p.index)
# Change the point position. In DrawBot this works interactive while holding cmd-drag in selected d.
d = -80
p.x += d
p.y += d
p.onCurve = False
# Now the glyph is dirty
print('Changed point:', p, 'Glyph is dirty:', g.dirty)
# Update the cached data, such as glyph.points, glyph.path
g.update()
print('Now it is clean. Glyph is dirty:', g.dirty)
# Draw the changed path
c.fill(None)
c.stroke(0, 1)
c.drawPath(g.path, (0, 0), s)
# Draw the position of the points
c.stroke((1, 0, 0), 2)
c.fill(None)
for p in g.points:
    if p.onCurve:
        R = 16
    else:
        R = 6
    c.oval(p.x*s-R/2, p.y*s-R/2, R, R)

c.saveImage(EXPORT_PATH)

