# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     FindVariableFontDeltas.py
#
#     Delta are stored per glyph in the Font.ttFont.
#     But you can better use the wrapper attribute font Font.
#
from pagebot import getContext
from pagebot.fonttoolbox.fontpaths import TEST_FONTS_PATH
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.fonttoolbox.variablefontbuilder import getVarFontInstance
from pagebot.fonttoolbox.varfontdesignspace import TTVarFontGlyphSet

# TODO: Needs variable font with predictable axes.

context = getContext()

SHOW_DIRECT = False

context.newPage(1500, 1500)

f = findFont('Amstelvar-Roman-VF') # Get PageBot Font instance of Variable font.
c = 'e'
g = f[c]
print(f.axes.keys())
axisDeltas = g.getAxisDeltas()['opsz']

for (minValue, defaultValue, maxValue), deltas in axisDeltas.deltas.items():
    print(minValue, defaultValue, maxValue)
    print(len(deltas), len(g.points4), len(g.points), len(g.coordinates), deltas)
    print

if 1:
    # Using PageBot Font wrapper.
    print('Axis count and names', len(f.axes), f.axes.keys())
    print('Font.rawDeltas[%s]:' % c, len(f.rawDeltas[c]) )
    for deltas in f.rawDeltas[c]:
        print(deltas.axes)
        print(deltas.coordinates)
        print()

context.translate(200, 200)
context.scale(0.75)
glyphSet = TTVarFontGlyphSet(f.ttFont)
g = glyphSet[c]
pen = CocoaPen(None)
g.draw(pen)
drawPath(pen.path)

fill(None)
strokeWidth(5)
R = 30
COLORS = ((0, 0.2, 1), (1, 0, 1))
for pIndex, point in enumerate(f[c].points4):
    if point.onCurve:
        stroke(1, 0, 0)
    else:
        stroke(0, 1, 0)
    oval(point.x-R/2, point.y-R/2, R, R)
    color = 0
    for axisValues, deltas in sorted(axisDeltas.deltas.items()):
        dx, dy = deltas[pIndex]
        rc, gc, bc = COLORS[color]
        color += 1
        stroke(rc, gc, bc)
        line((point.x, point.y), (point.x + dx, point.y + dy))

stroke(0.5)
strokeWidth(2)
line((0, 0), (0, 1500))
line((g.width, 0), (g.width, 1500))

if SHOW_DIRECT:
    # Direct on fonttools ttFont['gvar'] table.
    print('Keys in [gvar] table:', f.ttFont['gvar'].__dict__.keys())
    print('Axis count:', f.ttFont['gvar'].axisCount)
    print('Deltas of "a" points per axis:', f.ttFont['gvar'].variations['a'][0])
    print('Flags:', f.ttFont['gvar'].flags)
    print('tableTag:', f.ttFont['gvar'].tableTag)
    print('glyphCount:', f.ttFont['gvar'].glyphCount, len(f))
    print()

saveImage('_export/findVariableFontDeltas.pdf')
