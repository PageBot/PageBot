# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     kirbyview.py
#
from pagebot.elements.views.view import View

class KirbyView(View):
    viewId = 'Kirby'

    def drawPages(self, pageSelection):
    	print pageSelection

    def export(self, fileName, pageSelection, multiPage):
    	u"""Use an HTML/CSS builder to export the pages as website code."""
    	print fileName, pageSelection, multiplePage
