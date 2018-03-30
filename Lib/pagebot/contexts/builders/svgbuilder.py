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
#     svgbuilder.py
#
from pagebot.contexts.builders.nonedrawbotbuilder import NoneDrawBotBuilder

try: 
	import svgwrite
	svgBuilder = svgwrite
	# Id to make builder hook name. Views will try to call e.build_svg()
	svgBuilder.PB_ID = 'svg' 

except ImportError:
    svgBuilder = NoneDrawBotBuilder()
    print('Using NoneDrawBotBuilder instead of svgwriter')

