#!/usr/bin/env python3
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     InDesign.py
#
# Test InDesign Scripting.
#

from pagebot.contexts.indesigncontext import InDesignContext
from pagebot.toolbox.units import pt
from pagebot.toolbox.color import Color
from pagebot.constants import A4Rounded

context = InDesignContext()
path = context.getInDesignScriptPath() + 'test.jsx'
#print(path)
H, W = A4Rounded

# CMYK by default?
f = Color(c=0, m=0, y=1, k=0)
s = Color(c=0, m=1, y=0, k=0)

# FIXME: synchronize newDocument() and newDrawing() across contexts.
context.newDocument(W, H)
#context.newPage(w=W, h=H)
print(context.fill)
context.fill(f)
context.stroke(s)
context.text('bla', (pt(100), pt(100)))
#p1 = (100, 100)
#p2 = (200, 200)
#context.line(pt(p1), pt(p2))
context.oval(pt(100), pt(100), pt(200), pt(200))
context.rect(pt(100), pt(200), pt(110), pt(120))
print(context.b)
context.saveDocument(path)
