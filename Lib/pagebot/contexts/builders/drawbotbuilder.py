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
#     drawbotbuilder.py
#
try:
    import drawBot
    drawBotBuilder = drawBot
    # Id to make builder hook name. Views will be calling e.build_html()
    drawBotBuilder.PB_ID = 'drawBot' 

    import CoreText
    import AppKit
    import Quartz

except ImportError:
    drawBotBuilder = None

from pagebot.style import NO_COLOR, LEFT, css

