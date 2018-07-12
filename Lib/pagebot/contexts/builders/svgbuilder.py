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
#     Supporting Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     svgbuilder.py
#
#     https://svgwrite.readthedocs.io/en/master/
#     sudo pip install svgwrite
#
from pagebot.contexts.builders.nonebuilder import NoneSvgBuilder

try: 
	import svgwrite
	svgBuilder = svgwrite
	# Id to make builder hook name. Views will try to call e.build_svg()
	svgBuilder.PB_ID = 'svg' 

except ImportError:
    svgBuilder = NoneSvgBuilder()
    print('Using NoneSvgBuilder instead of svgwriter')

