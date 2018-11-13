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
#     14_BezierPaths.py
#
#     This script shows the behavior and functions of BezierPaths as they exist
#     the DrawBotContext. Most of the functions are directly defined by the
#     OSX defintion of BezierPaths.
#     (Note that BezierPaths sometimes get referred to as "path", but there is
#     not relation with the often used "path" in PageBot filepaths.)
#     In DrawBotContext the BezierPath is an integral part of the API.
#     TODO: FlatContext should copy this behavior. It's worthwhile to see if
#     it is possible to use the booleanOperator for the FlatContext version,
#     if the path description gets close to the code of BezierPath in DrawBot.
#
#     These example draw directly on the context canvas.
#     Look for the same examples working as BezierPathElement.py inside Document,
#     Page and Element layout usage.
#

from pagebot import getContext, getResourcesPath
from pagebot.elements.paths import PageBotPath
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.toolbox.color import color, noColor
from pagebot.toolbox.units import em, pt, upt
from pagebot.constants import * # Import all constants for convenience

context = getContext()

W = H = pt(1000) # Document size
P = pt(100) # Page padding on all sides. Select value and cmd-drag to change interactive.
COLS = ROWS = 4
G = pt(24)
TP = G/2
CW = (W - 2*P + G)/COLS - G
CH = (H - 2*P + G)/ROWS - G

context.newPage(W, H)
# Dummy text, used several times to create the length we need for this example
text = """Considering the fact that the application allows individuals to call a phone number and leave a voice mail, which is automatically translated into a tweet with a hashtag from the country of origin. """

#font = findFont('Roboto-Bold')
style = dict(font="Helvetica", fontSize=pt(24), textFill=1)

# Create a number of PageBotPath instances that can be drawn in a grid showing multiple functions.
# Create a new BezierPath as separate entity to talk to. This woe

x = y = P
path = PageBotPath(context=context)
path.rect(0, 0, CW, CW)
path.text('Rect', x=TP, y=TP, style=style)
#path = path.removeOverlap()
context.fill(color(1, 0, 0))
context.drawPath(path, (x, y))

x += CW+G
path = PageBotPath(context=context)
path.rect(0, 0, CW, CW)
path.text('moveBy', x=TP, y=TP, style=style)
context.fill(color(1, 0, 0))
context.drawPath(path, (x, y))
context.fill(color(0, 0.4, 1, 0.7))
path.moveBy((12, 12))
context.drawPath(path, (x, y))

x += CW+G
path1 = PageBotPath(context=context)
path1.rect(0, 0, CW, CW)
path1.text('Difference', x=TP, y=TP, style=style)
path2 = path1.copy()
path2.moveBy((50, 50))
context.fill(color(0, 0.2, 0.8, 0.7))
context.drawPath(path1.difference(path2), (x, y))

x += CW+G
path1 = PageBotPath(context=context)
path1.rect(0, 0, CW*2/3, CW*2/3)
path1.text('Union', x=TP, y=TP, style=style)
path2 = path1.copy()
path2.moveBy((CW/3, CW/3))
context.fill(color(0.6, 0, 0.6, 0.7))
context.drawPath(path1.union(path2), (x, y))


y += CW+G
path1 = PageBotPath(context=context)
path1.rect(0, 0, CW*2/3, CW*2/3)
path1.text('Xor', x=TP, y=TP, style=style)
path2 = path1.copy()
path2.moveBy((CW/3, CW/3))
context.fill(color(0.8, 0, 0.3, 1))
context.drawPath(path1.xor(path2), (x, y))

x -= CW+G
# Get the path of the image from PageBot resources
imagePath = getResourcesPath() + '/images/cookbot1.jpg'
iw, ih = context.imageSize(imagePath)
context.image(imagePath, p=(x, y), h=CH)
path = PageBotPath(context=context)
path.traceImage(imagePath)
path.scale(CW/iw)
path1.text('Trace Image', x=TP, y=TP, style=style)
context.fill(color(1, 0, 0))
context.stroke(noColor)
context.drawPath(path, (x+5, y+5))
context.fill(color(1, 0, 1))
context.drawPath(path, (x, y-10))
context.stroke(0, 0.5)
context.fill(noColor)
context.rect(x, y, CW, CW)

x -= CW+G
# Get the path of the image from PageBot resources
context.image(imagePath, p=(x, y), h=CH)
#path1.text('Scale Image', x=TP, y=TP, style=style)
context.drawPath(path, (x, y-10))
context.stroke(0, 0.5)
context.fill(noColor)
context.rect(x, y, CW, CW)

x -= CW+G
# Get the path of the image from PageBot resources
# Add yellow background
context.fill((1, 1, 0))
context.rect(x, y, CW, CW)
path.traceImage(imagePath)
path.scale(CW/iw)
context.fill(0)
context.drawPath(path, (x, y))
context.stroke(0, 0.5)
context.fill(noColor)
context.rect(x, y, CW, CW)


x = P
y += CW+G
path = PageBotPath(context=context)
path.circle(CW/2, CW/2, CW/2)
context.fill(0.8)
context.drawPath(path, (x, y))
path2 = PageBotPath(context=context)
for point in path.points:
    path2.circle(point[0], point[1], 6)
context.fill(noColor)
context.stroke(0, 1)
context.drawPath(path2, (x, y))
path2 = PageBotPath(context=context)
path2.text('Points', x=TP, y=TP, style=style)
context.stroke(noColor)
context.fill(0)
context.drawPath(path2, (x, y))

x += CW+G
path = PageBotPath(context=context)
path.circle(CW/2, CW/2, CW/3)
path.rotate(30, (CW/2, CW/3))
context.fill(color(0.4, 0.6, 0.3))
context.drawPath(path, (x, y))
path2 = PageBotPath(context=context)
for point in path.points:
    path2.circle(point[0], point[1], 6)
context.fill(noColor)
context.stroke(0, 1)
context.drawPath(path2, (x, y))
path2 = PageBotPath(context=context)
path2.text('Rotate 30°', x=TP, y=TP, style=style)
context.stroke(noColor)
context.fill(0)
context.drawPath(path2, (x, y))

x += CW+G
path = PageBotPath(context=context)
path.circle(CW/2, CW/2, CW/3)
path.skew(30, center=(CW/2, CW/3))
context.fill(color(0.4, 0.6, 0.3))
context.drawPath(path, (x, y))
path2 = PageBotPath(context=context)
for point in path.points:
    path2.circle(point[0], point[1], 6)
context.fill(noColor)
context.stroke(0, 1)
context.drawPath(path2, (x, y))
path2 = PageBotPath(context=context)
path2.text('Skew 30°', x=TP, y=TP, style=style)
context.stroke(noColor)
context.fill(0)
context.drawPath(path2, (x, y))

x += CW+G
path = PageBotPath(context=context)
path.circle(CW/2, CW/2, CW/3)
path0 = PageBotPath(context=context)
path0.circle(CW/2, CW/2, CW/5)
path = path.difference(path0)
path.skew(30, center=(CW/2, CW/3))
context.fill(color(0.4, 0.6, 0.3))
context.drawPath(path, (x, y))
path2 = PageBotPath(context=context)
for point in path.points:
    path2.circle(point[0], point[1], 6)
context.fill(noColor)
context.stroke(0, 1)
context.drawPath(path2, (x, y))
path2 = PageBotPath(context=context)
path2.text('Difference\nSkew 30°°', x=TP, y=TP+G, style=style)
context.stroke(noColor)
context.fill(0)
context.drawPath(path2, (x, y))

y += CW+G
path = PageBotPath(context=context)
path.rect(0, 0, CW-G, CW-G)
path.rect(G, G, CW-G, CW-G)
path2 = PageBotPath(context=context)
for point in path.intersectionPoints():
    path2.circle(point[0], point[1], 6)
context.fill(noColor)
context.stroke(0, 0.5)
context.drawPath(path, (x, y))
context.drawPath(path2, (x, y))
path = PageBotPath(context=context)
path.text('Intersections', x=TP, y=TP+G, style=style)
context.fill(0)
context.stroke(noColor)
context.drawPath(path, (x, y))

x -= CW+G
# Get the path of the image from PageBot resources
# Add yellow background
path = PageBotPath(context=context)
path.circle(CW/2, CW/2, CW/2)
context.fill(noColor)
context.stroke(0, 0.5)
context.drawPath(path, (x, y))
path2 = PageBotPath(context=context)
for xx in range(int(upt(CW/2 - CW/5)), int(upt(CW/2 + CW/5)), int(upt(CW/10))):
    for yy in range(int(upt(CH/2 - CH/5)), int(upt(CH/2 + CH/5)), int(upt(CH/10))):
        if path.pointInside((xx, yy)):
            path2.circle(x+xx-CW/2, y+yy-CW/2, 8)
context.stroke(noColor)
context.fill(color(1, 0, 0))
context.drawPath(path2, (xx, yy))
path = PageBotPath(context=context)
path.text('Point Inside', x=TP, y=TP+G, style=style)
context.fill(0)
context.stroke(noColor)
context.drawPath(path, (x, y))

x -= CW+G
path = PageBotPath(context=context)
path.rect(0, 0, CW-G, CW-G)
path.rect(G, G, CW-G, CW-G)
path.rect(G/2, G, CW-G, CW-G)
path.rect(G, G/2, CW-G, CW-G)
path = path.removeOverlap()
context.fill(noColor)
context.stroke(0, 0.5)
context.drawPath(path, (x, y))
path = PageBotPath(context=context)
path.text('Remove\nOverlap', x=TP, y=TP+G, style=style)
context.fill(0)
context.stroke(noColor)
context.drawPath(path, (x, y))

x -= CW+G
path = PageBotPath(context=context)
path.text('B', style=dict(font='Helvetica', fontSize=250))
path = path.removeOverlap()
context.fill(noColor)
context.stroke(color(1, 0, 0), 0.5)
context.drawPath(path, (x, y))
path = PageBotPath(context=context)
path.text('Text', x=TP, y=TP+G, style=style)
context.fill(0)
context.stroke(noColor)
context.drawPath(path, (x, y))

# Export the document to this PDF file.
context.saveImage('_export/BezierPaths.pdf')

