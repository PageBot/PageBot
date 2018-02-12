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
import os
from htmlcontext import HtmlContext
try:
    import AppKit # Force exception on non-OSX platforms
    from pagebot import getRootPath
    from pagebot.contexts.builders.drawbotbuilder import drawBotBuilder
    from drawbotcontext import DrawBotContext
    defaultContext = DrawBotContext() # Test if platform is supporing DrawBot:
    FlatContext = None

    FONT_PATHS = [os.path.expanduser('~/Library/Fonts'), '/Library/Fonts', getRootPath() + '/Fonts']

except ImportError:
    from flatcontext import FlatContext
    DrawBotContext = None
    defaultContext = FlatContext()

    if os.name == 'posix':
        FONT_PATHS = [getRootPath() + 'Fonts'] # TODO: Is there a standard directory for Linux?
    else: 
        FONT_PATHS = [getRootPath() + 'Fonts'] # What to do for other OS?

