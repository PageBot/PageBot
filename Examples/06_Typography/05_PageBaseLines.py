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
#     050_PageBaselines.py
#
#     Show the baseline grid of the page (drawn by the PageView)
#     and the relation with the usable page padding area.
#

from pagebot.document import Document # Get the main Document class
from pagebot.toolbox.units import pt
from pagebot import getContext
from pagebot.constants import BASE_LINE_BG, BASE_Y_LEFT, BASE_INDEX_LEFT, B5
from pagebot.elements import *

context = getContext() # Get the current context (e.g. DrawBotContext instance)

# Example baseline position, showing that start can be different from page side
# or top of text box.
BASELINE = pt(15)
BASELINE_START = 3.5 * BASELINE
PADDING = 5 * BASELINE # Page padding related to baseline in this example.

# TODO: View grid drawing does not work with originTop=True
doc = Document(size=B5, padding=PADDING, originTop=False,
    baselineGrid=BASELINE, baselineGridStart=BASELINE_START)

view = doc.view # Get the current view of this document. Default is PageView.
view.showBaselineGrid = [BASE_LINE_BG, BASE_INDEX_LEFT] # Set to True to show baseline index
#view.showBaselineGrid = [BASE_LINE_BG, BASE_Y_LEFT] # Use this line to show vertical positions
view.showPadding = True # Show the padding of the page. The size is then (page.pw, page.ph)
# The page has no child elements, just showing the metrics of the padding and baseline.

# Export the document showing the baselines of the page as horizontal lines and the padding.  
doc.export('_export/PageBaselines.pdf')
