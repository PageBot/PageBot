#!/usr/bin/env python
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
#     SimpleDocument.py
#
#     This is a simple page document to show the working of layouts
#     using conditions.
#
from pagebot.constants import A4
from pagebot.document import Document
from pagebot.elements import newRect, newTextBox
from pagebot.conditions import *
from pagebot.toolbox.color import color
from pagebot.toolbox.units import pt, p

if 1:
    from pagebot import getContext
    context = getContext() # DrawBotContext or FlatContext if available.
else:
    from pagebot.contexts.svgcontext import SvgContext
    context = SvgContext()

SIZE = 498, 770#A4 # Standard page size
# To see how the "responsive" layout works in landscape, swap W and H
#H, W = A4

PAD = pt(50) # Page padding
# Create a Document instance of the defined size and one automatic page.
doc = Document(size=SIZE, title="Demo pages", originTop=False, context=context)
# Get the view of the document. By default this is a PageView, writing
# on a DrawBotContext or FlatContext, whatever is avaialbe as default.
view = doc.view
view.padding = pt(40) # Space around the page to accommodate registratio and crop marks.
view.showCropMarks = True # Set the view flags what to show.
view.showRegistrationMarks = True
view.showPadding = True
view.showFrame = True
view.showNameInfo = True
view.showPageMetaInfo = True

# Get the page of the document. Since right pages are uneven, the list of pages
# startes at #1.
page = doc[1]
# Set the padding of the page, as we don't use a template here.
# In multipage documents this also can be done in the document, so pages inherit.
page.padding = PAD, PAD, 2*PAD, PAD
# Create rectangles. Default position and size is (0, 0, 100, 100). The conditions define the layout.
newRect(fill=color(1, 0, 0), parent=page, h=pt(62),
    conditions=(Left2Left(), Float2Top(),Fit2Right()))
newRect(fill=color(1, 0, 1), parent=page,
    conditions=(Left2LeftSide(), Float2Top()))
newRect(fill=color(spot=300), parent=page,
    conditions=(Right2Right(), Float2Top(), Float2Left(), Fit2Right()))

# Add a floating text box.
newTextBox('BB', parent=page, x=100, y=150, w=300, h=400, fill=color(spot=400),
    fontSize=p(8), font='Verdana', textFill=color(spot=120))

# Solve the conditions of the layout in defined order.
doc.solve()
# Export to PDF.
doc.export('_export/SimpleDocument.pdf')
