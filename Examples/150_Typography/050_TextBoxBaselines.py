#!/usr/bin/env python
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
#     060_TextBoxBaselines.py
#
#     Show the baseline grid of the page (drawn by the PageView)
#     and the relation with the baseline of a positioned text box.
#
from pagebot.document import Document
from pagebot.conditions import *
from pagebot.elements import newTextBox
from pagebot.toolbox.units import pt, em
from pagebot.toolbox.color import color
from pagebot.contexts.platform import getContext
from pagebot.constants import BASE_LINE_BG, BASE_INDEX_LEFT, BASE_INDEX_RIGHT

context = getContext()

W, H = pt(500, 500)

text = """Considering the fact that the application allows individuals to call a phone number and leave a voice mail, which is automatically translated into a tweet with a hashtag from the country of origin. """

# Example baseline position, showing that start can be different from page side
# or top of text box.
BASELINE = pt(15)
BASELINE_START = 1.5 * BASELINE
PADDING = 3 * BASELINE # Page padding related to baseline in this example.

doc = Document(w=W, h=H, padding=PADDING, originTop=True,
    baselineGrid=BASELINE, baselineGridStart=BASELINE_START)

view = doc.view # Get the current view of this document. Defaulse it PageView.
view.showBaselines = [BASE_LINE_BG, BASE_INDEX_LEFT] 
view.showPadding = True # Show the padding of the page. The size is then (page.pw, page.ph)

page = doc[1] # Get the first (and only) page of the document

style = dict(font='Verdana', fontSize=pt(12), leading=em(1.4))
conditions = [Fit()] # Fitting conditions for the text box on (page.pw, page.ph)

# Create a new text box and set the view-parameres, so they angue for today.
tb = newTextBox(text * 5, parent=page, stroke=0.5, strokeWidth=0.5,
    style=style, conditions=conditions, 
    baselineColor=color(1, 0, 0), # Show baselines and indices in red.
    showBaselines=[BASE_LINE_BG, BASE_INDEX_RIGHT]) # Define type of baseline view.
   
# Make the text box fit to the page padding.
doc.solve()

# Adjust vertical position of the textbox, so that textLines[4] locks on page baseline. 
tb.y += tb.baselineOffset(4)

# Export to the given file name. The "_export" folder content does snot commit to git.
doc.export('_export/TextBoxBaselines.pdf')
