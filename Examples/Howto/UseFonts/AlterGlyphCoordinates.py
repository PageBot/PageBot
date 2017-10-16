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
#     AlterGlyphCoordinates.py

import pagebot
from pagebot.contexts import defaultContext as c
from pagebot.fonttoolbox.objects.font import Font

EXPORT_PATH = '_export/TYPETR-Upgrade.pdf'
FONT_PATH = pagebot.getFontPath() + "/fontbureau/AmstelvarAlpha-VF.ttf"

W = H = 1000
# Scale em of 2048 back to page size.
s = 0.5
# Offset of drawing origin
c.translate(100, 100)

# Open the font and get the glyph
f = Font(FONT_PATH)
g = f['H']
# These are the points we have in the H
print g.points
# Get the 4th APoint instance, that has reference back to the glyph.points[p.index]
p = g.points[3]
# This is the point we got.
print 'glyph.points[3]:', p.x, p.y, 'Glyph:', p.glyph.name, 'Index:', p.index
# Change the point position. In DrawBot this works interactive while holding cmd-drag.
d = 30
p.x += d
p.y += d
p.onCurve = False
# Now the glyph is dirty
print 'Changed point:', p, 'Glyph is dirty:', g.dirty
# Update the cached data, such as glyph.points, glyph.path
g.update()
print 'Now it is clean:', g.dirty
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
    
    