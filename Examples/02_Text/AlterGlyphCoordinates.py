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
#     This script is using getContext(), so it should be able to run it with flatContext.
#

import pagebot
from pagebot import getContext
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.toolbox.units import pt
from pprint import pprint

context = getContext()
EXPORT_PATH = '_export/AlteredGlyphWithPoints.pdf'
f = findFont('Amstelvar-Roman-VF') # Get PageBot Font instance of Variable font.

W = H = 1000

# Scale em of 2048 back to page size.
s = 0.5

# Offset of drawing origin.
context.translate(pt(100), pt(100))

# Open the font and get the glyph.
g = f['H']

# These are the points we have in the H:
print('List of APoints of the glyph:')
pprint(g.points)

# Get the 4th APoint instance, that has reference back
# to the glyph.points[p.index]
p = g.points[3]

# This is the point we got.
print('Got glyph.points[3]:', p.x, p.y)
print('Glyph name is %s, Index is %d' % (p.glyph.name, p.index))

# Change the point position. In DrawBot this can be done interactively
# by holding CMD-drag in selected d.
d = -80
p.x += d
p.y += d
p.onCurve = False

# Now the glyph is dirty.
print('Changed point:', p, 'Glyph is dirty:', g.dirty)

# Update the cached data, such as glyph.points and glyph.path.
g.update()
print('Now it is clean. Glyph is dirty:', g.dirty)

# Draw the changed path.
context.fill(None)
context.stroke(0, 1)
context.drawPath(context.getGlyphPath(g), (0, 0), s)

# Draw the position of the points.
context.stroke((1, 0, 0), 2)
context.fill(None)

for p in g.points:
    if p.onCurve:
        R = 16
    else:
        R = 6
    context.oval(p.x*s-R/2, p.y*s-R/2, R, R)

context.saveImage(EXPORT_PATH)
