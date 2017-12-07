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
#     placer.py
#
from pagebot.elements.element import Element

class Placer(Element):

    DEFAULT_FILL = (0.8, 0.8, 0.8)

    def __init__(self, fill=None, **kwargs):  
        if fill is None:
            fill = self.DEFAULT_FILL
        Element.__init__(self, fill=fill, **kwargs)