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
#     01_Basics/02_Elements.py
#

from pagebot import getContext
from pagebot.toolbox.units import *
from pagebot.toolbox.color import Color, blackColor, blueColor, greenColor
from pagebot.elements import *
from pagebot.document import Document
from pagebot.toolbox.color import blueColor, darkGrayColor, redColor, Color, noColor, color
from pagebot.conditions import *
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.elements.paths.pagebotpath import PageBotPath
from pagebot.constants import A3

context = getContext()

# Landscape A3.
H, W = A3
X0 = 100
Y0 = 100
SQ = 150
P  = 50
bungee = findFont('BungeeInline-Regular')


doc = Document(w=W, h=H, originTop=False, autoPages=1, context=context)
page = doc[1]
page.padding = P

c = (Right2Right(), Top2Top(), Float2Left())
r = newRect(w=SQ, h=SQ, parent=page, conditions=(Left2Left(), Top2Top()), fill=(0,0,1), stroke=0)

o = newOval(w=SQ, h=SQ, parent=page, conditions=c, fill=(1, 0, 0), stroke=0)

l = newLine(parent=page, x=0, y=0, w=100, h=100, conditions=c, stroke=0, strokeWidth=10)
points=[(0,0), (100, 0), (150, 50), (150, 100), (100, 200)]
q = newQuire(parent=page, conditions=c, fill=1, strokeWidth=5, stroke=0.5)
r = newRuler(w=SQ, h=SQ, parent=page, conditions=c, fill=noColor, stroke=0, strokeWidth=1)


newText('Text    ', parent=page, conditions=c, fontSize=60, stroke=(1, 1, 0), strokeWidth=20, textFill=0.5, font=bungee)
newTextBox('Text Box', parent=page, conditions=c, stroke=0, strokeWidth=0.5, fill=(1, 1, 0), fontSize=30, font=bungee, textFill=(0, 0, 1))
page.solve()

# TODO: add a path.
#pths = newPaths(path) 

# Points should be merged with PageBotPath.
#points = []
#p = newPolygon(points=points, parent=page, conditions=c, fill=1, stroke=0)
#p = newPolygon(points=points, w=100)


# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/showElements.png'
doc.export(EXPORT_PATH)
pbp = PageBotPath(context)


