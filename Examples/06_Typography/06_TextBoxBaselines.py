#!/usr/bin/env python3
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
#     06a_TextBoxBaselines.py
#
#     Show the baseline grid of the page (drawn by the PageView)
#     and the relation with the baseline of a positioned text box.
#     Intentionally give the baseline grid and text grid a different leading.
#     Position the fifth text line from top on the page baseline grid.

from pagebot.document import Document
from pagebot.conditions import *
from pagebot.elements import newTextBox, newLine
from pagebot.toolbox.units import pt, em
from pagebot.toolbox.color import color
from pagebot import getContext
from pagebot.constants import BASE_LINE_BG, BASE_INDEX_LEFT, BASE_INDEX_RIGHT, BASE_Y_RIGHT

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
view.showBaselineGrid = [BASE_LINE_BG, BASE_INDEX_LEFT] # Draw baselines at background.
view.showPadding = True # Show the padding of the page. The size is then (page.pw, page.ph)
view.showOrigin = False # No origin showing

page = doc[1] # Get the first (and only) page of the document

# Define the style dictionary fir the main text.
style = dict(name='body', font='Verdana', fontSize=pt(12), leading=em(1.4))
conditions = [Fit()] # Fitting conditions for the text box on (page.pw, page.ph)

# Create a new text box and set the view-parameres, so they angue for today.
tb = newTextBox(text * 5, parent=page, stroke=0.5, strokeWidth=0.5,
    style=style, conditions=conditions, 
    baselineColor=color(1, 0, 0), # Show baselines and indices in red.
    showBaselineGrid=[BASE_LINE_BG, BASE_INDEX_RIGHT]) # Define type of baseline view.
   
# Make the text box fit to the page padding, solving position and size.
doc.solve()

# Adjust vertical position of the fitting textbox, so that textLines[4] 
# locks on page baseline. 
lineIndex = 4
print(tb.x, tb.y, tb.baselineOffset(lineIndex))
tb.y += tb.baselineOffset(lineIndex)
#print(tb.y)
# Add lines to indicate to position where the text box and grid match up.
#print(-tb.textLines[0].y)
#print(tb.textLines[lineIndex].y)
newLine(x=0, y=tb.y,
    #tb.textLines[lineIndex].y, 
    w=page.w, h=0, parent=page, 
    stroke=color(0, 0, 1), strokeWidth=pt(0.5))

# Export to the given file name. The "_export" folder content does snot commit to git.
doc.export('_export/TextBoxBaselines.pdf')
