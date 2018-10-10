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
from pagebot.elements import *

from pagebot.document import Document
from pagebot.contexts.svgcontext import SvgContext
from pagebot.toolbox.color import color 

context = SvgContext()
EXPORT_PATH = '_export/useSvg.svg'
doc = Document(autoPages=1, context=context)
page = doc[1]
newRect(x=100, y=200, w=300, h=400, fill=color(1, 0, 0), parent=page)
bs = context.newString('ABCDEF', style=dict(fontSize=100))
print(bs.__class__.__name__)
tb = newText(bs, x=100, y=400, fill=color(1, 0, 1), parent=page, )

doc.export(EXPORT_PATH)
os.system('open %s' % EXPORT_PATH)
