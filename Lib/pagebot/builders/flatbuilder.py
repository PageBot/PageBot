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
#     flatbuilder.py
#
try: 
    import flat
    flatBuilder = flat
    # Id to make builder hook name. Views will be calling e.build_html()
    flatBuilder.PB_ID = 'flat' 

except ImportError:
    flatBuilder = None

