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
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     drawbotbuilder.py
#
from pagebot.contexts.builders.nonebuilder import NoneDrawBotBuilder

# FIXME: bad exception usage.t
try:
    import drawBot # Test if drawBot is available on this platform
    drawBotBuilder = drawBot
    # Id to make builder hook name. Views will try to call e.build_html()
    drawBotBuilder.PB_ID = 'drawBot'
    # Test by import if MacOS specific imports are available.
    #import CoreText, AppKit, Quartz # #pylint: disable=unused-import
except (ImportError, AttributeError):
    drawBotBuilder = NoneDrawBotBuilder()
    print('Using NoneDrawBotBuilder')

