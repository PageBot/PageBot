# -*- coding: UTF-8 -*-
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
#     08-HeadlineAlignment.py
#
from pagebot.contexts.drawbotcontext import DrawBotContext
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.toolbox.units import em, p, pt
from pagebot.constants import *
from pagebot.elements import *
from pagebot.conditions import *
from pagebot.document import Document
from pagebot.toolbox.color import color

context = DrawBotContext()

W, H = pt(800, 500) # Document size
PADDING = pt(120, 20) # Page padding on all sides

NUM_PAGES = 1

# Get the font object, from te Roboto file that is included in PageBot resources for testing.
f = findFont('PageBot-Regular')

# Create a new document with 1 page. Set overall size and padding.
# TODO: View grid drawing, etc. does not work properly for originTop=True
doc = Document(w=W, h=H, padding=PADDING, context=context, 
    autoPages=NUM_PAGES, originTop=False)
view = doc.view
view.showPadding = True

page = doc[1]
page.padding = PADDING

t = 'Hkpx'

for c, conditions in (
	('green', [ 
	    Shrink2TextHeight(), Shrink2TextWidth(), 
	    Left2Left(), CapHeight2Top()]),
	('red', [ 
	    Shrink2TextHeight(), Shrink2TextWidth(), 
	    Center2Center(), Baseline2Top()]),
	('blue', [ 
	    Shrink2TextHeight(), Shrink2TextWidth(), 
	    Right2Right(), XHeight2Top()]),
	#('green', [ 
	#    Shrink2TextHeight(), Shrink2TextWidth(), 
	#    Left2Left(), CapHeight2Bottom()]),
	('red', [ 
	    Shrink2TextHeight(), Shrink2TextWidth(), 
	    Center2Center(), Baseline2Bottom()]),
	#('blue', [ 
	#    Shrink2TextHeight(), Shrink2TextWidth(), 
	#    Right2Right(), XHeight2Bottom()]),

):
	style = dict(font=f, fontSize=100, textFill=color(name=c))
	bs = context.newString(t, style=style)
	newTextBox(bs, parent=page, fill=(0.5, 0.5, 0.5, 0.5), conditions=conditions)

page.solve()

doc.export('_export/WordAlignment.pdf')