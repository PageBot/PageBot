# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#     
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     __init__.py
#
# DrawBot views
from pagebot.elements.views.drawbotview import DrawBotView
# Flat views
from pagebot.elements.views.flatview import FlatView
# Website views
from pagebot.elements.views.mampview import MampView # Saves in local Applications/MAMP/htdocs directory
from pagebot.elements.views.gitview import GitView # Saves in local position, so git works as website server.
