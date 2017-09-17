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
#     __init__.py
#
from pagebot.elements.views.view import View
from pagebot.elements.views.defaultview import DefaultView
from pagebot.elements.views.singleview import SingleView
from pagebot.elements.views.thumbview import ThumbView
from pagebot.elements.views.spreadview import SpreadView
# Website views
from pagebot.elements.views.htmlview import HtmlView # Abstract HTML/CSS generator view
from pagebot.elements.views.mampview import MampView # Saves in local Applications/MAMP/htdocs directory
from pagebot.elements.views.gitview import GitView # Saves in local position, so git works as website server.
