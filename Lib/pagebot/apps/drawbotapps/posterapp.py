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
#     posterapp.py
#
from pagebot.apps.drawbotapps.baseapp import BaseApp
from pagebot.publications.poster import Poster

class PosterApp(BaseApp):
    u"""Will be developed."""
    PUBLICATION_CLASS = Poster
