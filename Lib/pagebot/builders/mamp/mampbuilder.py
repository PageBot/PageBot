# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     mampbuilder.py
#
import os
from basehtmlcssbuilder import BaseHtmlCssBuilder

class MampBuilder(BaseHtmlCssBuilder):

    def build(self, doc, path):
    	assert os.path.exists(path)
    	print 'Build site from document.'
