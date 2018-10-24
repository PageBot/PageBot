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


context = InDesignContext()
path = context.getInDesignScriptPath() + 'text.jsx'
print(path)
w = 1000
h = 800
context.newDocument(w, h)
p1 = (100, 100)
p2 = (200, 200)
context.line(pt(p1), pt(p2))
print(context.b)
context.saveDocument(path)
