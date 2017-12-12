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
#     pagebot/contexts/__init__.py
#
from htmlcontext import HtmlContext

try:
    import AppKit # Force exception on non-OSX platforms
    from pagebot.contexts.builders.drawbotbuilder import drawBotBuilder
    from drawbotcontext import DrawBotContext
    defaultContext = DrawBotContext() # Test if platform is supporing DrawBot:
    FlatContext = None
except ImportError:
    from flatcontext import FlatContext
    DrawBotContext = None
    defaultContext = FlatContext()
	
