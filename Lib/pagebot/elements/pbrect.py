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
#     rect.py
#
from __future__ import division # Make integer division result in float.
from drawBot import rect

from pagebot import setStrokeColor, setFillColor
from pagebot.style import NO_COLOR
from pagebot.elements.element import Element
from pagebot.toolbox.transformer import pointOffset

class Rect(Element):
    pass

    # No separate draw, default behavior is in Element.draw()

