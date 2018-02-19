#!/usr/bin/env python
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
from nonedrawbotbuilder import NoneDrawBotBuilder

try:
    import drawBot # Test is drawBot is available on this platform
    drawBotBuilder = drawBot
    # Id to make builder hook name. Views will be calling e.build_html()
    drawBotBuilder.PB_ID = 'drawBot' 
    # Test by import if MacOS specific imports are available.
    #import CoreText, AppKit, Quartz # #pylint: disable=unused-import

except (ImportError, AttributeError):
    drawBotBuilder = None
    print('Not using DrawBotBuilder')

except:
    drawBotBuilder = NoneDrawBotBuilder()
    print('Using NoneDrawBotBuilder')
