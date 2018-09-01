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

context = getContext() # Get the current context (e.g. DrawBotContext instance)

# Example baseline position, showing that start can be different from page side
# or top of text box.
BASELINE = pt(14)
BASELINE_START = 1.5 * BASELINE
PADDING = 3 * BASELINE

doc = Document(w=500, h=500, baselineGrid=BASELINE, baselineGridStart=BASELINE_START,
    originTop=True)

view = doc.view
view.showBaselineGrid = True
view.showPagePadding = True # Show the padding of the page. The size is then (page.pw, page.ph)

# Export the document showing the baselines of the page as horizontal lines and the padding.  
doc.export('_export/PageBaselines.pdf')
