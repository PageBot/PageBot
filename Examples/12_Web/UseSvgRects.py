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
#     UseSvg.py
#
import os
from random import random
from pagebot.elements import *

from pagebot.document import Document
if 0:
    from pagebot.contexts.svgcontext import SvgContext
    context = SvgContext()
    EXPORT_PATH = '_export/useSvg.svg'
else:
    from pagebot import getContext
    context = getContext()
    EXPORT_PATH = '_export/useSvg.pdf'



doc = Document(autoPages=1, context=context)

page = doc[1]

column = 100
row = 30
gutter = 8
for x in range(0, 600, column):
    for y in range(0, 800, row):
        newRect(x=x, y=y, w=column-gutter, h=row-gutter, fill=color(random(), random(), random()), parent=page)

doc.export(EXPORT_PATH)
os.system('open %s' % EXPORT_PATH)
