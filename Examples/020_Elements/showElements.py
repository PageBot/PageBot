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
#     showElements.py
#

from pagebot.contexts.platform import getContext
from pagebot.toolbox.units import *
from pagebot.toolbox.color import Color, blackColor, blueColor, greenColor
from pagebot.elements import *
from pagebot.document import Document
from pagebot.toolbox.color import blueColor, darkGrayColor, redColor, Color, noColor, color
from pagebot.conditions import *

context = getContext()

# Landscape A3.
W = 1189
H = 842
X0 = 100
Y0 = 100
SQ = 150
P  = 50

doc = Document(w=W, h=H, originTop=False, autoPages=1, context=context)
page = doc[1]
page.padding = P
r = newRect(w=SQ, h=SQ, parent=page, conditions=(Left2Left(), Top2Top()), fill=0)
print(type(r))
o = newOval(w=SQ, h=SQ, parent=page, conditions=(Right2Right(), Top2Top()), fill=(1, 0, 0))
print(type(o))

page.solve()
# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/showElements.png'
doc.export(EXPORT_PATH)

