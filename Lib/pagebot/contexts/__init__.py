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
from drawbotcontext import DrawBotContext
from flatcontext import FlatContext
from htmlcontext import HtmlContext

if DrawBotContext.b is not None: # Platform is supporing DrawBot:
	Context = DrawBotContext
else:
	Context = FlatContext
	