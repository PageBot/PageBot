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
#     050_PageBaselines.py
#
#     Show the baseline grid of the page (drawn by the PageView)
#     and the relation with the usable page padding area.
#
from pagebot.document import Document # Get the main Document class
from pagebot.toolbox.units import pt
from pagebot.contexts.platform import getContext
from pagebot.constants import GRID_LINE, GRID_Y

context = getContext() # Get the current context (e.g. DrawBotContext instance)

W, H = pt(500, 500)

# Example baseline position, showing that start can be different from page side
# or top of text box.
BASELINE = pt(15)
BASELINE_START = 1.5 * BASELINE
PADDING = 3 * BASELINE # Page padding related to baseline in this example.

doc = Document(w=W, h=H, padding=PADDING, originTop=True,
    baselineGrid=BASELINE, baselineGridStart=BASELINE_START)

view = doc.view # Get the current view of this document. Defaulse it PageView.
view.showBaselineGrid = True # Set to True defaults to [GRID_LINE, GRID_INDEX]
#view.showBaselineGrid = [GRID_LINE, GRID_Y] # Use this line to show vertical positions
view.showPagePadding = True # Show the padding of the page. The size is then (page.pw, page.ph)

# Export the document showing the baselines of the page as horizontal lines and the padding.  
doc.export('_export/PageBaselines.pdf')
