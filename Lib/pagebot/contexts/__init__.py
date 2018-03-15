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
from pagebot.contexts.drawbotcontext import DrawBotContext
from pagebot.contexts.flatcontext import FlatContext
from pagebot.contexts.htmlcontext import HtmlContext

try:
    #import ForceImportError # Uncomment for simulate testing of other contexts/platforms
    import AppKit # Force exception on non-OSX platforms
    defaultContext = DrawBotContext() # Test if platform is supporing DrawBot:

except (ImportError, AttributeError):
    #import ForceOtherError # Uncomment for simulate testing of other contexts/platforms
    defaultContext = FlatContext()

except:
    raise NotImplementedError('Cannot decide on the platform context.')
