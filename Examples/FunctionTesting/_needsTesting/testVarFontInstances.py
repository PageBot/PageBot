#!/usr/bin/env python
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#       from https://github.com/fonttools/fonttools/blob/master/Lib/fontTools/varLib/mutator.py
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------

from pagebot.contexts.platform import defaultContext as context
from pagebot.fonttoolbox.objects.font import Font

f = Font("fonts/_instances/AmstelvarAlpha-Default.ttf")
fs = context.newString(u'Ae', style=dict(font=f.installedName,
                                         fontSize=500))
context.textBox(fs, (20, -10, 900, 900))
