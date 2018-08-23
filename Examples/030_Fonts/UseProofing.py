# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     AlterGlyphCoordinates.py
#
#

from pagebot.contexts.platform import getContext
from pagebot.toolbox.units import *
from pagebot.proofing.pagewide import PageWide
from pagebot.constants import A3
from pagebot.fonttoolbox.objects.font import findFont

font = findFont('Roboto-Regular')
WIDTH, HEIGHT = A3
context = getContext()
context.newPage(pt(WIDTH), pt(HEIGHT))
proof = PageWide(context)
context.scale(0.2)
context.translate(1000, 1000)
proof.draw(font, 'q', 12)