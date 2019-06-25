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
from pagebot.elements.web.simplesite.siteelements import *

def newHeader(**kwargs):
    return Header(**kwargs)
    
def newBanner(**kwargs):
    return Banner(**kwargs)
