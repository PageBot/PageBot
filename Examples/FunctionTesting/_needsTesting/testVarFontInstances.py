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
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------

from pagebot.contexts.platform import getContext
from pagebot.fonttoolbox.objects.font import findFont

context = getContext()

f = findFont('Roboto-Regular')
fs = context.newString(u'Ae', style=dict(font=f.path, fontSize=500))
context.textBox(fs, (20, -10, 900, 900))
