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
#     100_PageColorBars.py
#
#     Show the baseline grid of the page (drawn by the PageView)
#     and the relation with the usable page padding area.
#
from pagebot.document import Document # Get the main Document class
from pagebot.toolbox.units import pt, inch
from pagebot import getContext
from pagebot.constants import (BASE_LINE_BG, BASE_Y_LEFT, BASE_INDEX_LEFT, B5, 
    ECI_GrayConL, COLORBAR_LEFT, COLORBAR_RIGHT)
from pagebot.elements import *

context = getContext() # Get the current context (e.g. DrawBotContext instance)

# Example baseline position, showing that start can be different from page side
# or top of text box.
BASELINE = pt(15)
BASELINE_START = 3.5 * BASELINE
PADDING = 5 * BASELINE # Page padding related to baseline in this example.

doc = Document(size=B5, padding=PADDING, originTop=True, 
    autoPages=3, # Create multiple pages, to show the page number/total pages.
    baselineGrid=BASELINE, baselineGridStart=BASELINE_START)

view = doc.view # Get the current view of this document. Defaulse it PageView.
view.padding = inch(0.5) # Define padding of the view, so there is space for crop marks
view.showBaselineGrid = [BASE_LINE_BG, BASE_INDEX_LEFT] # Set to True to show baseline index
#view.showBaselineGrid = [BASE_LINE_BG, BASE_Y_LEFT] # Use this line to show vertical positions
view.showPadding = True # Show the padding of the page. The size is then (page.pw, page.ph)
view.showCropMarks = True
view.showRegistrationMarks = True
view.showColorBars = (ECI_GrayConL, COLORBAR_LEFT) #, COLORBAR_RIGHT) <-- Not right position
view.showNameInfo = True # Show document/name/date info in view padding area.
view.showFrame = True # Show frame of the page size.

# The page has no child elements, just showing the metrics of the padding and baseline.

# Export the document showing the baselines of the page as horizontal lines and the padding.  
doc.export('_export/PageColorBars.pdf')
