# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     UseSvg.py
#
import os
from random import random
from pagebot.elements import *

from pagebot.document import Document
from pagebot.contexts.svgcontext import SvgContext

context = SvgContext()

EXPORT_PATH = '_export/useSvg.svg'

doc = Document(autoPages=1, context=context)

page = doc[1]

column = 100
row = 30
gutter = 8
for x in range(0, 600, column):
    for y in range(0, 800, row):
        newRect(x=x, y=y, w=column-gutter, h=row-gutter, fill=(random(), random(), random()), parent=page)

doc.export(EXPORT_PATH)
os.system('open %s' % EXPORT_PATH)
